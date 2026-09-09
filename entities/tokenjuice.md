---
title: TokenJuice
category: entities
tags:
  - tokenjuice
  - data-preprocessing
  - openhuman
  - nlp
  - text-cleaning
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260905/OpenHuman_심층분석_및_사내_Group_2nd_Brain_연계.md]]"
created: "2026-09-06"
updated: "2026-09-06"
summary: "HTML 태그, 이메일 인용문, 메일 서명, 봇 자동 알림 등 불필요한 보일러플레이트를 제거하고 순수 비즈니스 텍스트만 추출하여 토큰을 70~80% 절감하는 텍스트 정제 파이프라인/필터."
---

# TokenJuice

## 📌 개요
**TokenJuice**는 [[entities/openhuman|OpenHuman]] 생태계에서 사용되는 스마트 토큰 압축 레이어(텍스트 정제 파이프라인)입니다.
원시 비정형 데이터(사내 이메일, Jira 티켓, Confluence 등)에 포함된 방대한 노이즈를 제거하여, 대형 언어 모델(LLM)에 전달되는 컨텍스트를 극도로 최적화하는 역할을 수행합니다.

## ⚙️ 주요 기능 및 메커니즘
- **보일러플레이트 제거:** 이메일의 무의미한 인용문 히스토리(`On 2026-xx-xx wrote...`), 회사 면책 고지(Disclaimer), HTML 서명 이미지 태그 등을 필터링합니다.
- **포맷 변환:** 복잡한 HTML DOM 트리를 순수한 Markdown 포맷으로 변환하여 가독성과 토큰 밀도를 높입니다.
- **토큰 청킹(Chunking):** 정제된 텍스트를 LLM의 처리 효율에 맞게 적절한 크기(예: 3k 토큰 이하) 단위의 마크다운으로 쪼개는 역할을 합니다.

## 💡 능동형 세컨드 브레인(Active Second Brain) 적용점
- 사내의 방대하고 지저분한 레거시 데이터를 [[concepts/memory-tree|Memory Tree]] 형태로 수집하기 전에 TokenJuice를 사내 전용으로 커스터마이징하여 적용하면, LLM 비용 절감과 응답 지연 시간 단축을 동시에 이룰 수 있습니다.
- 이는 그래프 쿼리를 통해 최종 어텐션을 집중시키는 [[entities/headroom|Headroom]]과 상호 보완적으로 작동합니다 (수집 전처리는 TokenJuice, 최종 검색 전처리는 Headroom).
