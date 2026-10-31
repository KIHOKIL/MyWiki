---
title: "Farol (PR Blast-Radius & Contract Breakage Analyzer)"
category: entities
tags:
  - ai-code-review
  - open-source-benchmark
  - graph-rag
sources:
  - "https://github.com/winnin/farol"
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/01_OpenSource_Code_Review_Benchmark.md"
created: 2026-10-31
updated: 2026-10-31
summary: "AI 코드 리뷰 이후 단계('After your AI review')에서 PR 병합 시 바뀌지 않은 상위 호출자 중 어디가 깨지는지(Blast Radius & Contract Breakage)와 0~100 리스크 점수를 산출하는 정적 분석 도구."
---

# Farol (`winnin/farol`)

- **GitHub:** [https://github.com/winnin/farol](https://github.com/winnin/farol)
- **라이선스:** `MIT`

---

## 핵심 가치 ("After Your AI Review")
일반 AI 코드 리뷰가 **바뀐 코드 줄(Diff)**의 결함을 찾는 데 그친다면, **Farol**은 시니어 리뷰어가 가장 우려하는 **"바뀌지 않은 파일 중 어디가 이 변경 때문에 깨지는가?"**를 컴파일러 기반으로 분석합니다:
1. **Contract Breakage Detection:** 함수 시그니처, 구조체 레이아웃, 반환 규약 변경 시 기존 호출자(Callers)와의 계약 파괴 감지.
2. **Deterministic Blast Radius:** 변경된 심볼로부터 직·간접적으로 영향받는 모듈의 반경 지도화.
3. **0~100 Quantitative Risk Score:** 변경 복잡도와 파급 반경, 테스트 유무를 종합한 정량 리스크 점수 및 인터랙티브 체크리스트 생성.

---

## 🔗 연관 문서
- [[phy-embedded-code-review]]
- [[hybrid-rule-agent-review]]
- [[clang-codegraph]]

