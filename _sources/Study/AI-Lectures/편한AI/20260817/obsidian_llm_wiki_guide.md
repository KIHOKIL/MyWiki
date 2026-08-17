# 🧠 Obsidian LLM Wiki 구축 및 사용 완벽 가이드

본 교안은 유튜브 강의 **"Obsidian LLM Wiki 초보자 설치부터 사용까지"** 와 **"못다한 이야기와 나의 AI 관련 팁 (1, 2부)"**, 그리고 **공식 블로그 매뉴얼**의 내용을 종합하여, 누구나 쉽게 LLM 기반의 두 번째 뇌(Second Brain)를 구축하고 사용할 수 있도록 작성되었습니다.

---

## 1. LLM 위키(LLM Wiki)란?

테슬라의 전 AI 디렉터이자 전 OpenAI 연구원인 **안드레이 카파시(Andrej Karpathy)** 가 제안한 개념입니다. 
지금까지는 지식의 수집, 정리, 연결을 모두 사람이 수작업으로 해야 했기에 많은 사람들이 '세컨드 브레인' 구축에 실패했습니다. 

LLM 위키는 **"사람과 AI의 역할 분담"** 에 핵심이 있습니다.
* **사람의 역할:** 원본 문서를 작성하고, 양질의 자료를 수집하여 폴더에 넣습니다.
* **LLM(AI)의 역할:** 수집된 문서를 분석 및 분해하여, 개념(Concept), 개체(Entity), 기술(Skill) 등으로 재구성하고 문서 간의 맥락을 파악하여 **자동으로 링크(연결)** 합니다.

### 왜 '노션(Notion)'이 아닌 '옵시디언(Obsidian)'인가?
* **로컬 저장소 (데이터 소유권):** 옵시디언은 클라우드가 아닌 내 컴퓨터(로컬)에 마크다운(.md) 파일 형태로 지식을 저장합니다. 이는 AI 에이전트(예: 안티그래비티 IDE)가 직접 파일에 접근하여 읽고 쓰기 매우 유리한 환경을 제공합니다.
* **강력한 연결성:** 마크다운 기반으로 문서 간 양방향 링크(`[[ ]]`)를 생성하여 지식을 시각적 그래프로 엮고 찾기 쉽게 연결하기 좋습니다.
* **완전 무료:** 동기화(Sync) 기능을 제외한 핵심 기능이 무료이며, 플러그인 생태계가 방대합니다.

---

## 2. 사전 준비: 하드웨어 권장 사양

LLM 위키를 로컬에서 구동(Local LLM)하려면 높은 하드웨어 사양이 요구되나, 우리는 **클라우드 API(Antigravity IDE 등)** 를 활용하므로 일반적인 환경에서는 충분히 구축 가능합니다.

* **운영체제:** Windows 11 이상 또는 macOS
* **메모리(RAM):** 최소 16GB (권장 24GB 이상)
* **저장장치(SSD):** 최소 512GB (권장 1TB 이상)

> [!TIP] 
> **로컬 LLM (Ollama 등)을 직접 구동하고 싶다면?**
> 로컬에서 AI 모델을 돌리려면 GPU의 VRAM 용량이 매우 중요합니다. 최소 16GB~32GB 이상의 VRAM이 필요하며, 비용 및 효율을 고려했을 때 개인은 **클라우드 기반의 AI 서비스(Gemini, Claude, ChatGPT 등)** 를 사용하는 것을 권장합니다.

---

## 3. 프로그램 설치 가이드 (초보자용 상세 매뉴얼)

### 단계 1: 폴더 구성하기
지식을 담을 근간이 되는 폴더를 생성합니다.

1. **단일 컴퓨터에서만 사용할 경우**
   * 바탕화면이나 문서 폴더에 원하는 이름의 폴더를 생성합니다. (예: `MyWiki`)
2. **다중 디바이스(스마트폰 등)와 동기화할 경우**
   * Obsidian Sync(유료)를 쓰지 않더라도 iCloud, Google Drive, Dropbox 등을 활용할 수 있습니다.
   * **Mac 사용자:** Obsidian 앱을 설치하면 iCloud에 `Obsidian` 폴더가 자동 생성됩니다. 그 안에 `MyWiki` 폴더를 만드세요.
   * **Windows 사용자:** Google Drive 앱 설치 후 `내 드라이브` 하위에 `MyWiki` 폴더를 생성합니다.

### 단계 2: 옵시디언 (Obsidian) 설치 및 설정
1. [옵시디언 공식 홈페이지(obsidian.md)](https://obsidian.md/)에서 OS에 맞는 버전을 다운로드 및 설치합니다.
2. 옵시디언을 실행하고 **'Open Vault(폴더 열기)'** 를 선택하여 방금 만든 폴더(`MyWiki`)를 엽니다.
3. 좌측 사이드바의 ‘그래프 뷰’를 통해 향후 파일들이 어떻게 연결되는지 시각적으로 확인할 수 있습니다.

### 단계 3: 옵시디언 웹 클리퍼(Web Clipper) 설치
인터넷의 유용한 정보나 글을 옵시디언으로 스크랩하는 도구입니다.
1. 크롬 웹스토어에서 [Obsidian Web Clipper](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf)를 브라우저에 추가합니다.
2. 브라우저 우측 상단 확장 프로그램 아이콘을 눌러 클리퍼의 **'옵션(Options)'** 으로 들어갑니다.
3. 저장 위치 설정: `기본 템플릿` -> `노트 위치` 값을 **`_sources/Clipping`** 으로 변경합니다.

### 단계 4: 안티그래비티 IDE (Antigravity IDE) 설치
AI 에이전트가 내 폴더에 접근하여 위키를 자동 구성해주는 핵심 도구입니다.
1. [Antigravity.google](https://antigravity.google/download#antigravity-ide)에 접속하여 본인의 칩셋 환경에 맞는 버전을 다운로드하고 설치합니다.
2. 구글 계정으로 로그인 후 초기 세팅을 진행합니다.
   * **AI 권한 설정 (중요):** `Agent-driven development`(자동 운전 모드) 또는 `Review-driven development`(사용자 승인 후 실행)를 선택합니다.
   * **Build with Google:** 플러그인 중 `Modern Web Guidance`를 체크한 후 설치를 완료합니다.
3. IDE 좌측 `Explorer` 아이콘 클릭 후 **[Open Folder]** 를 눌러 `MyWiki` 폴더를 엽니다.

---

## 4. LLM 위키 초기 구축 (AI 에이전트 프롬프팅)

Antigravity IDE 우측 AI 채팅창에 아래 문장들을 순서대로 붙여넣어 자동 구축을 진행합니다.

**1. 파이썬 환경 설정**
> "Python을 전역설정으로 설치해줘."

**2. 위키 리포지토리 설치 (AR9AV 버전)**
> "안드레이 카파시의 Obsidian + LLM + Wiki 개념으로 현재 폴더에 지식 베이스를 구축하려고 해. 현재 폴더에 https://github.com/Ar9av/obsidian-wiki 리포지터리를 설치해줘."

**3. 원본 소스(`_sources`) 폴더 설정**
> "root 폴더에 `_sources` 폴더를 생성해줘. 그리고, `.env` 파일에 이 폴더를 OBSIDIAN_SOURCES_DIR로 지정해줘."

**4. 폴더 인덱스 자동화 스크립트 작성 (중요)**
아래의 전체 코드를 복사해서 AI에게 지시합니다. (원본 보존 및 자동 갱신 파이썬 스크립트 작성)
```python
내가 관리하고 있는 Obsidian 위키 Vault 내부의 원본 소스 폴더들(`_sources/`)을 체계적으로 연결하고 요약해 주는 파이썬 자동화 스크립트 `scripts/generate_index.py`를 작성해줘.

이 스크립트는 하위 폴더별 인덱스(`_index.md`) 파일 생성과 상위 마스터 인덱스(`_sources/_index.md`) 갱신을 담당해야 해. 구체적인 동작 방식은 다음과 같아:

1. **설정 및 기본 정보 해석**
    - 현재 작업 디렉토리(CWD)부터 상위 폴더로 가며 `.env` 파일 내 `OBSIDIAN_VAULT_PATH`를 읽거나, `~/.obsidian-wiki/config` 파일에서 Vault의 절대경로를 찾아야 해. (없으면 오류 종료)
    - 소스 폴더의 기준은 `$OBSIDIAN_VAULT_PATH/_sources`로 잡고 동작해줘.
2. **개별 하위 폴더 내 `_index.md` 생성 및 보존**
    - 지정된 하위 폴더(혹은 인자가 없을 시 `_sources` 하위의 모든 폴더) 내부의 마크다운 파일(`.md`) 목록을 오름차순 정렬하여 수집해 (파일명이 `_`로 시작하는 인덱스 파일 등은 수집에서 제외).
    - **기존 설명 보존**: 폴더 내에 이미 `_index.md`가 존재한다면, 파일 내의 `[[파일명.md]] — 설명문` 패턴을 파싱해서 기존에 사람이 작성해 둔 설명들을 딕셔너리로 메모리에 보존해야 해.
    - **새로운 설명 추출**: 기존 인덱스에 없는 새로운 파일은 파일 내부의 첫 번째 제목(H1 `#`  또는 H2 `##` )을 읽어와 기본 설명(description)으로 설정하고, 제목이 없는 경우 "원본 문서 자료"를 기본값으로 사용해줘.
    - **인덱스 작성**: 아래 포맷에 맞춰 폴더 하위에 `_index.md` 파일을 작성/덮어쓰기 해줘.
        
        ```markdown
        # {폴더이름} 소스 인덱스
        
        이 폴더는 {폴더이름} 관련 원본 문서들을 모아놓은 디렉토리입니다.
        
        ## 소스 파일 목록
        - [[파일명1.md]] — 기존 보존된 설명 또는 첫 번째 제목
        - [[파일명2.md]] — 기존 보존된 설명 또는 첫 번째 제목
        
        ## 관련 위키 페이지
        *아직 인제스트되지 않았습니다. wiki-ingest를 실행하여 지식을 wiki로 변환하세요.*
        ```
        
3. **마스터 인덱스(`_sources/_index.md`) 자동 업데이트**
    - 하위 폴더 인덱스를 만들고 나면, 상위 디렉토리의 마스터 인덱스 파일(`_sources/_index.md`)을 읽어서 해당 폴더의 등록 여부를 검사해.
    - 만약 마스터 인덱스 내에 `[[폴더명/_index.md` 링크가 없다면, `## 주제별 폴더 목록` 헤더 하위에 다음과 같은 형식으로 링크를 자동으로 삽입해줘.
    `[[폴더명/_index.md|폴더명]] — 폴더명 관련 매뉴얼 및 문서 자료`
4. **실행 방식 및 매개변수 지원**
    - 명령줄 파라미터(sys.argv 또는 argparse)를 지원하여 다음과 같이 구동할 수 있어야 해:
        - `python3 scripts/generate_index.py` (전체 소스 폴더 일괄 처리)
        - `python3 scripts/generate_index.py "특정폴더명"` (지정한 폴더 하나만 타겟으로 처리)
    - 파일 경로에 한글과 공백이 포함될 수 있으므로, 파일 입출력 및 OS 경로 처리 시 유니코드 경로 에러가 나지 않도록 안전하게 처리해줘.
```

**5. 인덱스 생성 명령어(Skill) 등록**
스크립트가 완성되면 아래 명령을 입력하여 재사용 가능한 툴로 만듭니다.
> "이것을 skill로 만들어서 '/wiki-ingest'와 같은 형식의 명령으로 작동할 수 있도록 해줘. 명령어는 'generate-index'로 해줘."

---

## 5. 핵심 작업 흐름 요약 (7-Step Workflow)

위키 시스템 구축이 완료되면 일상적으로 아래 7단계를 거치게 됩니다.

1. **입력 (파일 클리핑):** 
   - 영구 보관용(PDF, 논문, 매뉴얼)은 `_sources/` 폴더에 복사.
   - 일회성 아이디어나 클립보드 복사는 `_raw/` 폴더에 드롭.
2. **Ingest 실행:** 
   - IDE 채팅창에 `/wiki-ingest` 입력. AI가 `.manifest.json`을 읽고 새 파일(Delta)만 골라냅니다.
3. **내부 처리:** 
   - Ingest(읽기) ➔ Extract(개념/인물 추출) ➔ Resolve(기존 문서 병합) ➔ Schema(링크 및 목차 정리) 순서로 자동 진행.
4. **결과물 분류:** 
   - 추출된 지식은 `concepts/`, `entities/`, `skills/`, `references/`, `journal/` 등의 적합한 서브 폴더로 쪼개져 저장됩니다.
5. **부수 기록 자동 갱신:** 
   - `index.md`, `log.md` 등 시스템 파일이 최신 상태로 유지됩니다.
6. **원본 파일 처리:** 
   - `_sources/`에 둔 원본은 보존되고, `_raw/`에 두었던 임시 파일은 지식으로 승격된 뒤 삭제됩니다.
7. **결과 확인:** 
   - 옵시디언 그래프 뷰를 통해 문서 간의 유기적 연결망(Link)을 시각적으로 탐험할 수 있습니다.

---

## 6. 못다한 이야기: AI 활용 팁 (마케팅 및 자동화)

* **행동하는 AI (Action-oriented AI):** 단순 질의응답을 넘어 브라우저를 띄워 행동하는 AI. (예: Perplexity + Comet 툴 조합)
* **반복 업무 자동화 (바이브 코딩):** "지난 2주간 뉴스 모아서 PPT 요약해줘" 같은 정형화된 업무를 스킬(Skill)로 묶고 주기적으로 실행되도록 스케줄링.
* **나만의 브랜드 만들기 (SSG):** 코딩 없이도 AI에게 `Hugo` 같은 정적 사이트 생성을 명령하여 연 $12로 강력한 개인 브랜드 허브 구축. 
* **구독(Subscribe) 자동화:** 매번 정보를 검색하지 말고, 양질의 유튜브나 뉴스레터를 AI가 읽고 요약해 내 위키에 밀어넣어주는(Push) 시스템 구축.

---

## 📚 참고 링크 모음

**필수 프로그램 및 리소스**
* [옵시디언 (Obsidian)](https://obsidian.md/)
* [옵시디언 웹 클리퍼 (Chrome Extension)](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf)
* [안티그래비티 IDE (Antigravity IDE)](https://antigravity.google/)
* [AR9AV Obsidian-Wiki 리포지토리](https://github.com/AR9AV/obsidian-wiki)
* [JIWU Mission 블로그 원문](https://jesusiswith.us/class/llm-wiki/obsidian-llm-wiki-%EC%B4%88%EB%B3%B4%EC%9E%90-%EC%84%A4%EC%B9%98%EB%B6%80%ED%84%B0-%EC%82%AC%EC%9A%A9%EA%B9%8C%EC%A7%80/)
