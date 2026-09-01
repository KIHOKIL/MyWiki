---
title: Action-oriented AI
category: concepts
tags:
  - automation
  - ai-agents
  - future-workflows
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260817/obsidian_llm_wiki_guide.md]]"
created: "2026-08-17"
updated: "2026-08-17"
summary: 단순 질의응답을 넘어 브라우저와 파일 시스템을 직접 조작하며 업무를 완수하는 행동하는 AI 에이전트 개념.
base_confidence: 0.9
lifecycle: draft
tier: core
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
relationships:
  - target: "[[concepts/e2e-agentic-engineering-workflow]]"
    type: related_to
---

# Action-oriented AI (행동하는 AI)

과거의 AI 모델들이 주로 '단순 질의응답(Chatbot)'에 머물렀다면, 최신 AI 시스템은 사용자를 대신해 **실제로 시스템을 제어하고 환경과 상호작용하는 행동(Action)** 에 초점을 맞춥니다. 이를 '능동적 에이전트(Autonomous Agents)'라고도 부릅니다.

## 주요 특징 (Key Characteristics)

1. **도구 사용 (Tool Use):** 브라우저 제어, 파일 시스템 접근(Read/Write), 터미널 명령 실행 등 다양한 컴퓨터 리소스를 다룰 수 있습니다.
2. **반복 업무 자동화 (Vibe Coding):** 정형화된 업무나 반복적인 데이터 수집, 파이프라인(예: 지난주 회의록을 모아 주간 보고서로 작성)을 스크립트 기반 코딩 없이 자연어(Vibe)로 스케줄링할 수 있습니다.
3. **자율적 리서치:** Perplexity 등 검색 엔진을 직접 쿼리하고, 웹페이지를 순회(Crawling)하여 결과만을 정제해서 가져옵니다.

## 응용 사례 (Applications in Big Tech)

- **구독(Subscribe) 자동화:** 매번 정보를 검색하지 않고, 특정 뉴스레터나 유튜브 채널을 AI가 모니터링하다가 핵심 내용만 위키로 밀어넣어주는(Push) 시스템 구축.
- **SSG (Static Site Generation):** Obsidian 위키 내부의 페이지를 바탕으로, 코딩 없이 Hugo나 Next.js 기반의 개인 브랜드 블로그(정적 웹사이트)를 자동 빌드 및 배포(`연 $12` 정도의 저비용 구축).

이처럼 LLM Wiki 환경 내에서의 AI 에이전트는 단순히 '글을 써주는 도구'가 아니라 지식의 흐름을 통제하는 '마스터 비서' 역할을 수행합니다.
