---
title: "WeKnora"
category: "entities"
tags: ["LLM", "Wiki", "Tool", "Open-Source"]
sources: ["_source/Study/AI-활용법/LLM_WiKi/LLM Wiki 설치 사이트.md"]
created: "2026-08-09"
updated: "2026-08-09"
summary: "원문서를 질의응답 및 마크다운 지식베이스로 자동 정리해주는 Tencent의 오픈소스 LLM Wiki 프로젝트."
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: "2026-08-09"
tier: supporting
---

# WeKnora

## 개요
WeKnora는 Tencent에서 개발한 오픈소스 지식 관리 도구로, 일반적인 RAG 기능을 넘어서 문서를 자동으로 마크다운 지식베이스로 정리하는 기능을 갖추고 있습니다.

## 주요 특징
- **Wiki Mode:** 원본 문서를 단순히 검색(RAG)하는 데 그치지 않고, 자율 추론 에이전트가 개입하여 서로 링크된 마크다운 기반의 영구적인 지식베이스로 자동 정리해줍니다.^[extracted]
- **로컬 및 프라이빗 클라우드 배포:** 데이터 통제권이 중요한 환경에서 완전한 프라이빗 구축이 가능합니다.^[extracted]

## 활용 목적
개인 및 소규모 팀 환경에서 지식 베이스를 자동으로 고도화(개인 고도화)하고 싶을 때 매우 적합한 도구입니다. `ChromaDB` 등의 로드맵과도 연결할 수 있습니다.^[inferred]

## 관련 문서
- [[llm-wiki-tools-comparison]]
- [[llm-wiki-vs-rag]]
