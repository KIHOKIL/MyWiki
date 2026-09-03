---
title: Agentic Vault
category: concepts
tags: [ai, second-brain, obsidian, architecture, agents]
sources: ["agent:research-agent 2nd Brain Architecture Plan (2026-08-16)"]
created: 2026-08-16
updated: 2026-08-16
summary: "에이전트가 코어 지식과 도구를 명확히 탐색하고 활용할 수 있도록 최적화된 하이브리드 지식보관소 구조."
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-16"
tier: supporting
relationships:
  - target: "[[concepts/stateless-orientation]]"
    type: uses
---

# Agentic Vault (에이전트 친화적 지식보관소)

최신 실리콘밸리 최고 수준의 개발자들과 AI 에이전트(Claude Code, Cursor 등) 사용자들이 채택하는 2nd Brain 아키텍처 패턴이다. AI 에이전트의 컨텍스트(Context) 인지 능력과 자율성을 극대화하기 위해 설계되었다.

## 핵심 원칙

1. **지식과 도구의 분리 및 연동 (Hybrid Architecture)**
   - **코어 지식(Monorepo)**: 개인의 생각, 프로젝트, 맥락 데이터는 하나의 Vault(예: MyWiki) 안에 유지하여 에이전트가 전체적인 연결고리를 볼 수 있게 한다.
   - **범용 스킬(Polyrepo)**: 범용적으로 쓰이는 에이전트 도구나 플러그인은 외부 레포지토리(예: `KIHOKIL/Utils`)에서 독립적으로 개발하고, 이를 Vault 내에 Git Submodule이나 패키지 형태로 당겨와서(Install) 사용한다.^[inferred]

2. **The "Skill" Pattern (스킬 모듈화)**
   - 에이전트의 프롬프트와 동작 지침을 거대한 시스템 프롬프트 하나에 하드코딩하지 않는다.
   - 특정 작업을 위한 지시사항을 `SKILL.md`라는 파일 단위로 모듈화하여 특정 경로(`.agents/skills/` 등)에 배치한다.
   - 에이전트는 작업이 주어졌을 때 이 디렉토리를 탐색(Discovery)하여 자신에게 필요한 스킬을 스스로 찾아 실행한다.

3. **[[stateless-orientation|무상태 방향성 유지 (Stateless Orientation)]]**
   - 세션이 종료되면 기억이 초기화되는 LLM의 한계를 극복하기 위해, Vault 자체가 에이전트의 '영구 메모리' 역할을 하도록 파일 기반의 프로토콜을 사용한다.

4. **[[human-on-the-loop|인간 중심의 데이터 검수 (Human-on-the-Loop)]]**
   - 에이전트는 `_raw/` (Inbox) 폴더에 쌓인 거친 데이터를 읽고 정제하여 `concepts/`나 `entities/`로 분류하는 자동화 파이프라인 역할을 수행하고, 인간은 그 결과물을 최종 리뷰 및 승인한다.

## 핵심 내장 스킬 및 워크플로우
- [[skills/wiki-organize]] — Ingest ➡️ Generate-Index ➡️ Lint & Link 3단계 자동화
- [[skills/prompt-creator]] — 상용급 맞춤 AI 프롬프트 및 에이전트 설계 스킬
- [[skills/generate-index]] — 소스 디렉토리 인덱스 동기화 스킬
