---
title: 에이전틱 스캐폴딩 (Agentic Scaffolding)
category: concepts
tags:
  - workflow
  - automation
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/big_tech_ai_workflow_proposal.md
created: 2026-08-17
updated: 2026-08-17
---

# 에이전틱 스캐폴딩 (Agentic Scaffolding)

단순한 보조 툴(Copilot) 수준을 넘어 프로젝트 전반의 문맥을 이해하고 스스로 행동할 수 있도록 AI 에이전트를 위한 **구조적 기반(Scaffolding)**을 구축하는 개념입니다.

빅테크(Meta, Google, Anthropic 등)의 최신 워크플로우를 개인 환경(LLM Wiki 기반)에 접목한 형태로, **"모든 컨텍스트(문맥)가 모이는 중앙 뇌(Central Brain)"**를 설정(예: Obsidian)하고, 이를 바탕으로 에이전트(예: Antigravity IDE)가 다앙한 행동을 수행할 수 있도록 파이프라인을 짭니다.

## 스캐폴딩 주요 적용 사례
- **지식 수집 동기화:** JIRA, Confluence, Email 등의 파편화된 정보를 위키의 `_raw/` 로 모으고 AI가 자동 분류(`entities/`, `journal/`).
- **바이브 코딩 및 다중 에이전트 코드 리뷰:** 위키의 문맥(JIRA 티켓 내용, 기획 문서)을 바탕으로 로컬에서 코드 구현 및 자동 PR 리뷰 수행.
- **로그 분석 / 모니터링:** 에러 로그를 스크립트 기반 스킬과 LLM으로 자동 패턴화 및 현황판 제공.
- **보고서 시각화 자동화:** 생성된 저널을 바탕으로 Weekly Digest를 생성하고 Marp 등을 이용해 PPT/PDF로 렌더링.

## 연관 개념
- [[active-second-brain]]
- [[vibe-coding]]
- [[multi-agent-code-review]]
