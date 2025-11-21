这是一个为您准备的中英双语版 `README.md`。您可以直接复制保存。

-----

# 🦅 宏观政策套利情报系统 | Macro Policy Arbitrage Intelligence System

**🇨🇳 中文**
这是一个基于 **LLM Agent** 架构的自动化情报分析系统。它能够自动抓取互联网新闻，利用 AI 进行两阶段的“筛选-分析”处理，从海量信息中精准捕捉涉及顶层设计变动、阶层财富转移和行业准入门槛变化的宏观信号，并生成结构化的分析报告。

**🇺🇸 English**
This is an automated intelligence analysis system based on **LLM Agent** architecture. It automatically scrapes internet news and utilizes AI for a two-stage "Selection-Analysis" process. It precisely captures macro signals regarding top-level design changes, wealth transfer between social classes, and industry entry barrier shifts from massive amounts of information, generating structured analysis reports.

-----

## ✨ 核心功能 (Core Features)

### 1\. 🕷️ 自动数据采集 (Auto-Crawler)

  * **Custom Sources**: 支持自定义新闻源 URL。 (Supports custom news source URLs.)
  * **Smart Deduplication**: 智能去重，防止重复抓取。 (Intelligent deduplication to prevent redundant scraping.)
  * **Universal Parsing**: 基于启发式规则的通用网页解析。 (Heuristic-based universal web page parsing.)

### 2\. 🧠 双阶段 AI 处理流水线 (Dual-Stage AI Pipeline)

  * **Stage 1: 宏观红利狙击手 (The Macro Bonus Sniper)**
      * 使用轻量级模型 (`Flash-Lite`) 快速扫描批量文章标题。 (Uses lightweight `Flash-Lite` model to rapidly scan batches of article titles.)
      * 根据“税收/社保变动”、“造富/返贫现象”、“行业准入壁垒”三大硬指标，从海量资讯中筛选出 **Top 5** 最具价值的信号。 (Filters the **Top 5** most valuable signals based on three hard criteria: "Tax/Social Security Changes", "Wealth Creation/Poverty Return", and "Industry Entry Barriers".)
  * **Stage 2: 政策套利分析师 (The Policy Arbitrage Analyst)**
      * 使用高性能模型 (`Flash`) 对筛选出的文章进行深度研读。 (Uses high-performance `Flash` model for deep reading of selected articles.)
      * **Structured Output**: 自动提取“矛盾点”、“政策温差”、“负面清单”、“实体信息”及“一句话结论”。 (Automatically extracts "Contradictions", "Policy Temperature Gaps", "Negative Lists", "Entity Info", and a "One-sentence Conclusion".)

### 3\. 📊 可视化情报看板 (Intelligence Dashboard)

  * **Interactive UI**: 基于 **Streamlit** 的交互式前端。 (Interactive frontend based on **Streamlit**.)
  * **Timeline View**: 支持按时间轴查看情报流。 (View intelligence streams chronologically.)
  * **Developer Dashboard**: 支持在线实时调整 LLM 的 Prompt（提示词），无需重启服务。 (Supports real-time online adjustment of LLM Prompts without restarting the service.)

### 4\. 🛡️ 企业级稳定性 (Enterprise-Grade Stability)

  * **JSON Schema**: 支持 **Structured Output**，确保 LLM 输出格式 100% 稳定，杜绝解析错误。 (Supports **Structured Output** to ensure 100% stable LLM output format and eliminate parsing errors.)
  * **Resilience**: 具备断点续传和积压任务自动清空机制。 (Features resume-from-break capability and automatic backlog clearing mechanisms.)

-----

## 🛠️ 技术栈 (Tech Stack)

  * **Language**: Python 3.10+
  * **LLM API**: Google Gemini (Supports `gemini-2.5-flash` series)
  * **Web Framework**: Streamlit
  * **Database**: SQLite (SQLAlchemy ORM)
  * **Scheduler**: APScheduler
  * **Crawler**: Requests + BeautifulSoup4

-----

## 🚀 快速开始 (Quick Start)

### 1\. 克隆项目 (Clone Repository)

```bash
git clone <your-repo-url>
cd news-intelligence-agent
```

### 2\. 安装依赖 (Install Dependencies)

建议使用 Python 虚拟环境 (Recommended to use Python virtual environment):

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### 3\. 配置环境变量 (Configure Environment)

在项目根目录创建一个 `.env` 文件，并填入你的 API Key (Create a `.env` file in the root directory and add your API Key):

```ini
# .env file content
GEMINI_API_KEY=your_google_api_key_here

# Optional Config / 可选配置
LLM_PROVIDER=gemini
# Keywords filter / 关键词过滤
HIGH_VALUE_KEYWORDS=AI,Policy,Economy,Reform
```

### 4\. 运行系统 (Run System)

#### 方式 A：启动可视化看板 (Option A: Launch Dashboard) - *Recommended*

这是最直观的使用方式，集成了手动触发抓取和数据查看功能。
(This is the most intuitive way, integrating manual crawl triggering and data viewing.)

```bash
streamlit run news/src/app.py
```

  * Open browser at `http://localhost:8501`.
  * Add news source URLs in the sidebar (e.g., `https://news.ycombinator.com`).
  * Click **"🚀 Fetch New Data"** to start.

#### 方式 B：后台静默运行 (Option B: Headless Background Task)

如果你希望让它在服务器后台每小时自动跑一次 (If you want it to run automatically every hour on a server):

```bash
python news/main.py --loop
```

-----

## 📂 项目结构 (Project Structure)

```text
news-intelligence-agent/
├── news/
│   ├── data/               # SQLite Database file / 数据库文件
│   ├── src/
│   │   ├── app.py          # Streamlit Frontend / 前端入口
│   │   ├── config.py       # Configuration / 配置管理
│   │   ├── crawler.py      # Crawler Logic / 爬虫逻辑
│   │   ├── database.py     # DB Models / 数据库模型
│   │   └── processor.py    # LLM Core (Selection & Analysis) / 智能核心
│   ├── main.py             # Background Scheduler / 后台调度入口
│   ├── list_models.py      # Utility: List Gemini Models / 工具脚本
│   └── requirements.txt    # Dependencies / 依赖列表
├── .env                    # Env Vars (DO NOT COMMIT) / 环境变量
├── .gitignore              # Git Ignore
└── README.md               # Documentation
```

-----

## ⚙️ 高级配置 (Developer Dashboard)

在 Streamlit 界面的 **"Developer Dashboard"** 标签页中 (In the **"Developer Dashboard"** tab of the Streamlit interface):

1.  **Database Overview**: 实时监控文章总数、已处理数量和高价值文章数量。 (Real-time monitoring of total, processed, and high-value articles.)
2.  **Prompt Engineering**:
      * 动态调整“狙击手”的筛选标准。 (Dynamically adjust "Sniper" selection criteria.)
      * 修改“分析师”的输出维度。 (Modify "Analyst" output dimensions.)
      * *Note: No need to modify JSON format instructions; the system enforces this via Schema.* (*注意：无需修改 JSON 格式说明，系统底层已通过 Schema 强制约束。*)
3.  **Data Management**: 按 ID 删除特定的文章。 (Delete specific articles by ID.)

-----

## ⚠️ 注意事项 (Notes)

1.  **API Costs**: 系统会消耗 Token。虽然使用了 Flash-Lite 进行初筛以节省成本，但在大量抓取时请留意 API 用量。 (The system consumes Tokens. While Flash-Lite is used for initial screening to save costs, please monitor API usage during heavy scraping.)
2.  **Network**: 请确保你的运行环境可以连接到 Google Gemini API 服务。 (Ensure your runtime environment can connect to Google Gemini API services.)
3.  **Crawler Etiquette**: 请勿对目标网站进行过高频率的抓取，以免触发反爬机制。 (Do not scrape target websites at excessively high frequencies to avoid triggering anti-bot mechanisms.)

-----

**License**: MIT
