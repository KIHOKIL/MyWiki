---
title: Multi-Tier Knowledge Architecture (다층 지식 아키텍처)
category: concepts
tags:
  - pkm
  - knowledge-architecture
  - multi-tier
  - privacy
  - enterprise-km
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260901/Research_report_LLM_2nd_Brain_Seoul (1).md]]"
created: "2026-09-01"
updated: "2026-09-01"
summary: 개인 지식(Personal), 팀 지식(Team), 전사 지식(Enterprise)을 분리하고, PII 마스킹 및 휴먼 승인 파이프라인을 통해 지식을 상위 레이어로 안전하게 승격시키는 3계층 아키텍처.
base_confidence: 0.95
lifecycle: reviewed
tier: core
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
relationships:
  - target: "[[concepts/active-second-brain]]"
    type: implements
  - target: "[[concepts/human-on-the-loop]]"
    type: relates_to
---

# Multi-Tier Knowledge Architecture (다층 지식 아키텍처)

## 📌 개념 개요
지식이 무분별하게 혼재되어 프라이버시 침해나 스파게티식 엉킴이 발생하는 것을 방지하기 위해, 데이터의 성격과 접근 권한에 따라 **개인(Personal) ↔ 팀(Team) ↔ 전사(Enterprise)**의 3단계 계층으로 분리하여 관리하고 정제된 지식만을 상위 단계로 승격(Promotion)시키는 아키텍처입니다.

---

## 🏛️ 3단계 계층 구조

```
┌────────────────────────────────────────────────────────┐
│  1. 전사 지식 레이어 (Enterprise Tier)                  │
│     - 전사 공지, 표준 가이드라인, 마스터 아키텍처 규격        │
└────────────────────────────────────────────────────────┘
                           ▲ (정제 및 관리자 승인 파이프라인)
┌────────────────────────────────────────────────────────┐
│  2. 팀/그룹 지식 레이어 (Team Tier)                     │
│     - Jira 스프린트, 공유 PRD, 팀 Confluence, 회의록     │
└────────────────────────────────────────────────────────┘
                           ▲ (민감 정보 마스킹 및 에이전트 요약)
┌────────────────────────────────────────────────────────┐
│  3. 개인 지식 레이어 (Personal Tier)                    │
│     - 개인 일기, 러프한 브레인덤프, 로컬 임시 메모           │
└────────────────────────────────────────────────────────┘
```

---

## 🔒 지식 승격 및 보안 프로토콜
1. **Personal Tier:** 완전 로컬 영역. 개인의 자유로운 사고 확장 및 브레인스토밍 지원.
2. **Personal → Team 승격:** 개인 일지나 트러블슈팅 메모 중 가치 있는 내용을 AI 에이전트가 감지하여 제안. **PII 마스킹(민감 개인정보 제거)**을 거친 후 사용자의 승인을 얻어 팀 위키로 배포.
3. **Team → Enterprise 승격:** 팀 단위에서 검증된 모범 사례(Best Practice)를 정형화하여 전사 레벨 지식 저장소로 등재.

---

## 🔗 연관 개념
- [[concepts/active-second-brain|Active Second Brain]]
- [[concepts/human-on-the-loop|Human-on-the-loop]]
- [[concepts/memgpt|MemGPT]]
