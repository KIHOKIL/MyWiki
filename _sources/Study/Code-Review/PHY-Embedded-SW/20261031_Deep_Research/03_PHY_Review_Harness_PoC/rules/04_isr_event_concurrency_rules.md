# Rulebook 04: Interrupt (ISR) & Event-Driven Concurrency Rules

## Scope
Applies to `isr/`, `sched/`, `evt/`, `hisr/`, and any function reachable in the call-graph of a hardware interrupt handler (`ISR_*`, `FIQ_*`, `IRQ_*`).

## Mandatory Invariants

### 1. `[PHY-ISR-01]` Zero Blocking, Zero Dynamic Allocation, Bounded Execution in ISR
- **Rule:** Functions executing in ISR context (and all transitive callees traced via `codebase-memory-mcp`) MUST NEVER call:
  - OS blocking primitives (`mutex_lock`, `sem_wait`, `osDelay`, `vTaskDelay`)
  - Heap allocation (`malloc`, `calloc`, `realloc`, `free`, `new`, `delete`)
  - Heavy synchronous formatting/logging (`printf`, `sprintf`, UART polling print)
- **Check:** Trace the 2-hop outbound call-graph of any modified function; if any caller is an ISR, enforce strict ISR constraints on the callee.

### 2. `[PHY-ISR-02]` Mandatory Timeout Bound on Hardware Polling Loops
- **Rule:** Never poll a hardware status register with an unbounded `while (!(REG & READY))` loop. If RF/BB hardware glitches or loses clock, the CPU hangs forever until Watchdog reset.
- **Check:** Every hardware wait loop MUST decrement an explicit `timeout` counter and execute a deterministic error-recovery return when `timeout == 0U`.

### 3. `[PHY-ISR-03]` Torn Read/Write & Shared State Protection (ISR ↔ Task/HISR)
- **Rule:** Any state shared between an ISR and a lower-priority HISR/Task must be protected against preemption races:
  - 64-bit variables (`uint64_t`) or multi-word structs read/written on 32-bit ARM cores without IRQ lock or Seqlock suffer from **Torn Reads**.
  - Flag any unprotected non-atomic shared state mutation.

### 4. `[PHY-ISR-04]` Top-Half (ISR) to Bottom-Half (HISR/Event Queue) Overflow Handling
- **Rule:** When an ISR defers work by pushing an event to an Event Queue or HISR ring buffer, it MUST check the enqueue return status (`PHY_QUEUE_FULL`).
- **Check:** Silent drop of an ISR event stalls the 3GPP state machine indefinitely. Require explicit overflow counter increment and recovery/assert handling.

