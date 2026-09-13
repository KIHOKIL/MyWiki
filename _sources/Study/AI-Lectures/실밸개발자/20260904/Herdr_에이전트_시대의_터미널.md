---
title: "에이전트 시대의 터미널 Herdr | 메타 시니어 엔지니어가 잘때도 에이전트를 돌리는 법"
category: "AI-Lectures"
tags: ["Herdr", "Terminal-Multiplexer", "AI-Agent", "Claude-Code", "Developer-Tools", "tmux"]
sources: ["https://www.youtube.com/watch?v=U9AConAimzM"]
created: "2026-09-13"
updated: "2026-09-13"
---

# 에이전트 시대의 터미널 Herdr

## 💡 Executive Summary
**AI 에이전트 다중 구동 시대의 필수 인프라: 에이전트를 이해하는 터미널 멀티플렉서**

과거에는 `tmux`가 개발자의 화면 분할 및 백그라운드 세션 유지를 위해 쓰였다면, 이제는 여러 개의 코딩 에이전트(예: Claude Code, Codex 등)를 동시에 띄워놓고 작업을 지시하는 '다중 에이전트 오케스트레이션' 시대입니다. 

에이전트를 2~3개씩 띄우다 보면, 어떤 에이전트가 승인을 기다리고 있고 어떤 에이전트가 작업 중인지 파악하기 힘들어 **'병목은 인간'**이 되는 현상이 발생합니다. 

**Herdr**는 기존 `tmux`의 서버-클라이언트 아키텍처(세션 유지)를 그대로 계승하면서도, **터미널 내부에서 구동 중인 AI 에이전트의 상태(Working, Blocked, Done)를 실시간으로 인식하고 알림을 주는 오픈소스 도구**입니다. 이를 통해 딥 다이브 중인 엔지니어는 에이전트의 작업 승인 대기 상태를 놓치지 않고, 에이전트 런타임 환경을 완벽하게 통제할 수 있습니다.

---

## 🛠️ Zero-Loss Detailed Summary (타임라인 기반 핵심 큐레이션)

### Part 1. 터미널 멀티플렉서의 귀환과 한계
- **터미널 멀티플렉서란?**: 터미널 창을 분할하고 묶어주며, 터미널 창을 닫아도 프로세스를 살려두는 **서버-클라이언트 3층 구조**.
- **에이전트 시대의 재부상**: 코딩 에이전트가 내가 보지 않는 동안에도 백그라운드에서 오랫동안 동작해야 하므로 20년 된 `tmux`가 다시 필수품이 됨.
- **`tmux`의 한계**: `pane` 안에서 실행 중인 프로세스가 봇인지, 빌드인지 알지 못하므로 에이전트가 "승인 대기" 중이어도 사용자가 화면을 보지 않으면 진행되지 않음.

### Part 2. Herdr - 에이전트 상태를 아는 터미널
- **Herdr의 정체성**: "The runtime your coding agents live on". 단순 터미널이 아니라 에이전트의 생태계이자 런타임.
- **tmux와 같은 점**: 서버-클라이언트 구조, Detach/Attach 지원, `ctrl+b` Prefix 키 사용.
- **tmux와 다른 3가지 핵심 강점**:
  1. **에이전트 상태 인식**: 사이드바를 통해 5가지 상태(blocked, working, done, idle, unknown)를 직관적으로 표시.
  2. **에이전트 주도 조작**: 에이전트가 명령 한 줄로 Herdr의 탭과 Pane을 스스로 쪼개고 조작할 수 있음. (`herdr --skill`)
  3. **세션 복원력**: 터미널이나 서버를 닫았다가 켜도 `claude --resume` 등을 통해 에이전트의 대화 맥락이 온전히 복원됨.

### Part 3. Herdr를 활용한 실무 파이프라인 (AutoKliq 개발기)
- **오케스트레이터의 등장**: 한 Claude Code 에이전트에게 지시하면, 해당 에이전트가 `herdr` 스킬을 사용하여 직접 `worktree`를 파고 새로운 `pane`을 3개 띄워 각각 독립된 에이전트들을 기동함.
- **비동기 협업 모델**: 한 에이전트가 막혀서 `Blocked` 알림을 띄우면, 다른 에이전트의 작업을 방해하지 않고 알림을 클릭해 승인만 처리(`herdr agent read`).
- **결과 취합 및 리뷰**: 작업이 끝나면 코드를 병합(npm run check/test) 후 자동 PR을 생성하고, Codex 리뷰어를 붙이는 일련의 자동화.

---

## 🔬 Agentic Engineering Analysis
### Herdr vs 기존 도구 (tmux, cmux, Warp, Conductor)
- **Warp / Conductor**: 모던 터미널 기반의 AI 기능 통합 도구들이나, "보고 있던 화면(클라이언트)이 꺼지면 에이전트도 죽는가?"라는 치명적 질문에 대해 Herdr는 명확한 해답(서버 아키텍처)을 제공.
- **cmux**: 유사한 접근이나, 에이전트의 상태를 네이티브로 파악하고 관리하는 사이드바 및 상태 머신(5 state) 통합은 Herdr가 압도적.
- **아키텍처 인사이트**: Herdr는 인간을 위한 UI가 아니라, **에이전트가 살아가고 스스로 화면을 통제하는 '가상 OS(런타임)'**라는 철학적 전환을 보여줌.

---

## 🎯 Next Action & Deep Research (모바일 SW 리더 페르소나 적용)

### 1. 실무 도입 실험: Legacy C/C++ 리팩토링 자동화 파이프라인
레거시 통신 프로토콜 코드 분석 및 하드웨어 레지스터 맵 정리에 다중 에이전트를 투입할 때 Herdr를 도입해 봅니다.
- **설계**: `Master Agent` (전체 아키텍처 파악) -> `herdr` 스킬 호출 -> `Sub Agent 1` (헤더 파일 추출), `Sub Agent 2` (레지스터 맵 파싱) 각각 독립된 Pane에서 백그라운드 실행.
- **이점**: 빌드 및 분석 시간이 오래 걸리는 C/C++ 프로젝트 특성상, 에이전트가 빌드 에러를 만나 `Blocked` 상태가 되면 리더가 즉시 사이드바 알림을 보고 방향성만 컨펌해주는 비동기 최적화 워크플로우 완성.

### 2. 추천 리서치 링크 (Deep Dive)
- **Herdr 공식 사이트**: [https://herdr.dev/](https://herdr.dev/)
- **Quick Start (설치 및 통합 가이드)**: [https://herdr.dev/docs/quick-start/](https://herdr.dev/docs/quick-start/)
- **블로그 (Coding agents are becoming runtimes)**: [https://herdr.dev/blog/coding-agents-are-becoming-runtimes/](https://herdr.dev/blog/coding-agents-are-becoming-runtimes/)
- **에이전트 개발 도구 모음**: AutoKliq ([https://autokliq.com](https://autokliq.com))
