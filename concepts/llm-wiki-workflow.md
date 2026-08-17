---
title: LLM Wiki 7-Step Workflow
category: concepts
tags:
  - workflow
  - llm-wiki
  - knowledge-management
sources:
  - "[[_source/Study/AI-Lectures/편한AI/20260817/obsidian_llm_wiki_guide.md]]"
created: "2026-08-17"
updated: "2026-08-17"
summary: LLM 위키에서 데이터를 수집하고 구조화된 지식으로 자동 변환하는 7단계 핵심 작업 흐름.
base_confidence: 0.9
lifecycle: draft
tier: core
provenance:
  extracted: 1.0
  inferred: 0.0
  ambiguous: 0.0
relationships:
  - target: "[[concepts/agentic-vault]]"
    type: related_to
---

# LLM Wiki 7-Step Workflow

LLM 기반 세컨드 브레인(Second Brain) 시스템이 원본 데이터를 유기적인 지식 네트워크로 변환하는 핵심 7단계 프로세스입니다.

## 1. 입력 (Input & Clipping)
- **영구 보존 데이터:** PDF, 논문, 공식 매뉴얼 등은 `_sources/` 폴더에 위치시킵니다.
- **임시 데이터:** 아이디어 메모나 웹 클리핑, 단순 텍스트는 `_raw/` 폴더에 드롭합니다.

## 2. Ingest 실행 (Triggering)
- 사용자가 에이전트(예: Antigravity IDE)에게 `/wiki-ingest` 명령을 내립니다.
- 에이전트가 `.manifest.json`을 확인하여 새롭게 추가되거나 변경된 파일(Delta)만 필터링합니다.

## 3. 내부 처리 (Internal Distillation)
에이전트가 단독으로 다음 과정을 백그라운드에서 수행합니다:
1. **읽기 (Read):** 소스 문서 분석.
2. **추출 (Extract):** 개념(Concepts), 개체(Entities), 기술(Skills)로 내용 분해.
3. **병합 (Resolve):** 기존 위키 지식과 충돌 여부를 검사하고 `[[Wikilinks]]`를 형성.
4. **구조화 (Schema):** 적절한 마크다운 파일로 포매팅.

## 4. 결과물 분류 (Categorization)
추출된 지식 조각들이 성격에 맞는 전용 디렉토리로 분배되어 저장됩니다.
- `concepts/` (추상적 개념)
- `entities/` (구체적 대상)
- `skills/` (실행 가능한 절차)
- `references/` (참고 문헌 및 팩트)

## 5. 시스템 파일 자동 갱신 (System Metadata)
추가된 지식 구조를 반영하여 위키의 인프라 파일들이 업데이트됩니다.
- `index.md`: 마스터 목차 갱신
- `log.md`: Ingest 히스토리 기록
- `.manifest.json`: 소스 파일 해시 및 처리 상태 기록

## 6. 원본 파일 처리 (Cleanup)
- `_sources/`에 위치한 원본(Layer 1)은 그대로 보존됩니다.
- `_raw/`에 존재하던 임시 초안은 지식으로 승격(Promotion)된 후 아카이브(`_raw/_archived/`)로 이동되거나 삭제됩니다.

## 7. 결과 확인 (Visualization)
- 사용자는 옵시디언(Obsidian)의 그래프 뷰(Graph View)를 열어, 흩어져 있던 문서들이 어떻게 의미적으로 연결되었는지(Link) 시각적 위상(Topology)을 확인하고 탐험합니다.
