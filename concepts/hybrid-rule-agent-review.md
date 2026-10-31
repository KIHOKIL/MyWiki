---
title: "결정론적 규칙 × 멀티 에이전트 하이브리드 코드 리뷰 (Hybrid Rule-Agent Code Review)"
category: concepts
tags:
  - ai-code-review
  - agentic-workflow
  - ast-grep
  - opencode
sources:
  - "_sources/Study/AI-Lectures/실밸개발자/20261031_AI_Code_Review/코드_리뷰가_병목이_되는_이유_메타_시니어_AI_코드_리뷰_실밸개발자.md"
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/01_OpenSource_Code_Review_Benchmark.md"
created: 2026-10-31
updated: 2026-10-31
summary: "순수 LLM 에이전트의 높은 토큰 비용과 오탐(False Positive) 한계를 극복하기 위해, 컴파일러/AST/호출 그래프 기반 결정론적 파이프라인과 이종 모델 반증(Disproving) 에이전트를 결합한 차세대 코드 리뷰 패러다임."
---

# 결정론적 규칙 × 멀티 에이전트 하이브리드 코드 리뷰 (Hybrid Rule-Agent Code Review)

**하이브리드 코드 리뷰(Hybrid Rule-Agent Code Review)**는 알리바바의 [[open-code-review]]와 Cloudflare의 감사 스킬에서 실전 검증된 아키텍처로, **컴파일러·AST·호출 그래프 기반의 결정론적 엔지니어링(Deterministic Engineering)**과 **다중 LLM 에이전트의 추론 및 자기 반증(Reflection / Disproving)**을 결합한 아키텍처입니다.

---

## 1. 왜 순수 에이전트(Pure Agent) 리뷰는 한계에 부딪히는가?
- **토큰 폭증 및 주의력 분산:** 대형 PR에서 에이전트가 스스로 파일을 탐색하느라 9배 이상의 토큰을 소모하며, 컨텍스트가 길어질수록 팀의 도메인 규칙을 망각합니다.
- **자기 확증 편향(Self-Bias):** 코드를 작성한 모델과 동일한 모델로 리뷰하면 동일한 맹점을 공유하여 치명적 버그를 놓칩니다.
- **추측성 오탐(Hallucinated Nitpicks):** 상위 호출자 함수에서 이미 락(Lock)이나 범위 검사를 수행했음에도 변경된 함수 단편만 보고 거짓 경고를 남발합니다.

---

## 2. 하이브리드 파이프라인의 4단계 구조

1. **Tier 1 — 결정론적 정적/AST 게이트 (`armclang` + `clang-tidy` + `ast-grep`):**
   - 문법적·구조적으로 명확한 안티패턴(예: `W1C` 레지스터 `|=` 사용, 타임아웃 없는 `while` 루프)을 토큰 비용 0원, 1초 이내에 100% 검출합니다.
2. **Tier 2 — 그래프 기반 스마트 번들링 (`codebase-memory-mcp` + `code-review-graph`):**
   - 변경된 심볼의 2-hop 호출 반경(Blast Radius)과 연관 헤더 파일만 묶어 에이전트에 주입할 컨텍스트 크기를 1/10로 압축합니다.
3. **Tier 3 — 도메인별 서브에이전트 분리 심사 (`OpenCode` Subagents):**
   - 변경 파일 경로에 맞는 규칙만 동적 주입하여 계층별 특화 에이전트(`ISR/HAL` vs `IPC/3GPP`)를 구동합니다.
4. **Tier 4 — 이종 모델 교차 검증 및 반증 패스 (Cross-Model Disproving Verifier):**
   - 코딩/초안 모델(`Qwen`/`GLM`)과 다른 계열의 추론 모델(`DeepSeek-R1`)이 후보 지적 사항의 반증을 시도하여 오탐을 `rejected`로 기각하고 확정된 블로커만 리포트합니다.

---

## 🔗 연관 개념 및 엔티티
- [[multi-agent-code-review]]
- [[phy-embedded-code-review]]
- [[open-code-review]]
- [[opencode]]
- [[farol]]
- [[phy-sw-ai-code-review-strategy]]

