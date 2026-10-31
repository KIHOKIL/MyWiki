---
title: "인터럽트 및 이벤트 구동 동시성 검증 (ISR & Event-Driven Concurrency Verification)"
category: concepts
tags:
  - embedded-phy-sw
  - isr-concurrency
  - arm-clang
  - ai-code-review
sources:
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/02_PHY_5Layer_Review_Invariants_Catalog.md"
created: 2026-10-31
updated: 2026-10-31
summary: "실시간 모바일 물리계층(PHY) 임베디드 SW에서 하드웨어 인터럽트(ISR)와 백그라운드 태스크/이벤트 루프 간의 선점 레이스, 블로킹 호출, 무한 폴링, Torn Read/Write를 정적 호출 그래프와 에이전트로 검증하는 기법."
---

# 인터럽트 및 이벤트 구동 동시성 검증 (ISR & Event-Driven Concurrency Verification)

모바일 물리계층(PHY) 임베디드 소프트웨어에서 **ISR(Interrupt Service Routine)**과 **이벤트 구동(Event-Driven / HISR) 액티비티**는 서브밀리초(Sub-ms) 단위의 슬롯(Slot)·심볼(Symbol) 타이밍 데드라인을 결정짓는 가장 치명적인 실행 컨텍스트입니다.

---

## 1. 4대 핵심 검증 불변조건 (4 Core ISR Invariants)

1. **전이적 비블로킹 보장 (Transitive Non-Blocking Guarantee):**
   - `ISR_*` 함수 본문뿐만 아니라, [[clang-codegraph]] 또는 `codebase-memory-mcp`를 통해 역추적한 **모든 하위 피호출자(Callees) 경로**에 `mutex_lock`, `semaphore`, `osDelay`, `malloc/free`, 포맷팅 `printf`가 존재해서는 안 됩니다.
2. **유한 폴링 루프 강제 (Bounded Hardware Polling):**
   - 하드웨어 PLL Lock이나 DMA 완료 비트를 기다리는 `while (!(REG & READY))` 루프에 탈출 카운터(`timeout--`)가 없으면, RF/하드웨어 글리치 발생 시 코어 전체가 영구 행(Hang)에 빠져 Watchdog 리셋을 유발합니다. `ast-grep` 구조 규칙으로 타임아웃 없는 `while` 폴링을 100% 사전 차단합니다.
3. **공유 상태 원자성 및 Torn Read 방지 (Shared State Atomicity):**
   - 32비트 ARM 코어에서 ISR이 갱신하는 64비트 타이머/카운터나 복합 구조체를 일반 태스크가 `IRQ_LOCK`이나 `Seqlock` 없이 읽으면 상위/하위 워드가 찢어지는 **Torn Read**가 발생합니다.
4. **Top-Half ↔ Bottom-Half 이벤트 큐 오버플로 방어:**
   - ISR(Top-Half)이 HISR/Event Queue(Bottom-Half)에 이벤트를 푸시할 때 `QUEUE_FULL` 반환값을 무시하면 3GPP 프로토콜 상태 머신이 영구 정지(Stall)합니다.

---

## 🔗 연관 개념
- [[phy-embedded-code-review]]
- [[hybrid-rule-agent-review]]
- [[clang-codegraph]]
- [[embedded-software]]

