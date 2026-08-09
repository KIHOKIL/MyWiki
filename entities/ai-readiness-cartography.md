---
title: "AI-Readiness Cartography"
category: "entities"
tags: ["AI-Agent", "Skill", "Audit", "Codebase"]
sources: ["https://github.com/jha0313/skills_repo"]
created: "2026-08-09"
updated: "2026-08-09"
summary: "코드베이스의 AI 에이전트 친화도(AI-Ready)를 100점 만점으로 감사하고 HTML 대시보드와 개선 액션 리스트를 제공하는 스킬."
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-09"
tier: supporting
---

# AI-Readiness Cartography

## 개요
임의의 코드베이스(레포지토리)가 Claude Code, Cursor 등 자율형 AI 에이전트가 탐색하고 이해하기 얼마나 적합한지 평가하는 프롬프트/스크립트 번들 스킬입니다.

## 주요 기능
- **자동 채점(Scoring):** Python 스크립트(`score.py`)를 통해 모듈 내비게이션, 빌드/테스트 인프라, 문서 퀄리티, 레포 컨텍스트 일치도 등 7개 카테고리(100점 만점)를 평가합니다.
- **HTML 대시보드 생성:** JSON 결과를 바탕으로 다크 테마/라이트 테마가 적용된 가독성 높은 HTML 보고서(대시보드)를 생성하여, 의사결정권자에게 현재 코드의 AI 호환성을 보고할 수 있게 합니다.
- **ROI 정렬 액션:** 단순 점수만 내는 것이 아니라, 어떤 부분을 고쳐야 가장 큰 임팩트(토큰 절감, 시간 절약)가 있는지 노력(Effort) 대비 성과(Impact) 리스트를 우선순위화하여 제시합니다.

## 활용 시점
- "우리 회사 레포가 Claude Agent에 적합한가?"
- "코드를 AI-Friendly하게 개선하고 싶은데 어디부터 손대야 할지 모를 때"

## 관련 문서
- [[ai-agent-skills-catalog]]
