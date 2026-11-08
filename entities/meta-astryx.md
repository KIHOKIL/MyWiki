---
title: "Meta Astryx (meta/astryx)"
category: entity
tags:
  - design-system
  - agentic-engineering
  - meta
  - spec-driven-development
  - llm-eval
sources:
  - _sources/Study/Agentic-Engineering/Meta-Astryx/20261108_Meta_Astryx_Architecture.md
  - https://github.com/meta/astryx
created: 2026-11-08
updated: 2026-11-08
summary: "Meta가 8년간 13,000개 이상의 사내 앱에서 검증한 뒤 오픈소스로 공개한 React 19 + StyleX 기반 디자인 시스템이자, 토큰 압축형 AGENTS.md, 양방향 스펙-코드 링커(pnpm specs:for), 10턴 문맥 열화 측정 하네스(Vibe-Tests)를 갖춘 대표적인 Agent-Ready 레퍼런스 저장소."
---

# Meta Astryx (`meta/astryx`)

**Meta Astryx**([`github.com/meta/astryx`](https://github.com/meta/astryx))는 Meta에서 8년간 13,000개 이상의 내부 애플리케이션을 구동하며 발전한 사내 최대 규모의 디자인 시스템을 오픈소스(MIT)로 공개한 프로젝트다. **React 19+**와 Meta의 빌드 타임 Atomic CSS 컴파일러인 **StyleX** 위에 구축되었으며, 150개 이상의 접근성 준수 컴포넌트와 7종의 테마, 그리고 인간 개발자와 AI 코딩 에이전트가 공용으로 사용하는 CLI(`@astryxdesign/cli`)를 제공한다.

## 핵심 아키텍처 특징

1. **Agent-Ready CLI & 초고밀도 `AGENTS.md`:**
   - `astryx component <Name> --dense`, `astryx template <name> --skeleton` 등 토큰 효율성이 극대화된 CLI 명령과 파이프(`|`) 구분자 기반의 `AGENTS.md` 제약조건 블록을 통해 에이전트가 500ms 이내에 환각 없이 정확한 API 명세를 부트스트랩하도록 설계되었다.
2. **Knowledge Contracts (`pnpm specs:for <path>`):**
   - 모든 아키텍처/컴포넌트 스펙 문서는 `authority: draft | current | archived` 상태를 명시하며, `applies_to`와 `verified_by` 필드를 통해 실제 코드 경로 및 테스트 파일과 양방향으로 연결된다.
   - `pnpm specs:for --diff origin/main`을 통해 PR 변경분이 건드리는 불변조건(Claims)과 시맨틱 리뷰 트리거(`review-applicability:v1`)를 자동 추출한다.
3. **Vibe-Tests (`internal/vibe-tests`):**
   - `AGENTS.md`와 문서 구조가 실제 LLM의 코드 생성 성공률에 미치는 영향을 측정하는 자체 Eval 벤치마크 스위트다.
   - 무균 서브에이전트(Context-Free Sub-Agents) 원칙과 10턴 대화 열화 곡선(`--degradation`, Turn 0/6/8/10 프로브) 측정을 통해 긴 세션에서의 규칙 유지력을 정량 평가한다.

## 관련 문서
- [[20261108_Meta_Astryx_Architecture|Meta Astryx 심층 해부 연구 노트]]
- [[01_Meta_Senior_2ndBrain_and_Eval_Notes|실밸개발자 — 개발자를 위한 2nd Brain과 Eval]]
- [[concepts/clang-codegraph|Clang 코드그래프 (Clang CodeGraph)]]
- [[synthesis/phy-sw-ai-code-review-strategy|PHY 임베디드 SW 하이브리드 AI 코드 리뷰 전략]]
