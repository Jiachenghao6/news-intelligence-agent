import logging
import json
from sqlalchemy.orm import Session
from .database import Article, get_db, SessionLocal, get_setting
from .config import config
import google.generativeai as genai
import typing_extensions as typing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schema Definitions
class ArticleSelection(typing.TypedDict):
    id: int
    Signal: str
    Actionability: str
    Prediction: str

class PolicyAnalysis(typing.TypedDict):
    contradictions: str
    temperature_diff: str
    negative_list: str
    entities: str
    conclusion: str

class Processor:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.setup_llm()

    def setup_llm(self):
        if config.LLM_PROVIDER == "gemini":
            genai.configure(api_key=config.GEMINI_API_KEY)

    def select_high_value_articles(self, articles: list[Article]):
        """
        Stage 2: Selection
        Sends a batch of titles to the LLM to select high-value ones using the "Macro Bonus Sniper" persona.
        """
        if not articles:
            return []

        # Prepare the list for the prompt
        articles_list = "\n".join([f"ID {a.id}: {a.title}" for a in articles])
        
        # Default prompt (Macro Bonus Sniper) - Purified
        default_prompt = """
        Role: 宏观红利狙击手
        Context: 只有能改变社会资源分配规则的新闻才值得关注
        Criteria: 
        1. 是否涉及[税收/社保/户籍]等顶层设计变动？(政策红利/黑天鹅) 
        2. 是否出现跨阶层的[造富/返贫]现象？(风口预警) 
        3. 是否改变了[特定行业]的准入门槛？(竞争壁垒) 
        
        Task:
        Review the following articles. Select the TOP 5 most impactful articles based on the criteria.
        Rank them from 1 (most impactful) to 5.
        
        Articles:
        {articles_list}
        """
        
        # Load from DB or use default
        prompt_template = get_setting("prompt_selection", default_prompt)
        
        # If the user edited the prompt, they might have removed the placeholder. 
        # We need to ensure {articles_list} is in there or append it.
        if "{articles_list}" in prompt_template:
            prompt = prompt_template.format(articles_list=articles_list)
        else:
            prompt = prompt_template + "\n\nArticles:\n" + articles_list

        try:
            model = genai.GenerativeModel(config.MODEL_SELECTION)
            
            # Use response_schema for hard constraint
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=list[ArticleSelection]
                )
            )
            
            text = response.text.strip()
            # Clean up potential markdown code blocks (though less likely with schema)
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("\n", 1)[0]
            
            selection_results = json.loads(text)
            logger.info(f"LLM Selection Results: {len(selection_results)} items")
            
            # Sort by order in list (assuming LLM returned ranked list) and take top 5
            top_results = selection_results[:5]
            top_ids = {item['id'] for item in top_results}
            
            # Map results to a dict for easy access
            results_map = {item['id']: item for item in top_results}
            
            selected_articles = []
            # Update DB
            for article in articles:
                article.is_processed = True
                if article.id in top_ids:
                    article.is_high_value = True
                    # Prepend the selection insights to the report (or placeholder)
                    meta = results_map[article.id]
                    article.analysis_report = f"""
**🎯 狙击手简报**
- **信号**: {meta.get('Signal')}
- **可操作性**: {meta.get('Actionability')}
- **预测**: {meta.get('Prediction')}
---
"""
                    selected_articles.append(article)
                else:
                    article.is_high_value = False
            self.db.commit()
            
            return selected_articles
            
        except Exception as e:
            logger.error(f"Error in batch selection: {e}")
            return []

    def analyze_article(self, article: Article):
        """
        Stage 3: Analysis
        Uses stronger LLM to analyze the article using "Policy Arbitrage Analyst" persona.
        """
        # Default prompt (Policy Arbitrage Analyst) - Purified
        default_prompt = """
        Role: 冷酷的政策套利分析师
        Task: Analyze the text.
        
        Content:
        {content} 
        
        Requirements:
        1. 【矛盾点】(contradictions): 提取文中“既要...又要...”的内容，并判断哪一个是当前的真实KPI（排在后面或有量化指标的）。
        2. 【温差】(temperature_diff): 对比该行业去年的常规表述，提取变化的形容词（如从“大力发展”变为“规范有序”）。
        3. 【负面清单】(negative_list): 提取所有“严禁”、“不得”、“清理”后面的具体行为。
        4. 【实体信息】(entities): 提取文中所有的金额、日期、负责部门。
        5. 【一句话结论】(conclusion): 这文件是发钱的（红利），还是收网的（整顿）？
        """
        
        prompt_template = get_setting("prompt_analysis", default_prompt)
        
        content_snippet = article.content[:8000]
        if "{content}" in prompt_template:
            prompt = prompt_template.format(content=content_snippet)
        else:
            prompt = prompt_template + "\n\nContent:\n" + content_snippet

        try:
            model = genai.GenerativeModel(config.MODEL_ANALYSIS)
            
            # Use response_schema for hard constraint
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=PolicyAnalysis
                )
            )
            
            text = response.text.strip()
            # Clean up potential markdown code blocks
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("\n", 1)[0]
            
            try:
                data = json.loads(text)
                formatted_report = f"""
### 🕵️ 政策套利分析
- **⚖️ 矛盾点**: {data.get('contradictions')}
- **🌡️ 温差**: {data.get('temperature_diff')}
- **🚫 负面清单**: {data.get('negative_list')}
- **🏛️ 实体信息**: {data.get('entities')}
- **💡 结论**: **{data.get('conclusion')}**
"""
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON from analysis: {text}")
                formatted_report = f"\n**Analysis Raw Output**:\n{text}"

            # Append to the existing report (which has the sniper brief)
            if article.analysis_report:
                article.analysis_report += "\n" + formatted_report
            else:
                article.analysis_report = formatted_report
                
            self.db.commit()
            logger.info(f"Analyzed article: {article.title}")
        except Exception as e:
            logger.error(f"Error analyzing article {article.id}: {e}")

    def process_pending_articles(self):
        """
        Main loop to process unprocessed articles in batches.
        """
        while True:
            # Get next batch of unprocessed articles
            # Limit to 20 at a time to fit in context window
            articles = self.db.query(Article).filter(Article.is_processed == False).limit(20).all()
            
            if not articles:
                logger.info("No more pending articles.")
                break

            logger.info(f"Processing batch of {len(articles)} articles...")
            
            # 1. Batch Selection
            high_value_articles = self.select_high_value_articles(articles)
            
            # 2. Individual Analysis
            for article in high_value_articles:
                self.analyze_article(article)

    def close(self):
        self.db.close()

if __name__ == "__main__":
    processor = Processor()
    processor.process_pending_articles()
    processor.close()
