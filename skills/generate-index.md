---
title: Generate Index Skill
category: skills
tags:
  - automation
  - python
  - indexing
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260817/obsidian_llm_wiki_guide.md]]"
created: "2026-08-17"
updated: "2026-08-17"
summary: Obsidian 원본 소스 폴더의 내부 문서를 스캔하여 인덱스 파일(_index.md)을 자동 생성 및 갱신하는 스킬.
base_confidence: 0.9
lifecycle: draft
tier: supporting
provenance:
  extracted: 1.0
  inferred: 0.0
  ambiguous: 0.0
---

# Generate Index Skill

LLM 위키의 `_sources/` 폴더 내에 저장된 수많은 원본 파일들을 구조적으로 탐색하기 위해, 파이썬 기반 스크립트를 사용하여 폴더별 인덱스(`_index.md`) 및 마스터 인덱스를 자동으로 갱신하는 자동화 기술입니다.

## 동작 방식 (Mechanism)

1. **Vault 탐색:** 상위 폴더로 이동하며 `.env`의 `OBSIDIAN_VAULT_PATH` 또는 `~/.obsidian-wiki/config`를 스캔하여 루트 경로를 잡습니다.
2. **기존 설명 보존:** 하위 폴더의 마크다운 파일을 정렬하여 수집하며, 기존 `_index.md`가 존재하면 사용자가 작성한 기존 설명을 딕셔너리로 보존합니다.
3. **새 설명 추출:** 기존 인덱스에 없는 새로운 파일은 문서 내부의 첫 번째 H1(`#`) 또는 H2(`##`) 제목을 추출하여 설명으로 사용합니다.
4. **마스터 인덱스 갱신:** `_sources/_index.md` 파일을 열고, 새롭게 추가된 하위 폴더의 링크가 없다면 `## 주제별 폴더 목록` 아래에 자동으로 삽입합니다.

## 사용법 (Usage)

Antigravity IDE 등 AI 에이전트 인터페이스에서 `/generate-index` 명령(Skill)으로 등록하여 사용합니다.

```bash
# 전체 소스 폴더 일괄 처리
python3 scripts/generate_index.py

# 특정 폴더 하나만 타겟으로 처리
python3 scripts/generate_index.py "특정폴더명"
```

## 프롬프트 레퍼런스 (Prompt Reference)

이 스킬의 핵심인 `scripts/generate_index.py` 코드는 AI에게 명확한 규칙(보존, 추출, 파일 갱신 등)을 지시하는 구체적인 프롬프트 엔지니어링을 통해 생성되었습니다. 자세한 프롬프트 원문 및 워크플로우는 [[concepts/llm-wiki-workflow]] 문서를 참고하십시오.
