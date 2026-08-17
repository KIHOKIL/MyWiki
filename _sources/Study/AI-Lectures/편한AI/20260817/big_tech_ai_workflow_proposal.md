# 🚀 빅테크 사례 기반 LLM Wiki 워크플로우 제안서 (Agentic Scaffolding)

이 문서는 Meta, Google, Anthropic, Apple 등 글로벌 빅테크 기업들의 최신 사내 AI 활용 트렌드를 분석하고, 이를 바탕으로 사용자님의 업무(코드 리뷰, 로그 분석, JIRA 관리, 보고서 작성 등)를 획기적으로 효율화할 수 있는 **'LLM Wiki 기반 에이전틱 워크플로우(Agentic Workflow)' 구축 방안**을 제시합니다.

---

## 1. 🔍 글로벌 빅테크의 사내 AI 활용 트렌드 (Deep Research)

최근 빅테크 기업들은 단순히 코드를 짜주는 'Copilot(보조자)' 수준을 넘어, 프로젝트 전반의 문맥을 이해하고 스스로 행동하는 **'다중 에이전트(Multi-agent)' 시스템**을 사내망에 구축하고 있습니다.

* **Anthropic (Claude):** 
  * 단일 모델이 아닌 **'다중 에이전트 리뷰(Multi-agent Code Review)' 시스템**을 운영합니다.
  * PR이 올라오면 보안 체크 에이전트, 로직 체크 에이전트, 사내 규정 체크 에이전트가 각자 리뷰를 수행하고, 서로의 결과를 **교차 검증(Verification Layer)**하여 오류(False Positive)를 걸러낸 뒤 사람에게 최종 결과를 보고합니다.
* **Meta:** 
  * 수백만 개의 소스 코드를 관리하기 위해 사내 전용 도구(EdenFS)와 결합된 디버깅 자동화 플랫폼 **'DrP'** 를 구축했습니다. 
  * 에러 로그가 발생하면 엔지니어가 조사하는 '로직' 자체를 코드로 만들어(인코딩), AI가 수천 개의 로그를 자동 분석하고 원인을 추론합니다.
* **Google / Apple:** 
  * 사내 데이터(JIRA, Confluence, Source Code) 외부 유출을 막기 위해 **로컬/프라이빗 클라우드에 고립된 사내용 LLM**(Gemini 기반 Vertex AI, 커스텀 Claude)을 연동합니다.
  * AI가 코드 내 버그를 발견하면 즉시 JIRA 이슈를 자동 생성(IssueOps)하고 담당자를 할당하는 파이프라인을 운영합니다.

---

## 2. 🏗️ 나의 업무에 적용하기: LLM Wiki Scaffolding 아키텍처

위 빅테크 사례의 핵심은 **"모든 컨텍스트(문맥)가 모이는 중앙 뇌(Central Brain)"** 가 있다는 것입니다. 우리는 **Obsidian(MyWiki)** 을 그 중앙 뇌(Agentic Memory)로 삼고, **Antigravity IDE**를 행동하는 에이전트로 활용합니다.

사용자님의 11가지 주요 업무를 AI로 효율화하는 구체적인 워크플로우를 제안합니다.

### 📥 [1] 지식 수집 및 동기화 (JIRA, Confluence, Email, Teams)
* **문제:** 흩어져 있는 업무 정보를 찾느라 시간이 낭비됨.
* **Scaffolding 방안:**
  * **Webhook/API 연동 스킬 구축:** Antigravity 에이전트에 파이썬 스크립트 스킬을 등록하여, JIRA/Confluence API를 정기적으로 호출.
  * **Wiki Ingest:** 가져온 티켓과 위키 문서를 옵시디언의 `_raw/` 폴더로 드롭. 에이전트가 이를 분석해 `entities`(프로젝트/이슈), `journal`(이메일/회의) 등으로 자동 분류 및 링크(`[[ ]]`) 생성.
  * **효과:** 옵시디언 그래프 뷰를 통해 "특정 JIRA 이슈"와 "관련 이메일 스레드"가 연결된 것을 한눈에 파악.

### 💻 [2] 코드 이해, 구현(Implementation), 리뷰(Code Review)
* **문제:** 방대한 코드베이스 파악 및 휴먼 에러 발생.
* **Scaffolding 방안:**
  * **Code Base 인덱싱:** 전체 소스코드를 에이전트가 접근 가능한 로컬 디렉토리에 두고, 중요 아키텍처(ADR) 문서만 위키의 `concepts` 폴더에 동기화하여 에이전트가 프로젝트 문맥을 이해하도록 함.
  * **바이브 코딩 (Vibe Coding):** JIRA 티켓 내용이 담긴 위키 문서를 에이전트에게 주고, *"이 기획을 바탕으로 로컬 환경에서 코드를 구현해(Implementation)"* 라고 지시.
  * **다중 에이전트 코드 리뷰 파이프라인:** Github Actions(`.github/workflows/`)를 활용하여 PR 생성 시 구동되는 CI 봇 구축. 
    * Anthropic 방식 적용: **[보안 에이전트]**, **[로직 에이전트]** 가 각각 PR을 리뷰하고, 결과를 종합하여 Github Issue 코멘트로 자동 등록 (IssueOps 연동).

### 🐛 [3] 로그 분석 및 이슈 현황 모니터링
* **문제:** 수많은 로그에서 에러 원인을 찾고, 그룹의 이슈 현황을 실시간 파악하기 어려움.
* **Scaffolding 방안:**
  * **Log Analyzer 스킬 로드:** 정규표현식과 LLM을 결합한 파이썬 스크립트 스킬 생성. 복잡한 로그 파일을 에이전트에게 던지면, 핵심 에러 패턴만 추출하여 위키의 `journal/` 하위로 `[에러 분석] 260817.md` 문서 자동 생성.
  * **Obsidian Dataview 대시보드:** 옵시디언 내에 플러그인(Dataview)을 사용하여, 위키 내 태그(`#jira`, `#error`)가 달린 문서를 실시간 표(Table) 형태로 렌더링하는 현황판(Dashboard) 구축.

### 📊 [4] 주간 보고서(Weekly Status) 및 임원 보고(PPT/PDF) 자동화
* **문제:** 금요일마다 흩어진 정보를 취합해 보고서 서식을 맞추는 단순 반복 업무.
* **Scaffolding 방안:**
  * **Weekly Digest 자동화:** 매일 `journal`과 `projects` 폴더에 쌓인 활동 내역을 바탕으로, 금요일 오후 5시에 에이전트가 `/wiki-digest` 명령을 백그라운드 실행. 1주일간의 핵심 성과를 마크다운 보고서로 초안 작성.
  * **Visually Appealing 포맷 변환:** **Marp (Markdown to PPT 플러그인)** 또는 Pandoc 프레임워크를 활용.
    * 에이전트에게 *"위키에 생성된 이번 주 주간 보고서를 글로벌 빅테크 임원진 보고 스타일로 시각화하여 PPT와 PDF 포맷으로 추출해줘"* 라고 명령.
    * CSS 테마를 미리 지정해두어 회사의 서식(Brand Color, Logo)에 정확히 맞춘 결과물 생성.

### 🗓️ [5] 회의 일정 관리 및 메일/Slack 작성
* **문제:** 잦은 회의와 커뮤니케이션 리소스 낭비.
* **Scaffolding 방안:**
  * **데일리 브리핑:** 아침에 에이전트가 캘린더 정보를 파싱하여 위키 오늘의 저널(Today's Journal) 상단에 참석해야 할 회의 일정을 리스팅.
  * **문맥 기반 텍스트 생성:** *"오늘 3시 회의(위키에 저장된 컨텍스트) 결과를 바탕으로, 개발실장님께 보고할 슬랙 메시지와 이메일을 정중한 서식으로 작성해줘"* 한 줄로 커뮤니케이션 문서 완성.

### 🔎 [6] 통합 키워드 Search 기능
* **Scaffolding 방안:**
  * 로컬에 축적된 수만 개의 지식(코드, 이메일, 슬랙 대화록, JIRA 티켓)을 기반으로, Antigravity 에이전트에게 채팅으로 질문.
  * *"최근 3개월 간 인증(Authentication) 모듈 에러와 관련된 슬랙 대화와 JIRA 이슈를 모두 찾아서 요약해줘"*
  * RAG(Retrieval-Augmented Generation) 방식을 통해 정확한 파일 링크(`[[ ]]`)를 달아 답변을 제시.

---

## 3. ✅ Next Steps: 실행 계획

이 거대한 LLM Wiki 기반 스캐폴딩을 실무에 안착시키기 위한 단계별 목표입니다.

1. **(Step 1) 코어 구축:** 
   * 기존 마이 위키(`MyWiki`) 내에 JIRA/Confluence 정보를 수동 또는 반자동(Web Clipper)으로 인제스트하여 연결하는 습관 들이기.
   * `Dataview` 플러그인 설치를 통해 위키 내 정보 대시보드화.
2. **(Step 2) 리뷰/분석 파이프라인 통합:** 
   * Github Actions를 활용한 다중 에이전트 코드 리뷰 봇 구축 (Anthropic 리뷰 모델 벤치마킹).
   * 로그 분석 전용 Python 스킬(`.agents/skills/log-analyzer/SKILL.md`) 커스텀 제작.
3. **(Step 3) 보고 및 시각화 자동화:** 
   * Marp CLI를 CI/CD 혹은 로컬 에이전트 환경에 셋업하여, 위키의 마크다운 글을 엔터프라이즈급 PPT/PDF로 렌더링하는 워크플로우 완성.
