---
title: NewsSummarizer
category: Entities
tags:
  - python
  - gemini
  - api-pacing
  - ai-agent
sources:
  - "agent:raw-draft NewsSummarizer Repository"
created: 2026-09-08
updated: 2026-09-13
summary: "Gemini 3.6 Flash 모델을 활용하여 매일 뉴스를 요약하고 리포트를 생성하는 자동화 AI 에이전트 프로젝트."
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-09-13"
tier: supporting
provenance:
  extracted: 1.0
  inferred: 0.0
  ambiguous: 0.0
---

# NewsSummarizer

NewsSummarizer는 매일 뉴스와 관련 정보를 수집하여 요약 리포트를 생성하는 자동화 AI 에이전트 파이프라인입니다.

## Architecture & Updates (2026-09-08)

최근 API Pacing(속도 제한) 문제 해결을 위한 아키텍처 개편이 있었습니다.

### Gemini 3.6 Flash & Rate Limit Fix
- **이슈 사항**: Gemini API의 Free tier 제한(15 RPM)으로 인해 `429 Too Many Requests` 에러가 발생.
- **모델 통합**: 이전에는 OpenAI(`gpt-4o-mini`) 폴백을 사용했으나, 계정 이슈로 인해 제거하고 모든 에이전트(`agents/tech/main.py`, `agents/finance/main.py`, `agents/tech/update_topic.py`)를 `gemini-3.6-flash`로 단일화했습니다.
- **Pacing 구현**: `time.sleep(5)`를 추가하여 주요 API 호출 전 속도를 조절했습니다.
- **재시도 전략 변경**: `tenacity` 패키지의 재시도 전략을 `wait_exponential`에서 `wait_fixed(10)`으로 변경하여 과도한 블로킹을 방지했습니다.

### 데이터 파이프라인
- Finance 출력 경로: `C:\Users\kihok\내 드라이브\MyWiki\_sources\News\Finance`로 이동.
- RSS Feed 수집의 신선도 유지를 위해 GitHub Actions 스케줄을 `when: 1d`로 갱신했습니다.

## Future Roadmap

Tech 에이전트는 기존 Google News 기반 수집에 더해, GitHub Search API(`fetch_github_trending`)를 통한 일일 트렌드 큐레이션 통합을 예정하고 있습니다.
