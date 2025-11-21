import streamlit as st
import pandas as pd
import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_db, Article, SessionLocal, delete_article, add_source, delete_source, get_sources, get_all_articles, get_setting, set_setting
from src.crawler import Crawler
from src.processor import Processor

st.set_page_config(page_title="Info Stream", layout="wide")

def get_data():
    db: Session = SessionLocal()
    # Fetch high value articles
    articles = db.query(Article).filter(Article.is_high_value == True).order_by(Article.fetched_at.desc()).all()
    db.close()
    return articles

def run_fetch_cycle():
    """Runs the crawler and processor."""
    sources = get_sources()
    urls = [s.url for s in sources]
    
    if not urls:
        st.warning("No sources configured! Add some URLs in the sidebar.")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. Crawl
    status_text.text("🕷️ Crawling sources...")
    crawler = Crawler()
    total_urls = len(urls)
    for i, url in enumerate(urls):
        crawler.crawl_site(url)
        progress_bar.progress((i + 1) / (total_urls * 2))
    crawler.close()
    
    # 2. Process
    status_text.text("🧠 Analyzing content...")
    processor = Processor()
    processor.process_pending_articles()
    processor.close()
    progress_bar.progress(100)
    
    status_text.text("✅ Done!")
    st.rerun()

def main():
    st.title("🌊 Information Stream & Analysis")

    # --- Sidebar: Configuration & Sources ---
    st.sidebar.header("Configuration")
    
    st.sidebar.subheader("Data Sources")
    sources = get_sources()
    for s in sources:
        col1, col2 = st.sidebar.columns([0.8, 0.2])
        col1.text(s.url)
        if col2.button("🗑️", key=f"del_src_{s.id}"):
            delete_source(s.id)
            st.rerun()
            
    new_url = st.sidebar.text_input("Add URL", placeholder="https://example.com")
    if st.sidebar.button("Add Source"):
        if new_url:
            if add_source(new_url):
                st.sidebar.success("Added!")
                st.rerun()
            else:
                st.sidebar.error("Failed (Duplicate?)")

    st.sidebar.markdown("---")
    if st.sidebar.button("🚀 Fetch New Data", type="primary"):
        run_fetch_cycle()

    if st.sidebar.button("Refresh View"):
        st.rerun()

    # --- Main Content ---
    tab1, tab2, tab3 = st.tabs(["Information Stream", "Daily Report", "Developer Dashboard"])

    with tab1:
        st.header("Latest High-Value Updates")
        articles = get_data()
        
        if not articles:
            st.info("No high-value articles found yet. Add sources and click 'Fetch New Data'!")
        
        # Group by date
        grouped_articles = {}
        for article in articles:
            date_key = article.fetched_at.date()
            if date_key not in grouped_articles:
                grouped_articles[date_key] = []
            grouped_articles[date_key].append(article)
            
        # Display grouped articles
        for date_key in sorted(grouped_articles.keys(), reverse=True):
            # Date Header
            if date_key == datetime.utcnow().date():
                date_label = "Today"
            elif date_key == (datetime.utcnow() - timedelta(days=1)).date():
                date_label = "Yesterday"
            else:
                date_label = date_key.strftime("%Y-%m-%d")
                
            st.subheader(f"📅 {date_label}")
            
            for article in grouped_articles[date_key]:
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    with st.expander(f"{article.title}"):
                        st.markdown(f"**Source**: [{article.url}]({article.url})")
                        st.markdown("### Analysis Report")
                        st.markdown(article.analysis_report or "Analysis pending...")
                        st.divider()
                        st.markdown("### Original Content Snippet")
                        st.text(article.content[:500] + "..." if article.content else "No content")
                with col2:
                    if st.button("🗑️", key=f"del_{article.id}", help="Delete this article"):
                        if delete_article(article.id):
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete.")

    with tab2:
        st.header("Daily Summary")
        # Filter for last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_articles = [a for a in articles if a.fetched_at >= yesterday]
        
        if not recent_articles:
            st.write("No articles in the last 24 hours.")
        else:
            st.write(f"**Total Articles**: {len(recent_articles)}")
            st.markdown("---")
            for article in recent_articles:
                st.subheader(article.title)
                st.markdown(article.analysis_report or "No analysis available.")
                st.markdown("---")

    with tab3:
        st.header("🛠️ Developer Dashboard")
        
        # --- Prompt Editor ---
        with st.expander("📝 Prompt Configuration", expanded=False):
            st.info("💡 **提示**：请专注于修改筛选标准、角色设定和分析维度。**不需要**在 Prompt 中指定输出格式（如 JSON），系统会自动接管格式控制。")
            st.info("Edit the prompts used by the AI. Use `{articles_list}` in Selection and `{content}` in Analysis as placeholders.")
            
            # Default Prompts (Same as in processor.py, for initial display if DB is empty)
            default_selection = """Role: 宏观红利狙击手
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
            default_analysis = """Role: 冷酷的政策套利分析师
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

            current_selection = get_setting("prompt_selection", default_selection)
            current_analysis = get_setting("prompt_analysis", default_analysis)
            
            new_selection = st.text_area("Selection Prompt (Stage 2)", value=current_selection, height=300)
            new_analysis = st.text_area("Analysis Prompt (Stage 3)", value=current_analysis, height=300)
            
            if st.button("Save Prompts"):
                set_setting("prompt_selection", new_selection)
                set_setting("prompt_analysis", new_analysis)
                st.success("Prompts updated!")

        st.divider()
        
        st.subheader("Database View")
        all_articles = get_all_articles()
        
        # Metrics
        total = len(all_articles)
        processed = sum(1 for a in all_articles if a.is_processed)
        high_value = sum(1 for a in all_articles if a.is_high_value)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Articles", total)
        m2.metric("Processed", processed)
        m3.metric("High Value", high_value)
        
        st.divider()
        
        # Data Table
        if all_articles:
            data = [{
                "ID": a.id,
                "Title": a.title,
                "URL": a.url,
                "Fetched": a.fetched_at,
                "Processed": a.is_processed,
                "High Value": a.is_high_value
            } for a in all_articles]
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        
        st.divider()
        
        # Delete Action
        st.subheader("Danger Zone")
        del_id = st.number_input("Enter Article ID to Delete", min_value=1, step=1)
        if st.button("Delete Article by ID", type="primary"):
            if delete_article(del_id):
                st.success(f"Deleted Article {del_id}")
                st.rerun()
            else:
                st.error(f"Article {del_id} not found.")

if __name__ == "__main__":
    main()
