---
title: "PHY 임베디드 코드 리뷰 아키텍처 (PHY Embedded Code Review Architecture)"
category: concepts
tags:
  - embedded-phy-sw
  - ai-code-review
  - arm-clang
  - register-hal
  - agentic-workflow
sources:
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/00_PHY_SW_Code_Review_Master_Blueprint.md"
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/02_PHY_5Layer_Review_Invariants_Catalog.md"
created: 2026-10-31
updated: 2026-10-31
summary: "ARM 코어 기반 모바일 물리계층(PHY) 임베디드 SW의 5개 아키텍처 계층(Upper IPC, 3GPP Procedure, Device, HAL Register, ISR/Event-driven)에 특화된 AI-Native 코드 리뷰 체계 및 5축 리스크 평가 모델."
---

# PHY 임베디드 코드 리뷰 아키텍처 (PHY Embedded Code Review Architecture)

**PHY 임베디드 코드 리뷰 아키텍처**는 일반적인 웹/백엔드 중심의 AI 코드 리뷰(단순 문법·스타일·웹 보안 점검)가 포착하지 못하는 **하드웨어 타이밍 결정성(Real-Time Determinism), 레지스터 직접 제어(MMIO/W1C/RMW), 멀티코어 공유 메모리 배리어(`DMB`/`DSB`), 3GPP 상태 머신 무결성**을 검증하기 위해 설계된 도메인 특화 코드 리뷰 체계입니다.

---

## 1. 5대 핵심 검증 계층 (5-Layer Verification Scope)

1. **Layer 1 — Upper-Layer IPC Interface (`L2/MAC ↔ L1/PHY`):**
   - 공유 메모리 메시지 구조체의 바이트 정렬(Alignment/Packing) 및 크기 불변성(`STATIC_ASSERT`).
   - ARM 약한 메모리 순서(Weak Memory Ordering) 환경에서 페이로드 기록 후 `__DMB()` ➡️ 링버퍼 인덱스 갱신 후 `__DSB()` ➡️ 하드웨어 메일박스(Doorbell) 트리거 순서 보장.
   - 상위 레이어 전달 파라미터(`cell_idx`, `harq_id`, `prb_num`)의 배열 인덱스 범위 검증.
2. **Layer 2 — 3GPP Standard Procedure Layer:**
   - HARQ, RACH, CSI, BWP Switching, DRX 상태 머신(FSM)에서 비정상 취소(`Abort`, `Reconfig`, `Timeout`) 발생 시 고아 상태(Dead-end) 및 버퍼 누수 방지.
   - SFN(`0..1023`) 및 슬롯 번호 랩어라운드(Wrap-around) 모듈로 연산 보장.
3. **Layer 3 — Device Layer:**
   - RF/Baseband/DMA 하드웨어 블록의 Clock/Power Domain 활성화 전 MMIO 접근으로 인한 ARM `BusFault` 원천 차단.
   - 비동기 DMA 버퍼 수명주기 및 캐시 Clean/Invalidate 일관성 보장.
4. **Layer 4 — HAL Layer (Register Control):**
   - Write-1-to-Clear (`W1C`) 상태/인터럽트 클리어 레지스터에 `|=` 연산 사용 금지(단순 대입 `=` 강제).
   - 공유 제어 레지스터의 비원자적 Read-Modify-Write (`RMW`) 경쟁 조건 방지 및 `volatile` / `1U << n` 부호 없는 시프트 강제.
5. **Layer 5 — Interrupt (ISR) & Event-Driven Activities:**
   - Hard ISR 및 그 하위 호출 그래프([[isr-concurrency-verification]]) 내 블로킹 OS API, 동적 할당(`malloc`), 타임아웃 없는 하드웨어 폴링 루프 절대 금지.

---

## 2. PHY 5축 Risk Score 루브릭 (0~100점)

| 축 (Axis) | 배점 | 핵심 평가 지표 |
| :--- | :---: | :--- |
| **1. Real-Time & ISR Determinism** | **30점** | ISR/FIQ 경로 포함 여부, 무한 폴링 위험, TTI/Slot 사이클 예산 영향 |
| **2. HAL Register & Concurrency** | **25점** | `volatile`, `W1C`, 비원자적 `RMW`, `DMB`/`DSB` 배리어, DMA 캐시 |
| **3. IPC & 3GPP Contract Breakage** | **20점** | L1-L2 IPC 구조체 정렬/패딩 변화, 3GPP 절차 상태 머신 전이 누락 |
| **4. Call-Graph Blast Radius** | **15점** | [[clang-codegraph]] / `code-review-graph` 기준 상위 호출자 파급 반경 |
| **5. Target Build & Test Evidence** | **10점** | `armclang` 경고 0건, `ast-grep` 통과, L1 시뮬레이터 테스트 동반 여부 |

---

## 🔗 연관 개념 및 엔티티
- [[hybrid-rule-agent-review]]
- [[isr-concurrency-verification]]
- [[clang-codegraph]]
- [[hw-change-contract]]
- [[opencode]]
- [[open-code-review]]
- [[farol]]
- [[phy-sw-ai-code-review-strategy]]

