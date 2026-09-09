---
title: NewsSummarizer Update - Gemini 3.6 Flash & Rate Limiting
category: Projects
tags:
  - python
  - gemini
  - api-pacing
  - ai-agent
sources:
  - NewsSummarizer Repository
created: 2026-09-08
updated: 2026-09-08
---

# NewsSummarizer - Gemini 3.6 Flash & Rate Limit Fix

## Background
- Pacing issue with Gemini API caused 429 Too Many Requests (15 RPM limit on free tier).
- OpenAI fallback (`gpt-4o-mini`) was used temporarily but user does not have an active OpenAI account.

## Fixes Implemented
- Standardized all AI requests in `agents/tech/main.py`, `agents/finance/main.py`, and `agents/tech/update_topic.py` to use `gemini-3.6-flash`.
- Removed OpenAI fallback logic and mock tests.
- Implemented API pacing using `time.sleep(5)` before main Gemini API calls.
- Switched `tenacity` retry strategy from `wait_exponential` to `wait_fixed(10)` to prevent excessive blocking.
- Moved Finance output paths to `C:\Users\kihok\내 드라이브\MyWiki\_sources\News\Finance`.
- Updated GitHub Actions to `when: 1d` on RSS feeds to ensure freshness.

## Future Plans
- The Tech agent incorporates a GitHub search API augmentation step (`fetch_github_trending`) to pull daily trend curation in addition to Google News.
