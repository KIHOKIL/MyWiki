---
title: Human-on-the-loop
category: concepts
tags: [concept, ai-agent, architecture, workflow]
sources: ["_source/Study/AI-Lectures/커리어해커알렉스/20260816_진짜AX/20260816_진짜AX_학습메모.md", "https://www.careerhackeralex.com/blog/ax-faq"]
created: "2026-08-16"
updated: "2026-08-16"
summary: 인간이 모든 프로세스에 개입하는 Human-in-the-loop를 넘어, 에이전트가 주도적으로 결정을 내리고 운영하되 인간은 결정적인 순간에만 개입하는 진화된 AI-인간 협업 시스템.
---

# Human-on-the-loop

**Human-on-the-loop**는 진정한 [[ax]]의 종착점입니다. AI를 잘 쓰는 조직을 넘어, **대부분의 운영과 의사결정을 에이전트(Agent)가 주도**하고, 인간은 반드시 필요한 상황(예: 최종 결재, 예외 상황 처리)에만 개입하는 시스템을 의미합니다.

## 핵심 요소

- **주도권의 이동:** 95%의 일상적인 결정은 에이전트가 내립니다. 인간의 역할은 나머지 5%의 치명적인 의사결정이나 방향 설정에 집중됩니다.
- **자체적인 피드백 루프:** 한 번 만들어 놓은 자동화(유지보수)가 아닙니다. Failure Case가 발생했을 때(예: "여기 리포트 숫자가 이상한데?"), 에이전트가 스스로 이를 인지하고 픽업하여 원인을 분석하고 시스템을 개선한 뒤 사람에게 승인을 요청하는 구조까지 설계되어야 합니다.
- **평가 체계 (Evaluation):** 프로덕션에 올라간 에이전트를 평가하기 위해 Online / Offline Eval, UXR(정성평가) 체계가 필수적입니다. 이 평가 체계를 바탕으로 에이전트는 진화합니다.
