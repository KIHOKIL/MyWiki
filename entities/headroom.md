---
title: Headroom
category: entities
tags:
  - headroom
  - open-source
  - python
  - typescript
  - mcp
  - proxy
  - context-compression
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/Headroom_심층분석_및_Group_2nd_Brain_연계.md]]"
  - "https://github.com/headroomlabs-ai/headroom"
created: "2026-09-03"
updated: "2026-09-03"
summary: 도구 출력·로그·대용량 JSON을 LLM 전달 직전에 무손실/최소손실 압축하여 토큰 소모를 20%~95% 절감하는 오픈소스 컨텍스트 압축 라이브러리, 로컬 프록시 및 MCP 서버.
base_confidence: 0.95
lifecycle: reviewed
tier: core
relationships:
  - target: "[[concepts/context-compression]]"
    type: implements
  - target: "[[concepts/mcp-server]]"
    type: implements
  - target: "[[concepts/graph-rag]]"
    type: optimizes
---

# Headroom

## 📌 개요
**Headroom**은 Headroom Labs에서 개발한 오픈소스 컨텍스트 압축 레이어([github.com/headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom))입니다. LLM 에이전트 루프나 RAG 파이프라인에서 발생하는 도구 출력, 시스템 로그, 방대한 JSON 데이터를 모델에 전달하기 직전에 가로채어 의미 손실 없이 토큰을 대폭 압축합니다.

- **라이선스:** Apache-2.0
- **지원 언어 및 환경:** Python, TypeScript, CLI, MCP Server
- **Star 수:** 64,000+ (GitHub Trending)

---

## 🛠️ 핵심 기능 및 배포 모드
1. **높은 압축률:**
   - 구조화된 JSON 데이터 및 API 응답: **60% ~ 95% 압축**
   - 코딩 에이전트 워크플로우(테스트/린트/diff 출력): **평균 20% 절감**
2. **다양한 연동 모드:**
   - **Library Mode:** Python/TS 코드 내에서 `compress()` 함수 직접 호출.
   - **Local Proxy Mode:** `headroom proxy` 구동 후 OpenAI/Anthropic 호환 엔드포인트의 baseURL만 변경하여 무수정 연동.
   - **Agent Wrap Mode:** `headroom wrap claude` 형태로 CLI 에이전트 감싸기.
   - **MCP Server Mode:** Cursor, Antigravity, Claude Code 등 MCP 지원 도구 체인에 플러그인 연동.
3. **지능형 제어:**
   - **CCR (Reversible Compression):** 필요 시 원문 복원 가능한 포인터 유지.
   - **Verbosity & Effort Routing:** 출력 서술 분량 억제 및 모델 추론 노력도 동적 배분.

---

## 🔗 연관 지식
- 개념: [[concepts/context-compression|Context Compression]]
- 연계 도구: [[concepts/mcp-server|MCP Server]], [[concepts/graph-rag|Graph RAG]], [[entities/neo4j|Neo4j]]
