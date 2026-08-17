---
title: 다중 에이전트 코드 리뷰 (Multi-agent Code Review)
category: concepts
tags:
  - workflow
  - engineering
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/big_tech_ai_workflow_proposal.md
created: 2026-08-17
updated: 2026-08-17
---

# 다중 에이전트 코드 리뷰 (Multi-agent Code Review)

단일 AI 모델에 리뷰 전체를 맡기는 것이 아니라, **역할이 분리된 여러 에이전트가 코드를 다각도에서 검토하고 서로 교차 검증하는 리뷰 시스템**입니다. Anthropic(Claude)과 같은 기업에서 사내에 운영하는 방식입니다.

## 작동 방식
1. PR(Pull Request)이 생성되면 리뷰 파이프라인(예: Github Actions 기반 CI 봇)이 동작합니다.
2. **역할 분담:** 
   - [보안 체크 에이전트]: 보안 취약점만 중점 검사.
   - [로직 체크 에이전트]: 비즈니스 로직과 알고리즘 정확성 검토.
   - [사내 규정 체크 에이전트]: 코딩 컨벤션 및 팀 룰 검사.
3. **교차 검증 (Verification Layer):** 각 에이전트의 결과를 취합하여 오탐(False Positive)을 걸러냅니다.
4. **결과 보고:** 최종 종합된 결과를 사람에게 보고(Github Issue 코멘트 등)합니다.

이러한 분업화된 에이전틱 리뷰를 통해 휴먼 에러를 방지하고 리뷰 품질을 획기적으로 높일 수 있습니다.

## 연관 개념
- [[agentic-scaffolding]]
- [[issueops]]
