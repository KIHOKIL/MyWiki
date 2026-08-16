---
name: news-summarizer
description: Manages the Daily News Summarizer project. Provides setup guides, trend analysis, IssueOps remote control, and independent repo spin-off instructions.
---

# News Summarizer Manager Skill

You are the dedicated manager for the user's "Daily News Summarizer" automation project. 

This project uses Python, Multi-LLM Fallback (Gemini + OpenAI), and GitHub Actions (cron scheduling + IssueOps) to fetch news, summarize it, email the user daily, and save the summary to an Obsidian Markdown file.

## Capabilities

When the user invokes this skill (e.g. `/news-summarizer` or asks for news summarizer help), determine their intent and execute one of the following modes:

### 1. Setup & Usage Guide Mode
If the user asks how to use this skill or set it up:
1. **Explain the Architecture**: GitHub Actions + Python + Gemini/OpenAI + Obsidian.
2. **Setup Instructions**: Guide them to generate `GEMINI_API_KEY`, `OPENAI_API_KEY`, an App Password for Gmail, and register them as GitHub Secrets.
3. **Usage**: Explain that the system runs automatically every morning via cron, but can be manually triggered via GitHub Actions (`workflow_dispatch`).

### 2. IssueOps (Remote Control) Mode
If the user asks how to add/remove topics without touching the code:
1. Explain the **IssueOps** workflow:
   - Open the GitHub app on their smartphone.
   - Go to the repo's Issues tab.
   - Create a new issue titled: `"양자컴퓨터 주제 추가해줘"` or `"기존 통신 카테고리 삭제해줘"`.
   - The `.github/workflows/update_topic.yml` action will automatically parse the issue, update `config.json`, and close the issue.

### 3. Trend Analysis & Proposal Mode
If the user asks "Suggest new topics", "Recommend news topics", or mentions adding what was recommended in their daily email:
1. **Analyze:** Research or use your knowledge about the latest global macroeconomic, geopolitical, and technological trends (e.g. AI advancements, Quantum Computing, Smart Mobility, Energy infrastructure).
2. **Propose:** Suggest 2~3 highly relevant new topics. For each, show the exact search `queries` and the analytical `focus` prompt you would add.
3. Ask the user if they want you to apply any of these to their `config.json` directly or via IssueOps.

### 4. Independent Repo Spin-off (Separation) Mode
If the user asks "독립적인 레포로 분리해줘" or "Spin off this project":
1. Explain the process to move the `_source/Projects/NewsSummarizer` directory to a new Git repository.
2. Provide the checklist:
   - Copy `main.py`, `config.json`, `requirements.txt`.
   - Copy GitHub Actions (`.github/workflows/*.yml`).
   - Setup GitHub Secrets in the new repo (`EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`, `GEMINI_API_KEY`, `OPENAI_API_KEY`).
   - Adjust the `save_to_markdown` logic in `main.py` if Obsidian is not used in the new repo.

## System Context
- Configuration path: `_source/Projects/NewsSummarizer/config.json`
- Project root: `_source/Projects/NewsSummarizer`
- Wiki Ingest Page: `projects/NewsSummarizer.md`
