---
title: Embedded SW Definition and Characteristics
category: Concepts
tags:
  - software-engineering
  - embedded-systems
  - hardware-interface
sources:
  - Personal Knowledge
created: 2026-09-08
updated: 2026-09-08
---

# Embedded SW Definition and Characteristics

Embedded SW(임베디드 소프트웨어)란 단순한 상위 레이어(Application/OS layer)의 소프트웨어와 구분되는 고유한 특성을 가집니다.

## 핵심 개념
- **하드웨어 기반 제어**: Modem HW block 등을 register, interrupt 등을 기반으로 직접 제어합니다.
- **하드웨어 이해 필수**: HW block design을 정확히 이해하는 것이 필수적입니다.
- **변경 사항의 신속한 반영**: HW block change를 코드 설계와 제어 로직에 잘 반영하는 것으로부터 개발이 시작됩니다.

## 중요성
이러한 기본(하드웨어의 이해 및 변경 사항 반영)이 잘 지켜지지 않으면, 상위 레이어와 달리 디버깅이 어렵고 하드웨어 자원의 제약으로 인해 매우 많은 이슈(버그, 안정성 문제)와 리소스 소모가 발생하게 됩니다.
