---
title: 이슈옵스 (IssueOps) 연동
category: concepts
tags:
  - workflow
  - automation
sources:
  - _sources/Study/AI-Lectures/편한AI/20260817/big_tech_ai_workflow_proposal.md
created: 2026-08-17
updated: 2026-08-17
---

# 이슈옵스 (IssueOps) 연동

AI 에이전트가 단독으로 코드를 검토하거나 이슈를 발견하는 데 그치지 않고, 그 결과를 **티켓팅 시스템(JIRA 등)이나 프로젝트 관리 도구(Github Issues 등)에 자동으로 연동(IssueOps)하여 후속 조치까지 파이프라인화하는 프로세스**입니다.

## 적용 사례
- 에이전트가 코드 내 잠재적 버그를 탐지하면, 해당 위치와 원인 추론 결과를 담은 **JIRA 이슈를 자동으로 생성**하고 적절한 담당자를 할당(Assign)합니다.
- PR 리뷰 시 오류가 발견되면 **Github Issue 코멘트로 결과를 자동 등록**합니다.

구글이나 애플 같은 기업에서 사내 데이터 유출을 방지하기 위해 로컬/프라이빗 클라우드에 고립된 LLM을 연결하여 활용하는 대표적인 파이프라인 중 하나입니다.

## 연관 개념 및 프로젝트
- [[agentic-scaffolding]]
- [[multi-agent-code-review]]
- [[projects/NewsSummarizer]] — GitHub IssueOps 기반 원격 제어 뉴스 요약 프로젝트
