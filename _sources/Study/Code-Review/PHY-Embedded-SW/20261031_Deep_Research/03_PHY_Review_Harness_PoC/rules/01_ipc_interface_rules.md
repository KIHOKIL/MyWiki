# Rulebook 01: Upper-Layer IPC Interface Rules (L2/MAC ↔ L1/PHY)

## Scope
Applies to all headers and source files under `ipc/`, `l1_l2_if/`, `shm/`, and any shared memory message structures between ARM cores or L2/L1 subsystems.

## Mandatory Invariants

### 1. `[PHY-IPC-01]` Explicit Alignment, Packing, and Size Assertions
- **Rule:** Every struct transmitted across shared memory or hardware mailboxes MUST have deterministic layout across compilers (`armclang` L1 vs L2 compiler).
- **Check:**
  - Verify `STATIC_ASSERT(sizeof(msg_t) == EXPECTED_BYTES)` or `_Static_assert` is present when modifying IPC structs.
  - Ensure 32-bit/64-bit fields do not cross natural alignment boundaries (causing ARM Alignment Fault on unaligned load/store instructions like `LDRD`/`STRD`).
  - Verify backward compatibility or explicit IPC version bumping when fields are reordered or inserted.

### 2. `[PHY-IPC-02]` Memory Barrier (`DMB`/`DSB`) & Cache Coherency Ordering
- **Rule:** On ARM Cortex-R/A/M cores, shared memory writes MUST complete before updating the ring-buffer write index or triggering the hardware IPC interrupt.
- **Required Sequence (Producer):**
  1. Write payload into `shm_ring->buf[write_idx]`.
  2. If non-cache-coherent shared SRAM/DDR: `SCB_CleanDCache_by_Addr(...)`.
  3. Execute `__DMB()` (Data Memory Barrier) so payload writes are observed before index update.
  4. Update `shm_ring->write_idx`.
  5. Execute `__DSB()` (Data Synchronization Barrier) before writing to the MMIO IPC doorbell register.

### 3. `[PHY-IPC-03]` Untrusted Upper-Layer Parameter Validation
- **Rule:** Treat all incoming IPC payload parameters (`cell_idx`, `cc_idx`, `harq_id`, `bwp_id`, `prb_start`, `prb_num`, `pdu_len`) as untrusted boundary inputs.
- **Check:** Block any PR where IPC payload fields are used directly as array indices or `memcpy` lengths without an explicit `if (val >= MAX_LIMIT)` guard at the IPC handler entry point.

