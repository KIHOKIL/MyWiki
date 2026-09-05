---
title: OpenHuman
category: entities
tags:
  - openhuman
  - open-source
  - rust
  - tauri
  - agentic-ai
  - local-first
  - memory-tree
  - context-compression
  - obsidian-compatible
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260905/github-trend-2026-09-05.md]]"
  - "https://github.com/tinyhumansai/openhuman"
  - "https://tinyhumans.ai/openhuman"
  - "https://www.elancer.co.kr/blog/detail/1111"
  - "https://honbul.tistory.com/266"
created: "2026-09-05"
updated: "2026-09-05"
summary: 이메일, 메신저, Jira, Confluence, GitHub 등 118개 이상의 업무 도구 데이터를 20분 주기로 자동 수집하여 로컬 SQLite 및 Obsidian 호환 Markdown 볼트에 영구 저장하고, TokenJuice 압축 레이어를 거쳐 LLM 에이전트와 연동하는 Rust/Tauri 기반 오픈소스 개인용 AI 에이전트 허브.
base_confidence: 0.98
lifecycle: reviewed
tier: core
relationships:
  - target: "[[concepts/active-second-brain]]"
    type: implements
  - target: "[[concepts/2nd-brain-system-design-blueprint]]"
    type: implements
  - target: "[[concepts/context-compression]]"
    type: implements
---

# OpenHuman

## 📌 개요
**OpenHuman**은 TinyHumans AI에서 개발한 오픈소스(GPL-3.0) 개인 AI 에이전트 허브([github.com/tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman))입니다. 
사용자의 일상적인 업무 도구(Gmail, Slack, Jira, Confluence, Notion, GitHub 등)와 연결하여 업무 맥락을 지속적으로 학습하고 로컬에 영구 보관합니다. 

단순한 일회성 챗봇(Chatbot)이 아니라, 사용자의 컴퓨터 안에서 상주하며 맥락을 기억하고 도구를 자율적으로 실행하는 **"로컬 우선 개인 AI 슈퍼 인텔리전스(Personal AI Super Intelligence)"**를 지향합니다.

- **라이선스:** GPL-3.0
- **개발 언어 및 기술 스택:** Rust (백엔드 코어), TypeScript & React (프론트엔드), Tauri (초경량 데스크톱 런타임)
- **지원 OS:** macOS (Apple Silicon / Intel), Windows (x64 exe / msi), Linux (AppImage)
- **GitHub Stars:** 37,000+ (공개 직후 급상승)

---

## 🏛️ 핵심 아키텍처 및 동작 원리

```mermaid
flowchart TD
    subgraph ExternalSources [외부 협업/업무 플랫폼]
        Gmail[Gmail / Outlook]
        Slack[Slack / Discord / Teams]
        Jira[Jira / Confluence / Notion]
        Git[GitHub / GitLab]
    end

    subgraph OpenHumanDaemon [백그라운드 동기화 엔진]
        OAuth[118+ 커넥터 & One-Click OAuth]
        AutoFetch[Auto-Fetch: 20분 주기 자동 동기화]
    end

    ExternalSources -->|API / OAuth| OAuth
    OAuth --> AutoFetch

    subgraph LocalStorage [Local-First 영구 메모리 계층]
        AutoFetch --> MemoryTree[(Memory Tree: SQLite)]
        AutoFetch --> ObsVault[(Obsidian 호환 Markdown 볼트)]
    end

    subgraph Optimization [컨텍스트 최적화 계층]
        MemoryTree --> TokenJuice[TokenJuice 압축 레이어<br>노이즈 제거, 토큰 70~80% 절감]
        ObsVault --> TokenJuice
    end

    subgraph Interaction [프론트엔드 및 실행 계층]
        TokenJuice --> AgentOrchestrator[에이전트 오케스트레이터]
        AgentOrchestrator <--> LLM[LLM 엔진: 로컬 Ollama / 클라우드 API]
        AgentOrchestrator <--> DesktopUI[초고속 검색 UI & 음성 마스코트]
    end
```

### 1. 로컬 우선 메모리 구조 (Local-First Memory Tree)
- 모든 수집 데이터는 외부 클라우드가 아닌 사용자 PC 로컬의 **SQLite(구조화 메타데이터 및 검색 인덱스)**와 **Obsidian 호환 Markdown 볼트(Memory Tree)** 형태로 저장됩니다.
- 에이전트가 사용하는 메모리를 사람이 직접 파일로 열람하고 편집·수정할 수 있어, 환각이나 잘못된 기억을 사용자가 직접 통제할 수 있습니다.

### 2. 118개 이상의 원클릭 통합 & 20분 주기 자동 수집 (Auto-fetch)
- Composio 커넥터 레이어를 채택하여 복잡한 API Key 발급 없이 **원클릭 OAuth**로 Gmail, Slack, Jira, Confluence, Teams, GitHub 등을 연결합니다.
- 사용자가 일일이 명령하지 않아도 **20분마다 백그라운드에서 새로운 메일, 댓글, 티켓, 커밋을 자동 수집(Auto-fetch)**하여 최신 컨텍스트를 유지합니다.

### 3. TokenJuice (스마트 토큰 압축 레이어)
- HTML 태그, 메일 서명, 슬랙 보일러플레이트 등의 불필요한 노이즈를 제거하고 Markdown으로 변환하여 모델에 전달되는 토큰 양을 최대 **70%~80%까지 절감**합니다.
- 이는 [[entities/headroom|Headroom]]과 동일한 문제의식을 해결하는 기술로, LLM 비용 절감과 응답 지연 시간 단축, 어텐션 집중도 극대화를 달성합니다.

### 4. 내장 에이전트 도구군
- 웹 검색 및 스크래퍼, 파일 시스템 및 Git/테스트 제어, 크론 스케줄링, 서브 에이전트 생성, 음성 입출력(STT/TTS)을 기본 지원합니다.
- Google Meet 회의에 참가자로 들어가 대화 내용을 실시간 전사(Transcription)하여 메모리에 기록하는 기능도 내장되어 있습니다.

---

## 💡 능동형 세컨드 브레인([[concepts/active-second-brain|Active Second Brain]])과의 연계 가치

1. **파편화된 워크스페이스 데이터의 중앙 집결지:**
   - 개인 지식 노트(MyWiki) 외에 업무 현장에서 실시간으로 쏟아지는 Email, Slack, Jira 로그를 로컬 마크다운으로 추출해 주므로, 세컨드 브레인의 **Phase 1 Ingestion 레이어**를 완벽하게 담당할 수 있습니다.
2. **Obsidian 상호 운용성:**
   - 수집된 메모리가 옵시디언 표준 마크다운 구조이므로, MyWiki의 Graph RAG 및 [[concepts/2nd-brain-system-design-blueprint|2nd Brain Blueprint]]와 아무런 장벽 없이 결합될 수 있습니다.

---

## 🔗 연관 지식 / 문서
- 연관 개념: [[concepts/active-second-brain|Active Second Brain]], [[concepts/2nd-brain-system-design-blueprint|2nd Brain System Design Blueprint]], [[concepts/context-compression|Context Compression]]
- 유사/연계 도구: [[entities/headroom|Headroom]], [[entities/firefly-iii|Firefly III]], [[entities/neo4j|Neo4j]]
- 소스 링크:
  - [공식 웹사이트](https://tinyhumans.ai/openhuman)
  - [GitHub 저장소](https://github.com/tinyhumansai/openhuman)
  - [이랜서 블로그 분석 가이드](https://www.elancer.co.kr/blog/detail/1111)
  - [Honbul 컴퓨터 블로그 리뷰](https://honbul.tistory.com/266)
