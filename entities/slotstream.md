---
title: Slotstream
category: entities
tags:
  - slotstream
  - open-source
  - swift
  - mlx
  - apple-silicon
  - moe
  - local-llm
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/20260903_학습노트.md]]"
  - "https://github.com/carloslfu/slotstream"
created: "2026-09-03"
updated: "2026-09-03"
summary: 104GB MoE 모델(Qwen 125B MoE)을 빠른 NVMe SSD에서 활성 전문가만 온디맨드 스트리밍하여 48GB Mac에서 구동할 수 있게 해주는 Swift/MLX 오픈소스 프로젝트.
base_confidence: 0.9
lifecycle: reviewed
tier: core
relationships:
  - target: "[[concepts/moe-streaming]]"
    type: implements
---

# Slotstream

## 📌 개요
**Slotstream**은 개발자 carloslfu가 개발한 오픈소스 도구([github.com/carloslfu/slotstream](https://github.com/carloslfu/slotstream))로, 4비트 양자화 기준 약 104GB에 달하는 초대형 MoE 모델(예: Qwen3.8-Flash-Next 125B MoE)을 48GB 통합 메모리를 갖춘 애플 실리콘 맥에서 안정적으로 구동할 수 있도록 설계된 소프트웨어입니다.

- **라이선스:** MIT
- **주요 기술 스택:** Swift, Apple MLX, NVMe Streaming
- **호환성:** Ollama 호환 로컬 API 엔드포인트 제공

---

## 🛠️ 핵심 원리
- **Expert-on-Demand Streaming:** 토큰 생성 시 라우터에 의해 선택된 소수(Top-K)의 전문가(Expert FFN) 가중치만 고속 SSD에서 실시간으로 읽어와 메모리에 올린 후 계산하고 해제합니다.
- **Unified Memory 대역폭 극대화:** Mac의 통합 메모리와 고속 PCIe NVMe SSD 간의 파이프라이닝을 통해 하드웨어의 VRAM 한계를 우회합니다.

---

## 🔗 연관 지식
- 개념: [[concepts/moe-streaming|MoE Streaming]]
