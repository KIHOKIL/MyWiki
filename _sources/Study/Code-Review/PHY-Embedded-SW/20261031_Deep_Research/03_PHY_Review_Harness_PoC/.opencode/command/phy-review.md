---
description: "PHY 임베디드 SW 5-Layer 하이브리드 코드 리뷰 실행 (AST-Grep + Call-Graph + 이종 오픈 모델 교차 검증)"
agent: phy-chief-verifier
model: litellm/deepseek-r1
---

다음 절차에 따라 현재 브랜치의 변경 사항(Git Diff)에 대해 **PHY 5-Layer 코드 리뷰 및 5축 Risk Score 채점**을 수행하라:

1. **결정론적 정적/AST 진단 수집**
   - `ast-grep scan --rule .ast-grep/rules/phy-hal-isr-rules.yml` 실행 결과 확인
   - 변경된 파일 목록 및 라인 수 확인: `git diff --stat origin/main...HEAD`
2. **호출 그래프 파급 반경(Blast Radius) 조회**
   - `codebase-memory` MCP의 `detect_changes` 및 `trace_path` 도구를 호출하여 수정된 C/C++ 함수의 상위 호출자(특히 `ISR_*` 핸들러 도달 여부)와 구조체 참조처를 파악하라.
3. **도메인 서브에이전트 위임 (필요 시)**
   - `hal/`, `dev/`, `isr/` 경로 포함 시 `@phy-isr-hal-auditor` 관점으로 Layer 3/4/5 불변조건 점검
   - `ipc/`, `proc/`, `ul/`, `dl/` 경로 포함 시 `@phy-ipc-3gpp-auditor` 관점으로 Layer 1/2 불변조건 점검
4. **반증 패스(Disproving Pass) 및 최종 리포트 출력**
   - 상위 함수에서 이미 방어되었거나 스타일 취향에 불과한 지적은 모두 기각(`rejected`)하라.
   - 살아남은 결함만 `[CONFIRMED_BLOCKER]` / `[NEEDS_HW_VALIDATION]`으로 분류하고, **PHY 5축 Risk Score (0~100점)** 마크다운 테이블과 최종 `VERDICT: PASS|FAIL`을 출력하라.
