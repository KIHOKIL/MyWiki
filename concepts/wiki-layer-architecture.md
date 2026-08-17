---
title: 위키 3계층 아키텍처 (Wiki 3-Layer Architecture)
category: concepts
tags:
  - architecture
  - agentic-vault
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/Agentic_2nd_Brain_Architecture.md
created: 2026-08-17
updated: 2026-08-17
---

# 위키 3계층 아키텍처 (Wiki 3-Layer Architecture)

능동형 세컨드 브레인을 구축하기 위한 전체 폴더/시스템 아키텍처는 데이터 흐름에 따라 크게 3개의 계층(Layer)으로 구분됩니다.

## Layer 1: 인간 지식 영역 (Knowledge)
- **목적:** AI가 읽고 답변의 근거로 삼는 **정제된 그라운드 트루스(Ground Truth)**.
- **주요 폴더:** `concepts/`, `entities/`, `synthesis/`, `journal/`
- **특징:** RAG(Retrieval-Augmented Generation) 환경에서 AI가 가장 먼저 검색하는 핵심 노드들. 마크다운 양방향 링크(`[[ ]]`)를 통해 강하게 결합됩니다.

## Layer 2: AI 행동 영역 (Agents & Skills)
- **목적:** AI가 텍스트 생성을 넘어 실제 행동(Action)을 수행하게 만드는 팔다리 및 통제 역할.
- **주요 폴더:** `.agents/` (또는 `skills/`), `.github/` (Harness), `scripts/`
- **특징:** 특정 목적을 달성하기 위한 행동 강령(`SKILL.md`)을 보관하며, CI/CD 크론잡 스케줄링을 통해 AI를 주기적으로 동작하게(Heartbeat) 만듭니다.

## Layer 3: 데이터 파이프라인 영역 (Sources & Raw)
- **목적:** 외부 세계의 정보를 위키 내부로 흡수하는 소화 기관.
- **주요 폴더:** `_sources/`, `_raw/`, `_archives/`
- **특징:** 스크랩, 대화 기록 등을 임시 보관(`_raw/`)하거나, 텍스트가 아닌 무거운 강의 자료, 실행 가능한 코드 등을 안전하게 격리 보관(`_sources/`)합니다. AI 에이전트가 이곳을 스캔해 Layer 1으로 정보를 끌어올립니다.

## 연관 개념
- [[active-second-brain]]
