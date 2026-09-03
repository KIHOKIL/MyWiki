---
title: Prompt Creator Skill
category: skills
tags:
  - prompt-engineering
  - meta-prompt
  - gems
  - custom-gpt
  - interactive-interview
  - automation
sources:
  - "[[_sources/Study/AI-Prompt/Gems Prompt Creator/gems_prompt_creator.md]]"
  - ".agents/skills/prompt-creator/SKILL.md"
  - "[[entities/career-hacker-alex]]"
  - "https://www.careerhackeralex.com/prompt-generator"
  - "https://www.careerhackeralex.com/image-prompts"
created: "2026-09-03"
updated: "2026-09-03"
summary: 6단계 정밀 아키텍처 인터뷰, 동적 스펙보드, A/B/C + Pro-Tip 추천을 통해 상용급 AI 시스템 지침을 설계하고 주제별 폴더에 마크다운 파일로 자동 저장하는 메타 프롬프트 스킬.
base_confidence: 0.95
lifecycle: reviewed
tier: core
---

# Prompt Creator Skill (범용 AI 에이전트 & 시스템 프롬프트 아키텍트)

## 📌 개요
**Prompt Creator Skill**은 Google Gemini(Gems), OpenAI(Custom GPTs / System Instructions), Anthropic Claude(Projects / Artifacts), 또는 Cursor/Antigravity(Agent Skills) 등 다양한 LLM 플랫폼에서 활용할 수 있는 맞춤형 AI 시스템 지침을 설계하는 메타 프롬프트 자동화 스킬입니다.

6단계 대화형 인터뷰를 통해 상용 서비스 수준(Production-level)의 시스템 프롬프트를 완성하고, **주제에 맞는 하위 폴더를 자동 생성하여 마크다운(`.md`) 파일로 영구 보관**합니다.

- **기반 원문:** [[_sources/Study/AI-Prompt/Gems Prompt Creator/gems_prompt_creator.md|Gems 맞춤형 프롬프트 생성기]]
- **스킬 명세:** `.agents/skills/prompt-creator/SKILL.md`
- **핵심 벤치마크:** [[entities/career-hacker-alex|커리어해커 알렉스]]의 [Prompt Generator](https://www.careerhackeralex.com/prompt-generator) 및 [Image Prompts](https://www.careerhackeralex.com/image-prompts)

---

## 🛠️ 핵심 동작 메커니즘
1. **간결한 2문장 킥오프 (Initial Kick-off):**
   - 첫 턴에서 장황한 설명 없이 *"어떤 맞춤형 AI 에이전트(Gems / GPTs / System Prompt / Skill)를 설계하고 싶으신가요?..."*로 시작.
2. **동적 스펙보드 실시간 갱신 (Dynamic Spec Board):**
   - 매 턴마다 상단에 `[- [x] 확정 / - [ ] 미확정]` 체크박스 현황판을 표시하여 진행 상황 시각화.
3. **A/B/C 선택지 + 💡 Pro-Tip (전문가 추천):**
   - 사용자가 막히지 않도록 객관식 옵션을 주면서 최선의 추천안 제시.
4. **엄격한 추측 금지 (No-Assumption):**
   - 6단계(목표/타겟플랫폼, 페르소나, CoT, 가드레일, 엣지케이스, 출력포맷)가 승인되기 전 임의 생성 금지.
5. **주제별 폴더 자동 생성 및 저장 (Auto-Filing):**
   - 승인 즉시 `_sources/Study/AI-Prompt/<Topic>/<파일명>.md`로 파일 자동 생성.
   - `_sources/Study/AI-Prompt/_index.md` 인덱스 자동 연결.

---

## 💬 호출 트리거
- `"/prompt-creator"`
- *"프롬프트 만들어줘"*
- *"AI 에이전트 설계해줘"*
- *"시스템 프롬프트 짜줘"*
- *"Gems / GPTs 만들어줘"*

---

## 📚 외부 참조 레퍼런스 및 벤치마크
- **[[entities/career-hacker-alex|커리어해커 알렉스]] [프롬프트 제너레이터](https://www.careerhackeralex.com/prompt-generator):**
  - 개발자, 기획자(PM), 마케터, 디자이너, 창업자, 리더/관리자, 연구자 등 **16대 실무 페르소나 및 목표 라이브러리**를 벤치마킹하여 2단계 인터뷰 시 맞춤형 옵션과 Pro-Tip을 제공합니다.
- **[[entities/career-hacker-alex|커리어해커 알렉스]] [이미지 프롬프트 저장소](https://www.careerhackeralex.com/image-prompts):**
  - "좋은 프롬프트는 결과물까지 보관합니다."
  - ① 결과물 맥락 명시, ② 복사 가능한 마스터 프롬프트와 미세 조정 노트 분리 원칙을 시각/이미지 프롬프트 설계에 필수 적용합니다.
