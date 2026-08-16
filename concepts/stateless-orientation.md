---
title: Stateless Orientation
category: concepts
tags: [ai, agents, second-brain, architecture, state-management]
sources: ["agent:research-agent 2nd Brain Architecture Plan (2026-08-16)"]
created: 2026-08-16
updated: 2026-08-16
summary: "상태(State)를 보존하지 않는 AI 에이전트가 파일 시스템을 영구 메모리로 사용하여 매 세션마다 문맥을 복원하는 기법."
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-16"
tier: supporting
relationships:
  - target: "[[concepts/agentic-vault]]"
    type: uses
---

# 무상태 방향성 유지 (Stateless Orientation)

AI 에이전트(LLM)는 본질적으로 세션 간의 상태(State)를 보존하지 않는 무상태(Stateless) 특성을 가진다. 세션이 종료되면 이전 대화나 기억은 모두 초기화된다. 이를 극복하기 위해 에이전트가 외부 파일 시스템(예: Obsidian Vault)을 영구 메모리(Persistent Memory)로 활용하여 매 세션마다 스스로의 위치와 역할을 재설정하는 기법이다.

## 핵심 프로토콜

1. **Session Start Protocol (세션 시작 프로토콜)**
   - 에이전트가 호출되면 가장 먼저 저장소 루트에 있는 `AGENTS.md` (또는 `CLAUDE.md`, `GEMINI.md`)와 같은 오리엔테이션 파일을 읽도록 지시받는다.
   - 이 파일에는 페르소나, 코딩 컨벤션, 금기어, 폴더 구조 등 전역적인 맥락(Context)이 담겨 있어 에이전트가 일관성 있게 행동하도록 돕는다.^[extracted]

2. **Handoff Protocol (핸드오프 프로토콜)**
   - 세션이 종료될 때 에이전트는 자신이 수행한 작업 내역과 앞으로 해야 할 일(Next steps)을 특정 파일(`hot.md`, `log.md` 등)에 기록한다.
   - 다음 세션에서 활성화된 에이전트나 다른 도구가 이 로그를 읽고 이전 세션의 컨텍스트를 그대로 이어받는다.^[inferred]

## [[agentic-vault|Agentic Vault]]와의 관계
이 패턴은 Agentic Vault 구조를 완성하는 핵심 매커니즘이다. 지식 보관소는 단순한 문서 저장소가 아니라 에이전트의 뇌(Brain) 상태를 기록하는 라이브 시스템이 된다.
