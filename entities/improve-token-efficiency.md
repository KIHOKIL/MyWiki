---
title: "Improve Token Efficiency"
category: "entities"
tags: ["AI-Agent", "Skill", "Claude", "Optimization", "Cost"]
sources: ["https://github.com/jha0313/skills_repo"]
created: "2026-08-09"
updated: "2026-08-09"
summary: "Claude Code의 로컬 세션 로그(JSONL)를 파싱하여 토큰 캐시 적중률과 비용을 분석하고 효율 최적화 방안을 제공하는 스킬."
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-09"
tier: supporting
---

# Improve Token Efficiency

## 개요
Claude Code CLI 사용 시 기록되는 세션 로그(JSONL)를 읽어들여, 프로젝트(레포) 단위로 API 토큰 사용 효율, 비용, 그리고 프롬프트 캐시(Prompt Caching) 적중률을 분석해 주는 에이전트 스킬입니다.

## 주요 기능
- **토큰 및 비용 추적:** Input/Output 토큰뿐만 아니라 `cache_creation_input_tokens`, `cache_read_input_tokens` 등 에페메럴(ephemeral) 캐시 항목을 완벽히 분리하여 정확한 달러($) 비용을 추산합니다.
- **효율성 점수(Rubric):** Cache utilization (40%), Output density (20%), Read redundancy (20%), Tool economy (20%) 4가지 지표를 바탕으로 세션별 A+ 부터 F까지의 등급을 매깁니다.
- **HTML 시각화 대시보드:** 누적 비용, Pareto 차트(비용을 많이 쓴 상위 세션 분석), Cost vs Score 버블 차트 등을 단일 HTML 파일로 렌더링해 줍니다.
- **예상 절감 비용 도출:** Sonnet 모델로의 라우팅, 장시간 세션 축소(`/compact`), 중복 Read 제거 등 액션 플랜을 적용했을 때 절약될 가상의 $ 비용을 계산해 제시합니다.

## 활용 시점
- "이번 달 Claude Code 요금이 왜 이렇게 많이 나왔지?"
- "어떻게 하면 Context 윈도우 캐싱을 극대화하여 비용을 줄일 수 있을까?" 고민될 때.

## 관련 문서
- [[ai-agent-skills-catalog]]
