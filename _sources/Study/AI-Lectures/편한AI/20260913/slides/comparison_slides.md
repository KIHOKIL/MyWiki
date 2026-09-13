---
marp: true
theme: default
class: lead
backgroundColor: #0f172a
color: #f8fafc
style: |
  h1 { color: #60a5fa; }
  h2 { color: #c084fc; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 0.5em; }
  li { line-height: 1.8; font-size: 1.2rem; }
  strong { color: #3b82f6; }
---

# 🧠 Obsidian LLM Wiki 3종 비교
**어떤 세컨드 브레인 아키텍처를 선택할 것인가?**

---

## 1. 비교 개요 (The Contenders)

안드레이 카파시의 '자가 조직(Self-organizing) 위키' 개념을 계승한 세 가지 도구:

1. **Local Guide (기본형):** Antigravity IDE와 파이썬 스크립트를 활용한 투명한 제어.
2. **OpenHuman:** 옵시디언을 거대 에이전트의 메모리 트리(Memory Tree)로 활용.
3. **Claude-Obsidian:** 원자적 트랜잭션(Atomic)과 출처 린팅(Linting)에 집중한 보수적 관리.

---

## 2. OpenHuman의 특징 (자동화와 확장성)

* **거대 에이전트 플랫폼:** 단순 노트 정리를 넘어 이메일, 슬랙 등을 스스로 확인.
* **Auto-fetch 기능:** 100여 개의 외부 서비스에서 데이터를 끊임없이 수집.
* **TokenJuice 압축:** 방대한 컨텍스트를 다루기 위해 토큰을 극단적으로 압축하여 효율성 극대화.

---

## 3. Claude-Obsidian의 특징 (안전성과 무결성)

* **트랜잭션 롤백:** 지식 갱신 중 에러가 발생하면 이전 상태로 완벽히 되돌림.
* **출처 엄격 보존:** 원본 데이터는 절대 지우지 않으며(Survive the summary), 파생된 클레임은 출처를 교차 검증.
* **승인 기반 실행:** 에이전트가 단독으로 덮어쓰지 못하고, 항상 사용자의 승인된 계획(Plan)만 적용.

---

## 4. Next Action: 하이브리드 도입 제언

사내 레거시 코드 리팩토링 및 민감 데이터를 다루는 우리 그룹을 위한 전략:

- **안전성 채택:** Claude-Obsidian의 트랜잭션 모델을 차용하여 기밀 문서 훼손 원천 차단.
- **수집망 채택:** OpenHuman의 Auto-fetch 로직을 가져와 Jira/Confluence 자동 동기화.
- **샌드박스(Sandbox):** 민감 데이터는 외부 퍼블릭 LLM에 노출되지 않도록 망분리 환경(Local LLM)에서 병행 처리.
