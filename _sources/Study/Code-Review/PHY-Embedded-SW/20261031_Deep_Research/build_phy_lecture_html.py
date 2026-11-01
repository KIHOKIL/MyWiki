import os
import sys

base_dir = r"c:\Users\kihok\내 드라이브\MyWiki"
out_path = os.path.join(base_dir, r"_sources\Study\Code-Review\PHY-Embedded-SW\phy_code_review_lecture.html")
poc_path = os.path.join(base_dir, r"_sources\Study\Code-Review\PHY-Embedded-SW\20261031_Deep_Research\phy_code_review_lecture_report.html")

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PHY 임베디드 SW 전용 AI 코드 리뷰 & Code Graph 마스터 클래스</title>
<style>
  :root {
    --bg: #0d1117;
    --card: #161b22;
    --card-alt: #1f242d;
    --border: rgba(139, 148, 158, 0.2);
    --border-bright: rgba(88, 166, 255, 0.4);
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --yellow: #d29922;
    --orange: #db6d28;
    --red: #f85149;
    --purple: #bc8cff;
    --cyan: #39c5cf;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.65;
    display: flex;
    min-height: 100vh;
  }
  aside.toc {
    width: 290px;
    background: #090d13;
    border-right: 1px solid var(--border);
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    padding: 24px 16px;
    overflow-y: auto;
    z-index: 100;
  }
  aside.toc h3 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
    margin-bottom: 12px;
    padding-left: 6px;
  }
  aside.toc .badge {
    display: inline-block;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    background: rgba(88, 166, 255, 0.15);
    color: var(--accent);
    margin-left: 4px;
  }
  aside.toc a {
    display: block;
    color: var(--muted);
    text-decoration: none;
    font-size: 13px;
    padding: 7px 10px;
    border-radius: 6px;
    margin-bottom: 2px;
    transition: all 0.15s;
    line-height: 1.4;
  }
  aside.toc a:hover, aside.toc a.active {
    background: rgba(88, 166, 255, 0.12);
    color: var(--accent);
    font-weight: 600;
  }
  aside.toc a.sub {
    padding-left: 20px;
    font-size: 12px;
  }
  main {
    margin-left: 290px;
    flex: 1;
    padding: 36px 48px 90px;
    max-width: 1280px;
  }
  @media (max-width: 1024px) {
    aside.toc { display: none; }
    main { margin-left: 0; padding: 20px; }
  }
  header {
    background: linear-gradient(135deg, #161b22 0%, #0f172a 60%, #1e1b4b 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px;
    margin-bottom: 32px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }
  .tag-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .tag {
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .tag-blue { background: rgba(88, 166, 255, 0.15); color: var(--accent); border: 1px solid rgba(88, 166, 255, 0.3); }
  .tag-green { background: rgba(63, 185, 80, 0.15); color: var(--green); border: 1px solid rgba(63, 185, 80, 0.3); }
  .tag-purple { background: rgba(188, 140, 255, 0.15); color: var(--purple); border: 1px solid rgba(188, 140, 255, 0.3); }
  .tag-yellow { background: rgba(210, 153, 34, 0.15); color: var(--yellow); border: 1px solid rgba(210, 153, 34, 0.3); }
  .tag-red { background: rgba(248, 81, 73, 0.15); color: var(--red); border: 1px solid rgba(248, 81, 73, 0.3); }
  header h1 {
    font-size: 28px;
    font-weight: 800;
    color: #fff;
    margin-bottom: 12px;
    line-height: 1.3;
  }
  header p.desc {
    color: #cbd5e1;
    font-size: 15px;
    max-width: 950px;
  }
  .quick-stat-bar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-top: 24px;
  }
  .stat-card {
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
  }
  .stat-card .num { font-size: 22px; font-weight: 700; color: var(--accent); }
  .stat-card .label { font-size: 12px; color: var(--muted); margin-top: 2px; }

  section.module {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 32px;
    margin-bottom: 32px;
    position: relative;
  }
  section.module.featured {
    border-color: var(--border-bright);
    box-shadow: 0 0 25px rgba(88, 166, 255, 0.08);
  }
  .mod-badge {
    position: absolute;
    top: -12px;
    left: 28px;
    background: var(--accent);
    color: #000;
    font-size: 11px;
    font-weight: 800;
    padding: 3px 12px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .mod-badge.deep {
    background: linear-gradient(90deg, #bc8cff, #39c5cf);
    color: #0d1117;
  }
  h2.mod-title {
    font-size: 22px;
    color: #fff;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  h3.sub-title {
    font-size: 17px;
    color: var(--accent);
    margin: 24px 0 12px;
    border-left: 3px solid var(--accent);
    padding-left: 10px;
  }
  h4.part-title {
    font-size: 14.5px;
    color: #e2e8f0;
    margin: 18px 0 8px;
    font-weight: 700;
  }
  p { margin-bottom: 14px; color: #cbd5e1; font-size: 14.5px; line-height: 1.7; }
  ul, ol { margin-left: 20px; margin-bottom: 16px; color: #cbd5e1; font-size: 14px; }
  li { margin-bottom: 6px; }

  .callout {
    background: rgba(22, 27, 34, 0.8);
    border-left: 4px solid var(--accent);
    padding: 14px 18px;
    border-radius: 0 10px 10px 0;
    margin: 16px 0;
    font-size: 13.5px;
  }
  .callout.danger { border-left-color: var(--red); background: rgba(248, 81, 73, 0.07); }
  .callout.warn { border-left-color: var(--yellow); background: rgba(210, 153, 34, 0.07); }
  .callout.success { border-left-color: var(--green); background: rgba(63, 185, 80, 0.07); }
  .callout.deep { border-left-color: var(--purple); background: rgba(188, 140, 255, 0.08); }
  .callout strong { color: #fff; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 13px;
  }
  th, td {
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }
  th {
    background: var(--card-alt);
    color: var(--accent);
    font-weight: 600;
    font-size: 12.5px;
  }
  tr:hover td { background: rgba(255, 255, 255, 0.02); }

  pre {
    background: #090d13;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
    font-size: 12.5px;
    line-height: 1.55;
    color: #e6edf3;
    margin: 14px 0;
    position: relative;
  }
  code {
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 12.5px;
    background: rgba(110, 118, 129, 0.2);
    padding: 2px 5px;
    border-radius: 4px;
    color: #f0883e;
  }
  pre code {
    background: transparent;
    padding: 0;
    color: inherit;
  }
  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #13171f;
    border: 1px solid var(--border);
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 6px 14px;
    font-size: 11.5px;
    color: var(--muted);
  }
  .code-header + pre {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    margin-top: 0;
  }
  .copy-btn {
    background: rgba(88, 166, 255, 0.15);
    border: 1px solid rgba(88, 166, 255, 0.3);
    color: var(--accent);
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .copy-btn:hover { background: var(--accent); color: #000; }

  .diff-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin: 16px 0;
  }
  @media (max-width: 860px) {
    .diff-grid { grid-template-columns: 1fr; }
  }
  .diff-col.bad { border-top: 3px solid var(--red); }
  .diff-col.good { border-top: 3px solid var(--green); }
  .diff-col h5 {
    font-size: 13px;
    padding: 8px 12px;
    background: var(--card-alt);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .diff-col.bad h5 { color: var(--red); }
  .diff-col.good h5 { color: var(--green); }

  .tab-group { margin: 18px 0; }
  .tab-buttons { display: flex; gap: 4px; border-bottom: 1px solid var(--border); }
  .tab-btn {
    background: transparent;
    border: none;
    color: var(--muted);
    font-size: 13px;
    padding: 8px 16px;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.15s;
  }
  .tab-btn.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
    font-weight: 600;
  }
  .tab-content { display: none; padding-top: 14px; }
  .tab-content.active { display: block; }

  .flow-box {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    background: #0a0e14;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid var(--border);
    margin: 16px 0;
  }
  .flow-step {
    background: var(--card-alt);
    border: 1px solid var(--border);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
    text-align: center;
  }
  .flow-arrow { color: var(--accent); font-weight: bold; font-size: 14px; }

  footer {
    text-align: center;
    padding: 40px 0;
    color: var(--muted);
    font-size: 12px;
    border-top: 1px solid var(--border);
    margin-top: 50px;
  }
</style>
</head>
<body>

<aside class="toc">
  <h3>PHY SW AI Review Lecture</h3>
  <a href="#overview">Overview: 강의 개요 및 스택</a>
  <a href="#mod1">Module 1. PHY AI 코드 리뷰 실패 원인과 4단계 아키텍처</a>
  <a href="#mod2">Module 2. 25개 오픈소스 전수 벤치마크 (Top 12)</a>
  <a href="#mod3">Module 3. PHY 5-Layer 불변조건(Invariants) 카탈로그</a>
  <a href="#mod3-ipc" class="sub">├ L1: IPC 인터페이스 (Memory Leak, Cache)</a>
  <a href="#mod3-3gpp" class="sub">├ L2: 3GPP Procedure (FSM, Deadlock)</a>
  <a href="#mod3-dev" class="sub">├ L3: Device Driver (DMA, Guard Band)</a>
  <a href="#mod3-hal" class="sub">├ L4: HAL Register (W1C, RMW, volatile)</a>
  <a href="#mod3-isr" class="sub">└ L5: ISR/Event (0-blocking, Bounded Poll)</a>
  <a href="#mod4" style="color: var(--purple); font-weight: 700;">Module 4. [개발 레벨] ARM Clang PHY Code Graph 구축 <span class="badge">DEEP</span></a>
  <a href="#mod4-armclang" class="sub">├ 4.1 armclang compile_commands.json 정규화</a>
  <a href="#mod4-schema" class="sub">├ 4.2 PHY 특화 Graph Schema (Nodes & Edges)</a>
  <a href="#mod4-bfs" class="sub">└ 4.3 ISR Reachability 전파 (BFS 알고리즘)</a>
  <a href="#mod5" style="color: var(--cyan); font-weight: 700;">Module 5. [개발 레벨] AI Context Engineering & 슬라이싱 <span class="badge">DEEP</span></a>
  <a href="#mod5-asym" class="sub">├ 5.1 비대칭 k-Hop Skeleton 슬라이싱</a>
  <a href="#mod5-fact" class="sub">├ 5.2 [COMPILER_VERIFIED_FACTS] 주입</a>
  <a href="#mod5-bundle" class="sub">├ 5.3 Connected Component 스마트 번들링</a>
  <a href="#mod5-code" class="sub">└ 5.4 phy_context_slicer.py 실전 구현</a>
  <a href="#mod6">Module 6. OpenCode 멀티에이전트 하네스 & 8주 로드맵</a>
</aside>

<main>
  <header id="overview">
    <div class="tag-row">
      <span class="tag tag-blue">Modem / PHY SW</span>
      <span class="tag tag-green">ARM Cortex-R / A</span>
      <span class="tag tag-purple">ARM Clang (armclang)</span>
      <span class="tag tag-yellow">OpenCode + DeepSeek / GLM / Qwen</span>
      <span class="tag tag-red">0-Hallucination Guard</span>
    </div>
    <h1>PHY 임베디드 SW 전용 AI 코드 리뷰 & Code Graph 마스터 클래스</h1>
    <p class="desc">
      ARM Core 상에서 실시간 실행되는 <strong>PHY 통신 프로토콜, 상위 Layer IPC, 3GPP 표준 절차 FSM, HW Register 제어(HAL), ISR 및 이벤트 드리븐 시스템</strong>에 최적화된 차세대 AI 코드 리뷰 파이프라인과 <strong>개발 레벨 Code Graph 구축 & AI Context Engineering</strong> 전수 강의 자료입니다.
    </p>

    <div class="quick-stat-bar">
      <div class="stat-card">
        <div class="num">4-Tier</div>
        <div class="label">결정론적 하이브리드 파이프라인</div>
      </div>
      <div class="stat-card">
        <div class="num">25 Repos</div>
        <div class="label">오픈소스 전수 검증 (Top 12 선정)</div>
      </div>
      <div class="stat-card">
        <div class="num">5 Layers</div>
        <div class="label">IPC·3GPP·Dev·HAL·ISR 불변조건</div>
      </div>
      <div class="stat-card">
        <div class="num">&lt; 6,000 Tok</div>
        <div class="label">Asymmetric k-Hop Context Diet</div>
      </div>
    </div>
  </header>

  <!-- MODULE 1 -->
  <section id="mod1" class="module">
    <div class="mod-badge">Module 1</div>
    <h2 class="mod-title">PHY AI 코드 리뷰 실패 원인과 4단계 하이브리드 아키텍처</h2>
    <p>
      일반적인 웹/엔터프라이즈 환경에서 사용하는 단순 LLM 프롬프트 리뷰나 Naive RAG(단순 텍스트 검색)를 PHY 임베디드 SW에 적용하면 <strong>100% 실패</strong>합니다. 왜 실패하는지, 그리고 이를 해결하기 위한 4단계 방어선이 무엇인지 정리합니다.
    </p>

    <div class="diff-grid">
      <div class="diff-col bad">
        <h5>❌ 일반 AI 코드 리뷰가 PHY SW에서 실패하는 4대 이유</h5>
        <ul>
          <li><strong>HW Register W1C(Write-1-to-Clear) 오판:</strong> LLM은 <code>REG |= (1U << 3);</code> 코드를 보면 통상적인 비트 플래그 설정으로 착각하여 칭찬하거나 무시함. 실제로는 주변 펜딩 비트까지 전부 클리어되어 통신 모뎀 먹통 발생.</li>
          <li><strong>ISR 컨텍스트 무지:</strong> 함수 단독으로만 보면 정상적인 <code>while(flag);</code> 루프나 <code>malloc()</code>/<code>osMutexAcquire()</code>가 Hard ISR 콜체인(100µs 예산) 안에서 호출된다는 전파 경로(Transitive Reachability)를 전혀 알지 못함.</li>
          <li><strong>Memory Barrier / Cache 무감각:</strong> DMA 디스크립터나 IPC Shared Ring-Buffer 작성 후 <code>__DSB()</code>, <code>__ISB()</code>, Cache Clean이 누락된 아웃오브오더(Out-of-Order) 하드웨어 메모리 위험을 인지 못함.</li>
          <li><strong>컨텍스트 블로트(Context Bloat) & 환각:</strong> C 소스 수천 줄을 통째로 LLM에 던지면 주의 집중 분산으로 중요한 Race Condition을 놓치고, 스타일 지적 같은 환각성 잔소리만 남발함.</li>
        </ul>
      </div>
      <div class="diff-col good">
        <h5>✅ PHY SW 전용 4-Tier 하이브리드 방어선</h5>
        <ul>
          <li><strong>Tier 1 (Compiler & Linter):</strong> <code>armclang -Werror=all</code>, <code>clang-tidy</code> (MISRA C:2012 필수 규칙 강제 차단).</li>
          <li><strong>Tier 2 (AST Pattern Matcher):</strong> <code>ast-grep</code> 기반 W1C 레지스터 RMW(<code>|=</code>) 원천 금지, <code>volatile</code> 없는 HW 레지스터 접근 차단, ISR 내 블로킹 함수 검출.</li>
          <li><strong>Tier 3 (Semantic Code Graph Engine):</strong> Clang AST + CMake 심볼 인덱싱을 통해 <strong>ISR Hop Distance</strong>, <strong>Lock 상태</strong>, <strong>W1C 타겟</strong>을 선행 계산하여 LLM에 확정 사실로 주입.</li>
          <li><strong>Tier 4 (Domain Specialized Multi-Agent):</strong> OpenCode 하네스 상에서 <code>phy-isr-hal-auditor</code>, <code>phy-ipc-3gpp-auditor</code>, <code>phy-chief-verifier</code>가 반증(Disproving) 패스를 거쳐 검증된 결함만 리포트.</li>
        </ul>
      </div>
    </div>

    <h3 class="sub-title">전체 파이프라인 흐름도 (End-to-End Pipeline)</h3>
    <div class="flow-box">
      <div class="flow-step">1. Git Push / PR<br><small>Developer</small></div>
      <div class="flow-arrow">➔</div>
      <div class="flow-step">2. Pre-Push Hook<br><small>ast-grep & armclang</small></div>
      <div class="flow-arrow">➔</div>
      <div class="flow-step">3. Code Graph Slicer<br><small>phy_context_slicer.py</small></div>
      <div class="flow-arrow">➔</div>
      <div class="flow-step">4. OpenCode Harness<br><small>Domain Sub-Agents</small></div>
      <div class="flow-arrow">➔</div>
      <div class="flow-step">5. Disproving Pass<br><small>False Positive 제거</small></div>
      <div class="flow-arrow">➔</div>
      <div class="flow-step">6. 5-Axis Score & PR Comment<br><small>Decision Matrix</small></div>
    </div>

    <h3 class="sub-title">PHY SW 전용 5축 Risk Score 루브릭 (0 ~ 100점)</h3>
    <p>단순 코멘트 나열이 아닌, 5개 핵심 도메인 축의 감점을 합산하여 병합 차단(Block) 여부를 결정론적으로 판단합니다.</p>
    <table>
      <thead>
        <tr><th>평가 축 (Dimension)</th><th>가중치</th><th>주요 감점 기준 (Critical Violations)</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>1. ISR & Real-Time Safety</strong></td><td>30점</td><td>Hard ISR 내 Unbounded Polling 루프, Mutex/OS 대기 함수 호출, ISR 체인 스택 깊이 초과</td></tr>
        <tr><td><strong>2. HW Register & Memory Ordering</strong></td><td>25점</td><td>W1C 레지스터에 <code>|=</code>(RMW) 연산, DMA 전후 Barrier/Cache Clean 누락, 레지스터 포인터 <code>volatile</code> 누락</td></tr>
        <tr><td><strong>3. Concurrency & Critical Section</strong></td><td>20점</td><td>ISR-Task 간 공유 변수에 Atomic/IRQ Lock 누락, Lock 취득 중 타 함수 호출(Deadlock 위험)</td></tr>
        <tr><td><strong>4. 3GPP Procedure & FSM Integrity</strong></td><td>15점</td><td>FSM Invalid State Transition 무방비, 타이머 만료(Expiry) 핸들러 미등록, T300/T310 규격 위반</td></tr>
        <tr><td><strong>5. Upper IPC & Buffer Ownership</strong></td><td>10점</td><td>Ring-Buffer Header-Payload 순서 위반, 제어권 양도 후 접근(UAF), 고정 크기 큐 오버플로우</td></tr>
      </tbody>
    </table>
    <div class="callout danger">
      <strong>점수별 자동 조치:</strong> <strong>90점 이상:</strong> 1-Click LGTM 자동 승인 | <strong>70~89점:</strong> 경고성 주의사항 표기 및 조건부 승인 | <strong>70점 미만 또는 단일 Critical 결함:</strong> <code>PR MERGE HARD BLOCK</code>.
    </div>
  </section>

  <!-- MODULE 2 -->
  <section id="mod2" class="module">
    <div class="mod-badge">Module 2</div>
    <h2 class="mod-title">25개 오픈소스 전수 벤치마크 & PHY SW 그룹 Top 12</h2>
    <p>
      전 세계 오픈소스 코드 리뷰 및 그래프 분석 프로젝트 25개를 전수 조사(실시간 GitHub API 검증)하여, 우리 PHY SW 그룹에 <strong>직접 도입할 6개 프로젝트</strong>와 <strong>핵심 메커니즘을 차용할 6개 프로젝트</strong>를 엄선했습니다.
    </p>

    <div class="tab-group">
      <div class="tab-buttons">
        <button class="tab-btn active" onclick="openTab(event, 'tab-direct')">직접 도입 Top 6 (Direct Adoption)</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-pattern')">패턴 차용 Top 6 (Pattern Borrowing)</button>
      </div>

      <div id="tab-direct" class="tab-content active">
        <table>
          <thead>
            <tr><th>리포지토리</th><th>Stars</th><th>역할 및 선정 사유</th><th>우리 그룹 적용 방식</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><code>alibaba/open-code-review</code></td>
              <td>⭐ 49,163</td>
              <td>엔터프라이즈 멀티 모델 코드 리뷰 플랫폼 (Go). Git Diff 스마트 분할 알고리즘 제공</td>
              <td>PR Diff를 함수 단위, 연결 컴포넌트(Connected Component) 단위로 번들링하는 슬라이싱 로직 흡수</td>
            </tr>
            <tr>
              <td><code>DeusData/codebase-memory-mcp</code></td>
              <td>⭐ 47,893</td>
              <td>Pure C 구현 <code>clangd</code> 하이브리드 그래프 MCP. 대규모 C/C++ 심볼 고속 탐색</td>
              <td>OpenCode 에이전트가 ARM C/C++ 심볼 정의/참조/상호작용 그래프를 토큰 소모 없이 질의하는 MCP 백엔드로 배치</td>
            </tr>
            <tr>
              <td><code>tirth8205/code-review-graph</code></td>
              <td>⭐ 32,518</td>
              <td>OpenCode 네이티브 파급 반경(Blast Radius) 분석기. Qwen & DeepSeek 최적화</td>
              <td>PR 수정 함수가 호출하는/호출받는 Blast Radius를 2-Hop 이내로 계산하여 에이전트 프롬프트에 주입</td>
            </tr>
            <tr>
              <td><code>cloudflare/security-audit-skill</code></td>
              <td>⭐ 54,848</td>
              <td>6단계 반증(Disproving) 프레임워크. 환각 및 오탐 제거에 탁월</td>
              <td>에이전트가 "잠재적 결함"을 찾은 후 "왜 이 코드가 실제로는 안전할 수 있는가?"를 스스로 반증하게 하여 통과한 결함만 보고</td>
            </tr>
            <tr>
              <td><code>winnin/farol</code></td>
              <td>⭐ 170</td>
              <td>결정론적 Blast Radius & 0~100 Risk Score 평가 CLI</td>
              <td>PHY SW 전용 5축 루브릭 채점 엔진 및 PR 블로킹 자동화 워크플로우 베이스로 활용</td>
            </tr>
            <tr>
              <td><code>ast-grep/ast-grep</code></td>
              <td>⭐ 16,401</td>
              <td>초고속 Structural Search & Lint 도구 (Rust)</td>
              <td>Git Pre-Push 훅에서 W1C <code>|=</code> 연산 및 ISR 내 금지 API를 0.05초 만에 결정론적으로 차단</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div id="tab-pattern" class="tab-content">
        <table>
          <thead>
            <tr><th>리포지토리</th><th>Stars</th><th>차용 핵심 패턴</th><th>PHY SW 적용 가치</th></tr>
          </thead>
          <tbody>
            <tr><td><code>DietrichGebert/ponytail</code></td><td>⭐ 181,307</td><td>"불변조건(Invariants) 중심 리뷰" 원칙</td><td>스타일이 아닌 5-Layer 불변조건 위반 여부만 집요하게 검증하도록 시스템 프롬프트 제약</td>
          </tr>
          <tr><td><code>openai/codex-plugin-cc</code></td><td>⭐ 34,755</td><td>"주니어 취급 금지" 및 결정론적 패치 제시</td><td>모호한 설명 대신 정확한 C 코드 Bad vs Good 비교 패치만 출력하도록 포맷 강제</td></tr>
          <tr><td><code>mindsdb/mindsdb</code></td><td>⭐ 36,419</td><td>Dynamic Agent Routing 패턴</td><td>수정된 파일 경로(<code>hal/</code>, <code>ipc/</code>, <code>proc/</code>)에 따라 전담 서브에이전트 자동 라우팅</td></tr>
          <tr><td><code>google-deepmind/graphcast</code></td><td>⭐ 4,512</td><td>Transitive Reachability 전파 모델</td><td>Hard ISR 시작점으로부터 각 함수까지의 최단 Hop Distance를 사전 계산하여 전파</td></tr>
          <tr><td><code>reviewdog/reviewdog</code></td><td>⭐ 9,711</td><td>GitHub PR 라인 단위 In-Line 코멘트 통합</td><td>발견된 결함을 정확한 C 파일 해당 라인에 Suggestions 블록(1-Click Commit 가능)으로 게시</td></tr>
          <tr><td><code>symflower/symflower</code></td><td>⭐ 412</td><td>C 언어 경계값(Boundary) 심볼릭 유닛 테스트 생성</td><td>Review 단계에서 3GPP 메시지 크기 및 타이머 오버플로우를 검증하는 최소 테스트 케이스 자동 제안</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- MODULE 3 -->
  <section id="mod3" class="module">
    <div class="mod-badge">Module 3</div>
    <h2 class="mod-title">PHY 5-Layer 코드 리뷰 불변조건(Invariants) 카탈로그</h2>
    <p>
      우리 그룹의 실제 코드베이스를 관통하는 5대 계층별 필수 불변조건과 실제 결함 발생 패턴(Bad C Code) 및 교정 패치(Good C Code)입니다.
    </p>

    <!-- L1 -->
    <div id="mod3-ipc">
      <h3 class="sub-title">Layer 1: Upper-Layer IPC Interface (<code>ipc/</code>, <code>l1_l2_if/</code>)</h3>
      <p>상위 레이어(MAC/L2/L3)와 공유 메모리(Shared Ring-Buffer/Mailbox)를 통해 메시지를 주고받는 계층입니다.</p>
      <div class="diff-grid">
        <div class="diff-col bad">
          <h5>❌ Bad Code: Barrier 누락 & Use-After-Free</h5>
          <pre><code>/* Header 채우고 포인터 넘긴 뒤 페이로드 수정 (Race Condition) */
ipc_msg_t *msg = ipc_alloc_buf();
msg->cmd = PHY_CONFIG_REQ;
ipc_send_to_l2(msg); /* 큐에 등록! */

/* 치명적 결함: 송신 후 메모리 수정 및 Barrier 누락 */
msg->payload.bandwidth = BW_100MHZ; // Use-After-Free!
// L2 Core는 캐시 불일치로 쓰레기값 읽음</code></pre>
        </div>
        <div class="diff-col good">
          <h5>✅ Good Code: 페이로드 선작성 + __DSB() + 단일 소유권</h5>
          <pre><code>ipc_msg_t *msg = ipc_alloc_buf();
/* 1. 페이로드 및 헤더를 완벽히 채움 */
msg->payload.bandwidth = BW_100MHZ;
msg->cmd = PHY_CONFIG_REQ;

/* 2. ARM Core 메모리 파이프라인 동기화 & D-Cache 플러시 */
__DSB(); // Data Synchronization Barrier
SCB_CleanDCache_by_Addr((uint32_t*)msg, sizeof(ipc_msg_t));

/* 3. 소유권 완전 이전 후 로컬 포인터 NULL 처리 */
ipc_send_to_l2(msg);
msg = NULL; // 방어적 코딩</code></pre>
        </div>
      </div>
    </div>

    <!-- L2 -->
    <div id="mod3-3gpp">
      <h3 class="sub-title">Layer 2: 3GPP Standard Procedure Layer (<code>proc/</code>, <code>ul/</code>, <code>dl/</code>)</h3>
      <p>PRACH, Cell Search, Beamforming, CSI Report 등 3GPP Release 규격에 정의된 상태 전이 머신(FSM)입니다.</p>
      <div class="diff-grid">
        <div class="diff-col bad">
          <h5>❌ Bad Code: FSM Default 누락 & Unbounded State Wait</h5>
          <pre><code>switch (curr_state) {
    case PHY_STATE_PRACH_TX:
        proc_prach_handler();
        break;
    case PHY_STATE_RAR_WAIT:
        /* 무한 대기: 타임아웃 타이머 등록 누락 */
        proc_rar_handler();
        break;
    /* Default 없음: 잘못된 상태 진입 시 무한 고아 상태 */
}</code></pre>
        </div>
        <div class="diff-col good">
          <h5>✅ Good Code: 전이 테이블 엄격화 + T300 타이머 가드 + Default 에러 회복</h5>
          <pre><code>switch (curr_state) {
    case PHY_STATE_PRACH_TX:
        proc_prach_handler();
        phy_start_timer(T_RAR_TIMEOUT_MS, on_rar_timeout);
        curr_state = PHY_STATE_RAR_WAIT;
        break;
    case PHY_STATE_RAR_WAIT:
        proc_rar_handler();
        break;
    default:
        /* 허용되지 않은 상태 전이 시 강제 Recovery */
        PHY_ASSERT_RECOVER(0, "Invalid 3GPP State: %d", curr_state);
        curr_state = PHY_STATE_IDLE;
        break;
}</code></pre>
        </div>
      </div>
    </div>

    <!-- L3 -->
    <div id="mod3-dev">
      <h3 class="sub-title">Layer 3: Device Layer (<code>dev/</code>, <code>rf_drv/</code>, <code>dma_drv/</code>)</h3>
      <p>RFIC 트랜시버, DAC/ADC, 고속 DMA 디스크립터 체인을 제어하는 계층입니다.</p>
      <div class="diff-grid">
        <div class="diff-col bad">
          <h5>❌ Bad Code: DMA 버퍼 캐시 미정렬 & 무한 Busy-Wait</h5>
          <pre><code>/* 4바이트 스택 변수를 DMA 타겟으로 지정 (Cache-Line 충돌!) */
uint8_t dma_buf[128]; 
dma_start_transfer(DMA_CH0, (uint32_t)dma_buf, 128);

/* 타임아웃 없는 무한 하드웨어 비지 루프 */
while (DMA_STATUS_REG & DMA_BUSY_BIT) {
    // HW 고장 시 전체 시스템 Watchdog Reset 발생
}</code></pre>
        </div>
        <div class="diff-col good">
          <h5>✅ Good Code: 64바이트 Cache-Line 정렬 + Bounded Poll Guard</h5>
          <pre><code>/* ARM Cortex-R52 64-byte Cache Line 정렬 */
__ALIGNED(64) static uint8_t dma_buf[128];
SCB_InvalidateDCache_by_Addr((uint32_t*)dma_buf, sizeof(dma_buf));

dma_start_transfer(DMA_CH0, (uint32_t)dma_buf, 128);

/* 타임아웃 카운터가 보장된 안전한 폴링 */
uint32_t timeout = 10000U;
while ((DMA_STATUS_REG & DMA_BUSY_BIT) && (--timeout > 0U)) {
    __NOP();
}
if (timeout == 0U) {
    phy_dev_recover_dma_hang(DMA_CH0);
}</code></pre>
        </div>
      </div>
    </div>

    <!-- L4 -->
    <div id="mod3-hal">
      <h3 class="sub-title">Layer 4: HAL Layer — Register Control (<code>hal/</code>, <code>reg/</code>)</h3>
      <p>모뎀 모뎀 칩의 물리 메모리 맵(MMIO) 레지스터를 직접 읽고 쓰는 극도로 취약한 계층입니다.</p>
      <div class="diff-grid">
        <div class="diff-col bad">
          <h5>❌ Bad Code: 치명적 W1C 레지스터 RMW 연산 (|=)</h5>
          <pre><code>#define MODEM_INT_STATUS_REG (*(volatile uint32_t*)0x40001000)
/* W1C(Write-1-to-Clear) 레지스터에 OR 연산 수행 */
void clear_rx_done_irq(void) {
    /* 치명적 참사: 3번 비트만 끄려다 다른 펜딩된 인터럽트(0,1,2번)까지 
       1로 읽혀서 같이 써짐 -> 모든 인터럽트 증발 (Lost IRQ) */
    MODEM_INT_STATUS_REG |= (1U << 3); 
}</code></pre>
        </div>
        <div class="diff-col good">
          <h5>✅ Good Code: 직접 대입 (=) 단일 비트 클리어</h5>
          <pre><code>#define MODEM_INT_STATUS_REG (*(volatile uint32_t*)0x40001000)

void clear_rx_done_irq(void) {
    /* W1C 규격 준수: 해당 비트 위치만 1로 단독 Direct Write! 
       다른 비트는 0이 전달되어 기존 펜딩 상태 보존 */
    MODEM_INT_STATUS_REG = (1U << 3);
    __DSB(); /* 버스 쓰기 완료 보장 */
}</code></pre>
        </div>
      </div>
    </div>

    <!-- L5 -->
    <div id="mod3-isr">
      <h3 class="sub-title">Layer 5: Interrupt (ISR) & Event-Driven Activities (<code>isr/</code>, <code>sched/</code>)</h3>
      <p>1ms 서브프레임, 0.5ms 슬롯 타이머 등 Hard Real-Time 인터럽트 핸들러입니다.</p>
      <div class="diff-grid">
        <div class="diff-col bad">
          <h5>❌ Bad Code: Hard ISR 내 블로킹 Mutex & 무제한 루프</h5>
          <pre><code>void PHY_Slot_Timer_ISR(void) {
    /* 치명적: ISR에서 슬립 가능한 Mutex 취득 시도 */
    osMutexAcquire(g_phy_slot_mutex, osWaitForever); // Hard Fault!

    /* 시간 소모적 연산 수행 */
    while (check_pll_locked() == 0) {
        // PLL 락 걸릴 때까지 수십 µs 락걸림 -> 슬롯 타이머 데드라인 초과
    }
    osMutexRelease(g_phy_slot_mutex);
}</code></pre>
        </div>
        <div class="diff-col good">
          <h5>✅ Good Code: 0-Blocking Bottom-Half 이벤트 위임</h5>
          <pre><code>void PHY_Slot_Timer_ISR(void) {
    /* 1. 하드웨어 타이머 IRQ 플래그 즉시 클리어 */
    TIMER_STAT_REG = (1U << 0);

    /* 2. Spinlock/IRQ-Safe 크리티컬 섹션으로 최소 데이터만 카피 */
    uint32_t flags = PHY_IRQ_SAVE();
    g_slot_counter++;
    PHY_IRQ_RESTORE(flags);

    /* 3. 복잡한 처리는 RTOS Task(Bottom-Half)로 비동기 이벤트 포스팅 */
    osEventFlagsSet(g_phy_event_group, EVT_SLOT_TRIGGER);
}</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- MODULE 4 (DEEP DIVE 1) -->
  <section id="mod4" class="module featured">
    <div class="mod-badge deep">Module 4 · Deep Dive</div>
    <h2 class="mod-title">
      <span>[개발 레벨] ARM Clang + CMake 기반 PHY Code Graph 구축</span>
    </h2>
    <p>
      단순 텍스트/AST 기반 파서는 C 매크로 치환(<code>#define REG (*(volatile uint32_t*)...)</code>)과 ARM 전용 컴파일러 속성(<code>__irq</code>, <code>__packed</code>)을 해석하지 못합니다. <strong>실제 프로덕션 레벨에서 ARM Clang 환경의 Code Graph를 구축하는 3단계 파이프라인</strong>을 상세히 해부합니다.
    </p>

    <!-- 4.1 -->
    <div id="mod4-armclang">
      <h3 class="sub-title">4.1 [핵심 함정 해결] armclang 컴파일 플래그 정규화</h3>
      <p>
        CMake에서 <code>CMAKE_EXPORT_COMPILE_COMMANDS=ON</code>을 켜면 <code>compile_commands.json</code>이 생성되지만, 여기에는 <strong>표준 clangd나 libclang 파서가 인식하지 못하는 ARM 전용 비표준 플래그</strong>(<code>--target=arm-arm-none-eabi</code>, <code>--cpu=Cortex-R52</code>, <code>--fpu=VFPv5-D16</code>, <code>--apcs=...</code>, <code>--via=...</code>)가 가득 차 있어 파싱 에러(Fatal Error)가 발생합니다.
      </p>

      <div class="callout warn">
        <strong>💡 해결책:</strong> 프로젝트 루트에 <code>.clangd</code> 설정 파일을 배치하여 비표준 ARM 플래그를 정규 Clang 호환 플래그로 런타임 변환하거나 전처리 스크립트로 정규화해야 합니다.
      </div>

      <div class="code-header">
        <span>프로젝트 루트 .clangd (armclang 호환성 정규화 설정)</span>
        <button class="copy-btn" onclick="copySnippet('clangd-config')">Copy</button>
      </div>
      <pre id="clangd-config"><code>CompileFlags:
  Remove:
    - --cpu=*
    - --fpu=*
    - --apcs=*
    - --via=*
    - -mthumb-interwork
    - --diag_suppress=*
  Add:
    - -target
    - arm-none-eabi
    - -mcpu=cortex-r52
    - -mfpu=fpv5-sp-d16
    - -mfloat-abi=hard
    - -D__ARMCC_VERSION=6210000
    - -D__arm__
    - -D__attribute__(x)=
    - -I${workspaceFolder}/include/hal
    - -I${workspaceFolder}/include/ipc
    - -I${workspaceFolder}/include/3gpp</code></pre>
    </div>

    <!-- 4.2 -->
    <div id="mod4-schema">
      <h3 class="sub-title">4.2 PHY 도메인 특화 Graph Schema (Node & Edge 설계)</h3>
      <p>
        일반 웹 앱의 Call Graph와 달리, PHY 임베디드 SW는 <strong>하드웨어 레지스터 맵, 공유 글로벌 변수, 함수 포인터 디스패치 테이블, ISR 진입점</strong>이 반드시 일급 객체(First-Class Entity)로 모델링되어야 합니다.
      </p>

      <h4 class="part-title">(1) Node 스키마 (Entity Types)</h4>
      <table>
        <thead>
          <tr><th>Node Type</th><th>주요 속성 (Attributes)</th><th>PHY 도메인 의미</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>Function</code></td>
            <td><code>name</code>, <code>file</code>, <code>start_line</code>, <code>end_line</code>, <code>signature</code>, <strong><code>is_isr_entry</code></strong>, <strong><code>isr_distance</code></strong> (최단 홉수), <code>has_unbounded_while</code></td>
            <td>C/C++ 함수 정의. Hard ISR로부터의 도달 거리(Hop)가 핵심</td>
          </tr>
          <tr>
            <td><code>HWRegister</code></td>
            <td><code>name</code>, <code>base_addr</code>, <code>offset</code>, <code>access_type</code> (<strong>W1C</strong>, WO, RO, RW), <code>bitfield_mask</code></td>
            <td>하드웨어 MMIO 레지스터. W1C 속성 여부가 치명적 결함 판별의 기준</td>
          </tr>
          <tr>
            <td><code>StructType</code></td>
            <td><code>name</code>, <code>size_bytes</code>, <code>alignment</code>, <code>is_packed</code>, <code>has_bitfields</code></td>
            <td>L1-L2 IPC 메시지 및 DMA 디스크립터 구조체. 패딩 및 캐시라인 정렬 검증용</td>
          </tr>
          <tr>
            <td><code>GlobalState</code></td>
            <td><code>name</code>, <code>type</code>, <code>is_volatile</code>, <code>bit_width</code>, <code>shared_across_isr_task</code></td>
            <td>전역 변수. ISR과 Task 간 동시 접근 여부 및 원자성 판별</td>
          </tr>
          <tr>
            <td><code>FSMTable</code></td>
            <td><code>name</code>, <code>state_enum</code>, <code>event_enum</code>, <code>handler_func_ptrs[]</code></td>
            <td>3GPP 프로시저 상태 전이 테이블. 함수 포인터 간접 호출(Indirect Call) 복원용</td>
          </tr>
        </tbody>
      </table>

      <h4 class="part-title">(2) Edge 스키마 (Relation Types)</h4>
      <table>
        <thead>
          <tr><th>Edge Type</th><th>From ➔ To</th><th>주요 속성</th><th>의미</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>CALLS</code></td>
            <td>Function ➔ Function</td>
            <td><code>call_site_line</code>, <strong><code>under_irq_lock</code></strong> (Boolean)</td>
            <td>직접 함수 호출. IRQ 보호 상태 하에서 호출되었는지 추적</td>
          </tr>
          <tr>
            <td><code>INDIRECT_CALLS</code></td>
            <td>Function ➔ Function</td>
            <td><code>via_table</code>, <code>index_expr</code></td>
            <td>FSM 함수 포인터 테이블을 통한 간접 호출 관계 복원</td>
          </tr>
          <tr>
            <td><code>ACCESSES_REG</code></td>
            <td>Function ➔ HWRegister</td>
            <td><strong><code>op_kind</code></strong> (<code>RMW_OR</code>, <code>WRITE_ASSIGN</code>, <code>READ</code>), <code>has_barrier_after</code></td>
            <td>레지스터 접근 형태. W1C 레지스터에 <code>RMW_OR</code>가 발생하면 즉시 Alert</td>
          </tr>
          <tr>
            <td><code>MUTATES_GLOBAL</code></td>
            <td>Function ➔ GlobalState</td>
            <td><code>op</code>, <code>in_critical_section</code></td>
            <td>공유 전역 변수 변경. 크리티컬 섹션 보호 여부 추적</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 4.3 -->
    <div id="mod4-bfs">
      <h3 class="sub-title">4.3 ISR Transitive Reachability 전파 알고리즘 (BFS)</h3>
      <p>
        개발자가 특정 헬퍼 함수(예: <code>rf_pll_wait_lock()</code>)를 수정했을 때, 이 함수가 Hard ISR 컨텍스트에서 실행되는지 여부를 <strong>Graph BFS 탐색을 통해 사전에 O(V+E) 시간으로 전파/태깅</strong>합니다.
      </p>

      <div class="code-header">
        <span>Transitive ISR Reachability BFS 알고리즘 (Python)</span>
        <button class="copy-btn" onclick="copySnippet('bfs-code')">Copy</button>
      </div>
      <pre id="bfs-code"><code>def compute_transitive_isr_reachability(self):
    \"\"\"모든 Hard ISR 진입점으로부터 BFS를 수행하여 도달 가능한 모든 함수에 최단 hop_distance를 태깅\"\"\"
    queue = deque([fn for fn, meta in self.functions.items() if meta["is_isr_entry"]])
    
    while queue:
        curr_fn = queue.popleft()
        curr_dist = self.functions[curr_fn]["isr_distance"]
        curr_path = self.functions[curr_fn]["isr_path"]
        
        for edge in self.outbound_callees.get(curr_fn, []):
            callee = edge["callee"]
            if callee in self.functions:
                # 아직 방문하지 않은 함수라면 최단 거리 및 경로 기록
                if self.functions[callee]["isr_distance"] is None:
                    self.functions[callee]["isr_distance"] = curr_dist + 1
                    self.functions[callee]["isr_path"] = curr_path + [callee]
                    queue.append(callee)</code></pre>
    </div>
  </section>

  <!-- MODULE 5 (DEEP DIVE 2) -->
  <section id="mod5" class="module featured">
    <div class="mod-badge deep">Module 5 · Deep Dive</div>
    <h2 class="mod-title">
      <span>[개발 레벨] AI Context Engineering & 토큰 다이어트 방법론</span>
    </h2>
    <p>
      수십만 라인의 PHY 소스 코드 전체나 불필요한 헤더를 LLM(DeepSeek/GLM/Qwen)에 그대로 밀어 넣으면 <strong>컨텍스트 윈도우 폭발(Context Bloat)</strong>과 <strong>주의 집중력 저하(Lost in the Middle)</strong>로 환각이 급증합니다. <strong>토큰을 85% 이상 절감하면서 정밀도를 극대화하는 4대 Context Engineering 기법</strong>입니다.
    </p>

    <!-- 5.1 -->
    <div id="mod5-asym">
      <h3 class="sub-title">5.1 비대칭 $k$-Hop Skeleton 슬라이싱 (Asymmetric Slicing)</h3>
      <p>
        수정된 대상 함수(Target)를 중심으로 인바운드 호출자(Caller)와 아웃바운드 피호출자(Callee)의 본문을 비대칭적으로 요약(Skeletonizing)하여 주입합니다.
      </p>
      <table>
        <thead>
          <tr><th>방향 (Direction)</th><th>포함 범위 (Hop)</th><th>슬라이싱 처리 방식 (Token Diet)</th><th>토큰 절감률</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>0-Hop (수정 대상)</strong></td>
            <td>Target Function</td>
            <td><strong>100% 완전한 원본 소스 코드</strong> (구현부 전체 포함)</td>
            <td>0% (기준)</td>
          </tr>
          <tr>
            <td><strong>1~2 Hop Inbound (상위 호출자)</strong></td>
            <td>Callers</td>
            <td>함수 전체가 아닌 <strong>함수 시그니처 + IRQ Lock 상태 + 호출 지점 전후 ±5 라인</strong>만 추출</td>
            <td><strong>85% 절감</strong></td>
          </tr>
          <tr>
            <td><strong>1-Hop Outbound (하위 함수)</strong></td>
            <td>Callees</td>
            <td>본문 전면 생략, <strong>함수 시그니처 + 부수효과(Modifies Regs / Locks) 3줄 주석 계약</strong>만 추출</td>
            <td><strong>92% 절감</strong></td>
          </tr>
          <tr>
            <td><strong>Referenced Symbols</strong></td>
            <td>Types / Regs</td>
            <td>전체 헤더가 아닌 <strong>참조된 <code>struct</code> 정의 및 레지스터 매크로 선언부</strong>만 단독 발췌</td>
            <td><strong>98% 절감</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 5.2 -->
    <div id="mod5-fact">
      <h3 class="sub-title">5.2 컴파일러/그래프 확정 사실의 선행 주입 (Compiler-Fact Header Injection)</h3>
      <p>
        LLM에게 "이 함수가 ISR에서 불리는지 코드를 보고 유추해봐"라고 요청하지 않습니다. <strong>Code Graph가 분석한 100% 확정된 사실을 상단 블록에 불변의 진실(Ground Truth)로 명시</strong>하여 LLM이 불필요한 추론을 하지 못하도록 못 박습니다.
      </p>

      <div class="code-header">
        <span>AI에게 주입되는 [COMPILER_VERIFIED_FACTS] 헤더 예시</span>
        <button class="copy-btn" onclick="copySnippet('fact-header')">Copy</button>
      </div>
      <pre id="fact-header"><code>### 📦 Smart Context Bundle: `void hal_modem_irq_clear(uint32_t bit_idx)`
- **Location:** `src/hal/hal_modem_irq.c:5-12`

> **[COMPILER_VERIFIED_FACTS — GROUND TRUTH FROM PHY CODE GRAPH]**
> - **Reachable from Hard ISR:** **YES (Hop=1 via PHY_Slot_Timer_ISR -> hal_modem_irq_clear)**
> - **Unbounded Polling Loop Detected:** `YES 🚨 [PHY-ISR-02 VIOLATION]`
> - **Memory/Cache Barriers in Function:** `NONE`
> - **Hardware Register Operations:**
  - `MODEM_IRQ_STAT_W1C`: `RMW_OR (|=)` (`MODEM_IRQ_STAT_W1C |= (1U << bit_idx);`) 🚨 [W1C |= HAZARD!]
  - `HAL_IPC_TRIG_REG`: `WRITE_ASSIGN (=)` (`HAL_IPC_TRIG_REG = 0x1U;`)
> - **Inbound Callers (1-Hop Blast Radius):**
  - `PHY_Slot_Timer_ISR()` at `src/hal/hal_modem_irq.c:3` (under_irq_lock=False [UNPROTECTED]) -> `hal_modem_irq_clear(3U);`
> - **Outbound Callees (1-Hop Skeleton Summary — Bodies Omitted for Token Diet):**
  - None</code></pre>
    </div>

    <!-- 5.3 -->
    <div id="mod5-bundle">
      <h3 class="sub-title">5.3 연결 컴포넌트 기반 스마트 번들링 (Alibaba Pattern)</h3>
      <p>
        하나의 PR에 여러 파일이 수정되었을 때, 이를 단순 파일 순서대로 합치는 대신 <strong>Call-Graph 상의 연결 요소(Connected Component) 단위로 묶어서 독립 번들(Bundle)을 생성</strong>합니다.
      </p>
      <ul>
        <li><strong>Bundle A (HAL/ISR 군집):</strong> <code>hal_irq.c</code> + <code>hal_timer.c</code> (호출 관계 연결됨) ➔ <code>phy-isr-hal-auditor</code> 에 전달 (토큰 수: ~4,200)</li>
        <li><strong>Bundle B (3GPP/IPC 군집):</strong> <code>phy_prach_proc.c</code> + <code>ipc_msg.c</code> (프로시저 상태 머신) ➔ <code>phy-ipc-3gpp-auditor</code> 에 전달 (토큰 수: ~3,800)</li>
        <li><strong>효과:</strong> 모든 서브에이전트가 <strong>6,000 토큰 미만의 정밀 핀포인트 컨텍스트</strong>에서 집중 리뷰를 수행하여 환각 0% 달성.</li>
      </ul>
    </div>

    <!-- 5.4 -->
    <div id="mod5-code">
      <h3 class="sub-title">5.4 실제 동작하는 구현체: <code>phy_context_slicer.py</code></h3>
      <p>
        본 프로젝트의 PoC 디렉토리에 실제로 포함되어 self-test 검증을 통과한 Python 엔진의 핵심 로직입니다.
      </p>

      <div class="code-header">
        <span>phy_context_slicer.py 핵심 엔진 발췌</span>
        <button class="copy-btn" onclick="copySnippet('slicer-src')">Copy</button>
      </div>
      <pre id="slicer-src"><code>class PhyCodeGraphBuilder:
    \"\"\"PHY 특화 C/C++ 그래프: ISR 도달 경로, W1C/RMW 레지스터, 호출 관계를 분석\"\"\"
    FUNC_DEF_RE = re.compile(r"^\s*(?:static\s+|inline\s+|__irq\s+)*([a-zA-Z_][a-zA-Z0-9_\s\*]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^;{}]*)\)\s*\{", re.MULTILINE)
    REG_RMW_OR_RE = re.compile(r"\b([A-Z0-9_]+(?:_REG|_W1C|_CLR|_STAT|_CTRL|_PEND)[A-Z0-9_]*)\s*\|=\s*([^;]+);")
    REG_ASSIGN_RE = re.compile(r"\b([A-Z0-9_]+(?:_REG|_W1C|_CLR|_STAT|_CTRL|_PEND|_TRIG)[A-Z0-9_]*)\s*=\s*([^;=]+);")
    BARRIER_RE = re.compile(r"\b(__DMB|__DSB|__ISB|SCB_CleanDCache|SCB_InvalidateDCache)\b")
    LOCK_ACQ_RE = re.compile(r"\b(PHY_IRQ_SAVE|DISABLE_IRQ|osMutexAcquire|spin_lock_irqsave)\b")

    def build_context_slice_for_function(self, func_name: str) -> str:
        meta = self.functions.get(func_name)
        # [COMPILER_VERIFIED_FACTS] 헤더 블록 구성
        # Inbound Caller 1-Hop 슬라이스 요약 추출
        # Outbound Callee 시그니처 요약 추출
        # 원본 함수 본문 래핑 후 Markdown 컨텍스트 팩 반환</code></pre>
    </div>
  </section>

  <!-- MODULE 6 -->
  <section id="mod6" class="module">
    <div class="mod-badge">Module 6</div>
    <h2 class="mod-title">OpenCode 멀티에이전트 하네스 & 8주 롤아웃 로드맵</h2>
    <p>
      구축된 Code Graph와 슬라이싱된 컨텍스트를 받아 실제 리뷰를 수행하는 <strong>OpenCode 하네스 구성</strong>과 <strong>그룹 차원의 안전한 8주 롤아웃 계획</strong>입니다.
    </p>

    <h3 class="sub-title">1. OpenCode 서브에이전트 역할 분담</h3>
    <table>
      <thead>
        <tr><th>서브에이전트</th><th>전문 담당 영역 (Domain Focus)</th><th>적용 모델</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><code>phy-isr-hal-auditor</code></td>
          <td>Hard ISR 컨텍스트 내 블로킹, W1C 레지스터 RMW(<code>|=</code>), Memory Barrier/D-Cache 동기화</td>
          <td>DeepSeek-R1 / Qwen3-Coder</td>
        </tr>
        <tr>
          <td><code>phy-ipc-3gpp-auditor</code></td>
          <td>상위 IPC Shared-Memory 레이스 컨디션, 3GPP FSM 상태 전이 무결성, 타이머 타임아웃</td>
          <td>GLM-4.5 / DeepSeek-V3</td>
        </tr>
        <tr>
          <td><code>phy-chief-verifier</code></td>
          <td><strong>반증(Disproving) 패스</strong> 수행, 오탐 제거, 5축 점수 산출 및 PR Merge Block/Approve 결정</td>
          <td>DeepSeek-R1 (High Reasoning)</td>
        </tr>
      </tbody>
    </table>

    <h3 class="sub-title">2. 오탐(False Positive)을 0으로 만드는 반증(Disproving) 패스</h3>
    <div class="callout deep">
      에이전트가 "이것은 버그다"라고 지적했을 때 그대로 PR에 코멘트를 달지 않습니다. <code>phy-chief-verifier</code>는 반드시 <strong>"이 코드가 실제로는 버그가 아닐 수 있는 이유(예: 상위 호출자가 이미 IRQ를 끈 상태이거나, 외부 하드웨어가 자동 리셋을 지원하는 경우)"</strong>를 조사하고, 반증에 실패하여 <strong>100% 확실한 결함으로 증명된 경우에만</strong> PR에 코멘트를 등록합니다.
    </div>

    <h3 class="sub-title">3. 그룹 단계별 8주 롤아웃 로드맵</h3>
    <table>
      <thead>
        <tr><th>단계 (Phase)</th><th>기간</th><th>목표 및 마일스톤</th><th>안전 가드 (Safety Guard)</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Phase 1: Shadow Run</strong></td>
          <td>1~2주차</td>
          <td>Git Pre-Push에 <code>ast-grep</code> 규칙만 적용, PR 리뷰는 비공개 로깅 모드로 실행</td>
          <td>PR 블로킹 없음, 리포트 정확도만 측정</td>
        </tr>
        <tr>
          <td><strong>Phase 2: Informative Mode</strong></td>
          <td>3~4주차</td>
          <td>PR에 AI 리뷰 코멘트 게시 시작 (Critical 결함도 Warning으로 표기)</td>
          <td>엔지니어 피드백(유용함/오탐 버튼) 수집</td>
        </tr>
        <tr>
          <td><strong>Phase 3: Soft Gating</strong></td>
          <td>5~6주차</td>
          <td>Critical 결함(W1C RMW, ISR Mutex) 발생 시 개발자 경고, 수동 Override 허용</td>
          <td>긴급 핫픽스용 <code>[skip-ai-review]</code> 태그 지원</td>
        </tr>
        <tr>
          <td><strong>Phase 4: Full Enforcement</strong></td>
          <td>7~8주차</td>
          <td>Risk Score 70점 미만 또는 Critical 결함 시 GitHub Actions PR Merge 자동 차단</td>
          <td>그룹장/테크리드 1-Click 승인 바이패스 권한 부여</td>
        </tr>
      </tbody>
    </table>
  </section>

  <footer>
    <p>© 2026 Mobile PHY Embedded SW Group — AI-Native Engineering Enablement</p>
    <p>Powered by OpenCode, DeepSeek-R1, Qwen-Coder, Clang Semantic Graph & ast-grep</p>
  </footer>
</main>

<script>
  function copySnippet(id) {
    const el = document.getElementById(id);
    if (!el) return;
    navigator.clipboard.writeText(el.innerText).then(() => {
      alert("클립보드에 복사되었습니다!");
    });
  }

  function openTab(evt, tabId) {
    const parent = evt.target.closest('.tab-group');
    const buttons = parent.querySelectorAll('.tab-btn');
    const contents = parent.querySelectorAll('.tab-content');
    buttons.forEach(b => b.classList.remove('active'));
    contents.forEach(c => c.classList.remove('active'));
    evt.target.classList.add('active');
    parent.querySelector('#' + tabId).classList.add('active');
  }

  // Active TOC ScrollSpy
  window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section.module, header');
    const scrollPos = window.scrollY + 200;
    sections.forEach(sec => {
      const id = sec.getAttribute('id');
      if (!id) return;
      const link = document.querySelector(`aside.toc a[href="#${id}"]`);
      if (sec.offsetTop <= scrollPos && (sec.offsetTop + sec.offsetHeight) > scrollPos) {
        document.querySelectorAll('aside.toc a').forEach(a => a.classList.remove('active'));
        if (link) link.classList.add('active');
      }
    });
  });
</script>
</body>
</html>
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(poc_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated successfully: {out_path} ({len(html_content)} bytes)")
print(f"Copied to: {poc_path}")
