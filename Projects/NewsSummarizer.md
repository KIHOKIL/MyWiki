---
title: "Daily News Summarizer"
category: projects
tags: [news, automation, llm, github-actions, issueops, multi-llm]
sources: []
created: 2026-08-16
updated: 2026-09-06
---

# 📰 Daily News Summarizer

## 프로젝트 개요
**Daily News Summarizer**는 관심 있는 IT/통신/AI 산업 트렌드 뉴스를 매일 자동으로 수집하여, 최고 수준의 애널리스트 관점에서 심층 분석 및 요약한 뒤 이메일로 발송하고, 동시에 개인 지식 저장소(Obsidian Wiki)에 아카이빙하는 "초자동화(Hyper-automation) 지식 관리 시스템"이다.

## 🚀 2026-09-06 고도화 (3-Section & HTML Email)
사용자의 주요 실무 관심사인 **Group 2nd Brain 구축** 및 **Codebase 이해를 통한 구현(Implementation Loop) & 코드 리뷰**에 완벽히 맞추어 3단계 리포트 구조로 개편되었으며, 현대적인 반응형 HTML 이메일 포맷을 전면 도입하였다.

### 1. 3단계 브리핑 구조
- **Section 1: Executive Summary (2nd Brain & Codebase Loop)**
  - 당일 수집된 모든 뉴스와 GitHub 오픈소스 트렌드를 종합 교차 분석(Synthesis).
  - 🚀 **핵심 혁신 (Key Innovations)**: 에이전트 지식 그래프, AST 기반 코드베이스 사전 인덱싱 등.
  - ⚠️ **핵심 리스크 및 과제 (Core Risks & Trade-offs)**: 사내 이메일/Jira 연동 시 개인정보/보안 유출 위험, LLM Context 한계로 인한 코드 환각(Hallucination), 코드 리뷰 False Negative 위험.
  - 🎯 **실무 적용 시사점 (Actionable Takeaways)**: 사내 Group 2nd Brain 구축 및 개발/리뷰 자동화 루프에 즉시 반영할 아키텍처 가이드.
- **Section 2: GitHub Trending Top 3 (2nd Brain & Codebase Intelligence)**
  - GitHub Search/Trending API로 글로벌 상위 오픈소스 저장소 중 사용자의 업무와 연계된 Top 3를 엄선.
  - 스타 수, 한 줄 목적, 핵심 아키텍처(Local-first, AST, MCP), 실무 활용 가치 분석.
  - 주요 추적 저장소: `tinyhumansai/openhuman`, `tirth8205/code-review-graph`, `AgriciDaniel/claude-obsidian` 등.
- **Section 3: 관심 분야별 심층 뉴스**
  - Group 2nd Brain & Enterprise Agent Architecture
  - Codebase Understanding & Agentic Implementation Loop
  - Global Big Tech & AI Frontier: M&A, Strategy & Capital Flow (OpenAI, Anthropic, xAI, Databricks, CoreWeave 및 빅테크 M&A/자본 동맹)
  - AI Era: Hardware & Infrastructure
  - Mobile Communication & Smart Mobility


### 2. 모던 반응형 HTML 이메일 포맷
- `EmailMessage.add_alternative(html_body, subtype='html')` 및 텍스트 Fallback 동시 지원.
- 딥 네이비/인디고 그라데이션 헤더와 슬레이트/그린/앰버/블루 카드 UI.
- Gmail, Apple Mail, Outlook 등 주요 메일 클라이언트 인라인 CSS 최적화.

## 핵심 아키텍처 및 구현체
- **뉴스 수집**: Google News RSS (`feedparser`)
- **오픈소스 트렌드 수집**: GitHub Search API (`fetch_github_trending`) + 큐레이션 Fallback
- **AI 요약 및 분석 (Multi-LLM Fallback)**: 
  - 1순위: `Gemini-3.1-flash-lite`
  - 2순위 (Fallback): `OpenAI gpt-4o-mini`
- **에러 핸들링**: 요약 실패 시 원문 링크를 담은 알림 메일 발송(`has_error=True`)
- **마크다운 아카이빙**: `_sources/News/Daily_Summaries/`에 Obsidian Frontmatter 및 태그와 함께 자동 저장.

## 📱 IssueOps (원격 제어 시스템)
PC 없이 스마트폰으로 저장소의 설정을 제어할 수 있는 구조.
- GitHub 앱에서 `KIHOKIL/MyWiki` 레포지토리의 Issues 탭에 "양자컴퓨터 주제 추가해줘"라고 작성하면, `update_topic.py`를 통해 `config.json`을 자동 갱신.

## 연관 개념
- [[concepts/2nd-brain-system-design-blueprint|2nd Brain System Design Blueprint]]
- [[concepts/active-second-brain|Active Second Brain]]
- [[concepts/harness-engineering|Harness Engineering (TDD in AI Agents)]]
- [[entities/openhuman|OpenHuman]]
- [[concepts/issueops|IssueOps]]

