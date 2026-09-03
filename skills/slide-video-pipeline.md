---
title: Slide Video Pipeline Skill
category: skills
tags:
  - workflow
  - presentation
  - video-production
  - bananalm
  - google-vids
  - style-presets
sources:
  - ".agents/skills/slide-video-pipeline/SKILL.md"
  - "[[concepts/slide-video-workflow]]"
  - "[[entities/notebooklm]]"
  - "[[entities/google-vids]]"
created: "2026-09-04"
updated: "2026-09-04"
summary: 연구 보고서와 위키 문서를 기반으로 스토리라인 구축, 7대 BananaLM 스타일 프레젠테이션 비주얼 생성, 발표자 메모(Google Vids TTS 대본) 탑재 슬라이드 덱을 원스톱 제작하는 스킬.
base_confidence: 0.95
lifecycle: active
tier: core
---

# Slide & Video Production Pipeline Skill (슬라이드 & AI 영상 제작 스킬)

## 📌 개요
**Slide Video Pipeline Skill**은 학습 노트, 연구 보고서, 위키 문서로부터 **"완성형 텍스트 스토리라인 구축 ➡️ 슬라이드별 분할 & 내레이션 대본 ➡️ BananaLM 맞춤 비주얼 프롬프트 ➡️ 발표자 메모(Speaker Notes) 연동"**까지 원스톱으로 처리하는 프레젠테이션 및 영상 제작 자동화 스킬입니다.

- **스킬 명세:** `.agents/skills/slide-video-pipeline/SKILL.md`
- **핵심 아키텍처:** [[concepts/slide-video-workflow]]
- **도구 연계:** [[entities/notebooklm]], [[entities/google-vids]]

---

## 🎨 7대 BananaLM 스타일 프리셋 지원
1. **Memphis Flat Corporate:** 모던 플랫 벡터 + 기하학적 멤피스 패턴 (IT 테크/사내 교육)
2. **Cyberpunk Neon Dark:** 딥 다크(#0A0E17) + 네온 시안/마젠타 (AI 아키텍처/해커톤)
3. **Swiss Minimal & Bauhaus:** 엄격한 그리드 + 흑백/레드 볼드 타이포그래피 (임원 보고/학술 지표)
4. **Warm Editorial & Notion:** 따뜻한 크림 배경 + 세리프 + 펜 드로잉 (리서치 에세이/도서 리뷰)
5. **Glassmorphism Fintech:** 반투명 글래스 카드 + 그라디언트 (금융/IR/대시보드)
6. **Neo-Brutalism Bold:** 굵은 블랙 스트로크 + 팝 컬러 + 하드 섀도우 (숏폼/MZ/혁신 피칭)
7. **Executive Navy & Gold:** 딥 네이비 + 샴페인 골드 (정통 B2B 제안서/전략 보고)

---

## 🛠️ 핵심 제작 워크플로우
- **Step 1:** 입력 소스 분석 및 타깃 청중/핵심 메시지 도출
- **Step 2:** 슬라이드 매수 및 7대 비주얼 스타일 선택
- **Step 3:** 슬라이드별 핵심 내용(최대 5블록) 및 구어체 발표자 대본(Speaker Notes) 작성
- **Step 4:** BananaLM 맞춤형 이미지/슬라이드 생성 프롬프트 출력
- **Step 5:** Google Vids 및 PowerPoint(PPTX) 연동 산출물 생성

---

## 💬 호출 트리거
- `"/slide-video"`
- *"슬라이드 만들어줘"*
- *"발표 자료 만들어줘"*
- *"슬라이드 영상 워크플로우 돌려줘"*
- *"PPT 제작해줘"*
