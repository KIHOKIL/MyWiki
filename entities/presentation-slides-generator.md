---
title: "Presentation Slides"
category: "entities"
tags: ["AI-Agent", "Skill", "Content-Generation", "Presentation"]
sources: ["https://github.com/jha0313/skills_repo"]
created: "2026-08-09"
updated: "2026-08-09"
summary: "스크립트나 마크다운 문서를 분석하여 브라우저에서 볼 수 있는 모던한 다크 테마 HTML 프레젠테이션 슬라이드를 자동 생성하는 스킬."
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-09"
tier: supporting
---

# Presentation Slides

## 개요
YouTube 영상 대본, 기술 문서, 블로그 포스트 등을 기반으로 구조화된 HTML 슬라이드 세트를 자동 생성해주는 에이전트 스킬입니다. 

## 주요 기능
- **콘텐츠 추출 및 구조화:** 원본 텍스트(`script.md` 등)를 분석하여 Intro, Main Concepts, Examples, Conclusion 등으로 논리를 전개합니다.
- **HTML/CSS 렌더링:** 외부 의존성(라이브러리) 없이 Vanilla HTML과 CSS만으로 깔끔한 다크 테마 기반 슬라이드 쇼를 만듭니다. 좌우 화살표 키로 네비게이션이 가능합니다.
- **Index 허브 구축:** 한 번에 여러 개의 슬라이드가 만들어질 경우, 이들을 한곳에 묶어 클릭해서 볼 수 있는 `index.html` (Presentation Hub) 파일을 구성합니다.

## 활용 시점
- "오늘 읽은 긴 논문이나 유튜브 대본을 팀원들에게 5분 만에 발표해야 할 때"
- "내용은 있는데 파워포인트/키노트 디자인 잡기가 귀찮을 때"

## 관련 문서
- [[ai-agent-skills-catalog]]
