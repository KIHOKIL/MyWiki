---
title: "OpenCode (오픈소스 터미널/CI AI 코딩 및 리뷰 에이전트 하네스)"
category: entities
tags:
  - opencode
  - ai-code-review
  - agentic-workflow
  - mcp-server
sources:
  - "https://github.com/anomalyco/opencode"
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/00_PHY_SW_Code_Review_Master_Blueprint.md"
created: 2026-10-31
updated: 2026-10-31
summary: "다양한 오픈 웨이트 LLM(DeepSeek, GLM, Qwen)과 로컬 MCP 서버를 네이티브로 연결하여 대화형 코딩 및 헤드리스 CI 코드 리뷰(opencode run)를 수행하는 오픈소스 에이전트 하네스 (GitHub Stars 223.4k+, MIT)."
---

# OpenCode (`anomalyco/opencode`)

- **GitHub:** [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)
- **검증 지표:** ⭐ **223,474 Stars** | 🍴 **30,006 Forks** | 언어: `TypeScript` | 라이선스: `MIT`

---

## PHY 임베디드 SW 코드 리뷰 핵심 기능
1. **사내 오픈 웨이트 LLM 완벽 호환:** OpenAI 호환 게이트웨이(`@ai-sdk/openai-compatible`)를 통해 사내에 구축된 `DeepSeek-R1/V3`, `GLM-4.5`, `Qwen3-Coder`를 에이전트별로 다르게 매핑할 수 있습니다.
2. **역할별 서브에이전트 분리 (`.opencode/agent/*.md`):** 읽기 전용 권한(`edit: deny`)을 가진 계층별 감사 서브에이전트(`phy-isr-hal-auditor`, `phy-ipc-3gpp-auditor`)와 최종 반증 검증기(`phy-chief-verifier`)를 선언적으로 구성합니다.
3. **로컬/CI 헤드리스 실행 (`opencode run`):** `.githooks/pre-push` 및 GitHub Actions에서 비대화형으로 즉시 실행되어 자동화된 PR 코멘트 및 리스크 채점을 수행합니다.
4. **네이티브 MCP 연동:** `DeusData/codebase-memory-mcp` (`compile_commands.json` 기반 C/C++ 호출 그래프)를 직결하여 무환각 심볼 추적을 수행합니다.

---

## 🔗 연관 문서
- [[phy-embedded-code-review]]
- [[hybrid-rule-agent-review]]
- [[phy-sw-ai-code-review-strategy]]

