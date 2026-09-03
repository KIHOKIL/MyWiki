---
title: "NotebookLM"
category: Entity
tags: [ai, google, research, note-taking, rag, grounding]
sources: ["_sources/Study/AI-Lectures/편한AI/20260901/20260901_슬라이드_영상제작_워크플로우.md"]
summary: "Google의 문서 기반 AI 리서치 및 개인화 지식 어시스턴트로, 소스 그라운딩과 오디오 브리핑(Audio Overview)을 지원."
base_confidence: 0.95
lifecycle: stable
tier: core
created: 2026-09-04
updated: 2026-09-04
---

구글(Google)이 개발한 문서 기반 개인 맞춤형 AI 리서치 및 노트 도우미입니다. 업로드된 PDF, 구글 닥스, 텍스트, 웹페이지 등 엄선된 소스 문서만을 바탕으로 정확한 출처 인용(Source Grounding) 기반의 질의응답과 요약, 오디오 팟캐스트 브리핑 생성을 제공합니다.

## 주요 기능 및 활용

- **소스 그라운딩 (Source Grounding):** 업로드된 참조 문서에 엄격하게 기반하여 환각(Hallucination)을 억제하고 신뢰성 높은 지식 추출 지원.
- **오디오 브리핑 (Audio Overview):** 소스 문서들의 핵심 논점을 두 명의 AI 호스트가 대화하는 팟캐스트 형태로 생성.
- **슬라이드/영상 리서치 파이프라인 연계:** [[concepts/slide-video-workflow]]의 1~3단계(자료 수집, 노이즈 필터링, 개요 도출)를 전담하는 핵심 리서치 두뇌로 활용.

## 관련 개념 및 문서
- [[concepts/slide-video-workflow]]
- [[concepts/active-second-brain]]
- [[concepts/active-knowledge-pipeline]]
- [[entities/google-vids]]
