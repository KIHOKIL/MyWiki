---
title: Wiki Log
---

# Wiki Log

- [2026-09-13 16:36] generate-index folders=Books,Clippings,News,Projects,Study,Work-Ideas files=49
- [2026-09-13 16:34] CHORE: Wiki-Organize Pipeline Execution
  - Ingested 5 sources into concepts (embedded-software, yield-curve-inversion, bond-laddering) and entities (news-summarizer, fable-5-1, gpt-6-astra).
  - Moved processed raw drafts to _raw/_archived/
  - Rebuilt all `_sources/` master indexes via `generate_index.py`.
  - Validated and updated master `index.md`, `log.md`, `hot.md`, and `.manifest.json`.
- [2026-09-10 23:03] FIX: Google Sheets Subscriber Synchronization & Secret Update (NewsSummarizer)
  - Issue: Scheduled agent ran and sent emails only to primary receiver (총 1명 발송 완료), missing 7 Google Form response subscribers.
  - Root Cause: GitHub Secret `SUBSCRIBERS_CSV_URL` was registered on Aug 21 with `/pub?output=csv` pointing to empty default sheet (`gid=652869560`). Code also only triggered multi-sheet discovery if URL explicitly contained `pubhtml`.
  - Fix: Upgraded `get_additional_subscribers()` in `tech/main.py` and `finance/main.py` to automatically detect any Google Sheets URL format, discover all tab `gid`s via `pubhtml`, and extract subscribers with `User-Agent` headers.
  - Secret Updated: Updated GitHub Secret `SUBSCRIBERS_CSV_URL` via `gh secret set`.
  - Verification: Added subscriber verification step to `verify_all.py` (7/7 checks pass) and unit tests in pytest (23/23 pass). Pushed to `main` and verified GitHub Actions CI pass.
- [2026-09-06 23:15] CHORE: Wiki-Organize Pipeline Execution (Study Notes Ingestion)
  - Extracted concepts & entities from `OpenHuman_심층분석_및_사내_Group_2nd_Brain_연계.md`.
  - Created `concepts/memory-tree.md` and `entities/tokenjuice.md`.
  - Rebuilt all `_sources/` master indexes via `generate_index.py`.
  - Validated and updated master `index.md` alphabetically.
- [2026-09-06 15:48] FEAT: Telecom & Mobility Strategy C-Pilot (통신·모빌리티 전략 분석기)
  - Persona & Role: C-Level Strategy Advisor (수익 모델/BM 다각화, TCO 절감, SWOT 위협/기회 분석).
  - Monitoring Target: Broadcom, Marvell, Qualcomm, MediaTek, NXP (Custom SoC/ASIC), Fibocom, Quectel (CPE/FWA), Starlink (Direct-to-Cell NTN), Telco.
  - Standard Format: Executive Summary (3줄), Business Impact, 벤더 다각화 매트릭스 표, 후속 질문 2~3개.
  - Markdown Table Parser: 이메일 클라이언트 인라인 스타일 <table> 및 모바일 가로스크롤 반응형 변환 엔진 탑재.
  - Test & Live Run: Pytest 12/12 All Pass, verify_all 6/6 All Pass, 2026-09-06_News_Briefing.md 생성 및 이메일 발송 완료.
- [2026-09-06 15:30] FEAT: Senior Mentor Developer GitHub Trend Curation (4-Category Balanced Selection)
  - Role & Persona: 20년 차 시니어 개발자(멘토) 관점의 담백하고 실용적인 톤앤매너 도입.
  - 4 Categories: Second-Brain, Code Review AI, Codebase understanding, Embedded SW implementation.
  - Balanced Selection: 스테디셀러(Star 다수 / All-time Classic) 1개 + 신흥 루키(Trending) 1개 조합 추천 (Overview + Senior's Insight).
  - Robust Ingestion & Fallback: Awesome-list/스팸 필터링 및 4대 카테고리 실존 오픈소스 Fallback(logseq, openhuman, pr-agent, code-review-graph, ast-grep, codebase-memory-mcp, FreeRTOS, embassy-rs) 구축.
  - Email & UI: 모던 인라인 CSS 뱃지(💡 Senior's Insight, 🎯 Overview) 및 카테고리 컬러 카드 도입.
  - Tests: Passed 10/10 pytest and 6/6 automated verify_all checks.
- [2026-09-06 00:53] FEAT: Automated Integrated Verification Pipeline (verify_all & CI)
  - Engine: Built `verify_all.py` with 6 automated checks (Config, RSS, GitHub API, HTML Render, Email Dispatch, Pytest).
  - Tests: Created `tests/test_email.py` (5 tests covering multipart MIME, HTML generation, and SMTP errors). Total 10/10 tests passing.
  - GitHub Actions: Updated `sys_news_summarizer_ci.yml` and `tmpl_python_ci.yml` with `workflow_dispatch` and Step Summary Markdown reporting.
- [2026-09-06 00:48] UPDATE: Add Global Big Tech & AI Frontier M&A to Daily News Summarizer
  - Config: Added `Global Big Tech & AI Frontier: M&A, Strategy & Capital Flow` to `config.json` tracking OpenAI, Anthropic, xAI, Databricks, CoreWeave, and hyperscaler deals.
  - Prompts: Updated `_build_executive_prompt` in `main.py` with the 3rd lens (Big Tech & AI Frontier strategic moves, compute alliances, ecosystem lock-in).
  - Documentation: Updated [[projects/NewsSummarizer]], `hot.md`. Verified all unit tests pass.
- [2026-09-06 00:05] UPDATE: Daily News Summarizer 3-Section & HTML Email Overhaul
  - Config: Restructured `config.json` around Group 2nd Brain, Codebase Loop & Review, AI Hardware, and Mobile Mobility + GitHub Trend queries.
  - Core Logic: Added `fetch_github_trending`, `analyze_github_trending`, `generate_executive_summary`, and `generate_html_email` in `main.py`.
  - Multi-LLM & Fallback: Maintained Gemini-3.1-flash-lite & OpenAI GPT-4o-mini dual engine.
  - HTML Email: High-aesthetic responsive newsletter layout with inlined CSS for universal mail client support.
  - Testing & Docs: Passed 5/5 pytest suite, updated `README.md`, [[projects/NewsSummarizer]], and `hot.md`.
- [2026-09-05 23:46] ORGANIZE: OpenHuman Enterprise 2nd Brain Integration
  - Source created: [[_sources/Study/AI-Lectures/편한AI/20260905/OpenHuman_심층분석_및_사내_Group_2nd_Brain_연계|OpenHuman 심층 분석 및 사내 Group 2nd Brain 연계 구축 전략]].
  - Concept updated: [[concepts/2nd-brain-system-design-blueprint]] (Phase 1 Ingestion 레이어에 OpenHuman 패턴 & Revisit 체크리스트 반영).
  - Journal updated: [[journal/2026-09-05]] (사내 구축 전략 연계 링크 추가).
  - Generate-Index: Re-synchronized `_sources/` folder indexes (Study 폴더 20개 파일 등록).
  - Wiki-Lint: 82개 지식 문서 전수 검사, 0개 orphan 페이지, 100% 링크 건전성 유지.
  - Tracking: log.md, hot.md, .manifest.json 갱신.
- [2026-09-05 23:21] ORGANIZE: Full 3-step wiki-organize pipeline execution
  - Ingest: Processed 20260905 GitHub trend note (_sources/Study/AI-Lectures/편한AI/20260905/github-trend-2026-09-05.md).
  - Entities created: [[entities/openhuman]], [[entities/firefly-iii]], [[entities/ecc]].
  - Synthesis created: [[synthesis/ai-trends-2026-09-05]].
  - Concepts updated: [[concepts/active-second-brain]], [[concepts/harness-engineering]].
  - Journal updated: [[journal/2026-09-05]].
  - Generate-Index: Re-synchronized all _sources/ folder indexes (34 files across 8 folders).
  - Wiki-Lint & Link: Full audit of 82 knowledge pages. 0 orphan pages, 100% schema compliance.
  - Master Index: Synchronized index.md, log.md, hot.md, and .manifest.json.
- [2026-09-05 23:18] CREATE & LINK: OpenHuman & Firefly III Integration
  - Created entities: [[entities/openhuman]], [[entities/firefly-iii]].
  - Updated concept: [[concepts/active-second-brain]] (linked workspace data & financial ledger layers).
  - Updated journal: [[journal/2026-09-05]] (recorded architectural insights and 4 reference links).
  - Synchronized: index.md, log.md, hot.md.
- [2026-09-04 02:20] ORGANIZE: Routine wiki-organize execution
  - Ingest: Verified _raw/ staging (clean) and .manifest.json (21 sources tracked).
  - Generate-Index: Re-synchronized all _sources/ folder indexes (34 files across 8 folders).
  - Wiki-Lint & Link: Full audit of 72 knowledge pages. 0 broken links, 0 orphans, 100% schema compliance.
  - Master Index: Synchronized index.md, log.md, and hot.md.
- [2026-09-04 02:00] ORGANIZE: Executed full 3-step wiki-organize pipeline
  - Ingest: Processed CodeMate clipping, 2026-09-01 Slide Video Workflow, and 2026-09-01 News Briefing.
  - Entities created: [[entities/codemate]], [[entities/unitree]], [[entities/notebooklm]], [[entities/google-vids]].
  - Concepts created: [[concepts/slide-video-workflow]].
  - Generate-Index: Rebuilt _sources/ folder indexes (34 files across 8 folders).
  - Wiki-Lint: 70 knowledge pages audited. 0 broken links, 0 orphans, 100% schema compliance.
  - Manifest & Index: Synchronized .manifest.json, index.md, log.md, and hot.md.
- [2026-08-02 20:05] INIT vault_path="c:\Users\kihok\내 드라이브\MyWiki" categories=concepts,entities,skills,references,synthesis,journal,projects
- [2026-08-09 18:14] INGEST https://www.youtube.com/watch?v=GrEFRTmbMfI -> concepts/llm-wiki-vs-rag.md
- [2026-08-09 18:33] CREATE references/AI-Tools/ai-agent-skills-catalog.md
- [2026-08-09 18:38] INGEST _source/Study/AI-활용법/LLM_WiKi/LLM Wiki 설치 사이트.md -> weknora.md, xwiki.md, obsidian-llm-plugins.md, llm-wiki-tools-comparison.md
- [2026-08-09 23:56] INGEST https://github.com/jha0313/skills_repo -> ai-readiness-cartography.md, improve-token-efficiency.md, presentation-slides-generator.md
- [2026-08-10 00:26] INGEST _source/Projects/HW Change List E2E implementation loop/handoff.md pages_updated=0 pages_created=6 mode=append
- [2026-08-16 02:24] INGEST _source/Study/AI-Lectures/커리어해커알렉스/20260816_진짜AX/20260816_진짜AX_학습메모.md -> ax.md, human-on-the-loop.md, harness-engineering.md, career-hacker-alex.md
-   [ 2 0 2 6 - 0 8 - 1 6   1 1 : 5 1 ]   G R A P H _ C O L O R I Z E   m o d e = b y - t a g   g r o u p s = 1 0   b a c k u p = g r a p h . j s o n . b a c k u p - 2 0 2 6 0 8 1 6 - 1 1 5 1 
 
 -   [ 2 0 2 6 - 0 8 - 1 6   1 1 : 5 6 ]   W I K I _ N A R R A T E   t o p i c = \ 
 
 L�	���X�
 
 $Ƙ�
 
 y o u t u b e 
 
 ���\   v o i c e = l e c t u r e r   r e s u l t _ p a g e s = 4   m o d e = n o r m a l   s a v e d = f a l s e   o u t c o m e = s u c c e s s 
 
 
- [2026-08-16 16:50] INGEST _source/Study/AI-Lectures/실밸개발자/20260816/AI_시대에_상위_1퍼센트가_되는_법.md pages_updated=1 pages_created=2 mode=append
- [2026-08-16 22:49] INGEST agent:research-agent 2nd Brain Architecture Plan (2026-08-16) -> agentic-vault.md, stateless-orientation.md

- [2026-08-17 13:25] INGEST _source/Study/AI-Lectures/편한AI/20260817/obsidian_llm_wiki_guide.md -> llm-wiki-workflow.md, generate-index.md, action-oriented-ai.md, ai-agent-reporting.md

- [2026-08-17 22:39] LINT issues_found=3487 orphans=368 broken_links=1324 missing_summary=374

- [2026-08-17 22:56] LINT_CONSOLIDATE links_fixed=3 orphans_rescued=0 lifecycle_updates=0 tier_demotions=0 tag_fixes=0 contradiction_callouts=0 report=synthesis/consolidation-2026-08-17.md

- [2026-08-17 23:19] INGEST _sources/Study/AI-Lectures/편한AI/20260817/Agentic_2nd_Brain_Architecture.md -> active-second-brain.md, wiki-layer-architecture.md

- [2026-08-17 23:19] INGEST _sources/Study/AI-Lectures/편한AI/20260817/big_tech_ai_workflow_proposal.md -> agentic-scaffolding.md, multi-agent-code-review.md, issueops.md, vibe-coding.md

- [2026-08-17 23:19] INGEST _sources/Study/AI-Lectures/편한AI/20260817/lecture_slides.md -> active-knowledge-pipeline.md, cognitive-overload.md

- [2026-08-17 23:21] generate-index folders=00_Inbox,90_MOC,Books,Clippings,News,Projects,Study,Work-Ideas files=16

- [2026-08-17 23:24] DIGEST period="1d" new_pages=8 updated_pages=0 themes=5 connections=0 saved=true

- [2026-08-23 21:13:21] generate-index  folders=00_Inbox, 90_MOC, Books, Clippings, News, Projects, Study, Work-Ideas  files=18

- [2026-08-23 21:22:38] LINT issues_found=97 orphans=5 broken_links=30 stale=0 contradictions=0 prov_issues=0 missing_summary=40 fragmented_clusters=0 visibility_issues=0 promotion_candidates=0 synthesis_gaps=0 relationship_issues=0



- **2026-08-23**: Ingested `_sources/News/Daily_Summaries/2026-08-23_News_Briefing.md` via `wiki-ingest`. Extracted 6 pages (AI-Native RAN, Physical AI, Agentic Workflow, etc.).

- [2026-09-01] INGEST source='2026-08-29~31_News_Briefing' pages_updated=4 pages_created=8 mode=append

- [2026-09-01] LINT: Completed wiki vault health audit. 52 wiki pages, 40 sources. Auto-repaired 15 syntax formatting issues. Graph integrity verified.

- [2026-09-01] generate-index folders=00_Inbox,90_MOC,Books,Clippings,News,Projects,Study,Work-Ideas files=31

- [2026-09-01] INGEST source=_sources/Study/AI-Lectures/편한AI/20260901/Research_report_LLM_2nd_Brain_Seoul (1).md created=5 (graph-rag, agentic-rag, memgpt, mcp-server, multi-tier-knowledge-architecture) updated=2 (active-second-brain, llm-wiki-vs-rag)- [2026-09-03] INGEST source=_sources/Study/AI-Lectures/편한AI/20260903/ created=7 (context-compression, moe-streaming, headroom, slotstream, smolcoder, rhema, neo4j) updated=1 (graph-rag)
- [2026-09-03 15:39] generate-index folders=00_Inbox,90_MOC,Books,Clippings,News,Projects,Study,Work-Ideas files=34
- [2026-09-03 15:41] LINT: Completed wiki vault health audit. 63 wiki pages in scope. 0 broken links. 0 frontmatter issues. Graph integrity verified.
- [2026-09-14 01:03] generate-index folders=Books,Clippings,News,Projects,Study,Work-Ideas files=60
- [2026-09-14 01:03] LINT: Completed wiki vault health audit. Graph integrity verified, no broken links found.
