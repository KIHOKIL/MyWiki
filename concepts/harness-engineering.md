---
title: Harness Engineering
category: concepts
tags: [concept, prompt-engineering, llm, system-design]
sources: ["_source/Study/AI-Lectures/커리어해커알렉스/20260816_진짜AX/20260816_진짜AX_학습메모.md", "https://www.careerhackeralex.com/blog/ax-faq"]
created: "2026-08-16"
updated: "2026-08-16"
summary: AI 결과물에서 'AI 느낌'을 지우고 조직의 요구사항에 맞추기 위해 Rules, Skills, Context, Hooks 등을 시스템화하여 축적하는 과정입니다.
---

# Harness Engineering

**Harness Engineering(하네스 엔지니어링)**은 거친 언어모델(LLM)을 통제하고 다듬어 특정 비즈니스나 조직의 표준에 맞는 고품질 결과물을 꾸준히 생산하게 만드는 프롬프트 엔지니어링의 확장판입니다.

## 개념과 필요성
- AI 결과물에서 흔히 느껴지는 특유의 톤(AI 느낌)을 지우거나, 코딩 에이전트가 반복적으로 범하는 실수를 방지하기 위해 사용됩니다.
- 모델에게 단순히 지시를 내리는 것을 넘어, 정확한 맥락(Context), 룰(Rules), 스킬(Skills)을 시스템 레벨에서 부여하는 작업입니다.

## 작동 방식 (축적의 시스템)
결과물이 틀어졌을 때 단순히 한 번 수정하고 마는 것이 아니라, **"이렇게 하지 말 것을 기억해"**라는 피드백을 시스템(Memory)에 영구적으로 저장하고 다음 생성 과정에 반영하는 루프를 만듭니다. 이 피드백의 축적이 바로 하네스(Harness)가 됩니다.
- **지속적인 유지보수:** 새로운 LLM 모델이 나오면 기존 하네스와 충돌할 수 있습니다. 하네스는 한 번 만들고 끝나는 것이 아니라, 모델의 진화와 함께 계속 깎아 나가는 "살아있는 시스템"입니다.
- **전사적 표준화:** 부서별로 중구난방인 하네스를 쓰면 퀄리티가 낮아집니다. 회사 차원의 공용 하네스 인프라와 플러그인을 구축하는 것이 [[ax]]의 핵심 과제 중 하나입니다.
