---
title: Hot Cache
updated: 2026-09-05
---

## Recent Activity
- **OpenHuman Enterprise 2nd Brain Architecture Integration (2026-09-05):**
  - **In-Depth Study Note:** Documented [[OpenHuman_심층분석_및_사내_Group_2nd_Brain_연계]] linking to 2026-09-03 Group 2nd Brain guide.
  - **Blueprint Enhancement:** Updated [[concepts/2nd-brain-system-design-blueprint]] Phase 1 Ingestion (20-min Auto-fetch + TokenJuice noise filter + 3-tier Memory Tree) and enterprise security checklist (Internal PAT, Exchange/Jira/Confluence on-prem).
  - **Full Wiki Organize Pipeline Executed:** Ingested 20260905 trend note, created [[entities/openhuman]], [[entities/firefly-iii]], [[entities/ecc]], and [[synthesis/ai-trends-2026-09-05]]. Re-indexed `_sources/` (35 files / 8 folders). Audited 82 knowledge pages with **0 orphan pages** and 100% schema compliance.
- **Documented `2nd-brain-system-design-blueprint` (2026-09-04):**
  - Synthesized 5-stage architecture lifecycle: Ingestion ➡️ Multi-Layer Storage (Markdown/Neo4j) ➡️ Hybrid Search (FTS 2gram + Vector + Neo4j) ➡️ Context Compression (Headroom) ➡️ Downstream Presentation/Video (BananaLM 7-styles & Google Vids) ➡️ Self-Evolving Feedback Loop.
- **Created `slide-video-pipeline` Skill (2026-09-04):**
  - E2E 13-stage presentation & AI video production workflow.
  - Features 7 distinct BananaLM / modern style presets (Memphis Flat, Cyberpunk Neon, Swiss Minimal, Warm Editorial, Glassmorphism, Neo-Brutalism, Executive Navy & Gold).
  - Automatically structures speaker notes for Google Vids / TTS video rendering.

## 📌 Skills TODO / Revisit Roadmap
1. **`context-compressor` (Headroom / TokenJuice 기반 토큰 압축기):**
   - *상태:* TODO (추후 보완 설치)
   - *목적:* 대용량 검색 로그, Git diff, JSON 도구 출력, 이메일/메신저 로그를 LLM 컨텍스트 주입 전 50~80% 압축하는 유틸리티/MCP 프록시.
   - *연계 대상:* Headroom Python 라이브러리 / OpenHuman TokenJuice / 로컬 MCP 서버 연동.
2. **`graph-rag-architect` (4계층 하이브리드 지식 그래프 검색 설계기):**
   - *상태:* TODO (추후 보완 설치)
   - *목적:* [2-gram FTS + Vector + Neo4j Graph Expansion ➡️ RRF ➡️ Cross-Encoder Reranker] 엔터프라이즈 아키텍처 스키마/쿼리 생성기.
   - *연계 대상:* Neo4j Docker 인스턴스 / KG-MCP 연계.

## Active Threads
- **Local-First Agentic Hub & Connectors:** `OpenHuman` (Workspace & Memory Tree), `Firefly III` (Finance MCP & Rule-Writer).
- **Multimodal Video & Content Workflow:** `slide-video-pipeline` (BananaLM 프롬프트 ➡️ Google Vids).
- **On-Device / Local Edge LLM:** CodeMate, Slotstream, Smolcoder.
- **Embodied AI & Physical AI:** Unitree H1/G1, Optimus, Atlas, Sim-to-Real transfer.
