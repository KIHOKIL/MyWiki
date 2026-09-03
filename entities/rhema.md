---
title: Rhema
category: entities
tags:
  - rhema
  - speech-to-text
  - tauri
  - ndi
  - church-it
  - open-source
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/20260903_학습노트.md]]"
  - "https://github.com/openbezal/rhema"
created: "2026-09-03"
updated: "2026-09-03"
summary: 설교 음성을 실시간 분석하여 언급되는 성경 구절을 자동 검출하고 NDI 방송 표준을 통해 OBS나 비디오 스위처로 실시간 자막 송출하는 Tauri 기반 오픈소스 데스크톱 앱.
base_confidence: 0.9
lifecycle: reviewed
tier: core
---

# Rhema

## 📌 개요
**Rhema**는 오픈소스 개발팀 openbezal이 개발한 실시간 성경 자막 감지 및 방송 송출 데스크톱 애플리케이션([github.com/openbezal/rhema](https://github.com/openbezal/rhema))입니다. 설교자의 음성을 온디바이스 AI로 실시간 인식(STT)하여 인용된 성경 구절을 찾아내고, 방송 장비에 NDI 비디오 스트림 형태로 자막을 자동 송출합니다.

- **라이선스:** MIT
- **주요 기술:** Tauri, TypeScript, Whisper STT, NDI(Network Device Interface)
- **Star 수:** 340+

---

## 🛠️ 주요 아키텍처 및 기능
1. **실시간 음성-성경 파싱 파이프라인:**
   - 마이크 음성 입력 ➡️ 온디바이스 STT 엔진 ➡️ 성경 엔티티 추출기(예: "요한복음 3장 16절") ➡️ 내부 성경 데이터베이스 매칭.
2. **NDI 방송 표준 송출:**
   - 텍스트 오버레이가 투명 알파 채널을 포함한 방송 표준 NDI 비디오 신호로 출력되어, OBS Studio나 vMix, 하드웨어 스위처에 드롭인으로 즉시 연결 가능.
3. **미디어팀 봉사자 수작업 자동화:**
   - 설교 중 갑작스럽게 인용되는 성경 구절을 검색하여 자막으로 띄우는 복잡한 수동 작업을 완전 자동화.
