
# 🦅 Macro Policy Arbitrage Intelligence System | 宏观政策套利情报系统

-----

## 🇺🇸 English Version

### 📖 Introduction

This is an automated intelligence analysis system based on **LLM Agent** architecture. It automatically scrapes internet news and utilizes AI for a two-stage "Selection-Analysis" process. It precisely captures macro signals regarding top-level design changes, wealth transfer between social classes, and industry entry barrier shifts from massive amounts of information, generating structured analysis reports.

### ✨ Core Features

1.  **🕷️ Auto-Crawler (Data Ingestion)**

      * **Custom Sources**: Supports adding custom news source URLs via the dashboard.
      * **Smart Deduplication**: Intelligent filtering to prevent redundant scraping of existing URLs.
      * **Universal Parsing**: Heuristic-based universal web page parsing adaptable to various news sites.

2.  **🧠 Dual-Stage AI Pipeline (The Brain)**

      * **Stage 1: The Macro Bonus Sniper**
          * Uses the lightweight `Flash-Lite` model to rapidly scan batches of article titles.
          * Filters the **Top 5** most valuable signals based on three hard criteria: "Tax/Social Security Changes", "Wealth Creation/Poverty Return", and "Industry Entry Barriers".
      * **Stage 2: The Policy Arbitrage Analyst**
          * Uses the high-performance `Flash` model for deep reading of selected high-value articles.
          * **Structured Output**: Automatically extracts "Contradictions", "Policy Temperature Gaps", "Negative Lists", "Entity Info", and provides a "One-sentence Conclusion".

3.  **📊 Intelligence Dashboard (UI)**

      * **Interactive Frontend**: Built with **Streamlit** for a smooth user experience.
      * **Timeline View**: View intelligence streams chronologically or by daily summary.
      * **Developer Dashboard**: Supports real-time online adjustment of LLM Prompts (System Instructions) without restarting the service.

4.  **🛡️ Enterprise-Grade Stability**

      * **JSON Schema Enforcement**: Uses Google Gemini's structured output feature to ensure 100% stable JSON formats, eliminating parsing errors.
      * **Resilience**: Features resume-from-break capability and automatic backlog clearing mechanisms (Batch Processing Loop).

### 🛠️ Tech Stack

  * **Language**: Python 3.10+
  * **LLM API**: Google Gemini (Supports `gemini-2.5-flash` series)
  * **Web Framework**: Streamlit
  * **Database**: SQLite (SQLAlchemy ORM)
  * **Scheduler**: APScheduler
  * **Crawler**: Requests + BeautifulSoup4

### 🚀 Quick Start

#### 1\. Clone Repository

```bash
git clone <your-repo-url>
cd news-intelligence-agent
```

#### 2\. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

#### 3\. Configure Environment

Create a `.env` file in the root directory and add your API Key:

```ini
# .env file content
GEMINI_API_KEY=your_google_api_key_here

# Optional Config
LLM_PROVIDER=gemini
HIGH_VALUE_KEYWORDS=AI,Policy,Economy,Reform
```

#### 4\. Run System

**Option A: Launch Visual Dashboard (Recommended)**
This creates a web interface to manage sources and view reports.

```bash
streamlit run news/src/app.py
```

  * Open your browser at `http://localhost:8501`.
  * Add news URLs in the sidebar.
  * Click **"🚀 Fetch New Data"** to start the agent.

**Option B: Headless Background Task**
Run the crawler and processor in a loop (e.g., every hour).

```bash
python news/main.py --loop
```

-----

## 🇨🇳 中文版

### 📖 项目简介

这是一个基于 **LLM Agent** 架构的自动化情报分析系统。它能够自动抓取互联网新闻，利用 AI 进行两阶段的“筛选-分析”处理，从海量信息中精准捕捉涉及顶层设计变动、阶层财富转移和行业准入门槛变化的宏观信号，并生成结构化的分析报告。

### ✨ 核心功能

1.  **🕷️ 自动数据采集 (数据摄入)**

      * **自定义源**: 支持在仪表盘中添加任意新闻源 URL。
      * **智能去重**: 防止重复抓取已存在的链接。
      * **通用解析**: 基于启发式规则的网页解析算法，适应性强。

2.  **🧠 双阶段 AI 处理流水线 (智能核心)**

      * **第一阶段：宏观红利狙击手 (The Sniper)**
          * 使用轻量级模型 (`Flash-Lite`) 快速扫描批量文章标题。
          * 根据“税收/社保变动”、“造富/返贫现象”、“行业准入壁垒”三大硬指标，从海量资讯中筛选出 **Top 5** 最具价值的信号。
      * **第二阶段：政策套利分析师 (The Analyst)**
          * 使用高性能模型 (`Flash`) 对筛选出的文章进行深度研读。
          * **结构化输出**: 自动提取“矛盾点”、“政策温差”、“负面清单”、“实体信息”及“一句话结论”。

3.  **📊 可视化情报看板 (前端)**

      * **交互式 UI**: 基于 **Streamlit** 构建。
      * **时间轴视图**: 支持按时间顺序或日报形式查看情报流。
      * **开发者后台**: 支持在线实时调整 LLM 的 Prompt（提示词），无需重启服务即可优化 AI 人设。

4.  **🛡️ 企业级稳定性**

      * **JSON Schema 强约束**: 使用 Gemini 原生结构化输出功能，确保 LLM 输出格式 100% 稳定，彻底杜绝解析报错。
      * **高可用逻辑**: 具备断点续传能力和积压任务自动清空机制 (Batch Processing Loop)。

### 🛠️ 技术栈

  * **语言**: Python 3.10+
  * **大模型 API**: Google Gemini (支持 `gemini-2.5-flash` 系列)
  * **Web 框架**: Streamlit
  * **数据库**: SQLite (SQLAlchemy ORM)
  * **调度器**: APScheduler
  * **爬虫**: Requests + BeautifulSoup4

### 🚀 快速开始

#### 1\. 克隆项目

```bash
git clone <your-repo-url>
cd news-intelligence-agent
```

#### 2\. 安装依赖

建议使用 Python 虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

#### 3\. 配置环境变量

在项目根目录创建一个 `.env` 文件，并填入你的 API Key：

```ini
# .env 文件内容
GEMINI_API_KEY=你的_Google_API_Key

# 可选配置
LLM_PROVIDER=gemini
HIGH_VALUE_KEYWORDS=AI,Policy,Economy,Reform
```

#### 4\. 运行系统

**方式 A：启动可视化看板 (推荐)**
这是最直观的使用方式，集成了手动触发抓取和数据查看功能。

```bash
streamlit run news/src/app.py
```

  * 打开浏览器访问 `http://localhost:8501`。
  * 在侧边栏添加新闻源 URL。
  * 点击 **"🚀 Fetch New Data"** 开始运行 Agent。

**方式 B：后台静默运行 (定时任务)**
如果你希望让它在服务器后台每小时自动跑一次：

```bash
python news/main.py --loop
```

-----

## ⚙️ Configuration & Notes (配置与注意事项)

### Developer Dashboard (开发者后台)

In the Streamlit interface, navigate to the **"Developer Dashboard"** tab to:

  * **Real-time Prompt Tuning**: Dynamically modify the selection criteria and analysis dimensions.
  * **Data Management**: Delete specific articles by ID.
  * **Metrics**: View system processing statistics.

### Important Notes (注意事项)

1.  **API Costs**: The system consumes Tokens. While Flash-Lite is used for initial screening to save costs, please monitor API usage during heavy scraping. (系统会消耗 Token。虽然使用了 Flash-Lite 进行初筛以节省成本，但在大量抓取时请留意 API 用量。)
2.  **Network**: Ensure your runtime environment can connect to Google Gemini API services. (请确保你的运行环境可以连接到 Google 服务。)
3.  **Crawler Etiquette**: Do not scrape target websites at excessively high frequencies to avoid triggering anti-bot mechanisms. (请勿对目标网站进行过高频率的抓取，以免触发反爬机制。)

-----

**License**: MIT
