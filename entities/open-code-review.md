---
title: "Alibaba Open-Code-Review (알리바바 오픈 코드 리뷰)"
category: entities
tags:
  - ai-code-review
  - open-source-benchmark
  - agentic-workflow
sources:
  - "https://github.com/alibaba/open-code-review"
  - "_sources/Study/Code-Review/PHY-Embedded-SW/20261031_Deep_Research/01_OpenSource_Code_Review_Benchmark.md"
created: 2026-10-31
updated: 2026-10-31
summary: "알리바바 그룹 내부에서 2년 이상 표준으로 검증된 결정론적 엔지니어링 × LLM 에이전트 하이브리드 코드 리뷰 프레임워크 (GitHub Stars 49.1k+, Go, Apache-2.0)."
---

# Alibaba Open-Code-Review (`alibaba/open-code-review`)

- **GitHub:** [https://github.com/alibaba/open-code-review](https://github.com/alibaba/open-code-review)
- **검증 지표:** ⭐ **49,163 Stars** | 🍴 **3,600 Forks** | 언어: `Go` | 라이선스: `Apache-2.0`
- **학술 벤치마크:** AACR-Bench (`arXiv:2603.11079`) 공개 및 F1/Precision 1위 기록.

---

## 핵심 아키텍처 특징
순수 에이전트 방식 대비 **약 1/9의 토큰만 소모**하면서 더 높은 정밀도를 달성하기 위해 4가지 결정론적 모듈과 에이전트를 결합합니다:
1. **Precise File Selection:** 리뷰 불필요 파일(자동 생성 코드, 빌드 산출물) 사전 배제.
2. **Smart File Bundling:** 연관된 헤더(`.h`)와 구현체(`.c`), 호출자/피호출자를 응집도 높은 번들로 묶어 컨텍스트로 전달.
3. **Fine-Grained Rule Matching:** 파일 경로·패턴에 매칭되는 팀 규칙만 선별 주입.
4. **Reflection & Positioning Module:** 에이전트 초안에서 근거가 부족한 오탐을 스스로 기각(Reflection)하고 정확한 Diff 라인에 매핑.

---

## 🔗 연관 문서
- [[hybrid-rule-agent-review]]
- [[phy-embedded-code-review]]
- [[phy-sw-ai-code-review-strategy]]

