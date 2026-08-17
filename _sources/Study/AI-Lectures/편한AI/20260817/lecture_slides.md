---
marp: true
theme: default
class: lead
backgroundColor: #f8f9fa
color: #202124
style: |
  h1 {
    color: #1a73e8;
  }
  h2 {
    color: #202124;
    border-bottom: 2px solid #e8eaed;
    padding-bottom: 0.5em;
  }
  li {
    line-height: 1.5;
  }
---

# 🧠 Building an Autonomous Second Brain
**Obsidian LLM Wiki: 지식 관리에서 능동적 AI 에이전트로의 진화**

---

## 1. The Problem: 왜 우리는 지식 관리에 실패하는가?

기존의 세컨드 브레인(Second Brain) 구축 방식은 본질적인 한계를 가집니다.

- **수동적 아카이빙:** Notion, Evernote에 수집만 하고 다시 열어보지 않는 '정보의 무덤'
- **인지적 과부하 (Cognitive Overload):** 문서를 어디에 넣을지, 어떤 태그를 달지 사람이 직접 결정해야 하는 높은 분류/연결 비용
- **고립된 지식:** 문서 간의 맥락(Context)이 연결되지 않아 인사이트 창출 실패

---

## 2. The Solution: 사람과 AI의 역할 분담 (Andrej Karpathy)

테슬라 전 AI 디렉터 안드레이 카파시(Andrej Karpathy)가 제안한 LLM 기반 위키의 핵심은 **철저한 분업**입니다.

* **👤 Human (사람):** 가치 있는 원본 데이터 수집 및 폴더 드롭 (Curation)
* **🤖 AI Agent (LLM):** 
  - 원본 데이터를 읽고 **개념(Concept), 개체(Entity), 기술(Skill)** 로 분해 (Extraction)
  - 지식 간의 맥락을 파악하여 **자동 양방향 링크** 생성 (Graph Resolution)
  - 마스터 인덱스 및 목차 자동 갱신 (Schema Management)

---

## 3. Why Obsidian? (아키텍처 선택의 이유)

Big Tech 수준의 AI 시스템을 구축하기 위해 '노션'이 아닌 '옵시디언'을 선택한 기술적 이유:

1. **Data Ownership (로컬 저장소):** 클라우드 DB가 아닌 로컬 마크다운(`.md`) 파일. AI 에이전트(Antigravity IDE 등)가 파일 시스템에 직접 접근(Read/Write)하기 가장 완벽한 환경.
2. **Knowledge Graph (양방향 링크):** `[[WikiLinks]]` 문법을 통한 문서 간 네트워크 형성. AI가 지식을 시각적 그래프로 매핑 가능.
3. **Open Ecosystem:** 방대한 플러그인 생태계와 완전한 오프라인 작동 구조.

---

## 4. System Architecture: 능동적 지식 파이프라인

데이터가 지식으로 변환되는 4단계 자동화 파이프라인

1. **Ingest (수집):** `_sources/` (보존용) 또는 `_raw/` (임시) 폴더에 원본 파일 드롭
2. **Extract (추출):** AI가 파일을 읽고 주요 지식을 조각(Chunk) 단위로 분해
3. **Resolve (병합):** 기존 위키 그래프와 대조하여 중복을 제거하고 관계망(Link) 형성
4. **Schema (구조화):** `index.md`, `log.md`, `manifest.json` 자동 갱신 및 파일 이동

---

## 5. Implementation: 7-Step Workflow

1. **클리핑:** Web Clipper를 통해 웹 문서를 `_sources/Clipping`으로 자동 저장
2. **Trigger:** `/wiki-ingest` 명령어 실행
3. **Delta Check:** AI가 `.manifest.json`을 검사하여 새로운 파일만 식별
4. **Processing:** 백그라운드에서 AI가 지식 추출 및 마크다운 생성
5. **Filing:** `concepts/`, `entities/`, `skills/` 디렉토리로 자동 분류
6. **Cleanup:** `_raw/`의 임시 파일 자동 삭제
7. **Visualization:** Obsidian Graph View를 통한 지식 토폴로지(Topology) 확인

---

## 6. Beyond Wiki: 능동적 에이전트 허브 (Action-oriented AI)

지식 보관소를 넘어, 내 업무를 대신 수행하는 AI 비서로 확장

* **Vibe Coding (반복 업무 자동화):** "지난 2주간 회의록을 모아 주간 보고서 PPT로 만들어줘" ➔ Cron Job 스케줄링 (`ops_` 워크플로우)
* **Agentic Automation:** AI가 직접 브라우저를 띄워 리서치(Perplexity, Web Search)하고 결과를 위키에 정리
* **Subscription Model:** 구독한 뉴스레터나 유튜브 채널의 핵심만 매일 아침 요약하여 Push
* **SSG (Static Site Generation):** 코딩 없이 위키 문서를 Hugo/Next.js 기반 개인 브랜드 블로그로 자동 퍼블리싱

---

## 7. Next Steps

* **Start Small:** 완벽한 구조를 고민하지 마세요. 일단 `_raw/` 폴더에 자료를 던지는 것부터 시작하십시오.
* **Trust the Agent:** 분류와 정리는 AI에게 맡기고, 당신은 '어떤 정보'를 넣을지에 집중하세요.
* **Iterate:** AI가 만들어낸 연결 고리(`Graph`)를 탐험하며 인사이트를 발견하세요.

**"The Future of Note-taking is Note-making by AI."**
