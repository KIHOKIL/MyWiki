---
title: Context Compression (컨텍스트 압축 기법)
category: concepts
tags:
  - context-compression
  - token-optimization
  - prompt-engineering
  - agent-efficiency
  - mcp
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/Headroom_심층분석_및_Group_2nd_Brain_연계.md]]"
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/20260903_학습노트.md]]"
created: "2026-09-03"
updated: "2026-09-03"
summary: LLM 및 에이전트 루프에 입력되기 직전, 도구 출력·로그·대용량 JSON 및 검색 청크의 의미적 손실 없이 불필요한 보일러플레이트를 사전에 압축하여 토큰 비용 절감과 어텐션 집중도를 극대화하는 기법.
base_confidence: 0.95
lifecycle: reviewed
tier: core
relationships:
  - target: "[[entities/headroom]]"
    type: implemented_by
  - target: "[[concepts/graph-rag]]"
    type: optimizes
  - target: "[[concepts/agentic-rag]]"
    type: enhances
---

# Context Compression (컨텍스트 압축 기법)

## 📌 개념 개요
**Context Compression(컨텍스트 압축)**은 LLM(대형 언어 모델) 및 자율 에이전트가 처리해야 하는 입력 프롬프트, 도구 반환값(Tool Output), RAG 검색 청크, 시스템 로그에서 의미적 정보 손실을 최소화하면서 불필요한 보일러플레이트, 중복 키, 공백을 사전에 축약·제거하는 최적화 패러다임입니다.

에이전트가 다단계 루프(Plan-Act-Observe)를 돌면서 발생하는 **"컨텍스트 비대증(Context Bloat)"**과 긴 컨텍스트 내에서 핵심 정보를 놓치는 **"주의력 저하(Lost in the Middle)"** 현상을 해결하는 필수 인프라 계층으로 자리잡고 있습니다.

---

## ⚙️ 핵심 원리 및 압축 메커니즘
1. **구조화 데이터 무손실/최소손실 정제 (Structural Pruning):**
   - 대규모 JSON이나 API 반환값에서 반복되는 메타데이터, 불필요한 null 필드, 장황한 스키마 정의를 LLM 친화적인 컴팩트 튜플이나 요약형 딕셔너리로 축소. (60%~95% 토큰 절감)
2. **코드 및 실행 로그 필터링 (AST & Log Slicing):**
   - 컴파일 에러, linter 결과, bash 출력에서 스택 트레이스 핵심부와 실패 원인만 남기고 성공한 수천 줄의 진행 로그를 자동 마스킹.
3. **가역 압축 (Reversible Compression / CCR):**
   - 원문 복원이 필요한 경우(예: 코드 라인 수정, 정밀 인용 Citation) 메타데이터 포인터를 유지하여 필요할 때 원본 청크로 디코딩 가능하도록 설계.
4. **Verbosity & Effort Steering:**
   - 프롬프트 압축뿐 아니라, LLM이 출력할 때 군더더기 인사말이나 중복 서술을 하지 않도록 시스템 프롬프트 및 파라미터를 동적으로 제어.

---

## ⚖️ 장점 및 적용 효과

| 항목 | 기존 직접 주입 | 컨텍스트 압축 적용 시 |
| :--- | :--- | :--- |
| **API 토큰 비용** | 도구 루프마다 수만 토큰 누적 (비용 폭증) | **20% ~ 최대 95% 토큰 절감** |
| **응답 지연(TTFT)** | 긴 프롬프트 인코딩으로 지연 시간 증가 | 사전 압축으로 입력 지연 대폭 단축 |
| **추론 정확도** | 노이즈 데이터로 인해 모델 어텐션 분산 | 핵심 증거(Evidence) 밀도 극대화로 정답률 향상 |

---

## 🔗 연관 지식
- 구현체: [[entities/headroom|Headroom]]
- 연계 아키텍처: [[concepts/graph-rag|Graph RAG]], [[concepts/agentic-rag|Agentic RAG]], [[concepts/mcp-server|MCP Server]]
