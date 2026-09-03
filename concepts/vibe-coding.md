---
title: 바이브 코딩 (Vibe Coding)
category: concepts
tags:
  - engineering
  - workflow
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/big_tech_ai_workflow_proposal.md
created: 2026-08-17
updated: 2026-08-17
---

# 바이브 코딩 (Vibe Coding)

기존의 코드 에디터(IDE)에서 사람과 AI가 한 줄씩 타이핑하며 코드를 완성해 나가는 방식(Copilot 방식)을 넘어서, **높은 수준의 문맥(기획 문서, JIRA 티켓 내용 등)만을 에이전트에게 던져주고 전체적인 구현(Implementation)을 일임하는 방식**을 말합니다.

위키(Agentic Vault)에 축적된 도메인 컨텍스트, JIRA 이슈 목표 등을 바탕으로, *"이 기획에 맞추어 로컬 환경에서 코드를 완성해"* 와 같이 지시함으로써, AI가 요구사항을 스스로 이해하고 프로젝트 전체에 걸쳐 코드를 수정 및 생성하게 만듭니다.

## 효과
- 단순 구현(Boilerplate 작성 등)에 소모되는 시간을 줄이고 개발자는 아키텍처 설계와 최종 검토에 집중할 수 있습니다.
- 프로젝트 내 중요한 결정 사항들이 위키라는 중앙 뇌(Central Brain)에 정리되어 있으므로, 바이브 코딩 시 컨텍스트 유실로 인한 엉뚱한 결과물이 생성될 확률이 크게 줄어듭니다.

## 연관 개념 및 도구
- [[agentic-scaffolding]]
- [[active-second-brain]]
- [[entities/smolcoder|Smolcoder]] — 로컬 LLM 기반 터미널 바이브 코딩 CLI
- [[entities/headroom|Headroom]] — 에이전트 루프 컨텍스트 사전 압축 도구
