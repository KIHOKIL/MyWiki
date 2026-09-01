---
title: Agentic RAG (에이전트 기반 RAG)
category: concepts
tags:
  - rag
  - agentic-rag
  - autonomous-agents
  - tool-calling
  - second-brain
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260901/Research_report_LLM_2nd_Brain_Seoul (1).md]]"
created: "2026-09-01"
updated: "2026-09-01"
summary: LLM을 단순 검색 결과 소비자가 아닌 자율형 에이전트로 배치하여 질의 재작성, 검색, 교차 검증 및 반사(Reflection)를 자율 수행하는 RAG 구조.
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

# Agentic RAG (에이전트 기반 RAG)

## 📌 개념 개요
**Agentic RAG**는 단일 패스(Single-pass) 검색 방식에서 벗어나, **LLM이 자율형 에이전트(Autonomous Agent)**로서 사용자의 복잡하고 모호한 질의를 분석하고 실행 계획(Planning)을 수립한 뒤, 다양한 도구(Tool Calling)를 활용해 반복적 질의 재작성, 검색 결과 검증(Reflection), 추가 탐색을 거쳐 신뢰할 수 있는 답을 완성하는 지능형 검색 프레임워크입니다.

---

## 🔄 핵심 파이프라인
1. **질의 분석 및 계획 (Planning):** 모호한 질의를 하위 태스크로 분해하고 필요한 정보 유형 규정.
2. **질의 재작성 (Query Rewriting):** 검색 정확도를 높이기 위한 키워드 확장 및 쿼리 변환.
3. **도구 호출 (Tool Calling):** 벡터 DB, 지식 그래프, 웹 검색, 사내 API 등 적절한 도구 선택 호출.
4. **반사 및 교차 검증 (Reflection & Verification):** 검색된 정보가 충분한지 평가하고, 모순이나 결핍 발견 시 재검색 루프 가동.
5. **최종 합성 (Synthesis):** 교차 검증된 사실들을 종합하여 정교한 최종 답변 산출.

---

## ⚖️ 장단점 분석

- **장점:** 고도의 자율성과 복합 추론 능력. 검색 실패 시 자동 복구 및 교차 검증을 통한 환각(Hallucination) 억제.
- **단점:** 다단계 추론(ReAct/CoT)에 따른 응답 레이턴시(Latency) 증가 및 반복적인 API 호출로 인한 토큰 비용 상승.

---

## 🔗 연관 개념
- [[concepts/agentic-workflow|Agentic Workflow]]
- [[concepts/graph-rag|Graph RAG]]
- [[concepts/active-second-brain|Active Second Brain]]
- [[concepts/mcp-server|MCP Server]]
