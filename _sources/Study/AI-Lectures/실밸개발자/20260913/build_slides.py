import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
slides_dir = os.path.join(base_dir, 'slides')
os.makedirs(slides_dir, exist_ok=True)

# ==========================================
# 1. COMMON STYLES FOR SLIDES (FORMAT A)
# ==========================================
common_slide_css = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0f1a;
  font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #e6edf3;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 60px;
  overflow-x: hidden;
  opacity: 0;
  animation: fadeIn 0.35s ease forwards;
}
body.fade-out { animation: fadeOut 0.25s ease forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-10px); } }

.container {
  width: 1280px;
  max-width: 95vw;
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background: rgba(124, 58, 237, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(124, 58, 237, 0.3);
  margin-bottom: 16px;
}

.title {
  font-size: 42px;
  font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  margin-bottom: 16px;
  line-height: 1.3;
}

.subtitle {
  font-size: 17px;
  color: #8b949e;
  text-align: center;
  max-width: 860px;
  margin-bottom: 36px;
  line-height: 1.6;
}

.card {
  background: rgba(139, 148, 158, 0.04);
  border: 1px solid rgba(139, 148, 158, 0.12);
  border-radius: 16px;
  padding: 24px 28px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: transform 0.2s, border-color 0.2s;
}
.card:hover {
  border-color: rgba(124, 58, 237, 0.4);
  transform: translateY(-2px);
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  width: 100%;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}

.model-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.model-name { font-size: 20px; font-weight: 800; display: flex; align-items: center; gap: 8px; }
.model-fable { color: #f43f5e; }
.model-astra { color: #10b981; }
.model-pill {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
}
.pill-fable { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
.pill-astra { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

.prompt-box {
  background: #060911;
  border: 1px solid rgba(124, 58, 237, 0.3);
  border-radius: 12px;
  padding: 16px 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #c9d1d9;
  position: relative;
  width: 100%;
  margin: 16px 0;
  white-space: pre-wrap;
}
.copy-btn {
  position: absolute;
  top: 10px;
  right: 12px;
  background: rgba(124, 58, 237, 0.2);
  border: 1px solid rgba(124, 58, 237, 0.4);
  color: #a78bfa;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.copy-btn:hover { background: #7c3aed; color: #fff; }

.table-custom {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 14px;
}
.table-custom th {
  background: rgba(124, 58, 237, 0.12);
  color: #e6edf3;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(124, 58, 237, 0.3);
}
.table-custom td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  color: #c9d1d9;
}
.table-custom tr:hover td { background: rgba(255, 255, 255, 0.02); }

.slide-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 54px;
  background: rgba(10, 15, 26, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid rgba(124, 58, 237, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.slide-nav-inner {
  width: 1280px;
  max-width: 95vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}
.slide-nav a {
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  color: #7c3aed;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}
.slide-nav a:hover { color: #38bdf8; }
.slide-nav .nav-disabled { font-size: 14px; font-weight: 700; color: #484f58; cursor: default; }
.slide-nav .nav-center { display: flex; align-items: center; gap: 16px; }
.slide-nav .nav-center a { color: #8b949e; font-size: 13px; font-weight: 500; }
.slide-nav .nav-center a:hover { color: #e6edf3; }
.key-hint {
  font-size: 11px;
  color: #6e7681;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
'''

def write_slide(filename, title, badge_text, subtitle, body_html, prev_url, next_url, curr_slide, total_slides):
    prev_link = f'<a href="javascript:void(0)" onclick="goTo(\'{prev_url}\')">← 이전 슬라이드</a>' if prev_url else '<span class="nav-disabled">← 이전 슬라이드</span>'
    next_link = f'<a href="javascript:void(0)" onclick="goTo(\'{next_url}\')">다음 슬라이드 →</a>' if next_url else '<span class="nav-disabled">다음 슬라이드 →</span>'
    
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>{title} — 실밸개발자 AI 강의</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
{common_slide_css}
</style>
</head>
<body>
<div class="container">
  <div class="badge">{badge_text}</div>
  <h1 class="title">{title}</h1>
  <p class="subtitle">{subtitle}</p>
  {body_html}
</div>

<nav class="slide-nav">
  <div class="slide-nav-inner">
    <div class="nav-left">{prev_link}</div>
    <div class="nav-center">
      <a href="index.html">☰ 전체 목차</a>
      <span style="color:#484f58;">|</span>
      <span style="color:#8b949e; font-size:13px;">{curr_slide} / {total_slides}</span>
      <span class="key-hint">좌우 방향키 [←] [→]</span>
    </div>
    <div class="nav-right">{next_link}</div>
  </div>
</nav>

<script>
function goTo(url) {{
  if(!url) return;
  document.body.classList.add('fade-out');
  setTimeout(function() {{ window.location.href = url; }}, 220);
}}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowLeft' && '{prev_url}') goTo('{prev_url}');
  if (e.key === 'ArrowRight' && '{next_url}') goTo('{next_url}');
  if (e.key === 'Home') goTo('index.html');
}});
function copyPrompt(btn) {{
  const code = btn.parentElement.innerText.replace('복사', '').trim();
  navigator.clipboard.writeText(code).then(() => {{
    const orig = btn.innerText;
    btn.innerText = '복사됨! ✓';
    btn.style.background = '#10b981';
    btn.style.color = '#fff';
    setTimeout(() => {{
      btn.innerText = orig;
      btn.style.background = '';
      btn.style.color = '';
    }}, 1800);
  }});
}}
</script>
</body>
</html>'''
    with open(os.path.join(slides_dir, filename), 'w', encoding='utf-8') as f:
        f.write(html)

slides_data = [
    {
        "filename": "01_intro.html",
        "badge": "01. Introduction",
        "title": "이틀 간격의 두 거인: Fable 5.1 vs GPT-6 Astra",
        "subtitle": "2026년 9월 초, Anthropic과 OpenAI의 최신 플래그십이 이틀 간격으로 격돌했습니다. 벤치마크 점수가 아닌 실제 프로덕션 서비스에서의 실전 결과를 비교합니다.",
        "body": '''
        <div class="grid-2">
          <div class="card" style="border-left: 4px solid #f43f5e;">
            <div class="model-header">
              <div class="model-name model-fable">Anthropic Claude Fable 5.1</div>
              <span class="model-pill pill-fable">2026. 09. 01 출시</span>
            </div>
            <p style="color:#c9d1d9; line-height:1.7; margin-bottom:14px;">
              엔트로픽의 최고봉 추론 모델. 깊이 있는 프로파일링, 시스템 최적화, 정밀한 버그 추적 및 장시간 사고 루프에 특화.
            </p>
            <ul style="color:#8b949e; font-size:14px; line-height:1.8; padding-left:18px;">
              <li><strong>실험 하네스:</strong> Claude Code (터미널 자율 에이전트)</li>
              <li><strong>강점:</strong> 코드 집착력, 보수적 안전성, P50/P90 최적화</li>
              <li><strong>특이사항:</strong> 긴 생각 시간, 무음 영상 생성</li>
            </ul>
          </div>
          <div class="card" style="border-left: 4px solid #10b981;">
            <div class="model-header">
              <div class="model-name model-astra">OpenAI GPT-6 Astra</div>
              <span class="model-pill pill-astra">2026. 09. 03 출시</span>
            </div>
            <p style="color:#c9d1d9; line-height:1.7; margin-bottom:14px;">
              OpenAI의 차세대 복합 에이전트 모델. 프로덕트 기획, UX/UI 리디자인, 3D 가상화, 멀티모달 오디오 생성에 압도적 창의성 발휘.
            </p>
            <ul style="color:#8b949e; font-size:14px; line-height:1.8; padding-left:18px;">
              <li><strong>실험 하네스:</strong> Codex CLI (Fast Mode 탑재)</li>
              <li><strong>강점:</strong> Home 화면 신설, 4단계 워크플로우, 음성/음악 탑재</li>
              <li><strong>특이사항:</strong> 최적화 폭 미미 (1%), 높은 토큰 소모</li>
            </ul>
          </div>
        </div>
        <div class="card" style="margin-top:24px; width:100%; text-align:center; background:rgba(56,189,248,0.06); border-color:rgba(56,189,248,0.2);">
          <span style="font-size:15px; color:#38bdf8; font-weight:700;">🎯 검증 대상 서비스: AutoKliq</span>
          <span style="color:#8b949e; font-size:14px; margin-left:12px;">3개월간 실서비스 중인 수만 줄 규모의 AI 유튜브 썸네일 생성 및 인텔리전스 플랫폼</span>
        </div>
        '''
    },
    {
        "filename": "02_summary.html",
        "badge": "02. Executive Summary",
        "title": "핵심 결론 & AI 실전 활용 5대 노하우",
        "subtitle": "영상에서 실리콘밸리 메타 엔지니어가 전하고자 한 가장 중요한 결론과 현업 개발자를 위한 AI 활용 법칙입니다.",
        "body": '''
        <div class="grid-3" style="margin-bottom:20px;">
          <div class="card">
            <div style="font-size:24px; margin-bottom:10px;">🏆</div>
            <h3 style="font-size:18px; color:#38bdf8; margin-bottom:8px;">1. 도메인별 승자 분립</h3>
            <p style="font-size:14px; color:#8b949e; line-height:1.6;">
              UI/UX 리디자인과 3D 공간화는 <strong>Astra</strong> 압승, 딥 시스템 최적화와 프로파일링은 <strong>Fable</strong> 판정승. 단일 최강 모델은 없습니다.
            </p>
          </div>
          <div class="card">
            <div style="font-size:24px; margin-bottom:10px;">🛡️</div>
            <h3 style="font-size:18px; color:#a78bfa; margin-bottom:8px;">2. 하네스가 결과를 좌우</h3>
            <p style="font-size:14px; color:#8b949e; line-height:1.6;">
              모델 자체보다 이를 감싸는 하네스(Claude Code vs Codex)의 툴 제어, 프롬프트 캐싱, 피드백 루프가 최종 산출물 완성도를 결정합니다.
            </p>
          </div>
          <div class="card">
            <div style="font-size:24px; margin-bottom:10px;">🤝</div>
            <h3 style="font-size:18px; color:#f43f5e; margin-bottom:8px;">3. 협업의 역설 (천재 둘의 함정)</h3>
            <p style="font-size:14px; color:#8b949e; line-height:1.6;">
              둘이 상호 리뷰를 거치면 가장 참신했던 기능(검색바 등)이 타협되어 사라집니다. 인간의 확고한 조타(Steering) 없는 협업은 퇴보합니다.
            </p>
          </div>
        </div>
        <div class="card" style="width:100%;">
          <h3 style="font-size:16px; color:#e6edf3; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
            <span style="color:#10b981;">⚡</span> 실무자를 위한 즉각 적용 액션 아이템
          </h3>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; font-size:13px; color:#c9d1d9;">
            <div style="background:rgba(0,0,0,0.3); padding:12px 16px; border-radius:8px;">
              <strong style="color:#38bdf8;">Effort 레벨의 유연한 조절:</strong> 무조건 Max 고집 금지. Fast 모드/Medium으로도 충분한 태스크가 많으며 토큰 비용 50% 절감 가능.
            </div>
            <div style="background:rgba(0,0,0,0.3); padding:12px 16px; border-radius:8px;">
              <strong style="color:#a78bfa;">Negative 제약조건 필수화:</strong> "지켜야 할 기존 기능 유지", "품질 저하 시 보고서 명시" 룰로 AI의 편법/해킹 방지.
            </div>
          </div>
        </div>
        '''
    },
    {
        "filename": "03_review113.html",
        "badge": "03. Community Reality",
        "title": "113개 실전 리뷰 분석: 왜 말이 정반대일까?",
        "subtitle": "출시 일주일간 레딧, X, 깃허브, 한국 커뮤니티의 113개 리뷰를 전수 조사한 결과, 완전히 상반된 반응이 공존했습니다.",
        "body": '''
        <table class="table-custom">
          <thead>
            <tr>
              <th style="width:20%;">평가 항목</th>
              <th style="width:40%; color:#fb7185;">🔴 부정 / 우려 리뷰</th>
              <th style="width:40%; color:#34d399;">🟢 긍정 / 찬사 리뷰</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>토큰 소모량</strong></td>
              <td>"1시간 만에 주간 할당량이 통째로 증발했다"</td>
              <td>"동일 작업 기준 Fable 5.1이 5.0보다 훨씬 절약된다"</td>
            </tr>
            <tr>
              <td><strong>Astra 갈아타기</strong></td>
              <td>"Astra는 기대에 못 미치는 쓰레기였다"</td>
              <td>"회사 메인 AI 전면 교체! Fable이 바보처럼 느껴진다"</td>
            </tr>
            <tr>
              <td><strong>글쓰기 / 리포트</strong></td>
              <td>"Fable 5.1 문장이 난해해져 읽기 힘들어졌다"</td>
              <td>"문맥 파악력과 디테일한 서술력이 극적으로 상승했다"</td>
            </tr>
            <tr>
              <td><strong>Effort 비용</strong></td>
              <td>"Medium만 썼는데 2턴 만에 주간 캡 도달"</td>
              <td>"추론 레벨을 높일수록 헛발질이 줄어 전체 비용 절감"</td>
            </tr>
            <tr>
              <td><strong>안전성 검사</strong></td>
              <td>"Fable 안전성 필터가 너무 민감해 Opus로 강제 폴백"</td>
              <td>"거부 없이 복잡한 대규모 리팩토링을 완벽 수행"</td>
            </tr>
          </tbody>
        </table>
        <div class="card" style="width:100%; margin-top:16px; background:rgba(124,58,237,0.06); border-color:rgba(124,58,237,0.25);">
          <strong style="color:#a78bfa;">💡 시니어 엔지니어의 해석:</strong>
          <span style="color:#c9d1d9; font-size:14px; margin-left:8px;">
            평가가 극단적으로 갈린 이유는 <strong>"실험 조건(서브에이전트 수, 문서 vs 코드, 시스템 프롬프트 개입)이 완전히 달랐기 때문"</strong>이며, 조건을 맞춰도 "말투가 거슬린다", "바보 같다"는 <strong>주관적 편향</strong>이 남기 때문입니다.
          </span>
        </div>
        '''
    },
    {
        "filename": "04_experiment_setup.html",
        "badge": "04. Methodology",
        "title": "실험 설계: herdr 듀얼 Pane 동시 주입",
        "subtitle": "인간의 중간 개입과 편향을 100% 배제하기 위해, 동일 프롬프트를 두 프로세스에 Zero-shot으로 동시 브로드캐스트했습니다.",
        "body": '''
        <div class="card" style="width:100%; margin-bottom:24px;">
          <h3 style="font-size:16px; color:#38bdf8; margin-bottom:12px;">🖥️ herdr 기반 병렬 오케스트레이션 아키텍처</h3>
          <div style="background:#060911; padding:20px; border-radius:10px; font-family:'JetBrains Mono',monospace; font-size:13px; line-height:1.8; color:#a78bfa;">
            [ Main Orchestrator (herdr) ]<br>
            &nbsp;&nbsp;├── Terminal Pane A: <strong>Claude Code</strong> (Fable 5.1 Max) ──► AutoKliq Local Env<br>
            &nbsp;&nbsp;└── Terminal Pane B: <strong>Codex CLI</strong> (GPT-6 Astra Max / Fast Mode) ──► AutoKliq Local Env<br>
            <span style="color:#6e7681;"># Zero-Shot 1회 주입 | 중간 질문 불허 | 자율 실행 & 셀프 테스팅 검증 강제</span>
          </div>
        </div>
        <div class="grid-3">
          <div class="card">
            <h4 style="color:#e6edf3; font-size:15px; margin-bottom:6px;">1. 동일 소스코드</h4>
            <p style="color:#8b949e; font-size:13px;">실제 서비스 AutoKliq의 전체 코드베이스를 복사 없이 동일한 로컬 상태에서 시작.</p>
          </div>
          <div class="card">
            <h4 style="color:#e6edf3; font-size:15px; margin-bottom:6px;">2. Zero-shot 1회 주입</h4>
            <p style="color:#8b949e; font-size:13px;">대화형 핑퐁 없이 단 한 번의 프롬프트로 최종 산출물(MP4, 빌드, 리팩토링)까지 자율 완수.</p>
          </div>
          <div class="card">
            <h4 style="color:#e6edf3; font-size:15px; margin-bottom:6px;">3. Effort 통일</h4>
            <p style="color:#8b949e; font-size:13px;">두 모델 모두 Max Reasoning Effort 적용 (Astra는 Fast Mode 설정 유지).</p>
          </div>
        </div>
        '''
    },
    {
        "filename": "05_round1_video.html",
        "badge": "05. Round 1",
        "title": "Round 1 · 영상 제작 (온보딩 45초 & 홍보 15초)",
        "subtitle": "앱을 로컬에서 띄워 직접 사용해보고 제품을 이해한 뒤, 순수 코드로 MP4 영상을 렌더링하도록 지시했습니다.",
        "body": '''
        <div class="prompt-box">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>당신은 오토클릭(AutoKliq)의 실제 서비스 소스코드를 가지고 있습니다.
1. 먼저 로컬 환경에서 앱을 직접 띄우고 실제로 사용해 보세요.
2. 제품의 사용자 경험과 핵심 가치를 파악한 뒤, 다음 두 가지 영상을 순수 코드로 작성하여 MP4 파일로 렌더링하세요.
   - 제품을 소개하는 온보딩 영상 (45초 분량) 1편
   - 핵심 기능을 임팩트 있게 보여주는 짧은 컷의 홍보 영상 (15초 분량) 1편</div>

        <div class="grid-2" style="margin-top:16px;">
          <div class="card">
            <div class="model-header">
              <div class="model-name model-fable">Fable 5.1 결과</div>
              <span style="color:#fb7185; font-size:13px; font-weight:700;">깔끔함 / 무음 (Silent)</span>
            </div>
            <ul style="color:#8b949e; font-size:14px; line-height:1.7; padding-left:18px;">
              <li>스텝 1~6단계 흐름을 시각적으로 정갈하게 렌더링</li>
              <li>음성 내레이션 및 배경음악이 일절 없는 <strong>무음 비디오</strong></li>
              <li>화면 전환과 타이포그래피는 매우 안정적</li>
            </ul>
          </div>
          <div class="card" style="border-color:rgba(16,185,129,0.3);">
            <div class="model-header">
              <div class="model-name model-astra">Astra 결과 (승리 🏆)</div>
              <span style="color:#34d399; font-size:13px; font-weight:700;">내레이션 · 자막 · BGM 완비</span>
            </div>
            <ul style="color:#8b949e; font-size:14px; line-height:1.7; padding-left:18px;">
              <li>자연스러운 한국어 TTS 보이스오버 탑재</li>
              <li>음악과 타이밍이 일치하는 자막 인라인 애니메이션</li>
              <li>비용은 Fast Mode로 약 2배 소모, 시간은 비슷</li>
            </ul>
          </div>
        </div>
        '''
    },
    {
        "filename": "06_round2_optimization.html",
        "badge": "06. Round 2",
        "title": "Round 2 · 성능 최적화 (\"생성 시간을 절반으로\")",
        "subtitle": "느린 썸네일 생성 파이프라인을 50% 단축하라. 단, 필수 기능을 훼손하지 말고 품질 저하 시 보고서에 명시하라.",
        "body": '''
        <div class="prompt-box">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>썸네일 생성이 너무 느립니다. 이를 절반(50%)으로 줄여주세요.
[지켜야 할 규칙]
1. 기존에 정상적으로 동작하는 필수 기능들은 하나도 변경하거나 누락하지 마세요.
2. 만약 실행 시간 단축을 위해 이미지/텍스트의 품질을 의도적으로 떨어뜨리는 변경을 했다면, 반드시 최종 보고서에 어떤 품질을 희생했는지 명시하세요.</div>

        <div class="grid-2" style="margin-top:16px;">
          <div class="card" style="border-color:rgba(244,63,94,0.3);">
            <div class="model-header">
              <div class="model-name model-fable">Fable 5.1 (판정승 🏆)</div>
              <span class="model-pill pill-fable">$47 · 1시간 30분 소요</span>
            </div>
            <ul style="color:#8b949e; font-size:14px; line-height:1.7; padding-left:18px;">
              <li><strong>성능 개선율:</strong> 시나리오별 2~6% 단축 (P50/P90 20~30초 실질 단축)</li>
              <li>1시간 30분 동안 집요하게 프로파일링하고 실제 병목 제거</li>
              <li>품질 저하 없는 정밀한 백엔드/파이프라인 리팩토링 달성</li>
            </ul>
          </div>
          <div class="card">
            <div class="model-header">
              <div class="model-name model-astra">Astra 결과</div>
              <span class="model-pill pill-astra">$22 · 24분 소요</span>
            </div>
            <ul style="color:#8b949e; font-size:14px; line-height:1.7; padding-left:18px;">
              <li><strong>성능 개선율:</strong> 평균 1% 단축 (~10초 단축에 불과)</li>
              <li>사람이 체감하기에 기존과 거의 동일한 속도</li>
              <li>시간을 덜 쓰고 빠르게 끝냈으나 깊이 있는 병목 해소 실패</li>
            </ul>
          </div>
        </div>
        '''
    },
    {
        "filename": "07_round3_ui_redesign.html",
        "badge": "07. Round 3",
        "title": "Round 3 · UI 전면 리디자인 (사람 & 에이전트 공존 UI)",
        "subtitle": "사람도 쓰고 미래의 에이전트도 쓰기 좋게 처음부터 다시 설계하라. 사소한 질문 없이 자율적으로 완수하라.",
        "body": '''
        <div class="prompt-box">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>오토클릭의 UI를 전면적으로 다시 디자인하세요.
우리가 제품을 완전히 다시 설계한다면 어떤 모습이어야 하는지 확인하고 싶습니다.
[필수 요구사항]
1. 사람이 쓰기에도 좋아야 하고, 앞으로 이 화면을 다룰 '에이전트'가 쓰기에도 좋아야 합니다.
2. 기존에 잘 작동하던 기능이 사라져서는 안 되며, 변경 후 실제로 에러 없이 돌아가는지 철저히 테스트하세요.
3. 시간제한은 없으며 중간에 질문하지 말고 스스로 판단하여 끝까지 진행하세요.</div>

        <div class="grid-2" style="margin-top:16px;">
          <div class="card">
            <div class="model-header">
              <div class="model-name model-fable">Fable 5.1 (보수적 개선)</div>
            </div>
            <p style="color:#8b949e; font-size:14px; line-height:1.6;">
              기존 단일 폼을 3개 섹션으로 분할하고 상단 탭을 정리하는 수준. 구조적인 혁신이나 새로운 경험 창출 없이 무난한 보수적 리팩토링에 그침.
            </p>
          </div>
          <div class="card" style="border-color:rgba(16,185,129,0.4); background:rgba(16,185,129,0.03);">
            <div class="model-header">
              <div class="model-name model-astra">Astra (압도적 압승 🏆)</div>
              <span class="model-pill pill-astra">비용/시간 동일 (~$25, ~30분)</span>
            </div>
            <ul style="color:#c9d1d9; font-size:14px; line-height:1.7; padding-left:18px;">
              <li><strong>전용 Home 화면 신설:</strong> "아이디어에서 한 장으로" 컨셉 대시보드</li>
              <li><strong>4단계 선형 마법사:</strong> Story ➔ Expression ➔ Asset/Ref ➔ Pre-check</li>
              <li><strong>프로젝트 검색바 & 필터:</strong> 제목/컨셉으로 이전 작업 즉시 탐색</li>
            </ul>
          </div>
        </div>
        '''
    },
    {
        "filename": "08_round4_3d_repo.html",
        "badge": "08. Round 4",
        "title": "Round 4 · 저장소를 3D 공간으로 걸어다니기",
        "subtitle": "복잡한 오토클릭 코드베이스를 신규 온보딩 개발자가 직관적으로 이해할 수 있도록 3D 인터랙티브 공간으로 모델링했습니다.",
        "body": '''
        <div class="grid-2">
          <div class="card">
            <div class="model-header">
              <div class="model-name model-fable">Fable 5.1 ($11, 29분)</div>
            </div>
            <ul style="color:#8b949e; font-size:14px; line-height:1.7; padding-left:18px;">
              <li>App, Lib, Shared 폴더를 디스트릭트 구역으로 분할</li>
              <li>컴포넌트/API를 색상 블록으로 표현, WASD 키보드 조작</li>
              <li>일반적인 3D 맵 수준으로 독창적인 메타포는 부재</li>
            </ul>
          </div>
          <div class="card" style="border-color:rgba(16,185,129,0.4);">
            <div class="model-header">
              <div class="model-name model-astra">Astra ($24, 35분 — 압승 🏆)</div>
            </div>
            <ul style="color:#c9d1d9; font-size:14px; line-height:1.7; padding-left:18px;">
              <li><strong>8개 아키텍처 구역:</strong> Foundation, Intelligence, Pipeline 등</li>
              <li><strong>건물 높이 = 코드 라인 수 (LOC)</strong> 시각 메타포 탑재</li>
              <li><strong>'썸네일의 여정' 투어:</strong> Request ➔ Cloud Task ➔ Vision ➔ DB 7단계 가이드</li>
            </ul>
          </div>
        </div>
        <div class="card" style="margin-top:20px; width:100%;">
          <h4 style="color:#e6edf3; font-size:15px; margin-bottom:10px;">📊 4개 라운드 누적 총비용 및 시간 요약</h4>
          <div style="display:flex; justify-content:space-around; text-align:center;">
            <div>
              <div style="font-size:24px; font-weight:800; color:#f43f5e;">$125</div>
              <div style="font-size:13px; color:#8b949e;">Fable 5.1 총비용 (시간 다소 김)</div>
            </div>
            <div style="border-right:1px solid rgba(255,255,255,0.1);"></div>
            <div>
              <div style="font-size:24px; font-weight:800; color:#10b981;">$134</div>
              <div style="font-size:13px; color:#8b949e;">Astra 총비용 (Fast Mode 적용)</div>
            </div>
          </div>
        </div>
        '''
    },
    {
        "filename": "09_round5_collaboration.html",
        "badge": "09. Round 5",
        "title": "Round 5 · 다중 에이전트 협업의 실체 (천재 둘의 역설)",
        "subtitle": "Astra(메인)와 Fable(리뷰어)이 의도 ➔ 플래닝 ➔ 구현 ➔ 검증 ➔ 보고 단계별로 서로의 코드를 상호 검증시켰습니다.",
        "body": '''
        <div class="card" style="width:100%; margin-bottom:20px; border-left:4px solid #f97316;">
          <h3 style="color:#fdba74; font-size:16px; margin-bottom:8px;">⚠️ 다중 에이전트 상호 협업의 충격적 결과</h3>
          <p style="color:#c9d1d9; font-size:14px; line-height:1.7;">
            단일 모델 실행 대비 드라마틱한 품질 개선은 전혀 없었으며, 상호 합의 과정에서 날카롭고 참신했던 기능(프로젝트 검색바 등)이 삭제되고 무난한 평균으로 퇴보했습니다. 반면 토큰 비용은 단일 과제당 <strong>$108, $62, $142</strong>로 폭증했습니다.
          </p>
        </div>
        <div class="grid-3">
          <div class="card">
            <h4 style="color:#38bdf8; margin-bottom:6px;">영상 협업</h4>
            <p style="color:#8b949e; font-size:13px;">Astra 영상에 음악을 입히는 미세 수정 외 큰 변화 없음.</p>
          </div>
          <div class="card">
            <h4 style="color:#a78bfa; margin-bottom:6px;">최적화 협업</h4>
            <p style="color:#8b949e; font-size:13px;">개선율 2~3% 수준에 정체. 단독 Fable보다 최적화 폭 감소.</p>
          </div>
          <div class="card">
            <h4 style="color:#f43f5e; margin-bottom:6px;">UI 리디자인 협업</h4>
            <p style="color:#8b949e; font-size:13px;">Astra의 홈과 Fable의 구식 입력 폼이 짬뽕되어 검색바 실종.</p>
          </div>
        </div>
        <div class="card" style="margin-top:20px; width:100%; text-align:center;">
          <span style="font-size:15px; color:#e6edf3; font-weight:700;">💬 메타 엔지니어의 핵심 교훈:</span>
          <span style="color:#8b949e; font-size:14px; margin-left:8px;">"인간의 단호한 방향 제시와 조타(Steering)가 빠진 자율 협업은 평균으로의 수렴일 뿐이다."</span>
        </div>
        '''
    },
    {
        "filename": "10_agentic_engineering.html",
        "badge": "10. Engineering Lessons",
        "title": "Agentic & Harness Engineering 5대 인사이트",
        "subtitle": "단순한 프롬프트 입력을 넘어 프로덕션 레벨에서 에이전트 시스템을 구축할 때 반드시 챙겨야 할 방법론입니다.",
        "body": '''
        <div class="grid-2">
          <div class="card">
            <h4 style="color:#38bdf8; font-size:16px; margin-bottom:8px;">1. 모델과 하네스의 결합성 이해</h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              우리가 체감하는 AI의 성능은 [모델 + 툴 샌드박스 + 프롬프트 캐싱 + 컨텍스트 압축]의 결합체입니다. 하네스를 고도화하지 않고 모델 탓만 해서는 안 됩니다.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#a78bfa; font-size:16px; margin-bottom:8px;">2. Negative Constraint (품질 가드레일)</h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              "품질을 낮췄다면 보고서에 적어라"처럼 AI가 목표 수치를 맞추기 위해 본질을 왜곡하는 편법을 방지하는 투명성 조항이 필수적입니다.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#34d399; font-size:16px; margin-bottom:8px;">3. Dual-User Framing (사람 + AI)</h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              앞으로의 모든 소프트웨어는 사람뿐만 아니라 에이전트가 DOM 트리와 API를 통해 쉽게 조작할 수 있는 구조(Accessible & Agentic)로 설계되어야 합니다.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#f43f5e; font-size:16px; margin-bottom:8px;">4. Human Gatekeeper (Phase Gate)</h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              전체 루프를 방임하지 말고, <strong>의도 정의(Intent)</strong>와 <strong>최종 배포(Deploy)</strong> 단계에서 인간이 컨펌하는 체크포인트를 두어야 비용과 품질이 보장됩니다.
            </p>
          </div>
        </div>
        '''
    },
    {
        "filename": "11_github_resources.html",
        "badge": "11. Resources",
        "title": "공유된 핵심 리소스 & 깃허브 아키텍처 분석",
        "subtitle": "영상에서 강사가 직접 사용하거나 언급한 핵심 오픈소스 및 공식 레퍼런스 모음입니다.",
        "body": '''
        <div class="grid-2">
          <div class="card">
            <h4 style="color:#a78bfa; margin-bottom:6px;"><a href="https://github.com/herdrdev/herdr" target="_blank" style="color:#a78bfa; text-decoration:none;">herdr (GitHub) ↗</a></h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              다중 CLI 세션을 오케스트레이션하는 터미널 매니저. 여러 에이전트 Pane을 생성하고 동일 입력을 브로드캐스트하여 동시 A/B 테스트에 최적화.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#38bdf8; margin-bottom:6px;"><a href="https://github.com/openai/codex" target="_blank" style="color:#38bdf8; text-decoration:none;">Codex CLI (OpenAI) ↗</a></h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              OpenAI의 자율 코딩 에이전트. 로컬 샌드박스 실행, 파일 트리 고속 인덱싱, Fast/High 추론 모드 선택 지원.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#f43f5e; margin-bottom:6px;"><a href="https://claude.com/claude-code" target="_blank" style="color:#f43f5e; text-decoration:none;">Claude Code (Anthropic) ↗</a></h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              앤트로픽 공식 CLI. 프로젝트 전역 심볼 검색, 정밀 리팩토링, 안정적 장시간 추론 최적화.
            </p>
          </div>
          <div class="card">
            <h4 style="color:#34d399; margin-bottom:6px;"><a href="https://autokliq.com" target="_blank" style="color:#34d399; text-decoration:none;">AutoKliq (SaaS) ↗</a></h4>
            <p style="color:#8b949e; font-size:13px; line-height:1.6;">
              실제 3개월간 운영 중인 AI 썸네일 생성 서비스. 복잡한 실제 프로덕션 코드를 테스트베드로 활용.
            </p>
          </div>
        </div>
        '''
    },
    {
        "filename": "12_next_actions.html",
        "badge": "12. Next Actions",
        "title": "Next Actions & Deep Research 추천 소스",
        "subtitle": "이 강의를 마친 후 실전 역량을 한 단계 끌어올리기 위해 지금 당장 시작해야 할 실행 계획과 추천 리소스입니다.",
        "body": '''
        <div class="grid-2">
          <div class="card">
            <h3 style="color:#38bdf8; font-size:16px; margin-bottom:12px;">📌 그룹장 맞춤형 실행 과제 (Mobile SW & Physical Layer)</h3>
            <ul style="color:#c9d1d9; font-size:13px; line-height:1.8; padding-left:18px;">
              <li><strong>AST + Grep 기반 레지스터 맵 파이프라인 실험:</strong> herdr 로컬 세팅 후 Claude Code와 Codex를 동시 띄워 C/C++ 레거시 코드베이스의 심벌 추출 및 2nd Brain 인덱싱 고도화 테스트.</li>
              <li><strong>AI-native HW 요구사항 매핑:</strong> 3대 프로덕션 프롬프트 패턴을 응용하여 HW 변경 사항 리스트와 JIRA 티켓을 자동 대조/검증하는 에이전트 프롬프트 템플릿 설계.</li>
              <li><strong>협업 가드레일 기반 코드 리뷰 자동화:</strong> 멀티 에이전트 상호 리뷰 시 "기존 물리 계층 최적화 로직 보존 의무" 등 엄격한 Negative 제약조건 주입 훈련.</li>
            </ul>
          </div>
          <div class="card">
            <h3 style="color:#a78bfa; font-size:16px; margin-bottom:12px;">🌐 Deep Research 추천 채널 & 사이트</h3>
            <ul style="color:#8b949e; font-size:13px; line-height:1.8; padding-left:18px;">
              <li><strong style="color:#e6edf3;">실밸개발자 (YouTube):</strong> 메타 엔지니어의 에이전틱 엔지니어링 실전 가이드</li>
              <li><strong style="color:#e6edf3;">AI Jason (YouTube):</strong> LangGraph, CrewAI 기반 멀티에이전트 패턴 분석</li>
              <li><strong style="color:#e6edf3;">OpenCode (opencode.ai):</strong> 중립 하네스 기반 순수 코딩 LLM 벤치마크</li>
              <li><strong style="color:#e6edf3;">Aider (aider.chat):</strong> Git 기반 페어 프로그래밍 아키텍처 공식 문서</li>
            </ul>
          </div>
        </div>
        <div class="card" style="margin-top:20px; width:100%; text-align:center; background:rgba(16,185,129,0.06); border-color:rgba(16,185,129,0.2);">
          <span style="font-size:15px; color:#34d399; font-weight:700;">🚀 강의 자료 완독 완료!</span>
          <a href="index.html" style="color:#38bdf8; text-decoration:underline; margin-left:12px; font-weight:600;">전체 허브로 돌아가기</a>
          <span style="color:#8b949e; margin:0 8px;">|</span>
          <a href="../lecture_report.html" style="color:#a78bfa; text-decoration:underline; font-weight:600;">싱글 대시보드 리포트(Format B) 보기</a>
        </div>
        '''
    }
]

total = len(slides_data)
for i, s in enumerate(slides_data):
    prev_url = slides_data[i-1]['filename'] if i > 0 else None
    next_url = slides_data[i+1]['filename'] if i < total - 1 else None
    write_slide(
        filename=s['filename'],
        title=s['title'],
        badge_text=s['badge'],
        subtitle=s['subtitle'],
        body_html=s['body'],
        prev_url=prev_url,
        next_url=next_url,
        curr_slide=i+1,
        total_slides=total
    )
print(f"Generated {total} individual slide HTMLs.")

# ==========================================
# 2. GENERATE INDEX.HTML (FORMAT A HUB)
# ==========================================
cards_html = ""
for i, s in enumerate(slides_data):
    cards_html += f'''
    <a href="{s['filename']}" class="card hub-card">
      <div style="font-size:12px; font-weight:700; color:#a78bfa; margin-bottom:8px;">{s['badge']}</div>
      <h3 style="font-size:17px; font-weight:800; color:#e6edf3; margin-bottom:8px; line-height:1.4;">{s['title']}</h3>
      <p style="font-size:13px; color:#8b949e; line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">{s['subtitle']}</p>
      <div style="margin-top:14px; display:flex; align-items:center; justify-content:space-between;">
        <span style="font-size:12px; color:#6e7681;">Slide #{i+1}</span>
        <span style="font-size:13px; color:#38bdf8; font-weight:700;">보기 →</span>
      </div>
    </a>
    '''

index_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>메타 시니어 엔지니어의 Fable 5.1 vs GPT-6 Astra 실전 비교 — 슬라이드 허브</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
{common_slide_css}
.hub-card {{
  text-decoration: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}}
.hub-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
}}
</style>
</head>
<body>
<div class="container" style="padding-bottom:80px;">
  <div class="badge">Lecture Deck Hub</div>
  <h1 class="title">Fable 5.1 vs GPT-6 Astra 실전 비교</h1>
  <p class="subtitle">
    실밸개발자 (메타 시니어 엔지니어) 강의 전수 요약 & 에이전틱 엔지니어링 분석 슬라이드 덱 (총 {total}장)<br>
    <span style="color:#38bdf8; font-size:14px; font-weight:600;">[Format A: 인터랙티브 슬라이드 세트]</span>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="../lecture_report.html" style="color:#a78bfa; font-size:14px; font-weight:600; text-decoration:underline;">[Format B: 싱글 대시보드 리포트 바로가기]</a>
  </p>

  <div class="hub-grid">
    {cards_html}
  </div>

  <div style="margin-top:40px; text-align:center;">
    <a href="01_intro.html" style="background:linear-gradient(135deg,#7c3aed,#38bdf8); color:#fff; text-decoration:none; padding:14px 36px; border-radius:9999px; font-weight:800; font-size:16px; box-shadow:0 8px 24px rgba(124,58,237,0.3); display:inline-block;">
      첫 슬라이드부터 시작하기 ▶
    </a>
  </div>
</div>
</body>
</html>'''

with open(os.path.join(slides_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Generated slides/index.html hub.")


# ==========================================
# 3. GENERATE LECTURE_REPORT.HTML (FORMAT B)
# ==========================================
report_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fable 5.1 vs GPT-6 Astra 실전 비교 — 인터랙티브 심층 리포트</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: #0a0f1a;
  color: #e6edf3;
  font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.7;
  overflow-x: hidden;
}}
a {{ color: #38bdf8; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* Layout */
.app-container {{
  display: flex;
  min-height: 100vh;
}}
.sidebar {{
  width: 320px;
  background: #080c15;
  border-right: 1px solid rgba(124, 58, 237, 0.15);
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  padding: 32px 24px;
  overflow-y: auto;
  z-index: 100;
}}
.main-content {{
  margin-left: 320px;
  flex: 1;
  padding: 48px 64px;
  max-width: 1100px;
}}

/* Sidebar Elements */
.side-title {{
  font-size: 16px;
  font-weight: 800;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}}
.side-sub {{
  font-size: 12px;
  color: #8b949e;
  margin-bottom: 24px;
}}
.toc-list {{ list-style: none; }}
.toc-item {{ margin-bottom: 8px; }}
.toc-link {{
  font-size: 13px;
  color: #8b949e;
  display: block;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}}
.toc-link:hover, .toc-link.active {{
  background: rgba(124, 58, 237, 0.15);
  color: #a78bfa;
  font-weight: 700;
  text-decoration: none;
}}

/* Hero Section */
.hero {{
  margin-bottom: 48px;
  padding-bottom: 32px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}
.hero-badge {{
  display: inline-block;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  background: rgba(124, 58, 237, 0.15);
  color: #a78bfa;
  border: 1px solid rgba(124, 58, 237, 0.3);
  margin-bottom: 16px;
}}
.hero-title {{
  font-size: 38px;
  font-weight: 900;
  line-height: 1.3;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 40%, #8b949e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.hero-meta {{
  font-size: 14px;
  color: #8b949e;
  display: flex;
  gap: 16px;
  align-items: center;
}}

/* Cards & Sections */
.section {{
  margin-bottom: 64px;
  scroll-margin-top: 40px;
}}
.section-title {{
  font-size: 24px;
  font-weight: 800;
  color: #e6edf3;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.section-title::before {{
  content: '';
  width: 4px;
  height: 24px;
  background: linear-gradient(to bottom, #7c3aed, #38bdf8);
  border-radius: 2px;
}}

.report-card {{
  background: rgba(139, 148, 158, 0.04);
  border: 1px solid rgba(139, 148, 158, 0.12);
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 20px;
  backdrop-filter: blur(12px);
}}

.grid-2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}}

/* Prompt Block */
.prompt-container {{
  background: #060911;
  border: 1px solid rgba(124, 58, 237, 0.3);
  border-radius: 10px;
  padding: 16px 20px;
  position: relative;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.7;
  color: #c9d1d9;
  margin: 16px 0;
  white-space: pre-wrap;
}}
.copy-btn {{
  position: absolute;
  top: 10px;
  right: 12px;
  background: rgba(124, 58, 237, 0.2);
  border: 1px solid rgba(124, 58, 237, 0.4);
  color: #a78bfa;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}}
.copy-btn:hover {{ background: #7c3aed; color: #fff; }}

/* Comparison Table */
.cmp-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 14px;
}}
.cmp-table th {{
  background: rgba(124, 58, 237, 0.15);
  color: #e6edf3;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(124, 58, 237, 0.3);
}}
.cmp-table td {{
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  color: #c9d1d9;
}}
.cmp-table tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}

.badge-win {{
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid rgba(16, 185, 129, 0.3);
}}
</style>
</head>
<body>
<div class="app-container">
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="side-title">실밸개발자 심층 리포트</div>
    <div class="side-sub">Fable 5.1 vs GPT-6 Astra 실전 분석</div>
    <div style="margin-bottom:16px;">
      <a href="slides/index.html" style="display:inline-block; font-size:12px; padding:6px 12px; border-radius:6px; background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); font-weight:700;">
        📺 슬라이드 모드 (Format A) 열기
      </a>
    </div>
    <ul class="toc-list">
      <li class="toc-item"><a href="#summary" class="toc-link">1. Executive Summary</a></li>
      <li class="toc-item"><a href="#reviews" class="toc-link">2. 113개 실전 리뷰 분석</a></li>
      <li class="toc-item"><a href="#experiment" class="toc-link">3. 실험 환경 및 조건</a></li>
      <li class="toc-item"><a href="#round1" class="toc-link">4. Round 1: 영상 제작</a></li>
      <li class="toc-item"><a href="#round2" class="toc-link">5. Round 2: 성능 최적화</a></li>
      <li class="toc-item"><a href="#round3" class="toc-link">6. Round 3: UI 리디자인</a></li>
      <li class="toc-item"><a href="#round4" class="toc-link">7. Round 4: 3D 저장소 탐색</a></li>
      <li class="toc-item"><a href="#round5" class="toc-link">8. Round 5: 다중 에이전트 협업</a></li>
      <li class="toc-item"><a href="#agentic" class="toc-link">9. Agentic Engineering 인사이트</a></li>
      <li class="toc-item"><a href="#resources" class="toc-link">10. 핵심 깃허브 & 리소스</a></li>
      <li class="toc-item"><a href="#next" class="toc-link">11. Next Action & 딥 리서치</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <div class="hero">
      <span class="hero-badge">Format B: Interactive Single-Page Report</span>
      <h1 class="hero-title">메타 시니어 엔지니어의 Fable 5.1 vs GPT-6 Astra 실전 비교</h1>
      <div class="hero-meta">
        <span>👨‍💻 강사: 실밸개발자 (메타 시니어 엔지니어)</span>
        <span>📅 정리일: 2026-09-13</span>
        <span>🎯 검증 대상: AutoKliq 프로덕션 코드</span>
      </div>
    </div>

    <!-- 1. Executive Summary -->
    <section id="summary" class="section">
      <h2 class="section-title">1. Executive Summary & 핵심 결론</h2>
      <div class="grid-2">
        <div class="report-card" style="border-left:4px solid #38bdf8;">
          <h3 style="color:#38bdf8; font-size:16px; margin-bottom:8px;">💡 핵심 결론 3줄 요약</h3>
          <p style="font-size:14px; color:#c9d1d9; line-height:1.7;">
            1. <strong>도메인별 특화 우위:</strong> 창의적 기획, UX 리디자인, 3D 시각화는 <strong>Astra</strong> 압승 / 딥 시스템 프로파일링 및 최적화는 <strong>Fable 5.1</strong> 판정승.<br>
            2. <strong>하네스의 결정적 영향:</strong> 모델 자체보다 이를 감싸는 하네스(Claude Code vs Codex)의 툴 제어와 피드백 루프가 품질을 좌우함.<br>
            3. <strong>협업의 역설:</strong> 두 모델 간 자율 협업은 평균으로 퇴보(짬뽕)하며 비용만 폭증. 인간의 단호한 방향 제시가 필수적.
          </p>
        </div>
        <div class="report-card" style="border-left:4px solid #10b981;">
          <h3 style="color:#10b981; font-size:16px; margin-bottom:8px;">⚡ AI 실전 활용 팁</h3>
          <ul style="font-size:13px; color:#c9d1d9; line-height:1.8; padding-left:18px;">
            <li><strong>Effort 레벨:</strong> 무조건 Max 고집하지 말고 Fast/Medium 모드로 비용과 속도 최적화.</li>
            <li><strong>Negative 가드레일:</strong> "품질 저하 시 보고서 명시", "기존 기능 보존" 제약조건 주입.</li>
            <li><strong>Dual-User 시각:</strong> 사람뿐 아니라 AI 에이전트가 쓰기 쉬운 아키텍처로 UI 설계.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 2. Reviews -->
    <section id="reviews" class="section">
      <h2 class="section-title">2. 일주일간 쏟아진 113개 리뷰 분석</h2>
      <div class="report-card">
        <p style="margin-bottom:16px; color:#8b949e; font-size:14px;">
          레딧, X, 깃허브 등에서 수집한 113개 리뷰 중 같은 모델을 두고 완벽히 대립한 5대 쟁점입니다.
        </p>
        <table class="cmp-table">
          <thead>
            <tr>
              <th>쟁점</th>
              <th style="color:#fb7185;">부정적 / 반대 의견</th>
              <th style="color:#34d399;">긍정적 / 찬성 의견</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>토큰 소모</strong></td>
              <td>1시간 만에 주간 할당량 전소</td>
              <td>동일 작업 기준 Fable 5.1이 5.0보다 훨씬 덜 소모</td>
            </tr>
            <tr>
              <td><strong>Astra 전환</strong></td>
              <td>기대 이하의 조잡한 수준</td>
              <td>회사 메인 AI 전면 교체, Fable이 바보처럼 느껴짐</td>
            </tr>
            <tr>
              <td><strong>글쓰기 능력</strong></td>
              <td>문맥이 복잡해져 가독성 저하</td>
              <td>기술적 뉘앙스와 구조화 완성도 대폭 개선</td>
            </tr>
            <tr>
              <td><strong>추론 비용</strong></td>
              <td>Medium만 써도 2턴 만에 한도 도달</td>
              <td>추론 레벨을 높여야 헛발질이 줄어 실질 비용 감소</td>
            </tr>
            <tr>
              <td><strong>안전성 검사</strong></td>
              <td>너무 민감하여 Opus로 자꾸 강제 폴백</td>
              <td>거부 없이 프로덕션급 대규모 리팩토링 완수</td>
            </tr>
          </tbody>
        </table>
        <p style="color:#a78bfa; font-size:13px; margin-top:12px;">
          📌 <strong>원인:</strong> 서브에이전트 수(10개 이상 vs 단일 세션), 문서 vs 코드, 시스템 프롬프트 차이 등 실험 조건의 격차 + 주관적 체감(말투, 짜증 등)의 개입.
        </p>
      </div>
    </section>

    <!-- 3. Experiment Setup -->
    <section id="experiment" class="section">
      <h2 class="section-title">3. 실험 환경 및 통제 조건</h2>
      <div class="report-card">
        <div class="grid-2">
          <div>
            <h4 style="color:#38bdf8; margin-bottom:8px;">🛠️ 도구 및 모델 세팅</h4>
            <ul style="color:#8b949e; font-size:14px; line-height:1.8; padding-left:18px;">
              <li><strong>모델 A:</strong> Anthropic Claude Fable 5.1 Max on <code>Claude Code</code></li>
              <li><strong>모델 B:</strong> OpenAI GPT-6 Astra Max (Fast mode) on <code>Codex CLI</code></li>
              <li><strong>오케스트레이터:</strong> <code>herdr</code> 멀티 터미널 분할 브로드캐스트</li>
              <li><strong>주입 방식:</strong> 인간 중간 개입 없는 100% Zero-shot 1회 주입</li>
            </ul>
          </div>
          <div>
            <h4 style="color:#a78bfa; margin-bottom:8px;">🎯 대상 프로젝트</h4>
            <p style="color:#8b949e; font-size:14px; line-height:1.7;">
              <strong>AutoKliq:</strong> 메타 엔지니어와 커리어 알렉스(상현)가 3개월간 실제 운영/개발 중인 수만 라인의 AI 유튜브 썸네일 SaaS. 장난감 토이 프로젝트가 아닌 실제 코드베이스.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Round 1 -->
    <section id="round1" class="section">
      <h2 class="section-title">4. Round 1 · 온보딩 및 홍보 영상 제작</h2>
      <div class="report-card">
        <div class="prompt-container">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>당신은 오토클릭(AutoKliq)의 실제 서비스 소스코드를 가지고 있습니다.
1. 먼저 로컬 환경에서 앱을 직접 띄우고 실제로 사용해 보세요.
2. 제품의 사용자 경험과 핵심 가치를 파악한 뒤, 다음 두 가지 영상을 순수 코드로 작성하여 MP4 파일로 렌더링하세요.
   - 제품을 소개하는 온보딩 영상 (45초 분량) 1편
   - 핵심 기능을 임팩트 있게 보여주는 짧은 컷의 홍보 영상 (15초 분량) 1편</div>
        <div class="grid-2" style="margin-top:16px;">
          <div style="background:rgba(244,63,94,0.05); padding:16px; border-radius:10px; border:1px solid rgba(244,63,94,0.2);">
            <strong style="color:#fb7185;">Fable 5.1 결과:</strong><br>
            시각적 단계 구성은 매우 훌륭하고 정갈했으나, 오디오/내레이션이 일절 없는 무음 비디오로 렌더링됨.
          </div>
          <div style="background:rgba(16,185,129,0.05); padding:16px; border-radius:10px; border:1px solid rgba(16,185,129,0.2);">
            <strong style="color:#34d399;">Astra 결과 (승리 🏆):</strong><br>
            자연스러운 한국어 음성(TTS), 자막, 배경음악까지 완벽히 임베딩된 온보딩 영상 렌더링. 비용은 Fast 모드로 2배 소모.
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Round 2 -->
    <section id="round2" class="section">
      <h2 class="section-title">5. Round 2 · 성능 최적화 (\"생성 시간을 절반으로\")</h2>
      <div class="report-card">
        <div class="prompt-container">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>썸네일 생성이 너무 느립니다. 이를 절반(50%)으로 줄여주세요.
[지켜야 할 규칙]
1. 기존에 정상적으로 동작하는 필수 기능들은 하나도 변경하거나 누락하지 마세요.
2. 만약 실행 시간 단축을 위해 이미지/텍스트의 품질을 의도적으로 떨어뜨리는 변경을 했다면, 반드시 최종 보고서에 어떤 품질을 희생했는지 명시하세요.</div>
        <div class="grid-2" style="margin-top:16px;">
          <div style="background:rgba(244,63,94,0.05); padding:16px; border-radius:10px; border:1px solid rgba(244,63,94,0.2);">
            <strong style="color:#fb7185;">Fable 5.1 결과 (판정승 🏆 — $47, 1시간 30분):</strong><br>
            집요하게 프로파일링하여 시나리오별 2~6% (P50/P90 기준 20~30초 실질 단축) 개선 달성. 실질적인 아키텍처 리팩토링 성공.
          </div>
          <div style="background:rgba(16,185,129,0.05); padding:16px; border-radius:10px; border:1px solid rgba(16,185,129,0.2);">
            <strong style="color:#34d399;">Astra 결과 ($22, 24분):</strong><br>
            평균 1% 단축(~10초 단축)에 그쳐 체감 불가. 시간을 적게 썼으나 깊이 있는 병목 해결에는 실패.
          </div>
        </div>
      </div>
    </section>

    <!-- 6. Round 3 -->
    <section id="round3" class="section">
      <h2 class="section-title">6. Round 3 · UI 전면 리디자인</h2>
      <div class="report-card">
        <div class="prompt-container">
<button class="copy-btn" onclick="copyPrompt(this)">복사</button>오토클릭의 UI를 전면적으로 다시 디자인하세요.
우리가 제품을 완전히 다시 설계한다면 어떤 모습이어야 하는지 확인하고 싶습니다.
[필수 요구사항]
1. 사람이 쓰기에도 좋아야 하고, 앞으로 이 화면을 다룰 '에이전트'가 쓰기에도 좋아야 합니다.
2. 기존에 잘 작동하던 기능이 사라져서는 안 되며, 변경 후 실제로 에러 없이 돌아가는지 철저히 테스트하세요.
3. 시간제한은 없으며 중간에 질문하지 말고 스스로 판단하여 끝까지 진행하세요.</div>
        <div class="grid-2" style="margin-top:16px;">
          <div style="background:rgba(244,63,94,0.05); padding:16px; border-radius:10px;">
            <strong style="color:#fb7185;">Fable 5.1 (보수적 개선):</strong><br>
            기존 폼을 3개 영역으로 쪼개고 상단 탭을 정리한 정도의 안전 위주 리팩토링. 혁신적 변화 부재.
          </div>
          <div style="background:rgba(16,185,129,0.05); padding:16px; border-radius:10px; border:1px solid rgba(16,185,129,0.3);">
            <strong style="color:#34d399;">Astra (압도적 압승 🏆 — 비용/시간 동일):</strong><br>
            1) '아이디어에서 한 장으로' 전용 Home 대시보드 신설.<br>
            2) 4단계 선형 마법사 (Story ➔ Expression ➔ Asset ➔ Pre-check).<br>
            3) 이전 작업물을 빠르게 찾는 실시간 검색바 및 상태 필터 추가.
          </div>
        </div>
      </div>
    </section>

    <!-- 7. Round 4 -->
    <section id="round4" class="section">
      <h2 class="section-title">7. Round 4 · 저장소 3D 공간 탐색 & 총비용</h2>
      <div class="report-card">
        <div class="grid-2">
          <div>
            <h4 style="color:#f43f5e; margin-bottom:8px;">Fable 5.1 ($11, 29분)</h4>
            <p style="font-size:13px; color:#8b949e; line-height:1.6;">
              디스트릭트 구역 분할 및 컴포넌트/API 색상 구분. WASD 조작 지원. 평이한 3D 맵.
            </p>
          </div>
          <div>
            <h4 style="color:#10b981; margin-bottom:8px;">Astra ($24, 35분 — 압승 🏆)</h4>
            <p style="font-size:13px; color:#c9d1d9; line-height:1.6;">
              8개 공간 분할, <strong>건물 높이 = 코드 라인 수</strong> 메타포, '썸네일의 여정' 7단계 가이드 투어 및 조감도 탑재.
            </p>
          </div>
        </div>
        <div style="margin-top:20px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-around; text-align:center;">
          <div><strong style="color:#f43f5e; font-size:20px;">Fable 총 $125</strong><div style="font-size:12px; color:#8b949e;">4개 과제 합계</div></div>
          <div><strong style="color:#10b981; font-size:20px;">Astra 총 $134</strong><div style="font-size:12px; color:#8b949e;">4개 과제 합계 (Fast mode)</div></div>
        </div>
      </div>
    </section>

    <!-- 8. Round 5 -->
    <section id="round5" class="section">
      <h2 class="section-title">8. Round 5 · 다중 에이전트 상호 협업의 실체</h2>
      <div class="report-card" style="border-left:4px solid #f97316;">
        <h3 style="color:#fdba74; font-size:16px; margin-bottom:8px;">🚨 천재 둘의 협업이 가져온 역설</h3>
        <p style="color:#c9d1d9; font-size:14px; line-height:1.7; margin-bottom:14px;">
          의도(인간 컨펌 1회) ➔ 플래닝 ➔ 구현 ➔ 검증 ➔ 보고 단계별로 Astra(메인)와 Fable(리뷰어)이 상호 리뷰하도록 설계했습니다. 그러나 상호 합의 과정에서 가장 유용했던 <strong>프로젝트 검색바가 사라지고</strong>, 어설픈 '짬뽕' UI로 전락했습니다.
        </p>
        <div style="background:#060911; padding:14px; border-radius:8px; font-size:13px; color:#f87171;">
          💸 단일 과제당 토큰 비용: <strong>$108 (영상), $62 (최적화), $142 (UI)</strong>로 폭증!<br>
          👉 <strong>교훈:</strong> 명확한 인간의 디렉션이 없으면 에이전트 간 리뷰는 서로의 날카로운 혁신성을 깎아내려 무난하고 진부한 결과물로 수렴함.
        </div>
      </div>
    </section>

    <!-- 9. Agentic Engineering -->
    <section id="agentic" class="section">
      <h2 class="section-title">9. Agentic & Harness Engineering 핵심 교훈</h2>
      <div class="grid-2">
        <div class="report-card">
          <h4 style="color:#38bdf8; margin-bottom:6px;">하네스 엔지니어링의 위력</h4>
          <p style="font-size:13px; color:#8b949e; line-height:1.6;">
            순수 모델 비교는 환상입니다. 툴 호출 규격, 프롬프트 캐싱, 파일 인덱싱 등 하네스의 완성도가 실제 서비스 개발 생산성을 70% 이상 결정합니다.
          </p>
        </div>
        <div class="report-card">
          <h4 style="color:#a78bfa; margin-bottom:6px;">Human Gatekeeper의 필요성</h4>
          <p style="font-size:13px; color:#8b949e; line-height:1.6;">
            Zero-shot 에이전트가 발전할수록 인간은 코더에서 '조타수(Steering Director)'로 변해야 합니다. 최초 의도와 마일스톤별 게이트 검증을 인간이 통제해야 합니다.
          </p>
        </div>
      </div>
    </section>

    <!-- 10. Resources -->
    <section id="resources" class="section">
      <h2 class="section-title">10. 핵심 깃허브 & 리소스</h2>
      <div class="report-card">
        <ul style="list-style:none; font-size:14px; line-height:2;">
          <li>🔗 <a href="https://github.com/herdrdev/herdr" target="_blank"><strong>herdr (GitHub):</strong></a> 멀티 터미널 CLI 에이전트 오케스트레이터</li>
          <li>🔗 <a href="https://github.com/openai/codex" target="_blank"><strong>Codex CLI:</strong></a> OpenAI 공식 터미널 자율 코딩 에이전트</li>
          <li>🔗 <a href="https://claude.com/claude-code" target="_blank"><strong>Claude Code:</strong></a> 엔트로픽 공식 CLI 도구</li>
          <li>🔗 <a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1" target="_blank"><strong>Anthropic Fable 5.1 Guide:</strong></a> 엔트로픽 공식 프롬프트 가이드</li>
          <li>🔗 <a href="https://autokliq.com" target="_blank"><strong>AutoKliq:</strong></a> 테스트베드로 사용된 실서비스 썸네일 SaaS</li>
        </ul>
      </div>
    </section>

    <!-- 11. Next Action -->
    <section id="next" class="section">
      <h2 class="section-title">11. Next Actions & 추천 소스</h2>
      <div class="report-card" style="border-color:rgba(56,189,248,0.3); background:rgba(56,189,248,0.03);">
        <h4 style="color:#38bdf8; margin-bottom:10px;">📌 그룹장 맞춤형 즉시 실행 과제 (Mobile SW Protocol Design / Physical Layer)</h4>
        <ol style="font-size:14px; color:#c9d1d9; line-height:1.8; padding-left:20px;">
          <li><strong>AST + Grep 기반 레지스터 맵 파이프라인 실험:</strong> herdr 로컬 세팅 후 Claude Code와 Codex를 동시 띄워 C/C++ 레거시 코드베이스의 심벌 추출 및 2nd Brain 인덱싱 고도화 테스트.</li>
          <li><strong>AI-native HW 요구사항 매핑:</strong> 3대 프로덕션 프롬프트 패턴(특히 Negative 제약)을 응용하여 HW 변경 사항 리스트와 JIRA 티켓을 자동 대조/검증하는 에이전트 프롬프트 템플릿 설계.</li>
          <li><strong>협업 가드레일 기반 코드 리뷰 자동화:</strong> 멀티 에이전트 상호 리뷰 시 "기존 물리 계층 최적화 로직 보존 의무" 등 엄격한 Negative 제약조건 주입을 통한 리뷰 퇴보 방지 훈련.</li>
        </ol>
      </div>
    </section>
  </main>
</div>

<script>
function copyPrompt(btn) {{
  const code = btn.parentElement.innerText.replace('복사', '').trim();
  navigator.clipboard.writeText(code).then(() => {{
    const orig = btn.innerText;
    btn.innerText = '복사됨! ✓';
    btn.style.background = '#10b981';
    btn.style.color = '#fff';
    setTimeout(() => {{
      btn.innerText = orig;
      btn.style.background = '';
      btn.style.color = '';
    }}, 1800);
  }});
}}

// Scrollspy for TOC
window.addEventListener('scroll', () => {{
  const sections = document.querySelectorAll('.section');
  const links = document.querySelectorAll('.toc-link');
  let current = '';
  sections.forEach(sec => {{
    const top = sec.offsetTop;
    if (pageYOffset >= top - 100) {{
      current = sec.getAttribute('id');
    }}
  }});
  links.forEach(l => {{
    l.classList.remove('active');
    if (l.getAttribute('href') === '#' + current) {{
      l.classList.add('active');
    }}
  }});
}});
</script>
</body>
</html>'''

report_path = os.path.join(base_dir, 'lecture_report.html')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_html)
print("Generated lecture_report.html (Format B).")
print("ALL DONE SUCCESSFULLY!")
