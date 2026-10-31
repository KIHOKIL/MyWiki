import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.join(BASE_DIR, "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)

REPORT_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>코드 리뷰가 병목이 되는 이유 | 메타 시니어 AI 코드 리뷰 & PHY SW 적용 리포트</title>
<style>
  :root {
    --bg: #0d1117;
    --card: #161b22;
    --card-alt: #1f242d;
    --border: rgba(139, 148, 158, 0.2);
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --yellow: #d29922;
    --orange: #db6d28;
    --red: #f85149;
    --purple: #bc8cff;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.65;
    display: flex;
    min-height: 100vh;
  }
  aside.toc {
    width: 270px;
    background: #090d13;
    border-right: 1px solid var(--border);
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    padding: 28px 18px;
    overflow-y: auto;
  }
  aside.toc h3 {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin-bottom: 14px;
  }
  aside.toc a {
    display: block;
    color: var(--muted);
    text-decoration: none;
    font-size: 13.5px;
    padding: 8px 10px;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: all 0.15s;
  }
  aside.toc a:hover, aside.toc a.active {
    background: rgba(88, 166, 255, 0.12);
    color: var(--accent);
    font-weight: 600;
  }
  main {
    margin-left: 270px;
    flex: 1;
    padding: 36px 40px 90px;
    max-width: 1180px;
  }
  @media (max-width: 960px) {
    aside.toc { display: none; }
    main { margin-left: 0; padding: 20px; }
  }
  header {
    background: linear-gradient(135deg, #161b22 0%, #111827 60%, #1e1b4b 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px;
    margin-bottom: 28px;
  }
  .badge-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
  .badge {
    font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 999px;
    background: rgba(88,166,255,0.12); color: var(--accent); border: 1px solid rgba(88,166,255,0.3);
  }
  .badge.green { background: rgba(63,185,80,0.12); color: var(--green); border-color: rgba(63,185,80,0.3); }
  .badge.purple { background: rgba(188,140,255,0.12); color: var(--purple); border-color: rgba(188,140,255,0.3); }
  h1 { font-size: 28px; font-weight: 800; margin-bottom: 10px; letter-spacing: -0.02em; }
  .subtitle { color: var(--muted); font-size: 15px; margin-bottom: 18px; }
  .meta-links a {
    display: inline-block; margin-right: 14px; color: var(--accent); text-decoration: none;
    font-size: 14px; font-weight: 600;
  }
  .section {
    background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 28px; margin-bottom: 24px;
    scroll-margin-top: 24px;
  }
  h2 {
    font-size: 20px; font-weight: 700; margin-bottom: 18px; padding-bottom: 10px;
    border-bottom: 1px solid var(--border); color: #fff;
  }
  h3 { font-size: 16px; font-weight: 700; margin: 18px 0 10px; color: var(--accent); }
  .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 18px; }
  .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
  .subcard {
    background: var(--card-alt); border: 1px solid var(--border); border-radius: 10px; padding: 18px;
  }
  .subcard h4 { font-size: 15px; margin-bottom: 8px; color: #fff; }
  .subcard p, .subcard li { font-size: 14px; color: var(--muted); }
  ul { padding-left: 18px; }
  li { margin-bottom: 6px; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
  th, td { border: 1px solid var(--border); padding: 11px 14px; text-align: left; vertical-align: top; }
  th { background: #21262d; color: #fff; font-weight: 600; }
  tr:nth-child(even) td { background: rgba(255,255,255,0.015); }
  .prompt-box {
    position: relative; margin-top: 12px;
  }
  .copy-btn {
    position: absolute; top: 10px; right: 10px;
    background: #21262d; color: var(--text); border: 1px solid var(--border);
    padding: 5px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;
  }
  .copy-btn:hover { border-color: var(--accent); color: var(--accent); }
  pre {
    background: #090d13; border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; overflow-x: auto; font-size: 13px; color: #d2a8ff;
    font-family: "JetBrains Mono", Consolas, monospace; white-space: pre-wrap;
  }
  .tabs { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
  .tab-btn {
    background: #21262d; color: var(--muted); border: 1px solid var(--border);
    padding: 7px 14px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px;
  }
  .tab-btn.active { background: rgba(88,166,255,0.16); color: var(--accent); border-color: var(--accent); }
  .tab-panel { display: none; }
  .tab-panel.active { display: block; }
  .tier-low { color: var(--green); font-weight: 700; }
  .tier-med { color: var(--yellow); font-weight: 700; }
  .tier-high { color: var(--orange); font-weight: 700; }
  .tier-crit { color: var(--red); font-weight: 700; }
  .callout {
    border-left: 4px solid var(--accent); background: rgba(88,166,255,0.08);
    padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 14px 0; font-size: 14px;
  }
</style>
</head>
<body>
<aside class="toc">
  <h3>📑 Lecture & PHY Deep Research</h3>
  <a href="#sec-paradigm" class="active">1. 2024 vs 2026 패러다임 & 4대 강점</a>
  <a href="#sec-stages">2. Pre-PR vs Post-PR 누적 방어선</a>
  <a href="#sec-routing">3. 6대 리뷰 기법 & 경로 자동 라우팅</a>
  <a href="#sec-rubric">4. 5축 리스크 루브릭 & 액션 매트릭스</a>
  <a href="#sec-prompts">5. 원문 프롬프트 팩 (원클릭 복사)</a>
  <a href="#sec-repos">6. 검증된 오픈소스 Top 12 벤치마크</a>
  <a href="#sec-phy">7. PHY 5-Layer 불변조건 & 안전 가드</a>
</aside>

<main>
  <header>
    <div class="badge-row">
      <span class="badge">실밸개발자 (Meta Senior Engineer)</span>
      <span class="badge green">Pre-PR + Post-PR 2-Stage Defense</span>
      <span class="badge purple">PHY SW Group (GitHub + OpenCode + DeepSeek/GLM/Qwen + ARM Clang + CMake)</span>
    </div>
    <h1>코드 리뷰가 병목이 되는 이유 | 메타 시니어 엔지니어가 AI 코드 리뷰 하는법</h1>
    <p class="subtitle">강의 19개 챕터 전수 요약 · 5축 리스크 점수 루브릭(0~100) · 25대 오픈소스 실시간 벤치마크 · PHY 임베디드 SW 5-Layer 마스터 리포트</p>
    <div class="meta-links">
      <a href="https://www.youtube.com/watch?v=Be5b6D1IoLI" target="_blank">▶ 원본 YouTube 강의 보기 (38:23)</a>
      <a href="slides/index.html">🖥 인터랙티브 슬라이드 덱 열기 (8 Slides)</a>
    </div>
  </header>

  <section id="sec-paradigm" class="section">
    <h2>1. 2024 vs 2026: 코드 리뷰 패러다임의 전환과 4대 강점 (Ch 01~04)</h2>
    <div class="grid-2">
      <div class="subcard">
        <h4>⏳ 2024년: 전부 사람의 손으로 (리뷰가 최대 병목)</h4>
        <ul>
          <li>아침 출근 시 PR 큐에 <strong>14개 적체</strong> (1개는 700줄 대형 PR)</li>
          <li><code>null check</code> 누락, 컨벤션 위반, 테스트 추가 요청을 시니어가 수작업 코멘트</li>
          <li>점심 전까지 <strong>3개만 처리</strong>, 나머지 <strong>11개는 내일로 이월</strong> (동료 전원 대기)</li>
        </ul>
      </div>
      <div class="subcard">
        <h4>⚡ 2026년: 기계가 1차 필터링, 사람은 고차원 결정</h4>
        <ul>
          <li>새벽 사이 에이전트가 <strong>14개 전부에 1차 리뷰 및 리스크 채점 완료</strong></li>
          <li>시니어는 <strong>사람의 판단이 필수적인 고위험 PR 3개만 심층 검토</strong></li>
          <li>오후에는 본인의 설계·구현에 몰입 (인간을 빼는 것이 아니라 <strong>고차원 결정에 재배치</strong>)</li>
        </ul>
      </div>
    </div>
    <div class="grid-4" style="margin-top:16px;">
      <div class="subcard"><h4>01. 24/7 즉시성</h4><p>새벽 2시 PR도 올리는 즉시 리뷰 개시, 대기 시간 0</p></div>
      <div class="subcard"><h4>02. 완벽한 일관성</h4><p>컨디션·일정·작성자(시니어/주니어)에 흔들리지 않는 동일 기준</p></div>
      <div class="subcard"><h4>03. 누락 없음</h4><p>700줄 PR에서도 첫 줄과 마지막 줄을 동일한 정밀도로 스캔</p></div>
      <div class="subcard"><h4>04. 고차원 재배치 ★</h4><p>컨벤션 지적에서 시니어를 해방시켜 아키텍처·보안·도메인에 집중</p></div>
    </div>
  </section>

  <section id="sec-stages" class="section">
    <h2>2. 누적 방어선: Pre-PR (pre-push 훅) vs Post-PR (GitHub Actions) (Ch 05, 12~16)</h2>
    <table>
      <thead>
        <tr>
          <th>구분</th>
          <th>PRE-PR REVIEW (로컬 셀프 리뷰)</th>
          <th>POST-PR REVIEW (GitHub Actions 자동 리뷰)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>실행 시점</strong></td>
          <td><code>git push</code> 직전 (<code>.githooks/pre-push</code> 훅 강제화)</td>
          <td>GitHub PR 생성 / 새 커밋 푸시 시 (CI 파이프라인)</td>
        </tr>
        <tr>
          <td><strong>왜 commit이 아닌 push인가?</strong></td>
          <td>매 <code>git commit</code>마다 LLM이 돌면 수십 초 블로킹 및 토큰 낭비 발생 ➡️ PR 직전인 <code>pre-push</code>에서 누적 diff를 한 번에 검증</td>
          <td>팀 전체가 공유하는 단일 요약 코멘트(<code>&lt;!-- ai-pr-review --&gt;</code> 마커 Upsert) 및 리스크 라벨링</td>
        </tr>
        <tr>
          <td><strong>판정 및 차단</strong></td>
          <td>명백한 버그·보안 결함 시 <code>VERDICT: FAIL</code> 출력 후 <code>exit 1</code>로 푸시 차단 (장애 시에는 Fail-open)</td>
          <td><strong>이종 모델 크로스 리뷰(Cross-Review)</strong>로 자기 확증 편향 제거 + 0~100점 리스크 채점</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section id="sec-routing" class="section">
    <h2>3. 6대 코드 리뷰 기법과 경로/라벨 기반 자동 라우팅 (Ch 06)</h2>
    <table>
      <thead>
        <tr><th>#</th><th>리뷰 기법</th><th>적용 조건 (강의 원문)</th><th>PHY SW 그룹 라우팅 매핑</th></tr>
      </thead>
      <tbody>
        <tr><td>1</td><td><strong>Full diff review</strong></td><td>작은 PR · 100줄 이하</td><td>단일 <code>opencode run</code> 패스로 빠른 전체 검토</td></tr>
        <tr><td>2</td><td><strong>File-by-file review</strong></td><td>큰 PR · 500줄 이상</td><td>파일/번들 단위로 쪼개 서브에이전트 컨텍스트 분리 (Lost-in-the-middle 방지)</td></tr>
        <tr><td>3</td><td><strong>Security / Safety-focused</strong></td><td>인증·권한·외부 입력 변경</td><td><code>hal/</code>, <code>ipc/</code> 변경 시 <code>volatile</code>, <code>W1C</code>, <code>DMB/DSB</code> 배리어, 범위 검증 감사</td></tr>
        <tr><td>4</td><td><strong>Performance-focused</strong></td><td>DB 쿼리 · Hot path 변경</td><td><code>isr/</code>, <code>sched/</code> 변경 시 ISR 사이클 예산, 무한 폴링 루프, 블로킹 호출 집중 감사</td></tr>
        <tr><td>5</td><td><strong>Test-coverage-focused</strong></td><td>소스만 바뀌고 테스트 미변경</td><td>L1 시뮬레이터 / CTest 누락 경고</td></tr>
        <tr><td>6</td><td><strong>Architecture-focused</strong></td><td>신규 모듈 · 의존성 변화</td><td><code>CMakeLists.txt</code> 및 공용 헤더 변경 시 계층 침범 및 파급 반경(Blast Radius) 분석</td></tr>
      </tbody>
    </table>
  </section>

  <section id="sec-rubric" class="section">
    <h2>4. 5축 리스크 점수 루브릭 (0~100점) & 액션 매트릭스 (Ch 07~09)</h2>
    <table>
      <thead>
        <tr>
          <th>강의 원본 5축 (Web/Backend 기준)</th>
          <th>배점</th>
          <th>PHY SW 그룹 전용 5축 (ARM Embedded PHY SW 치환)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1. 보안 (Security)</strong>: auth, permissions, secrets, 외부 입력, CVE</td>
          <td><strong>30점</strong></td>
          <td><strong>1. Real-Time & ISR Determinism (30점)</strong>: ISR/FIQ 블로킹, 타임아웃 없는 <code>while</code> 폴링, 동적 할당, TTI/Slot 데드라인 위반</td>
        </tr>
        <tr>
          <td><strong>2. Breaking Change</strong>: Public API, DB 스키마, 환경 변수</td>
          <td><strong>20점</strong></td>
          <td><strong>2. HAL Register & Concurrency Safety (25점)</strong>: MMIO <code>volatile</code> 누락, 비원자적 RMW(<code>|=</code>), <code>W1C</code> 오조작, ARM <code>DMB/DSB/ISB</code> 배리어 누락</td>
        </tr>
        <tr>
          <td><strong>3. 스코프 (Scope)</strong>: 변경 파일 수·라인 수·모듈 수</td>
          <td><strong>20점</strong></td>
          <td><strong>3. IPC & 3GPP Procedure Contract (20점)</strong>: L2↔L1 IPC 구조체 패딩/정렬 변경, HARQ/RACH/CSI 상태 머신 Dead-end</td>
        </tr>
        <tr>
          <td><strong>4. 테스트 커버리지 (Test)</strong>: 신규 테스트 유무, 기존 테스트 삭제</td>
          <td><strong>15점</strong></td>
          <td><strong>4. Call-Graph Blast Radius (15점)</strong>: <code>CMake compile_commands.json</code> + <code>code-review-graph</code> 2-hop 호출 파급도</td>
        </tr>
        <tr>
          <td><strong>5. 마이그레이션 (Migration)</strong>: DB 마이그레이션, 롤백 난이도</td>
          <td><strong>15점</strong></td>
          <td><strong>5. Target Build & Test Evidence (10점)</strong>: <code>armclang</code> 경고 0건, <code>ast-grep/clang-tidy</code> 통과, L1 Sim 테스트 유무</td>
        </tr>
      </tbody>
    </table>

    <h3>점수 구간별 액션 매트릭스 (Action Matrix)</h3>
    <table>
      <thead>
        <tr><th>점수 구간</th><th>라벨</th><th>강제 게이트 액션 (강의 원문 + PHY 그룹 정책)</th></tr>
      </thead>
      <tbody>
        <tr><td class="tier-low">0 ~ 15점</td><td><code>risk:low</code></td><td>AI 코멘트 게시 · 1명 승인으로 Fast-Merge 후보 (초기엔 Dry-Run)</td></tr>
        <tr><td class="tier-med">16 ~ 35점</td><td><code>risk:medium</code></td><td>AI 코멘트 + <strong>동료 PHY 리뷰어 1명 필수 지정</strong> (Auto-merge 비활성)</td></tr>
        <tr><td class="tier-high">36 ~ 60점</td><td><code>risk:high</code></td><td>AI 코멘트 + <strong>시니어/서브시스템 오너 1명 지정 + HAL/ISR/Architecture 특화 에이전트 추가 호출</strong></td></tr>
        <tr><td class="tier-crit">61 ~ 100점</td><td><code>risk:critical</code></td><td><strong>즉시 Merge 차단 + 그룹장/아키텍트 알림 + 3GPP/HW 변경 사양서(RFC/ADR) 링크 필수</strong></td></tr>
      </tbody>
    </table>
  </section>

  <section id="sec-prompts" class="section">
    <h2>5. 추출 프롬프트 원문 & PHY OpenCode 변환 프롬프트 (원클릭 복사)</h2>
    <div class="tabs">
      <button class="tab-btn active" onclick="showTab(0)">Prompt 1: Pre-push 훅 셋업 (원문)</button>
      <button class="tab-btn" onclick="showTab(1)">Prompt 2: GitHub Actions + 5축 루브릭 (원문)</button>
      <button class="tab-btn" onclick="showTab(2)">Prompt 3: PHY SW 그룹 OpenCode + DeepSeek/GLM/Qwen</button>
    </div>

    <div class="tab-panel active">
      <div class="prompt-box">
        <button class="copy-btn" onclick="copyText('p1', this)">📋 복사</button>
        <pre id="p1">[초기 요청]
어, pre-commit hook 하나 add 하고 싶어. Claude hook이고, commit 하기 전에 코드 리뷰를 꼭 돌려주는 그 Claude의 '/codereview' 커맨드가 있거든? 그걸 꼭 돌려주는 hook을 설정을 해서 add를 해줘.

[피벗 요청 — Pre-push 훅으로 전환]
커밋 전이 아니라 PR 생성 전으로 가자.

[내장 헤드리스 프롬프트 규격]
Review this git diff that is about to be pushed.
Focus ONLY on issues that should block a PR: bugs, security issues, broken logic, missing error handling at system boundaries, accidental debug code/secrets.
Skip style nitpicks. Keep it concise (under 25 lines).
On the VERY LAST LINE output exactly VERDICT: PASS or VERDICT: FAIL.</pre>
      </div>
    </div>

    <div class="tab-panel">
      <div class="prompt-box">
        <button class="copy-btn" onclick="copyText('p2', this)">📋 복사</button>
        <pre id="p2">[초기 요청]
Github PR에 자동으로 클로드가 그 PR을 리뷰하고 코멘트를 달아주는 그런 Github Actions를 넣어줄 거야. 이거를 셋업하고 싶은데, 어떻게 셋업해야 될지 한번 우리 같이 의논해보자.

[이종 모델 크로스 리뷰 전환]
클로드가 PR을 리뷰하는게 아니라 GPT API를 써서 PR을 리뷰하자.

[5축 루브릭 고도화]
risk score rubric 너가 다듬어서 risk score 도 보여줄수 있도록 해줘</pre>
      </div>
    </div>

    <div class="tab-panel">
      <div class="prompt-box">
        <button class="copy-btn" onclick="copyText('p3', this)">📋 복사</button>
        <pre id="p3">opencode run --model litellm/deepseek-r1 --agent phy-chief-verifier \\
  "Analyze the PHY Embedded SW PR diff, AST-Grep findings, and Call-Graph Blast Radius.
   1. Run Disproving Pass: reject style nitpicks or issues already guarded by caller IRQ_LOCK / range checks.
   2. Score across PHY 5-Axis Risk Rubric (0-100):
      - Real-Time & ISR Determinism (30 pts)
      - HAL Register & Concurrency Safety (25 pts: volatile, W1C |= bug, RMW race, DMB/DSB)
      - IPC & 3GPP Procedure Contract (20 pts: struct alignment, HARQ/RACH FSM dead-ends, SFN wrap)
      - Call-Graph Blast Radius (15 pts)
      - Target Build & Test Evidence (10 pts)
   3. Output markdown table and end with exact final line VERDICT: PASS or VERDICT: FAIL."</pre>
      </div>
    </div>
  </section>

  <section id="sec-repos" class="section">
    <h2>6. 검증된 오픈소스 Top 12 벤치마크 ([직접 도입 6종] vs [패턴 차용 6종])</h2>
    <table>
      <thead>
        <tr><th>구분</th><th>리포지토리</th><th>실시간 ⭐ Stars</th><th>PHY SW 그룹 적용 핵심 가치</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>🅰️ 직접 도입 1</strong></td><td><code>anomalyco/opencode</code></td><td><strong>223,474</strong></td><td>그룹 표준 CLI/CI 에이전트 하네스 (오픈 모델 & MCP 직결)</td></tr>
        <tr><td><strong>🅰️ 직접 도입 2</strong></td><td><code>DeusData/codebase-memory-mcp</code></td><td><strong>47,893</strong></td><td>Pure C + <code>clangd</code> (<code>compile_commands.json</code>) C/C++ 정밀 호출 그래프 MCP</td></tr>
        <tr><td><strong>🅰️ 직접 도입 3</strong></td><td><code>tirth8205/code-review-graph</code></td><td><strong>32,518</strong></td><td><code>--platform opencode/qwen</code> 공식 지원 · 2-hop 파급 반경 추출로 토큰 65배 절감</td></tr>
        <tr><td><strong>🅰️ 직접 도입 4</strong></td><td><code>ast-grep/ast-grep</code></td><td><strong>16,401</strong></td><td>Rust 기반 C/C++ 구조적 AST 매칭 (<code>W1C |=</code>, 무한 <code>while</code> 폴링 1초 차단)</td></tr>
        <tr><td><strong>🅰️ 직접 도입 5</strong></td><td><code>reviewdog/reviewdog</code></td><td><strong>9,711</strong></td><td><code>armclang</code> / <code>clang-tidy</code> 출력을 PR 변경 라인에만 필터링 매핑</td></tr>
        <tr><td><strong>🅰️ 직접 도입 6</strong></td><td><code>danmar/cppcheck</code> + <code>clang-tidy</code></td><td><strong>6,790</strong></td><td>CMake 빌드 DB 연동 정적 포인터·배열 경계·초기화 검증</td></tr>
        <tr><td><strong>🅱️ 패턴 차용 1</strong></td><td><code>alibaba/open-code-review</code></td><td><strong>49,163</strong></td><td>결정론적 파일 번들링 + 경로별 규칙 매칭 + Reflection(오탐 자기반증) 구조</td></tr>
        <tr><td><strong>🅱️ 패턴 차용 2</strong></td><td><code>cloudflare/security-audit-skill</code></td><td><strong>54,848</strong></td><td>6단계 감사 + Disproving Pass + <code>confirmed/needs_validation/rejected</code> 원장</td></tr>
        <tr><td><strong>🅱️ 패턴 차용 3</strong></td><td><code>winnin/farol</code></td><td><strong>170</strong></td><td>바뀌지 않은 상위 호출자 계약 파괴(Contract Breakage) 및 Blast Radius 산출</td></tr>
        <tr><td><strong>🅱️ 패턴 차용 4~6</strong></td><td><code>ECC</code> / <code>ponytail</code> / <code>codex-plugin-cc</code></td><td><strong>293.8k / 181.3k / 34.8k</strong></td><td>하네스 룰 모듈화 · 과잉 추상화 억제 · 이종 모델 적대적 크로스 리뷰 프롬프트</td></tr>
      </tbody>
    </table>
  </section>

  <section id="sec-phy" class="section">
    <h2>7. 도입 전 6대 안전 가드 (Ch 11, 슬라이드 125)</h2>
    <div class="callout">
      <strong>⚠️ 슬라이드 125 핵심 경고:</strong> 메인 리포지토리에 첫날부터 Auto-merge나 강제 차단을 켜지 마세요.<br>
      <strong>① 팀 동의 먼저</strong> ➡️ <strong>② 저위험(.md) PR부터</strong> ➡️ <strong>③ 보수적 임계치(전부 medium으로 시작)</strong> ➡️ <strong>④ 라벨·작성자 화이트리스트</strong> ➡️ <strong>⑤ 야간·주말 금지(평일 10~17시 제한)</strong> ➡️ <strong>⑥ 첫 1~2주 Dry-Run</strong> 원칙을 반드시 준수해야 합니다.
    </div>
  </section>
</main>

<script>
  function showTab(i) {
    document.querySelectorAll('.tab-btn').forEach((b, idx) => b.classList.toggle('active', idx === i));
    document.querySelectorAll('.tab-panel').forEach((p, idx) => p.classList.toggle('active', idx === i));
  }
  function copyText(id, btn) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
      const orig = btn.innerText;
      btn.innerText = '✅ 복사됨!';
      setTimeout(() => btn.innerText = orig, 1800);
    });
  }
  const sections = document.querySelectorAll('section.section');
  const navLinks = document.querySelectorAll('aside.toc a');
  window.addEventListener('scroll', () => {
    let cur = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 120) cur = '#' + s.id;
    });
    if (cur) {
      navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === cur));
    }
  });
</script>
</body>
</html>
"""

with open(os.path.join(BASE_DIR, "lecture_report.html"), "w", encoding="utf-8") as f:
    f.write(REPORT_HTML)

print("Upgraded lecture_report.html with TOC sidebar, scroll-spy, tabs, and copy buttons.")
