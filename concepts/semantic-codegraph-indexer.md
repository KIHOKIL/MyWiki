---
title: 시맨틱 코드그래프 인덱서 (Semantic CodeGraph Indexer)
category: concepts
tags:
  - codebase-understanding
  - clang
  - libclang
  - ast
  - graph-rag
  - embedded-software
sources:
  - _sources/Study/Codebase-Understanding/Clang-CodeGraph/20260920/Semantic_CodeGraph_Indexer_Clang.md
created: 2026-09-20
updated: 2026-09-20
summary: "Clang 컴파일러 정적 분석 및 LibTooling/libclang AST를 기반으로 C/C++ 소스코드의 전처리기 매크로, 호출 계층, HW 레지스터 맵 접근 경로를 지식 그래프(Knowledge Graph)로 정밀 색인하는 기술."
---

# 시맨틱 코드그래프 인덱서 (Semantic CodeGraph Indexer)

대규모 C/C++ 모바일 통신 프로토콜(PHY/MAC) 및 실시간 임베디드 소프트웨어의 구조를 정확하게 이해하기 위해, 단순 텍스트 검색(`grep`)이나 문맥 없는 구문 분석기(`tree-sitter`)의 한계를 극복하고 **실제 컴파일러 플래그(`compile_commands.json`)가 적용된 Clang AST를 분석하여 코드 지식 그래프를 구축하는 기법**입니다.

---

## 💡 핵심 메커니즘

1. **빌드 컨텍스트 완전 주입**:
   - `compile_commands.json`에 정의된 매크로(`#ifdef`), 헤더 검색 경로(`-I`), 컴파일 타깃 아키텍처 플래그를 그대로 반영하여 전처리 이후의 정확한 AST를 생성합니다.
2. **함수 호출 계층(Call Graph) 추출**:
   - 함수 정의(`FUNCTION_DECL`)와 호출 표현식(`CALL_EXPR`)을 연결하여 정확한 호출 관계망(`CALLS`)을 형성합니다.
3. **하드웨어 레지스터 맵 및 비트필드 링크**:
   - 베이스밴드/RF 제어 코드의 핵심인 구조체 포인터 역참조(`pReg->CTRL.bit.ENABLE`) 및 멤버 참조(`MEMBER_REF_EXPR`)를 식별하여 `Function -> RegisterField (ACCESSES_REG)` 엣지를 도출합니다.
4. **Graph-RAG & MCP 연계**:
   - 추출된 노드와 엣지를 그래프 DB(Neo4j, Kùzu, DuckDB)에 저장하고, AI 에이전트(Cursor, Claude, Antigravity)가 필요한 서브그래프(1~3 홉 이내)만을 MCP 서버를 통해 컨텍스트로 전달받아 토큰 낭비 없이 완벽한 코드 리뷰와 이슈 분석을 수행합니다.

---

## 🎯 조직 내 기대 효과 (Group 2nd Brain)

- **환각 없는 레거시 코드베이스 파악**: 모호한 동명 함수나 매크로 분기로 인한 AI 환각을 원천 차단.
- **HW 요구사항 변경 영향도 자동 추적**: 특정 레지스터 비트가 수정될 때 영향을 받는 모든 C 함수 경로를 그래프 쿼리 한 번으로 역추적.
- **정밀한 코드 리뷰 자동화**: 호출 계층과 하드웨어 제어 타이밍의 정합성을 사전 검증.

---

## 🔗 연관 자료 및 개념
- [[active-second-brain]]
- [[vibe-coding]]
- [[_sources/Study/Codebase-Understanding/Clang-CodeGraph/20260920/Semantic_CodeGraph_Indexer_Clang|Clang CodeGraph Indexer 상세 연구 및 파이프라인 가이드]]
- [[_sources/Study/Codebase-Understanding/Clang-CodeGraph/20260920/semantic_codegraph_indexer.py|libclang 기반 인덱서 PoC 스크립트]]
