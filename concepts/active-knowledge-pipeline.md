---
title: 능동적 지식 파이프라인 (Active Knowledge Pipeline)
category: concepts
tags:
  - workflow
  - knowledge-management
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/lecture_slides.md
created: 2026-08-17
updated: 2026-08-17
---

# 능동적 지식 파이프라인 (Active Knowledge Pipeline)

단순히 문서를 폴더에 넣고 끝나는 것이 아니라, 외부에서 들어온 데이터가 AI에 의해 자동으로 지식으로 변환되고 위키 네트워크에 결합되는 **4단계 자동화 프로세스**입니다.

## 4단계 데이터 변환 파이프라인
1. **Ingest (수집):** Web Clipper나 수동 복사를 통해 `_sources/` 또는 `_raw/` 폴더에 원본 파일이 드롭되는 단계입니다.
2. **Extract (추출):** AI가 파일을 읽고 주요 지식을 조각(Chunk) 단위, 즉 개념(Concept), 개체(Entity), 기술(Skill)로 분해하는 단계입니다.
3. **Resolve (병합):** 추출된 조각들을 기존 위키 지식 그래프와 대조하여 중복을 제거하고 관계망(Link)을 형성합니다.
4. **Schema (구조화):** `index.md`, `log.md`, `.manifest.json` 등의 시스템 파일을 자동 갱신하고 임시 파일을 정리(Cleanup)하는 단계입니다.

인간은 1단계인 큐레이션(어떤 데이터를 넣을 것인가)에만 집중하고, 2~4단계의 분류/정제/연결 작업은 전적으로 AI 에이전트에게 맡기는 것이 핵심입니다.

## 연관 개념
- [[active-second-brain]]
- [[cognitive-overload]]
