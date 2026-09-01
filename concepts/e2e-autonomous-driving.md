---
title: "End-to-End (E2E) Autonomous Driving"
category: Concept
tags: [autonomous-driving, ai, sdv, physical-ai]
sources: [[[2026-08-29_News_Briefing]], [[2026-08-30_News_Briefing]], [[2026-08-31_News_Briefing]]]
summary: "센서 데이터 입력부터 차량의 조향·가감속 제어 출력까지 분절된 모듈 없이 단일 신경망으로 학습 및 구동하는 자율주행 방식."
base_confidence: 0.8
lifecycle: draft
tier: supporting
created: 2026-09-01
updated: 2026-09-01
---

인식(Perception), 판단(Planning), 제어(Control)가 분리되어 있던 기존의 규칙 기반(Rule-based) 모듈형 자율주행 아키텍처와 달리, 센서 데이터(카메라, 레이더 등) 입력부터 차량의 주행 제어 출력까지 하나의 통합 신경망으로 직접 처리하는 차세대 자율주행 기술입니다.

## 주요 특징
- **도심 복잡 환경 대응력 향상:** 수작업 룰북의 한계를 극복하고 인간 운전자의 방대한 데이터로부터 자연스러운 주행 습관 학습.
- **SDV 아키텍처와의 융합:** 고성능 중앙 집중형 SoC 및 클라우드 데이터 파이프라인(NVIDIA, AWS) 기반으로 무선 업데이트(OTA) 지원.
- **관련 개념 및 이슈:** [[vla-model]], [[physical-ai]], 자율주행 사고 시 법적 책임 프레임워크.
