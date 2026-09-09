---
title: Memory Tree
category: concepts
tags:
  - memory-tree
  - data-structure
  - openhuman
  - knowledge-graph
  - hierarchy
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260905/OpenHuman_심층분석_및_사내_Group_2nd_Brain_연계.md]]"
created: "2026-09-06"
updated: "2026-09-06"
summary: "데이터를 무작정 벡터 DB에 넣지 않고, Source Tree, Topic Tree, Global Tree의 3단계 계층 구조로 체계화하여 LLM 환각을 방지하고 컨텍스트를 압축하는 로컬 마크다운 기반 데이터 저장 구조."
---

# Memory Tree

## 📌 개요
**Memory Tree**는 비정형 데이터를 벡터 DB에 단순 텍스트 청크로 분할해 넣는 대신, **계층적인 3단계 구조(Source -> Topic -> Global)**로 체계화하여 저장하는 데이터 파이프라인 및 저장 구조 설계 패턴입니다. [[entities/openhuman|OpenHuman]]과 같은 로컬 기반 개인 AI 에이전트 허브에서 적극적으로 사용됩니다.

이 방식은 최종적으로 [[entities/neo4j|Neo4j]]와 같은 지식 그래프로 데이터를 주입할 때 노이즈를 획기적으로 줄여주며, LLM의 환각(Hallucination) 현상을 원천 차단하는 중간 정규화 버퍼 역할을 수행합니다.

## 🏛️ 3계층 아키텍처

1. **Source Tree (원천별 격리)**
   - 수집된 원본 데이터(이메일, Jira 티켓, Confluence 문서 등)를 원천 시스템의 고유 ID를 기준으로 1:1 저장합니다.
   - 예: `jira/PROJ-1024.md`, `confluence/page-8921.md`

2. **Topic Tree (도메인/프로젝트별 집약)**
   - 특정 기능, 모듈, 프로젝트별로 관련 이슈, 회의록, 이메일 의사결정을 자동 그룹핑합니다. 통상 LLM 컨텍스트 한계를 고려해 3k 토큰 이하로 정제합니다.
   - 예: `CDC_CLK_Validation.md`, `Lint_Engine_Roadmap.md`

3. **Global Tree (일일 다이제스트)**
   - 하루 동안 발생한 주요 상태 변경, 릴리즈 이슈, 공지사항 등을 날짜별 타임라인으로 요약하여 전역적인 메타 인지(Meta-cognition)를 제공합니다.

## 💡 장점 (Neo4j 지식 그래프와의 시너지)
- **노드/엣지 추출 비용 절감:** 정제된 Memory Tree 텍스트를 Neo4j 추출기에 넣으면, 불필요한 보일러플레이트가 이미 제거되어 있어 그래프 추출 비용이 약 80% 절감됩니다.
- **가시성 확보:** 사용자가 에이전트의 기억(메모리)을 파일 시스템에서 직접 열람하고 수정할 수 있어 투명성이 보장됩니다.
