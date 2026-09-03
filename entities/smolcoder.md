---
title: Smolcoder
category: entities
tags:
  - smolcoder
  - coding-agent
  - local-llm
  - ollama
  - typescript
  - open-source
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/20260903_학습노트.md]]"
  - "https://github.com/leonvanzyl/smolcoder"
created: "2026-09-03"
updated: "2026-09-03"
summary: Ollama 및 LM Studio와 연동하여 클라우드 비용 없이 로컬에서 안전하게 작동하는 초경량 터미널 코딩 에이전트 CLI 도구.
base_confidence: 0.9
lifecycle: reviewed
tier: core
---

# Smolcoder

## 📌 개요
**Smolcoder**는 유튜버이자 개발자인 Leon van Zyl이 개발한 오픈소스 프로젝트([github.com/leonvanzyl/smolcoder](https://github.com/leonvanzyl/smolcoder))로, Ollama와 LM Studio 등 로컬 모델 실행 환경에 연결하여 사용하는 초경량 터미널 코딩 에이전트 CLI입니다.

- **라이선스:** MIT
- **주요 언어:** TypeScript (npm 패키지 배포)
- **특징:** Claude Fable 5.1을 활용한 바이브 코딩 실증 사례로 제작됨

---

## 🛠️ 주요 특징
- **완전 로컬 자립형:** 클라우드 API 호출 비용이 0원이며, 민감한 코드베이스가 외부로 유출되지 않는 100% 온프레미스/로컬 개발 환경 지원.
- **최소 구현 아키텍처:** Plan-Act-Observe-Diff로 이어지는 에이전트 핵심 루프를 수백 줄의 TypeScript 코드로 간결하게 구현하여, 에이전트 구조 학습 및 커스텀 도구 확장에 최적화됨.

---

## 🔗 연관 지식
- 패러다임: [[concepts/vibe-coding|Vibe Coding]], [[concepts/agentic-workflow|Agentic Workflow]]
