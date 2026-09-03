---
title: Hot Cache
updated: 2026-09-04
---

## Recent Activity
- **Documented `2nd-brain-system-design-blueprint` (2026-09-04):**
  - Synthesized 5-stage architecture lifecycle: Ingestion ➡️ Multi-Layer Storage (Markdown/Neo4j) ➡️ Hybrid Search (FTS 2gram + Vector + Neo4j) ➡️ Context Compression (Headroom) ➡️ Downstream Presentation/Video (BananaLM 7-styles & Google Vids) ➡️ Self-Evolving Feedback Loop.
- **Created `slide-video-pipeline` Skill (2026-09-04):**
  - E2E 13-stage presentation & AI video production workflow.
  - Features 7 distinct BananaLM / modern style presets (Memphis Flat, Cyberpunk Neon, Swiss Minimal, Warm Editorial, Glassmorphism, Neo-Brutalism, Executive Navy & Gold).
  - Automatically structures speaker notes for Google Vids / TTS video rendering.
- **Full Wiki Organize Pipeline Executed (2026-09-04):**
  - Ingested CodeMate clipping, 20260901 Slide Workflow, 2026-09-01 News Briefing.
  - Synchronized `_sources/` indexes (34 files / 8 folders) via `generate-index`.
  - Audited 72 knowledge pages with **0 broken links, 0 orphan pages**.

## 📌 Skills TODO / Revisit Roadmap
1. **`context-compressor` (Headroom 기반 토큰 압축기):**
   - *상태:* TODO (추후 보완 설치)
   - *목적:* 대용량 검색 로그, Git diff, JSON 도구 출력을 LLM 컨텍스트 주입 전 50~80% 압축하는 유틸리티/MCP 프록시.
   - *연계 대상:* Headroom Python 라이브러리 / 로컬 MCP 서버 연동.
2. **`graph-rag-architect` (4계층 하이브리드 지식 그래프 검색 설계기):**
   - *상태:* TODO (추후 보완 설치)
   - *목적:* [2-gram FTS + Vector + Neo4j Graph Expansion ➡️ RRF ➡️ Cross-Encoder Reranker] 엔터프라이즈 아키텍처 스키마/쿼리 생성기.
   - *연계 대상:* Neo4j Docker 인스턴스 / KG-MCP 연계.

## Active Threads
- **Multimodal Video & Content Workflow:** `slide-video-pipeline` (BananaLM 프롬프트 ➡️ Google Vids).
- **On-Device / Local Edge LLM:** CodeMate, Slotstream, Smolcoder.
- **Embodied AI & Physical AI:** Unitree H1/G1, Optimus, Atlas, Sim-to-Real transfer.
