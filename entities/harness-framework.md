---
title: Harness Framework
category: entities
tags: [entity, tool, open-source, harness-engineering, claude-code, python, sdd]
sources:
  - "https://github.com/jha0313/harness_framework"
  - "https://www.youtube.com/watch?v=v6UAPUnOSxA"
  - "_sources/Study/AI-Lectures/실밸개발자/20261029_Spec_Driven_Development/AI_시대_새로운_패러다임_Spec_Driven_Development_실밸개발자.md"
created: "2026-10-29"
updated: "2026-10-29"
summary: 실밸개발자(하재상)가 개발한 Spec-Driven Development(SDD) 지원 오픈소스 하네스 프레임워크로, 4대 스펙 문서(PRD, Architecture, ADR, UI Guide)와 claude -p 헤드리스 격리 세션을 통해 메인 컨텍스트 오염을 방지하고 3회 자가 교정 및 원자적 커밋을 수행하는 경량 오케스트레이터입니다.
---

# Harness Framework (`jha0313/harness_framework`)

**Harness Framework**는 실리콘밸리 메타 시니어 엔지니어 하재상(실밸개발자)이 공개한 [[concepts/spec-driven-development|Spec-Driven Development (SDD)]] 실전 지원 경량 오케스트레이션 프레임워크입니다.

---

## 1. 아키텍처 및 구성 요소

```
harness_framework/
├── .claude/
│   ├── commands/
│   │   ├── harness.md       # /harness 7대 Step 설계 원칙 및 index.json 명세
│   │   └── review.md        # /review 5대 체크리스트 기반 코드 리뷰 자동 판정
│   └── settings.json        # 허용 도구, 훅(Hook) 및 권한 설정
├── docs/
│   ├── PRD.md               # 제품 요구사항 정의서 (목표, 사용자 페르소나, 핵심 기능, 제외 범위)
│   ├── ARCHITECTURE.md      # 디렉토리 구조, 디자인 패턴, 데이터 흐름, 상태 관리
│   ├── ADR.md               # 아키텍처 결정 레코드 (결정, 이유, 트레이드오프 삼위일체)
│   └── UI_GUIDE.md          # 디자인 원칙 및 AI 슬롭(AI Slop) 7대 안티패턴 금지
├── phases/                  # [실행 시 생성] 태스크 및 스텝 관리 폴더
│   ├── index.json           # 전체 Phase 상태 인덱스
│   └── 0-mvp/
│       ├── index.json       # Step별 status, summary, error_message
│       ├── step0.md         # 프로젝트 셋업 및 스캐폴딩 프롬프트
│       └── step1.md ~ ...   # 단위별 독립 실행 프롬프트
├── scripts/
│   ├── execute.py           # 핵심 오케스트레이터 (claude -p 독립 세션 기동)
│   └── test_execute.py      # 오케스트레이터 단위 테스트 (20KB+)
└── CLAUDE.md                # 기술 스택, CRITICAL 규칙, 빌드/테스트 명령어
```

---

## 2. 핵심 메커니즘: `scripts/execute.py`

### 1) `claude -p` 헤드리스 독립 서브세션 기동
단일 대화 세션에서 연속으로 5개 이상의 Step을 실행하면 컨텍스트 윈도우가 150k 토큰을 초과하며 성능이 30% 수준으로 붕괴합니다. `execute.py`는 각 Step마다 `claude -p --dangerously-skip-permissions --output-format json` 명령으로 깨끗한 1회용 독립 세션을 기동하여 메인 컨텍스트 오염을 원천 차단합니다.

### 2) Preamble 가드레일 & 컨텍스트 누적
매 세션 기동 시:
- `CLAUDE.md` + `docs/*.md` 가드레일 합성 주입.
- 이전 완료된 Step들의 산출물 1줄 요약(`summary`)만 누적 주입하여 컨텍스트 효율 극대화.

### 3) 3회 자가 교정 루프 (Self-Correction)
AC(Acceptance Criteria, 예: `npm test`) 검증 실패 시, 직전 `error_message`를 다음 프롬프트에 피드백하며 최대 3회까지 자율 수정 시도.

### 4) 원자적 2단계 커밋 (Atomic Commits)
- 코드 변경 커밋: `feat({phase}): step {num} — {name}`
- 오케스트레이션 메타데이터 커밋: `chore({phase}): step {num} output`

---

## 3. UI 디자인 가이드: AI 슬롭(AI Slop) 7대 금지 규정

시니어 엔지니어의 품격을 유지하기 위해 `docs/UI_GUIDE.md`에서 AI 템플릿의 전형적 클리셰 7가지를 원천 차단:
1. `backdrop-filter: blur()` (글래스모피즘 남발 금지)
2. `gradient-text` (배경 그라데이션 텍스트 금지)
3. `"Powered by AI"` 배지 (무가치한 장식 금지)
4. `box-shadow` 네온 글로우 애니메이션 금지
5. 보라/인디고 브랜드 색상 클리셰 ("AI = 보라색" 금지)
6. 모든 카드에 균일한 `rounded-2xl` 적용 금지
7. 배경 `gradient orb` (blur-3xl 원형 배경) 금지

---

## 4. 연결된 지식
- [[concepts/spec-driven-development|스펙 주도 개발 (Spec-Driven Development)]] — 하네스 프레임워크가 실체화하는 개발 방법론
- [[concepts/harness-engineering|하네스 엔지니어링 (Harness Engineering)]] — 상위 시스템 설계 개념
- [[entities/ecc|ECC (Everything Claude Code)]] — 전역 규칙 및 TDD 가드 훅 프레임워크
