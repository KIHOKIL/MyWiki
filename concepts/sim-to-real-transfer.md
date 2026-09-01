---
title: "Sim-to-Real Transfer"
category: Concept
tags: [robotics, ai, simulation, embodied-ai]
sources: [[[2026-08-29_News_Briefing]], [[2026-08-30_News_Briefing]], [[2026-08-31_News_Briefing]]]
summary: "가상 시뮬레이션 환경에서 학습된 AI 모델을 실제 물리 로봇 및 디바이스에 적용할 때 발생하는 간극(Gap)을 최소화하는 기술."
base_confidence: 0.8
lifecycle: draft
tier: supporting
created: 2026-09-01
updated: 2026-09-01
---

가상 환경(NVIDIA Omniverse/Isaac Sim 등)에서 대규모 병렬 시뮬레이션을 통해 학습된 AI 정책(Policy)과 제어 모델을 실제 물리적 로봇 하드웨어에 배포할 때 발생하는 현실 세계와의 오차(Sim-to-Real Gap)를 최소화하는 기술입니다.

## 핵심 기법 및 필요성
- **도메인 무작위화 (Domain Randomization):** 마찰력, 질량, 센서 노이즈 등 물리 파라미터를 무작위로 변경하며 강건한 모델 학습.
- **학습 비용 및 안전성 극대화:** 실제 하드웨어의 파손 위험 없이 클라우드 인프라(AWS Batch 등)를 통해 수천만 시간 상당의 주행/조작 데이터를 사전 학습.
- **관련 기술 및 개체:** [[physical-ai]], [[isaac-groot]], [[optimus]].
