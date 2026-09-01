---
title: MCP Server (Model Context Protocol)
category: concepts
tags:
  - mcp
  - model-context-protocol
  - integrations
  - agent-architecture
  - tool-use
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260901/Research_report_LLM_2nd_Brain_Seoul (1).md]]"
created: "2026-09-01"
updated: "2026-09-01"
summary: LLM이 Email, Jira, Confluence, Git 등 다양한 이종 데이터 소스 및 도구에 표준화된 방식으로 안전하게 접근할 수 있도록 연결하는 모델 컨텍스트 프로토콜 서버.
base_confidence: 0.95
lifecycle: reviewed
tier: core
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
relationships:
  - target: "[[concepts/agentic-workflow]]"
    type: implements
  - target: "[[concepts/active-second-brain]]"
    type: related_to
---

# MCP Server (Model Context Protocol)

## 📌 개념 개요
**Model Context Protocol (MCP)**는 Anthropic이 제안한 개방형 표준 프로토콜로, AI 모델(에이전트)이 로컬 및 클라우드의 다양한 **이종 데이터 소스(Email, Jira, Confluence, Git 저장소 등)**와 툴(Tool)을 일관된 인터페이스로 안전하게 탐색하고 실행할 수 있도록 중계하는 서버 구조입니다.

---

## ⚙️ 세컨드 브레인에서의 역할
- **도구 호출 표준화:** 각 서비스(Jira API, Confluence REST API, Git Hooks)마다 개별 코드를 작성할 필요 없이, MCP Server가 제공하는 표준 함수 규격을 통해 에이전트가 데이터 질의 및 명령 실행.
- **실시간 컨텍스트 동기화:** 대화 중 "현재 결제 모듈 배포 현황 확인해줘"라는 질의에 대해 MCP Server를 통해 실시간 Git 커밋 diff, Jira 티켓 상태, Confluence 설계 가이드를 병렬 수집하여 LLM에 주입.
- **보안 및 권한 통제:** 개인 인증 토큰 및 API 키를 MCP Server 계층에서 격리 관리하여 모델에 직접 노출되는 보안 위험 방지.

---

## 🔗 연관 개념
- [[concepts/agentic-rag|Agentic RAG]]
- [[concepts/active-second-brain|Active Second Brain]]
- [[concepts/agentic-vault|Agentic Vault]]
