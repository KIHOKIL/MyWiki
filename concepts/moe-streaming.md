---
title: MoE Streaming (MoE 가중치 온디맨드 스트리밍)
category: concepts
tags:
  - moe
  - model-streaming
  - apple-silicon
  - mlx
  - local-llm
  - memory-optimization
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/20260903_학습노트.md]]"
created: "2026-09-03"
updated: "2026-09-03"
summary: MoE(Mixture of Experts) 모델에서 토큰 생성 시 필요한 활성 전문가 가중치만 고속 SSD에서 메모리로 실시간 파이프라이닝하여 물리 RAM 용량 이상의 초대형 모델을 구동하는 기법.
base_confidence: 0.9
lifecycle: reviewed
tier: core
relationships:
  - target: "[[entities/slotstream]]"
    type: implemented_by
---

# MoE Streaming (MoE 가중치 온디맨드 스트리밍)

## 📌 개념 개요
**MoE Streaming(혼합 전문가 가중치 스트리밍)**은 대규모 MoE(Mixture of Experts) 모델을 구동할 때, 전체 가중치를 VRAM이나 시스템 RAM에 상주시키지 않고 **고속 NVMe SSD에서 활성화된 전문가(Active Experts) 계층만 토큰 단위로 실시간 스트리밍(로드)**하여 추론하는 메모리 최적화 기법입니다.

이 기법을 통해 물리적 RAM이 48GB인 일반 소비자용 기기(예: Apple Silicon Mac)에서도 100GB가 넘는 대형 MoE 모델(예: Qwen 125B MoE)을 성공적으로 실행할 수 있습니다.

---

## ⚙️ 동작 메커니즘
1. **상주 계층과 비상주 계층 분리:**
   - 어텐션 계층(Attention Layers)과 라우터(Router) 가중치 등 공통 필수 연산 부분은 RAM에 상주시킵니다.
   - MoE의 수십~수백 개 전문가(Expert FFN) 가중치는 빠른 NVMe SSD에 압축된 형태로 저장합니다.
2. **MoE 라우팅 및 사전 패치(Prefetch):**
   - 라우터가 입력 토큰에 대해 Top-K(예: 8개 전문가 중 2개) 전문가를 선별하는 즉시, 비동기 I/O 파이프라인을 통해 해당 Expert 가중치 블록만 SSD에서 RAM으로 즉시 스트리밍합니다.
3. **토큰 추론 및 교체:**
   - 연산이 끝난 전문가 블록은 버퍼에서 해제하거나 LRU 캐시로 관리하여 메모리 점유율을 제한적으로 유지합니다.

---

## ⚖️ 장점 및 트레이드오프

| 항목 | 일반 메모리 적재 | MoE 스트리밍 방식 |
| :--- | :--- | :--- |
| **요구 메모리** | 모델 크기 전체 (100GB+ VRAM 필수) | **공통 계층 + 활성 전문가 분량만 필요 (32~48GB RAM 가능)** |
| **하드웨어 비용** | 고가의 엔터프라이즈 GPU 클러스터 필요 | 일반 애플 실리콘 맥 또는 고속 NVMe 환경에서 구동 가능 |
| **추론 속도** | 최고 속도 (메모리 대역폭 제한) | SSD 읽기 속도에 따른 오버헤드로 인해 초당 토큰 생성 속도는 일부 감소 |

---

## 🔗 연관 지식
- 구현체: [[entities/slotstream|Slotstream]]
- 하드웨어 프레임워크: Apple Silicon, MLX, NVMe PCIe 4.0/5.0
