물론입니다. Claude에 그대로 붙여 넣으면 **현재까지의 논의 맥락과 다음 작업 방향을 이어갈 수 있도록** handoff 문서를 작성했습니다.

# Handoff Document — PHY SW AI-driven HW Change E2E Engineering

## 0. 목적

나는 Mobile Modem의 **PHY SW Group Leader**이다.

현재 신규 chipset bring-up 및 commercialization 과정에서 발생하는 **HW Change List 대응 업무를 AI/Agentic Engineering 기반으로 E2E 혁신**하는 과제를 추진하고 있다.

이 문서는 ChatGPT와 진행한 현재까지의 논의를 Claude에서 이어가기 위한 **working context / project handoff**이다.

Claude는 아래 내용을 충분히 이해한 후, 단순한 AI Coding 아이디어가 아니라 **실제 Mobile PHY SW 조직에서 2026~2027년에 구현 가능한 수준의 현실적인 Engineering Transformation Plan**을 제안해야 한다.

---

# 1. 조직 / 업무 Context

## 업무 분야

* Mobile Protocol SW Development
* 3GPP 기반 Modem Physical Layer SW
* Chipset Bring-up
* Pre-silicon verification
* Silicon bring-up
* Commercialization
* Performance / Functionality / GCF verification

PHY SW Group은 여러 domain/block으로 구성되어 있으며, HW 변경사항을 SW에 반영하고 검증하는 것이 신규 chipset 개발의 핵심 업무 중 하나이다.

---

# 2. 핵심 문제

신규 chipset이 나올 때마다 약 **300~400개의 HW Change List**가 발생한다.

각 HW Change에 대해 PHY SW가 다음 작업을 수행해야 한다.

1. HW Change 내용 이해
2. SW 영향성 분석
3. 담당 domain/block 결정
4. Design Guide 확인
5. SW implementation
6. Code Review
7. Build / Unit Test
8. Virtual Platform 검증
9. Hybrid Zebu 검증
10. Silicon Bring-up
11. Basic Call
12. Live Network Call
13. Voice
14. Performance / Functionality
15. Selective GCF
16. ES Release

현재 가장 큰 문제는 **초기 단계에서 HW Change의 의미와 SW 영향성을 정확하게 이해하지 못하면 뒤 단계에서 매우 큰 비용으로 문제가 발견된다는 것**이다.

---

# 3. 현재 AS-IS Process

## Step 1. HW Change List Review

현재는 HW Change List를 사람이 읽고 다음을 판단한다.

* SW modification 필요 여부
* 영향받는 PHY SW domain/block
* 담당자
* implementation 필요 여부

과거에는 별도의 HW Change List JIRA 체계가 없었다.

여러 차례 JIRA comment를 주고받은 후 구현이 시작된다.

즉,

HW → SW Impact Analysis → Assignment

가 상당히 manual하다.

---

## Step 2. Code Review

Implementation이 시작되면 Code Review가 진행된다.

그러나 현재 Code Review는 비교적 초기 수준이며 특히 다음 문제가 있다.

* HW Change 의도와 code가 정확히 일치하는지 확인하기 어려움
* Legacy code의 context를 reviewer가 모두 이해해야 함
* HW register / bit field와 SW implementation 간 consistency 검증이 어려움
* Design Guide와 실제 implementation의 차이를 자동으로 찾기 어려움
* 과거 유사 HW Change를 찾아 비교하는 것이 어려움

특히 HW Change를 잘못 구현하면 문제가 초기 단계에서 발견되지 않고 commercialization 단계까지 넘어갈 수 있다.

---

# 4. Current Verification Flow

## Step 3. Pre-silicon Virtual Platform

Implementation 이후 Virtual Platform에서 검증한다.

주요 방식:

* Modem System Design Team이 제공한 vector 사용
* SW가 write하는 register 값 비교
* HW/SW interaction 검증

하지만 현재 VP 단계에서는 test case가 build error 수정 등 초기 안정화 단계에 가까워 **TDD를 제대로 적용하기 어렵다.**

---

## Step 4. Hybrid Zebu

VP Pilot TC를 통과하면 Hybrid Zebu에서 다음을 검증한다.

* RFIC
* Modem System
* Platform
* AP/CP Interface
* HW/SW integration

---

## Step 5. Silicon 이후

Chip out 이후에는 다음 순서로 진행된다.

Basic Call
→ Live Network Call
→ Voice Call
→ Performance / Functionality Automation
→ Selective GCF
→ ES Release

문제는 HW Change의 잘못된 구현이 이 단계에서 발견될 경우 이미 많은 비용이 발생한다는 것이다.

---

# 5. 현재 진행 중인 개선

현재 조직에서는 이미 **Pre-silicon 중심의 Shift Left**를 추진하고 있다.

## Virtual Platform

HW Change에 해당하는 register에 대해서는 가능하면 **100% 자동 검증**하는 방향으로 SW base를 준비하고 있다.

## Hybrid Zebu

VP 이후 system-level integration 검증을 강화하고 있다.

## One Dashboard

모든 단계의 검증 항목을 JIRA issue화하고 하나의 dashboard에서 관리하는 방향을 추진하고 있다.

예:

HW Change
→ VP
→ Hybrid Zebu
→ Basic Call
→ Functionality
→ Performance
→ GCF
→ ES

모든 단계가 JIRA 기반으로 traceable하게 연결되는 것이 목표다.

---

# 6. 중요한 현실적 제약

이 프로젝트에서 반드시 고려해야 하는 핵심 제약이다.

## VP / Hybrid Zebu Coverage가 높지 않다.

따라서 단순히

> "검증 TC를 계속 늘려서 coverage를 높이자"

라는 접근은 현실적인 해결책이 아니다.

---

## VP 자체의 한계

* 모든 modem HW behavior를 SystemC로 modeling하기 어렵다.
* HW design complexity 때문에 모든 behavior를 simulation으로 재현하기 어렵다.
* Vector를 이용한 비교에도 한계가 있다.
* 일부 HW Change는 VP에서 meaningful하게 검증하기 어렵다.

---

## 따라서 목표를 다음처럼 정의해야 한다.

### Coverage-driven Verification

에서

### Evidence-driven Engineering

으로 전환해야 단다.

즉,

Static Analysis
+
Register Contract
+
Design Guide Consistency
+
Code Review
+
Unit Test
+
Focused VP
+
Focused H-Zebu
+
Silicon Evidence

를 risk에 따라 조합해야 한다.

모든 HW Change를 동일한 수준의 simulation에 넣는 것은 비효율적이다.

---

# 7. AI / Agentic Coding을 이용하려는 핵심 방향

단순히

> "Claude가 HW Change를 보고 코드를 작성하게 하자."

가 목표가 아니다.

목표는 다음과 같은 **E2E Agentic Engineering Workflow**다.

```text
HW Change
    ↓
Change Understanding
    ↓
Historical / Dependency Analysis
    ↓
Impact Analysis
    ↓
Risk Classification
    ↓
Implementation Plan
    ↓
AI-assisted Implementation
    ↓
Automated Review
    ↓
Build / UT
    ↓
Risk-based Verification
    ↓
VP / H-Zebu
    ↓
Silicon / Commercial
    ↓
Knowledge Feedback
    ↓
Next Chip
```

핵심은 모든 단계에서 동일한 **Change Identity / Evidence Chain**을 유지하는 것이다.

---

# 8. 제안한 E2E Architecture

현재까지 다음 4개의 기반 Layer를 생각하고 있다.

## A. Engineering Knowledge Layer

AI가 PHY SW를 이해할 수 있도록 다음 정보를 구축한다.

### Architecture

* PHY SW architecture
* Domain / block
* Task
* ISR
* IPC
* MSG
* State machine
* Data flow

### Code Graph

* Symbol
* Call graph
* Reference
* Register access
* Function relationship
* File dependency

### HW Knowledge

* Register
* Bit field
* Reset value
* Access type
* HW behavior
* HW design intent

### Design Guide

* HW/SW interface
* Expected SW behavior
* Constraints
* Forbidden behavior
* Implementation guideline

### History

* Historical HW Change
* Bug
* Workaround
* Silicon issue
* Commercial issue

### Verification

* Unit Test
* VP
* Hybrid Zebu
* Vector
* Register comparison
* Field issue

---

# 9. Legacy Code Knowledge 문제

AI에게 단순히 source code repository만 주는 것으로는 충분하지 않다고 판단하고 있다.

특히 PHY SW는 legacy code가 매우 복잡하다.

따라서 다음과 같은 **Group LLM Wiki / Engineering Knowledge Base**를 고려하고 있다.

하지만 Wiki를 사람이 계속 작성하는 방식은 지속성이 떨어진다.

따라서 다음 구조를 검토해야 한다.

```text
Git / Perforce
      ↓
Code Parser
      ↓
AST / Symbol / Call Graph
      ↓
Architecture Knowledge
      ↓
LLM Wiki / RAG
```

그리고 사람이 관리하는 정보:

```text
Design Intent
HW behavior
Known issue
Architecture decision
Workaround
Historical insight
```

와 자동 생성되는 정보:

```text
Function summary
Call graph
Register access
Dependency
Change impact
Code structure
```

를 분리해야 한다.

---

# 10. Knowledge Freshness 문제

Code는 계속 변경된다.

따라서 Wiki가 한번 생성되고 끝나는 방식은 안 된다.

권장 방향:

```text
Code Commit
   ↓
Changed Function / Symbol detection
   ↓
Affected Knowledge detection
   ↓
Knowledge regeneration
   ↓
Human review when necessary
   ↓
Versioned Knowledge
```

즉 **Commit-linked Knowledge**가 필요하다.

AI가 답변할 때도

> "현재 code version에서의 knowledge"

와

> "과거 version에서의 knowledge"

를 구분해야 한다.

---

# 11. Historical HW Change Reconstruction 문제

매우 중요한 문제다.

과거 chipset에서는 별도의 HW Change List JIRA가 없었다.

대신 공통된 **Bring-up CL 제출용 SOC 번호**를 통해 관리되었다.

따라서 과거 HW Change를 다음 artifact에서 역추적해야 한다.

### 후보 Data Source

1. SOC CL
2. Register Change
3. Git / Perforce history
4. Code diff
5. Commit message
6. Review comment
7. Changed file
8. Changed symbol
9. Build history
10. Test case
11. VP vector
12. Bug issue
13. Silicon issue
14. Commercial issue
15. Design Guide version

특히 다음 전략이 중요하다.

### Register Diff

Chip A와 Chip B의

* Register
* Field
* Address
* Reset
* Access type

변화를 추출한다.

그리고 해당 register를 access하는 SW를 찾는다.

```text
Register Change
      ↓
Register Access Search
      ↓
Function
      ↓
Call Graph
      ↓
Task / ISR / Domain
      ↓
Historical Code Change
      ↓
SOC CL
      ↓
Bug / Test / Issue
```

이렇게 해서 과거 HW Change를 reconstruction한다.

---

# 12. Historical Dependency 문제

단순히 register 변경에 해당하는 코드만 찾으면 부족하다.

실제로는 HW Change에 dependency를 가진 여러 SW 수정이 발생할 수 있다.

따라서 다음 signal을 결합해야 한다.

### Direct Dependency

* Register access
* Macro
* Struct
* Enum
* API
* Function call

### Historical Dependency

과거에 같은 HW Change에서 함께 수정되었던

* file
* function
* symbol
* test
* configuration
* state machine

을 찾는다.

### Semantic Dependency

Code 의미상 영향을 받을 수 있는 영역을 찾는다.

예:

```text
HW Register change
    ↓
Register API
    ↓
PHY abstraction
    ↓
Scheduler
    ↓
ISR
    ↓
Message
    ↓
State transition
```

따라서 단순 text search가 아니라 **Code Graph + Historical Coupling + LLM Semantic Analysis**를 조합하는 것이 중요하다.

---

# 13. HW ↔ SW Design Guide 문제

Design Guide는 다른 팀에서 작성한다.

따라서 팀 간 정보 전달이 핵심 bottleneck이다.

단순 PDF / Word 문서 전달 방식에서 벗어나야 한다.

목표는:

## HW Change Contract

를 표준화하는 것이다.

최소 항목:

```text
Change ID
HW Block
Register
Field
Previous behavior
New behavior
Why changed
HW design intent
SW impact
Required SW behavior
Forbidden behavior
Compatibility constraint
Affected interface
Verification expectation
Owner
Version
```

이 정보를 machine-readable format으로 관리한다.

예:

```yaml
change_id:
hw_block:
register:
field:
old_behavior:
new_behavior:
design_intent:
sw_impact:
required_behavior:
forbidden_behavior:
verification:
owner:
version:
```

이렇게 하면 AI가 Design Guide를 읽는 것이 아니라 **구조화된 HW Change Contract**를 읽을 수 있다.

---

# 14. AI Agent Architecture

처음부터 완전 Autonomous Agent를 만들지 않는다.

단계적으로 권한을 확대한다.

## Agent 1 — Change Analyst

입력:

* HW Change
* Register diff
* Design Guide
* Code graph
* Historical knowledge

출력:

* Impact analysis
* Dependency
* Risk
* Candidate owner
* Historical precedent

---

## Agent 2 — Implementation Agent

출력:

* Implementation plan
* Files to modify
* Functions
* Expected behavior
* Patch
* Build result
* Unit test

처음에는 **Low-risk HW Change**만 허용한다.

---

## Agent 3 — Review Agent

다음을 cross-check한다.

```text
HW Change
    ↕
Design Guide
    ↕
Register Definition
    ↕
Code
    ↕
Historical Implementation
    ↕
Test
```

Review 결과에는 반드시:

* Evidence
* Confidence
* Reason
* Unknown

을 포함한다.

---

## Agent 4 — Verification Agent

AI가 모든 테스트를 실행하는 것이 아니라,

> "이 HW Change에서 어떤 evidence가 필요한가?"

를 판단한다.

예:

```text
LOW
Static + Contract

MEDIUM
Static + Contract + UT

HIGH
Static + Contract + UT + VP

CRITICAL
Static + UT + VP + H-Zebu + Human Review
```

---

## Agent 5 — Knowledge Agent

Code 변경 후 영향을 받는 knowledge를 찾아 업데이트한다.

---

# 15. Risk Classification

모든 HW Change를 동일하게 처리하면 AI automation이 실패할 가능성이 높다.

따라서 처음부터 Risk Score를 만든다.

예:

```text
Risk =
HW criticality
+
code complexity
+
dependency count
+
historical defect rate
+
verification weakness
+
commercial impact
```

그리고

### Low Risk

반복적 register handling

### Medium Risk

일부 algorithm / state change

### High Risk

Scheduler / ISR / timing / HARQ / PHY pipeline

### Critical

Architecture / interface / timing-critical / commercial-critical

등으로 구분한다.

---

# 16. Verification Philosophy

핵심 원칙:

> "100% simulation coverage"가 목표가 아니다.

대신:

> "100% HW Change가 최소 하나 이상의 독립적인 evidence를 갖도록 한다."

예:

```text
HW Change
 ↓
Contract Check
 ↓
Register Consistency
 ↓
Code Static Check
 ↓
Unit Test
 ↓
Focused VP
 ↓
H-Zebu
 ↓
Silicon
```

중요한 것은 **Evidence Chain Completeness**다.

---

# 17. One Dashboard

JIRA를 중심으로 다음 관계를 만든다.

```text
HW Change
   │
   ├── Design Guide
   │
   ├── Implementation CL
   │
   ├── Code Review
   │
   ├── Build
   │
   ├── UT
   │
   ├── VP
   │
   ├── H-Zebu
   │
   ├── Silicon Issue
   │
   └── Commercial Release
```

Dashboard에서는 최소 다음을 보여야 한다.

* 전체 HW Change
* Risk
* Owner
* Implementation status
* Review status
* Verification status
* Evidence completeness
* Blocker
* Escape
* Commercial issue
* AI recommendation
* AI acceptance rate

---

# 18. Roadmap

현재 제안하는 현실적인 단계는 다음과 같다.

## Phase 0 — Foundation

목표:

* Historical data 확보
* HW Change Contract 정의
* Knowledge schema 정의
* JIRA linkage 정의

---

## Phase 1 — AI Review

가장 먼저 성공시킬 영역이다.

AI가:

```text
HW Change
+
Design Guide
+
Code
+
Register
+
Historical knowledge
```

를 보고

* 영향성
* dependency
* 누락 가능성
* review checklist
* risk

를 제시한다.

**AI가 코드를 직접 수정하지 않아도 된다.**

이 단계에서 review quality 향상을 증명한다.

---

## Phase 2 — Low-risk AI Implementation

AI가 다음을 수행한다.

```text
Analyze
→ Plan
→ Patch
→ Build
→ UT
→ Review
```

단,

**Low-risk change부터 시작한다.**

---

## Phase 3 — Risk-based Verification

AI가 Change별로 필요한 evidence를 추천한다.

VP/H-Zebu resource를 중요한 Change에 집중한다.

---

## Phase 4 — E2E Agentic Engineering

최종적으로:

```text
HW Change
 ↓
AI Analysis
 ↓
AI Implementation
 ↓
AI Review
 ↓
AI Verification Planning
 ↓
Automated Evidence
 ↓
JIRA Dashboard
 ↓
Commercial Release
 ↓
Knowledge Feedback
```

까지 연결한다.

---

# 19. 제안 KPI

AI가 몇 줄의 코드를 작성했는지는 핵심 KPI가 아니다.

핵심 KPI:

### Quality

* HW Change escape rate ↓
* Commercial defect ↓
* Bring-up defect ↓

### Early Detection

* Pre-silicon detection rate ↑
* VP/H-Zebu detection effectiveness ↑

### Efficiency

* HW Change analysis 대기시간 ↓
* Implementation time ↓
* Review time ↓
* Debug time ↓

### AI

* AI recommendation acceptance rate
* AI review defect recall
* AI patch acceptance rate
* AI generated patch rework rate

### Traceability

* HW Change → Design → Code → Test traceability
* Evidence completeness

---

# 20. 가장 중요한 전략적 원칙

이 프로젝트에서 피해야 할 접근:

### ❌ "AI Coding Tool 도입"

Claude Code / Copilot / 기타 LLM을 단순히 개발자에게 제공하는 것은 목표가 아니다.

### ❌ "VP coverage를 계속 높이자"

현실적인 HW modeling / vector / SystemC 한계가 있다.

### ❌ "RAG Wiki를 크게 만들자"

Legacy code는 계속 변경되므로 static Wiki는 빠르게 낡는다.

### ❌ "처음부터 Autonomous Agent"

PHY SW의 risk가 높기 때문에 실패 가능성이 높다.

---

# 21. 반드시 지향해야 할 것

### ✅ HW Change를 Engineering Object로 정의

### ✅ HW Change Contract

### ✅ Code Graph + Register Graph

### ✅ Historical Change Reconstruction

### ✅ Versioned Engineering Knowledge

### ✅ Evidence-based AI Review

### ✅ Risk-based Agentic Coding

### ✅ Risk-based Verification

### ✅ JIRA-based Traceability

### ✅ Silicon / Commercial feedback → Knowledge feedback

---

# 22. 현재까지 만든 Executive Presentation

ChatGPT에서 다음 결과물을 이미 생성했다.

## PPT

`PHY_SW_AI_E2E_Executive_Diagram.pptx`

한 장의 Executive E2E 그림:

```text
HW CHANGE
    ↓
INTELLIGENCE
    ↓
AI IMPLEMENT
    ↓
AI REVIEW
    ↓
RISK-BASED VERIFY
    ↓
COMMERCIAL
```

하부 Layer:

```text
Engineering Knowledge
AI Agent Layer
Evidence Layer
One Dashboard / JIRA
```

그리고 핵심 메시지:

```text
Coverage-driven
       ↓
Evidence-driven
       ↓
Lower escape rate
Faster bring-up
Less developer effort
```

---

# 23. Claude에서 이어서 해야 할 다음 작업

이 프로젝트를 실제 임원 보고 및 개발 프로젝트로 발전시키려면 다음 작업을 수행해라.

## TASK 1 — Deep Research

해외 Big Tech / Leading Mobile Modem 회사의 실제 사례를 조사한다.

특히:

* Google
* Apple
* Qualcomm (참조: [Codemate: Coding with On-Device AI](https://www.qualcomm.com/developer/blog/2025/09/codemate-coding-with-on-device-ai?utm_source=chatgpt.com))
* MediaTek
* NVIDIA
* Meta

등에서 공개적으로 확인 가능한 자료를 우선한다.

다음 주제를 조사한다.

1. Agentic coding
2. AI software engineering
3. AI code review
4. AI-assisted verification
5. Hardware/software co-design
6. Pre-silicon verification
7. Regression automation
8. Engineering knowledge systems
9. Change impact analysis
10. Large-scale codebase AI

단, **확인되지 않은 회사 내부 사례를 사실처럼 만들지 말 것.**

공개된 기술 블로그 / conference / paper / engineering article / official publication을 기반으로 한다.

---

# 24. Deep Research 결과의 요구사항

각 사례를 다음 형식으로 정리한다.

| Company | Problem | AI/Automation Approach | 실제 적용 수준 | 효과 | PHY SW 적용 가능성 |
| ------- | ------- | ---------------------- | -------- | -- | ------------- |

그리고 단순히 사례를 나열하지 말고

> "왜 이 사례가 PHY SW HW Change 문제에 적용 가능한가?"

를 분석한다.

---

# 25. 특히 조사해야 할 Agentic Coding 개념

다음 개념을 실제 Engineering Workflow 관점에서 설명한다.

* Agentic coding
* Coding agent
* Planning
* Context engineering
* Tool use
* Retrieval
* Code graph
* Repository understanding
* Memory
* Long-running agent
* Multi-agent
* Human-in-the-loop
* Verification loop
* Evaluation
* Rubric
* Guardrail
* Confidence
* Evidence
* Autonomous coding
* SWE-bench
* Software engineering benchmark

특히 **RL을 coding/agentic task에 강하게 적용한다는 의미**도 설명한다.

---

# 26. 최종적으로 만들고 싶은 것

단순 발표 자료가 아니라 실제 프로젝트의 **PRD**를 만들고 싶다.

PRD에는 최소 다음이 포함되어야 단다.

1. Background
2. Problem Statement
3. Current Process
4. Pain Points
5. Goals
6. Non-goals
7. Target E2E Architecture
8. HW Change Contract
9. Historical Knowledge Reconstruction
10. PHY SW Code Knowledge Architecture
11. AI Agent Architecture
12. AI Review
13. AI Implementation
14. Risk Classification
15. Verification Strategy
16. VP / H-Zebu limitation strategy
17. JIRA / Dashboard
18. Data Architecture
19. Security / IP considerations
20. Human-in-the-loop
21. KPI
22. Pilot plan
23. Rollout plan
24. Risks
25. Expected ROI

---

# 27. Claude에게 요구하는 답변 방식

나는 PHY SW Group Leader이므로 단순한 AI 설명보다 **Engineering Manager / Architect 관점**으로 답변해라.

특히 다음 질문에 답해야 한다.

> "이것을 실제 PHY SW 조직에서 올해 성공시킬 수 있는가?"

각 제안마다 다음을 명확하게 표시해라.

* Feasibility
* Required data
* Required infrastructure
* Required manpower
* Expected benefit
* Risk
* Implementation difficulty
* Pilot size
* Expected timeline

그리고 가능하면:

```text
Quick Win
↓
Pilot
↓
Scale
↓
E2E Automation
```

형태로 단계화한다.

---

# 28. 가장 중요한 질문

최종적으로 다음 질문에 대한 명확한 답을 만들어야 한다.

### Q1.

과거 HW Change JIRA가 없는 상황에서 어떻게 Historical HW Change Knowledge를 만들 것인가?

### Q2.

HW Design Team과 PHY SW Team 사이의 Design Guide / HW Change 정보 전달을 어떻게 표준화할 것인가?

### Q3.

AI에게 Legacy PHY SW를 어떻게 이해시킬 것인가?

### Q4.

Code가 계속 변경되는 상황에서 AI Knowledge를 어떻게 최신 상태로 유지할 것인가?

### Q5.

VP/H-Zebu coverage가 낮은 상황에서 어떻게 HW Change의 품질을 보증할 것인가?

### Q6.

AI가 잘못된 코드를 생성하는 문제를 어떻게 방지할 것인가?

### Q7.

AI Review가 실제 인간 Senior Engineer Review보다 좋은지 어떻게 측정할 것인가?

### Q8.

300~400 HW Change 중 어느 범위부터 Agentic Coding을 적용해야 하는가?

### Q9.

어떤 KPI로 프로젝트 성공 여부를 판단할 것인가?

### Q10.

이 프로젝트가 실제 commercialization schedule을 단축시키는지 어떻게 증명할 것인가?

---

# 29. 최종 목표

궁극적인 목표는 다음이다.

현재:

```text
HW Change
 ↓
Human Interpretation
 ↓
Manual Implementation
 ↓
Weak Review
 ↓
Late Verification
 ↓
Commercial Issue
```

를

```text
HW Change Contract
       ↓
AI Change Understanding
       ↓
Historical + Code + HW Dependency Analysis
       ↓
Risk Classification
       ↓
AI Implementation
       ↓
Evidence-based AI Review
       ↓
Risk-based Verification
       ↓
JIRA E2E Traceability
       ↓
Commercialization
       ↓
Knowledge Feedback
```

으로 바꾸는 것이다.

**핵심 목표는 AI Coding 자체가 아니라 PHY SW HW Change 대응의 구조적인 업무 방식을 바꾸는 것이다.**

Claude는 이 목표를 기준으로 이후 모든 연구와 설계를 진행해야 한다.
