# Rulebook 02: 3GPP Standard Procedure Layer Rules

## Scope
Applies to `proc/`, `ul/`, `dl/`, `meas/`, `harq/`, `rach/`, `csi/`, `bwp/`, and `drx/` modules implementing 3GPP TS 38.211 / 38.212 / 38.213 / 38.214 physical layer procedures.

## Mandatory Invariants

### 1. `[PHY-PROC-01]` Finite State Machine (FSM) Abort/Timeout Completeness
- **Rule:** Every active procedure state (e.g., `RACH_WAIT_RAR`, `HARQ_WAIT_ACK`, `BWP_SWITCH_PENDING`, `CSI_MEAS_ACTIVE`) MUST handle abnormal termination events:
  - `EVENT_ABORT` / `EVENT_CELL_RELEASE`
  - `EVENT_BWP_SWITCH` / `EVENT_RECONFIG`
  - `EVENT_SLOT_TIMEOUT`
- **Check:** Verify that on abnormal exit, all allocated DMA descriptors, HARQ buffers, and hardware timers are explicitly released and the state resets to `IDLE`.

### 2. `[PHY-PROC-02]` SFN (0..1023) and Slot Wrap-Around Arithmetic
- **Rule:** System Frame Number (`SFN`, `0..1023`) wraps around every `10.24` seconds. Direct comparison (`target_sfn > curr_sfn`) or naive subtraction (`curr_sfn - start_sfn`) is a confirmed bug.
- **Check:** Require wrap-around safe modular arithmetic macros:
  ```c
  #define PHY_SFN_DIFF(curr, prev) (((uint32_t)(curr) + 1024U - (uint32_t)(prev)) & 0x3FFU)
  ```

### 3. `[PHY-PROC-03]` Slot/Symbol Processing Budget & Cross-Channel Symmetry
- **Rule:** Slot/Symbol tick handlers must execute within deterministic cycle budgets.
- **Check:**
  - Flag nested loops over `(MAX_UE * MAX_RB * MAX_SYM)` added inside real-time slot scheduling paths.
  - When a bug is fixed in one channel/RAT handler (e.g., NR PUSCH), check via `code-review-graph` if the symmetric handler (e.g., NR PDSCH or LTE PUSCH) shares the same cloned logic.

