# AGENTS.md — PHY Embedded SW Group Code Review Harness Rules

> **Target Harness:** `OpenCode` (`anomalyco/opencode`)
> **LLM Providers:** Open-Weight Models (`DeepSeek-R1/V3`, `GLM-4.5`, `Qwen3-Coder`)
> **Compiler & Build:** `ARM Clang` (`armclang`) + `CMake` (`compile_commands.json`)

## 1. Core Review Philosophy
1. **Zero Tolerance for Real-Time & Hardware Glitches:** In ARM-based Mobile PHY SW, an unbounded loop in an ISR, a missing `volatile` on MMIO, a `|=` on a Write-1-to-Clear (`W1C`) register, or a missing `DMB`/`DSB` barrier before an IPC doorbell is a **P0 Production Blocker**.
2. **Zero Noise (Lazy Senior Principle — `ponytail`):** Never comment on formatting, variable naming preferences, or speculative "what-if" defensive checks that add unnecessary branches/cycles in hot paths.
3. **Mandatory Disproving Pass (`cloudflare/security-audit-skill`):** Before reporting any candidate issue, verify the caller chain via `codebase-memory-mcp` (`clangd` call-graph) or `code-review-graph`. If the caller already holds `IRQ_LOCK` or validates the range, discard the finding (`REJECTED`).

## 2. Dynamic Path-Based Rule Routing (`alibaba/open-code-review` Pattern)
When reviewing files in a Pull Request, load and enforce the corresponding layer rulebook from `.opencode/rules/` (or `rules/`):
- `ipc/`, `l1_l2_if/`, `shm/` ➡️ Read and enforce [`rules/01_ipc_interface_rules.md`](rules/01_ipc_interface_rules.md)
- `proc/`, `ul/`, `dl/`, `meas/`, `rach/`, `harq/` ➡️ Read and enforce [`rules/02_3gpp_procedure_rules.md`](rules/02_3gpp_procedure_rules.md)
- `dev/`, `hal/`, `reg/`, `rf/`, `dma/` ➡️ Read and enforce [`rules/03_device_hal_register_rules.md`](rules/03_device_hal_register_rules.md)
- `isr/`, `sched/`, `evt/`, `hisr/` ➡️ Read and enforce [`rules/04_isr_event_concurrency_rules.md`](rules/04_isr_event_concurrency_rules.md)

