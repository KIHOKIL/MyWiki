---
title: Wiki Organize Skill
category: skills
tags:
  - automation
  - pipeline
  - ingest
  - indexing
  - lint
  - workflow
sources:
  - ".agents/skills/wiki-organize/SKILL.md"
created: "2026-09-03"
updated: "2026-09-03"
summary: 사용자가 '위키 정리해줘'라고 요청 시 Ingest, Generate-Index, Wiki-Lint & Link의 3단계를 순서대로 자동 완결하는 올인원 위키 통합 파이프라인 스킬.
base_confidence: 0.95
lifecycle: reviewed
tier: core
---

# Wiki Organize Skill (올인원 위키 자동 정리)

## 📌 개요
**Wiki Organize Skill**은 사용자가 학습이나 메모를 마친 후 **"위키 정리해줘"**, **"공부한 거 정리해줘"**, 또는 **`/wiki-organize`**라고 요청했을 때, 분리되어 있던 3가지 필수 유지관리 작업을 단일 파이프라인으로 묶어 순차적으로 자동 실행하는 종합 오케스트레이션 스킬입니다.

---

## 🛠️ 자동 수행 3단계 파이프라인
1. **1단계: 지식 증류 (wiki-ingest)**
   - `_raw/` 임시 초안 및 `_sources/` 신규 노트를 분석하여 `concepts/`와 `entities/`로 증류·컴파일.
   - 프론트매터 스키마 및 요약(`summary`), `.manifest.json` 해시 등록.
2. **2단계: 소스 인덱스 갱신 (generate-index)**
   - `python scripts/generate_index.py`를 실행하여 `_sources/` 내 각 폴더별 `_index.md` 및 마스터 인덱스 동기화.
3. **3단계: 링크 치유 및 건전성 검사 (wiki-lint & cross-link)**
   - 깨진 링크(Broken links) 자동 복구.
   - 고립 문서(Orphans) 상호 위키링크 연결.
   - `index.md`, `log.md`, `hot.md` 최종 갱신 및 완료 리포트 제출.

---

## 💬 호출 트리거
- *"위키 정리해줘"*
- *"공부한 거 정리해줘"*
- *"전체 정리해줘"*
- *`/wiki-organize`*
