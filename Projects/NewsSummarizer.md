---
title: "Daily News Summarizer"
category: projects
tags: [news, automation, llm, github-actions, issueops, multi-llm]
sources: []
created: 2026-08-16
updated: 2026-08-16
---

# 📰 Daily News Summarizer

## 프로젝트 개요
**Daily News Summarizer**는 관심 있는 IT/통신/AI 산업 트렌드 뉴스를 매일 자동으로 수집하여, 최고 수준의 애널리스트 관점에서 심층 분석 및 요약한 뒤 이메일로 발송하고, 동시에 개인 지식 저장소(Obsidian Wiki)에 아카이빙하는 "초자동화(Hyper-automation) 지식 관리 시스템"이다.

## 핵심 아키텍처 및 구현체
- **뉴스 수집**: Google News RSS (`feedparser`)
- **AI 요약 (Multi-LLM Fallback)**: 
  - 1순위: `Gemini-flash-latest` (무료, 일일 1500회 제한)
  - 2순위 (Fallback): `OpenAI gpt-4o-mini` (Gemini 한도 초과 시 즉각 대체 투입)
- **에러 핸들링**: 어떠한 경우에도 프로그램이 다운되지 않고, 요약 실패 시 원문 링크를 담은 이메일을 발송(`has_error=True`)
- **자동화 스케줄링**: `.github/workflows/news_summarizer.yml` (매일 아침 자동 실행)

## 📱 IssueOps (원격 제어 시스템)
PC 없이 스마트폰으로 저장소의 설정을 제어할 수 있는 구조.
- GitHub 앱에서 `KIHOKIL/MyWiki` 레포지토리의 Issues 탭에 "양자컴퓨터 주제 추가해줘"라고 작성하면, `update_topic.yml` Action이 실행되어 `config.json`을 수정 및 커밋함.

## 📦 독립 레포지토리 분리 가이드 (Spin-off)
향후 본 스킬을 독립적인 레포지토리로 분리하기 위한 절차:
1. 새 레포지토리 생성.
2. `MyWiki/_source/Projects/NewsSummarizer` 내의 `main.py`, `config.json`, `requirements.txt` 이동.
3. `.github/workflows/news_summarizer.yml` 및 `update_topic.yml` 이동.
4. GitHub Secrets에 `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`, `GEMINI_API_KEY`, `OPENAI_API_KEY` 등록.

## 연관 개념
- [[concepts/issueops|IssueOps]]
- [[concepts/agentic-workflow|Agentic Workflow (LLM Fallback Architecture)]]
- [[concepts/harness-engineering|Harness Engineering (TDD in AI Agents)]]
