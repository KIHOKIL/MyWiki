---
title: MemGPT (Memory-GPT / 가상 컨텍스트 관리)
category: concepts
tags:
  - memgpt
  - letta
  - virtual-memory
  - memory-paging
  - second-brain
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260901/Research_report_LLM_2nd_Brain_Seoul (1).md]]"
created: "2026-09-01"
updated: "2026-09-01"
summary: 컴퓨터 운영체제(OS)의 가상 메모리 계층 구조를 차용하여 LLM이 자체 함수 호출로 Core Memory와 Archival Memory를 자율 페이징하는 무제한 컨텍스트 아키텍처.
base_confidence: 0.95
lifecycle: reviewed
tier: core
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0.0
relationships:
  - target: "[[concepts/active-second-brain]]"
    type: implements
  - target: "[[concepts/multi-tier-knowledge-architecture]]"
    type: related_to
---

# MemGPT (Memory-GPT / 가상 컨텍스트 관리)

## 📌 개념 개요
**MemGPT (현재 Letta로 발전)**는 컴퓨터 운영체제(OS)의 **가상 메모리 페이징(Virtual Memory Paging)** 메커니즘을 LLM에 적용한 아키텍처입니다. LLM의 유한한 컨텍스트 윈도를 **'Main Context (RAM)'**로 취급하고, 외부 벡터 DB 및 대규모 아카이브를 **'External Context (Disk)'**로 분리하여 LLM 스스로 메모리를 동적 페이징(Paging In/Out)하며 장기 기억을 유지합니다.

---

## 🧠 메모리 계층 구조

```
┌────────────────────────────────────────────────────────┐
│  Main Context (RAM / LLM Context Window)               │
│  - System Instructions & Persona                       │
│  - Core Memory (사용자 프로필, 당면 태스크, 작업 지침)       │
│  - FIFO Conversation Buffer                            │
└────────────────────────────────────────────────────────┘
                           ▲
             Function Calling (Read/Write/Edit)
                           ▼
┌────────────────────────────────────────────────────────┐
│  External Context (Disk / Persistent Storage)          │
│  - Recall Memory (과거 대화 전체 로그)                     │
│  - Archival Memory (외부 문서, 기술 보고서, RAG 데이터)     │
└────────────────────────────────────────────────────────┘
```

---

## 💡 핵심 동작 특징
1. **자율적 메모리 조작:** LLM이 스스로 `core_memory_append`, `core_memory_replace`, `archival_memory_insert` 등의 함수를 호출하여 필요한 사실을 기억하고 불필요해진 세부사항은 외부 디스크로 보관.
2. **영구 세션 (Perpetual Chat):** 세션이 수개월 이상 지속되어도 사용자의 핵심 선호도와 페르소나가 휘발되지 않고 점진적으로 진화.
3. **무제한 컨텍스트 환상 제공:** 컨텍스트 길이 제한에 구애받지 않고 무한한 문서와 히스토리를 필요 시점에 메모리로 끌어올려 활용.

---

## 🔗 연관 개념
- [[concepts/active-second-brain|Active Second Brain]]
- [[concepts/multi-tier-knowledge-architecture|Multi-tier Knowledge Architecture]]
- [[concepts/graph-rag|Graph RAG]]
