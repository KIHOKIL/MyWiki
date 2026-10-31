# Rulebook 03: Device & HAL Register Control Rules

## Scope
Applies to `dev/`, `hal/`, `reg/`, `rf_drv/`, and `dma_drv/` modules performing direct hardware control via Memory-Mapped I/O (MMIO) registers.

## Mandatory Invariants

### 1. `[PHY-HAL-01]` Never Use `|=` on Write-1-to-Clear (`W1C`) Registers
- **Rule:** Hardware interrupt pending and status clear registers (`*_W1C`, `*_CLR`, `*_PEND`, `*_STAT`) clear bits where `1` is written. Using `REG |= (1U << bit)` reads all currently asserted status bits as `1` and writes `1` back to ALL of them, silently dropping concurrent interrupts.
- **Check:** Always enforce direct assignment `REG = (1U << bit);`.

### 2. `[PHY-HAL-02]` Atomic Read-Modify-Write (`RMW`) on Shared Control Registers
- **Rule:** If a hardware control register is modified by both Task/Procedure context and ISR context (or across multiple cores), `REG |= BIT` or `REG &= ~BIT` is a non-atomic Read-Modify-Write race hazard.
- **Check:**
  - Prefer hardware atomic `SET`/`CLR` alias registers if provided by the IP block.
  - Otherwise, require `uint32_t irq_state = PHY_IRQ_SAVE(); ... PHY_IRQ_RESTORE(irq_state);` around the RMW sequence.

### 3. `[PHY-HAL-03]` Mandatory `volatile`, Unsigned Bit Shifts (`1U << n`), and Field Masking
- **Rule:**
  - All MMIO pointers and struct mappings MUST be qualified with `volatile`.
  - Never use signed `1 << 31` (Undefined Behavior in C); always use `1U << 31` or `BIT32(n)`.
  - Multi-bit field writes MUST mask the input value before shifting: `((val & FIELD_MASK) << FIELD_SHIFT)`.

### 4. `[PHY-DEV-01]` Clock & Power Domain Sequencing Before MMIO Access
- **Rule:** Reading or writing any MMIO register of a power-gated or clock-gated modem/RF block triggers an immediate ARM synchronous `BusFault` / `Data Abort`.
- **Check:** Verify in wake-up, abort, and error-dump routines that `hal_clk_is_enabled(block_id)` is verified or enabled (followed by `__DSB()`) before touching block registers.

