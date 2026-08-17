---
title: "AI 에이전트 스킬 & 도구 카탈로그"
category: "references"
tags: ["AI", "Agent", "Skills", "Tools", "Catalog"]
created: "2026-08-09"
updated: "2026-08-09"
---

# AI 에이전트 스킬 & 도구 카탈로그

이 문서는 코딩 에이전트 및 LLM 활용 시 생산성과 품질을 높여주는 유용한 스킬(.md 가이드라인)과 프레임워크들을 모아둔 참고용(Reference) 카탈로그입니다.

## 🛠️ 코딩 & 퀄리티 향상 스킬

| 이름                      | 설명                                                                 | 링크                                                             |
| ----------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- |
| **Karpathy Guidelines** | AI 코딩 시 반복적인 실수를 방지하기 위한 안드레이 카파시의 가이드라인                           | [GitHub](https://github.com/multica-ai/andrej-karpathy-skills) |
| **Superpowers**         | 시니어 개발자의 프로세스를 강제하여 생성되는 코드의 퀄리티를 대폭 높이는 스킬                        | [GitHub](https://github.com/obra/superpowers)                  |
| **Understand-Anything** | 복잡한 코드 베이스를 스캔하고 지식 그래프로 시각화하여 이해도를 돕는 스킬                          | [GitHub](https://github.com/Lum1104/Understand-Anything)       |
| **Ponytail**            | 불필요한 라이브러리 설치나 복잡한 코드 생성을 방지하고, 최소한의 구현으로 효율성을 극대화                 | [GitHub](https://github.com/DietrichGebert/ponytail)           |
| **Taste Skill**         | AI의 디자인 언어를 다듬고 레이아웃/애니메이션 수준을 조절하여 UI 품질을 높이는 안티 슬롭(Anti-slop) 도구 | [GitHub](https://github.com/Leonxlnx/taste-skill)              |

## 🧠 에이전트 워크플로우 & 메모리

| 이름                     | 설명                                                          | 링크                                                 |
| ---------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| **agentmemory**        | 작업 세션 간의 문맥을 기억하고 필요한 정보를 장기적으로 관리하는 스킬                     | [GitHub](https://github.com/rohitg00/agentmemory)  |
| **Matt Pocock Skills** | 'GrillMe' 등 개발자의 작업을 체계화하고 명확한 요구사항을 정의할 수 있게 돕는 실용적인 스킬 모음 | [GitHub](https://github.com/mattpocock/skills)     |
| **Caveman**            | 클로드의 답변을 간결하게 만들어 토큰 사용량을 줄이고 텍스트 읽기 속도를 높임                 | [GitHub](https://github.com/JuliusBrussee/caveman) |
| **ECC**                | 앤트로픽 해커톤 우승자의 세팅을 담은 방대한 도구. 작업 환경 구축 시 참고용 카탈로그로 유용        | [GitHub](https://github.com/affaan-m/ECC)          |

## 📹 미디어 & 트렌드 분석

| 이름               | 설명                                                           | 링크                                                                                        |
| ---------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **claude-video** | 유튜브 영상을 분석하여 내용을 파악하는 스킬                                     | [GitHub](https://github.com/bradautomates/claude-video)                                   |
| **Remotion**     | React를 사용하여 프로그래밍 방식으로 영상을 제작하는 프레임워크. 코딩 에이전트와 연동하여 자동화에 유용 | [Website](https://www.remotion.dev/) / [GitHub](https://github.com/remotion-dev/remotion) |
| **last30days**   | 최근 30일간의 커뮤니티(레딧, X 등) 반응을 검색해 트렌드 브리핑을 제공하는 스킬              | [GitHub](https://github.com/mvanhorn/last30days-skill)                                    |

## 📊 분석 및 리포팅 도구

| 이름 | 설명 | 링크 |
|---|---|---|
| **[[ai-readiness-cartography|AI-Readiness Cartography]]** | 코드베이스가 AI 에이전트에 얼마나 친화적인지 분석해 대시보드로 만들어 주는 스킬 | [GitHub](https://github.com/jha0313/skills_repo/tree/main/ai-readiness-cartography) |
| **[[improve-token-efficiency|Improve Token Efficiency]]** | Claude의 JSONL 로그를 파싱해서 토큰 재사용률(캐싱)을 분석하고 절감안을 알려주는 스킬 | [GitHub](https://github.com/jha0313/skills_repo/tree/main/improve-token-efficiency) |

## 📄 콘텐츠 생성

| 이름 | 설명 | 링크 |
|---|---|---|
| **[[presentation-slides-generator|Presentation Slides]]** | 마크다운 대본을 바탕으로 브라우저에서 열리는 인터랙티브 HTML 슬라이드를 생성해 주는 스킬 | [GitHub](https://github.com/jha0313/skills_repo/tree/main/presentation_slides) |

---
*💡 나중에 특정 도구(예: Superpowers, Remotion)를 깊게 파고들게 된다면 `entities/superpowers.md` 처럼 개별 문서로 분리한 후 여기에 위키링크를 걸어주세요.*
