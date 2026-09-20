---
title: Codebase Understanding Study Archive
category: study
tags:
  - codebase-understanding
  - ast
  - graph-rag
  - embedded-software
  - static-analysis
created: 2026-09-20
updated: 2026-09-20
summary: C/C++ 대규모 통신 프로토콜 및 임베디드 SW를 위한 AST, Graph-RAG, 레지스터 맵 심볼 링킹, 정적 분석 도구 체계적 연구 아카이브.
---

# Codebase Understanding Study Archive (코드베이스 이해 및 심층 분석 연구)

모바일 통신 프로토콜 스택(PHY/MAC), 실시간 임베디드 SW, 복잡한 하드웨어-소프트웨어 제어 레거시 코드베이스의 **이해 정확도를 극대화하고 AI 에이전트의 토큰 소모를 최소화하기 위한 정적 분석(AST, Graph-RAG, Code Graph)** 연구 아카이브입니다.

---

## 🎯 핵심 연구 영역 (Key Focus Areas)

1. **AST & 컴파일러 정적 분석**: Clang LibTooling, `libclang`, `clang-query`, `ast-grep`, `tree-sitter` 비교 및 평가.
2. **코드 지식 그래프 (Code Graph & Graph-RAG)**: 함수 호출망(Call Graph), 전역 변수/상태 참조망, 헤더 포함 관계의 그래프 DB(Neo4j, Kùzu, DuckDB) 색인.
3. **하드웨어 레지스터 맵 & 심볼 링킹**: 메모리 맵 기반 HW 레지스터 접근(`volatile`, 구조체 비트필드)과 상위 SW 호출 체인 간의 1:1 인덱싱.
4. **AI 에이전트 & MCP(Model Context Protocol) 연동**: Cursor, Claude Code, Antigravity 에이전트에 필요한 최소한의 1% 서브그래프만 컨텍스트로 주입하여 비용 80~90% 절감 및 환각 차단.

---

## 📂 하위 주제별 아카이브

- [[_sources/Study/Codebase-Understanding/Clang-CodeGraph/README|Clang-CodeGraph]]: Clang LibTooling 및 컴파일러 기반 시맨틱 코드그래프 인덱싱
