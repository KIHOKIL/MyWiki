import os

base_dir = r'c:\Users\kihok\내 드라이브\MyWiki\_source\Study\AI-Lectures\커리어해커알렉스\20260816_진짜AX\slides'
os.makedirs(base_dir, exist_ok=True)

common_css = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0f1a;
  font-family: 'Noto Sans KR', sans-serif;
  color: #e6edf3;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 50px;
}
.container {
  width: 1280px;
  padding: 44px 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  font-size: 48px;
  font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  margin-bottom: 44px;
  line-height: 1.3;
}
.slide-nav {
  position: fixed; bottom: 0; left: 0; right: 0; height: 50px;
  background: rgba(10, 15, 26, 0.95);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(124, 58, 237, 0.2);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999; font-family: 'Noto Sans KR', sans-serif;
}
.slide-nav-inner {
  width: 1280px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 60px;
}
.slide-nav a {
  text-decoration: none; font-size: 14px; font-weight: 700;
  color: #7c3aed; transition: color 0.2s;
}
.slide-nav a:hover { color: #a78bfa; }
.slide-nav .nav-disabled { font-size: 14px; font-weight: 700; color: #484f58; cursor: default; }
.slide-nav .nav-center a { color: #8b949e; font-size: 13px; font-weight: 400; }
.slide-nav .nav-center a:hover { color: #e6edf3; }
body { opacity: 0; animation: fadeIn 0.4s ease forwards; }
body.fade-out { animation: fadeOut 0.3s ease forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-12px); } }
'''

def write_html(filename, title, css, body_content, nav_left, nav_center, nav_right, scripts):
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
{common_css}
{css}
</style>
</head>
<body>
<div class="container">
  <h1 class="title">{title}</h1>
  {body_content}
</div>
<nav class="slide-nav">
  <div class="slide-nav-inner">
    <div class="nav-left">{nav_left}</div>
    <div class="nav-center">{nav_center}</div>
    <div class="nav-right">{nav_right}</div>
  </div>
</nav>
<script>
function navigateTo(url) {{
  document.body.classList.add('fade-out');
  setTimeout(function() {{ window.location.href = url; }}, 300);
}}
{scripts}
</script>
</body>
</html>'''
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        f.write(html)


# 1. index.html
index_css = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0f1a; font-family: 'Noto Sans KR', sans-serif;
  color: #e6edf3; min-height: 100vh; display: flex; justify-content: center;
  padding: 60px 0 80px;
}
.container { width: 1280px; padding: 0 80px; }
.page-title {
  font-size: 42px; font-weight: 900;
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  text-align: center; margin-bottom: 10px;
}
.page-subtitle { text-align: center; font-size: 16px; color: #8b949e; margin-bottom: 50px; }
.section { margin-bottom: 36px; }
.section-header {
  font-size: 18px; font-weight: 700; padding: 12px 20px;
  border-left: 4px solid; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;
}
.num-range { display: inline-block; font-size: 12px; font-weight: 700; color: white; padding: 3px 10px; border-radius: 10px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.card {
  display: flex; flex-direction: column; gap: 6px; padding: 18px 20px;
  background: rgba(139,148,158,0.04); border: 1px solid rgba(139,148,158,0.1);
  border-radius: 12px; text-decoration: none; transition: all 0.25s ease;
}
.card:hover { transform: translateY(-3px); }
.card .card-num { font-size: 28px; font-weight: 900; }
.card .card-title { font-size: 14px; font-weight: 700; color: #c9d1d9; }
.card .card-file { font-size: 11px; color: #484f58; font-family: 'Courier New', monospace; }

.section-intro .section-header { border-color: #7c3aed; color: #a78bfa; }
.section-intro .num-range { background: #5b21b6; }
.section-intro .card:hover { border-color: #7c3aed; box-shadow: 0 8px 32px rgba(124, 58, 237, 0.18); }
.section-intro .card .card-num { color: #7c3aed; }
.section-1 .section-header { border-color: #38bdf8; color: #7dd3fc; }
.section-1 .num-range { background: #0369a1; }
.section-1 .card:hover { border-color: #38bdf8; box-shadow: 0 8px 32px rgba(56, 189, 248, 0.18); }
.section-1 .card .card-num { color: #38bdf8; }
.section-2 .section-header { border-color: #34d399; color: #6ee7b7; }
.section-2 .num-range { background: #047857; }
.section-2 .card:hover { border-color: #34d399; box-shadow: 0 8px 32px rgba(52, 211, 153, 0.18); }
.section-2 .card .card-num { color: #34d399; }
.section-3 .section-header { border-color: #f97316; color: #fdba74; }
.section-3 .num-range { background: #c2410c; }
.section-3 .card:hover { border-color: #f97316; box-shadow: 0 8px 32px rgba(249, 115, 22, 0.18); }
.section-3 .card .card-num { color: #f97316; }
.section-outro .section-header { border-color: #e879f9; color: #f0abfc; }
.section-outro .num-range { background: linear-gradient(90deg, #7c3aed, #38bdf8, #34d399, #f97316); }
.section-outro .card:hover { border-color: #e879f9; box-shadow: 0 8px 32px rgba(232, 121, 249, 0.18); }
.section-outro .card .card-num { background: linear-gradient(135deg, #7c3aed, #38bdf8, #34d399, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
body { opacity: 0; animation: fadeIn 0.4s ease forwards; }
body.fade-out { animation: fadeOut 0.3s ease forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-12px); } }
'''
index_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280">
<title>진짜 AX와 에이전틱 코딩의 미래 — 비주얼 자료</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>{index_css}</style>
</head>
<body>
<div class="container">
  <h1 class="page-title">진짜 AX와 에이전틱 코딩의 미래 — 비주얼 자료</h1>
  <p class="page-subtitle">전체 5개 슬라이드 · 클릭하여 개별 페이지로 이동</p>
  <div class="section section-intro">
    <div class="section-header"><span class="num-range">01</span> 인트로</div>
    <div class="grid">
      <a class="card" href="01-intro.html" onclick="event.preventDefault(); navigateTo(this.href)">
        <span class="card-num">01</span><span class="card-title">왜 지금 AX인가?</span><span class="card-file">01-intro.html</span>
      </a>
    </div>
  </div>
  <div class="section section-1">
    <div class="section-header"><span class="num-range">02</span> 섹션 1</div>
    <div class="grid">
      <a class="card" href="02-metrics.html" onclick="event.preventDefault(); navigateTo(this.href)">
        <span class="card-num">02</span><span class="card-title">성공의 지표와 리더십</span><span class="card-file">02-metrics.html</span>
      </a>
    </div>
  </div>
  <div class="section section-2">
    <div class="section-header"><span class="num-range">03</span> 섹션 2</div>
    <div class="grid">
      <a class="card" href="03-harness.html" onclick="event.preventDefault(); navigateTo(this.href)">
        <span class="card-num">03</span><span class="card-title">통제와 축적의 시스템</span><span class="card-file">03-harness.html</span>
      </a>
    </div>
  </div>
  <div class="section section-3">
    <div class="section-header"><span class="num-range">04</span> 섹션 3</div>
    <div class="grid">
      <a class="card" href="04-human-loop.html" onclick="event.preventDefault(); navigateTo(this.href)">
        <span class="card-num">04</span><span class="card-title">Human-on-the-loop</span><span class="card-file">04-human-loop.html</span>
      </a>
    </div>
  </div>
  <div class="section section-outro">
    <div class="section-header"><span class="num-range">05</span> 아웃트로</div>
    <div class="grid">
      <a class="card" href="05-summary.html" onclick="event.preventDefault(); navigateTo(this.href)">
        <span class="card-num">05</span><span class="card-title">요약 및 마무리</span><span class="card-file">05-summary.html</span>
      </a>
    </div>
  </div>
</div>
<script>
function navigateTo(url) {{
  document.body.classList.add('fade-out');
  setTimeout(function() {{ window.location.href = url; }}, 300);
}}
</script>
</body>
</html>'''
with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)


# 2. 01-intro.html
css_01 = '''
.cards { display: flex; gap: 32px; margin-bottom: 40px; width: 100%; }
.card { flex: 1; background: linear-gradient(145deg, rgba(124, 58, 237, 0.1), rgba(56, 189, 248, 0.05)); border: 1px solid rgba(124, 58, 237, 0.25); border-radius: 20px; padding: 40px 28px; text-align: center; position: relative; overflow: hidden; opacity: 0; transform: translateY(30px); animation: cardAppear 0.6s ease-out forwards; }
.card:nth-child(1) { animation-delay: 0.2s; }
.card:nth-child(2) { animation-delay: 0.6s; }
@keyframes cardAppear { to { opacity: 1; transform: translateY(0); } }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #7c3aed, #38bdf8); }
.card-icon { font-size: 48px; margin-bottom: 20px; display: block; position: relative; z-index: 1; }
.card-text { font-size: 17px; font-weight: 500; line-height: 1.7; color: #c9d1d9; position: relative; z-index: 1; }
.card-label { display: inline-block; margin-top: 14px; padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; position: relative; z-index: 1; background: #7c3aed; color: #fff;}
'''
body_01 = '''
<div class="cards">
  <div class="card">
    <span class="card-icon">⚠️</span>
    <p class="card-text">흔한 오해:<br>"우리 팀도 AI 툴을 쓰면<br>AX 아닌가요?"</p>
    <span class="card-label">도구 도입 ≠ AX</span>
  </div>
  <div class="card">
    <span class="card-icon">🚀</span>
    <p class="card-text">비즈니스 병목을 정의하고,<br>조직의 문화와 프로세스를<br>재설계하는 것</p>
    <span class="card-label">진정한 의미의 AX</span>
  </div>
</div>
'''
write_html('01-intro.html', '왜 지금 AX인가?', css_01, body_01,
           '<span class="nav-disabled">&larr; 이전</span>',
           '<a href="index.html">01 / 05</a>',
           '<a href="02-metrics.html" onclick="event.preventDefault(); navigateTo(this.href)">다음 &rarr;</a>',
           "document.addEventListener('keydown', function(e) { if(e.key==='ArrowRight') navigateTo('02-metrics.html'); });")


# 3. 02-metrics.html
css_02 = '''
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; width: 100%; max-width: 1000px; }
.feature-card { background: rgba(139, 148, 158, 0.04); border: 1px solid rgba(139, 148, 158, 0.1); border-radius: 16px; padding: 28px 24px; transition: all 0.25s ease; opacity: 0; transform: translateY(20px); animation: cardIn 0.5s ease-out forwards;}
.feature-card:nth-child(1) { animation-delay: 0.1s; }
.feature-card:nth-child(2) { animation-delay: 0.2s; }
.feature-card:nth-child(3) { animation-delay: 0.3s; }
.feature-card:nth-child(4) { animation-delay: 0.4s; }
@keyframes cardIn { to { opacity: 1; transform: translateY(0); } }
.feature-card:hover { transform: translateY(-3px); border-color: #38bdf8; box-shadow: 0 8px 32px rgba(56, 189, 248, 0.18);}
.feature-icon { font-size: 36px; margin-bottom: 12px; display: block; }
.feature-name { font-size: 20px; font-weight: 700; margin-bottom: 6px; }
.feature-desc { font-size: 15px; color: #8b949e; line-height: 1.5; }
'''
body_02 = '''
<div class="grid">
  <div class="feature-card">
    <span class="feature-icon">📈</span>
    <h3 class="feature-name">가치 창출 우선주의</h3>
    <p class="feature-desc">도입률이나 툴 채택률은 무의미합니다. 숫자로 증명 가능한 비즈니스 임팩트(시간, 돈, 리소스 절약)만이 진짜 지표입니다.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">👑</span>
    <h3 class="feature-name">리더의 과감한 결단</h3>
    <p class="feature-desc">"이제부터 모든 보고서는 마크다운으로 받겠다"와 같은 과감한 Risk Taking이 변화를 만듭니다.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">🗣️</span>
    <h3 class="feature-name">프로세스와 커뮤니케이션</h3>
    <p class="feature-desc">테크 리드(TL)에게는 딥러닝 지식보다 전체 프로세스에 대한 깊은 이해도와 다방면의 설득 능력이 요구됩니다.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">🎯</span>
    <h3 class="feature-name">실행 중심의 리더십</h3>
    <p class="feature-desc">문제를 끝까지 물고 늘어지는 리더십이 AX의 핵심 성공 요인입니다.</p>
  </div>
</div>
'''
write_html('02-metrics.html', '성공의 지표와 리더십', css_02, body_02,
           '<a href="01-intro.html" onclick="event.preventDefault(); navigateTo(this.href)">&larr; 이전</a>',
           '<a href="index.html">02 / 05</a>',
           '<a href="03-harness.html" onclick="event.preventDefault(); navigateTo(this.href)">다음 &rarr;</a>',
           "document.addEventListener('keydown', function(e) { if(e.key==='ArrowLeft') navigateTo('01-intro.html'); if(e.key==='ArrowRight') navigateTo('03-harness.html'); });")

# 4. 03-harness.html
css_03 = '''
.diagram { width: 100%; max-width: 900px; background: rgba(22, 27, 40, 0.6); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 30px; opacity: 0; animation: fadeIn 0.8s ease-out forwards 0.2s;}
.diagram-center { display: inline-block; padding: 16px 32px; border-radius: 12px; background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(56, 189, 248, 0.1)); border: 2px solid #7c3aed; font-size: 24px; font-weight: 900; margin-bottom: 20px; }
.diagram-arrows { font-size: 28px; color: #7c3aed; margin: 12px 0; }
.diagram-row { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.diagram-node { background: rgba(139, 148, 158, 0.06); border: 1px solid rgba(139, 148, 158, 0.15); border-radius: 12px; padding: 16px 20px; min-width: 140px; }
.diagram-node-title { font-size: 16px; font-weight: 700; margin-bottom: 4px; color: #34d399; }
.diagram-node-desc { font-size: 13px; color: #8b949e; }
'''
body_03 = '''
<div class="diagram">
  <div class="diagram-center">Harness Engineering</div>
  <div class="diagram-arrows">↓</div>
  <div class="diagram-row">
    <div class="diagram-node">
      <div class="diagram-node-title">영구적 기억 (Memory)</div>
      <div class="diagram-node-desc">무엇을 하지 말아야 하는지 축적</div>
    </div>
    <div class="diagram-node">
      <div class="diagram-node-title">룰과 맥락 (Context)</div>
      <div class="diagram-node-desc">객관적으로 확장 가능한 퀄리티 보장</div>
    </div>
    <div class="diagram-node">
      <div class="diagram-node-title">살아있는 시스템 (Living)</div>
      <div class="diagram-node-desc">모델 진화에 맞춘 지속적 유지보수</div>
    </div>
    <div class="diagram-node">
      <div class="diagram-node-title">전사적 표준화 (Standard)</div>
      <div class="diagram-node-desc">인프라/플러그인 표준화로 병목 제거</div>
    </div>
  </div>
</div>
'''
write_html('03-harness.html', '통제와 축적의 시스템', css_03, body_03,
           '<a href="02-metrics.html" onclick="event.preventDefault(); navigateTo(this.href)">&larr; 이전</a>',
           '<a href="index.html">03 / 05</a>',
           '<a href="04-human-loop.html" onclick="event.preventDefault(); navigateTo(this.href)">다음 &rarr;</a>',
           "document.addEventListener('keydown', function(e) { if(e.key==='ArrowLeft') navigateTo('02-metrics.html'); if(e.key==='ArrowRight') navigateTo('04-human-loop.html'); });")

# 5. 04-human-loop.html
css_04 = '''
.comparison { width: 100%; max-width: 1000px; opacity: 0; transform: translateY(20px); animation: stepIn 0.6s ease-out forwards 0.2s;}
@keyframes stepIn { to { opacity: 1; transform: translateY(0); } }
.comparison-title { font-size: 22px; font-weight: 700; text-align: center; margin-bottom: 20px; color: #a78bfa; }
.comparison-row { display: grid; grid-template-columns: 1fr auto 1fr; gap: 16px; align-items: center; margin-bottom: 16px; }
.comp-label { font-size: 14px; font-weight: 700; color: #f97316; margin-bottom: 4px; }
.comp-old { background: rgba(139, 148, 158, 0.06); border: 1px solid rgba(139, 148, 158, 0.15); border-radius: 12px; padding: 20px; font-size: 16px; color: #8b949e; }
.comp-arrow { font-size: 24px; color: #7c3aed; }
.comp-new { background: rgba(124, 58, 237, 0.08); border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 12px; padding: 20px; font-size: 16px; color: #e6edf3; font-weight: 600; }
'''
body_04 = '''
<div class="comparison">
  <div class="comparison-title">권한의 이동</div>
  <div class="comparison-row">
    <div class="comp-label">Human-in-the-loop</div>
    <div></div>
    <div class="comp-label" style="text-align: right">Human-on-the-loop</div>
  </div>
  <div class="comparison-row">
    <div class="comp-old">인간이 모든 프로세스에 개입하여 의사결정</div>
    <div class="comp-arrow">&rarr;</div>
    <div class="comp-new">에이전트가 95% 주도, 인간은 결정적인 5%만 개입</div>
  </div>
  <br><br>
  <div class="comparison-title">자체적인 피드백 루프</div>
  <div class="comparison-row">
    <div class="comp-old">단방향 실패 복구</div>
    <div class="comp-arrow">&rarr;</div>
    <div class="comp-new">에이전트 자체 원인 분석 및 시스템 개선 후 승인 요청</div>
  </div>
  <div class="comparison-row">
    <div class="comp-old">주관적 평가</div>
    <div class="comp-arrow">&rarr;</div>
    <div class="comp-new">Online/Offline 평가 및 UXR 정성평가 필수 수반</div>
  </div>
</div>
'''
write_html('04-human-loop.html', 'Human-on-the-loop', css_04, body_04,
           '<a href="03-harness.html" onclick="event.preventDefault(); navigateTo(this.href)">&larr; 이전</a>',
           '<a href="index.html">04 / 05</a>',
           '<a href="05-summary.html" onclick="event.preventDefault(); navigateTo(this.href)">다음 &rarr;</a>',
           "document.addEventListener('keydown', function(e) { if(e.key==='ArrowLeft') navigateTo('03-harness.html'); if(e.key==='ArrowRight') navigateTo('05-summary.html'); });")

# 6. 05-summary.html
css_05 = '''
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; margin-bottom: 44px; }
.summary-card { background: rgba(22, 27, 40, 0.8); border: 1px solid rgba(139, 148, 158, 0.1); border-radius: 16px; padding: 32px 24px; text-align: center; position: relative; overflow: hidden; opacity: 0; transform: translateY(20px); animation: cardIn 0.5s ease-out forwards; }
@keyframes cardIn { to { opacity: 1; transform: translateY(0); } }
.summary-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.summary-card:nth-child(1) { animation-delay: 0.1s; } .summary-card:nth-child(1)::before { background: #7c3aed; } .summary-card:nth-child(1) .card-name { color: #7c3aed; }
.summary-card:nth-child(2) { animation-delay: 0.2s; } .summary-card:nth-child(2)::before { background: #38bdf8; } .summary-card:nth-child(2) .card-name { color: #38bdf8; }
.summary-card:nth-child(3) { animation-delay: 0.3s; } .summary-card:nth-child(3)::before { background: #34d399; } .summary-card:nth-child(3) .card-name { color: #34d399; }
.summary-card:nth-child(4) { animation-delay: 0.4s; } .summary-card:nth-child(4)::before { background: #f97316; } .summary-card:nth-child(4) .card-name { color: #f97316; }
.summary-card:nth-child(5) { animation-delay: 0.5s; } .summary-card:nth-child(5)::before { background: #ec4899; } .summary-card:nth-child(5) .card-name { color: #ec4899; }
.summary-card:nth-child(6) { animation-delay: 0.6s; } .summary-card:nth-child(6)::before { background: #fbbf24; } .summary-card:nth-child(6) .card-name { color: #fbbf24; }
.card-icon { font-size: 40px; margin-bottom: 14px; display: block; }
.card-name { font-size: 20px; font-weight: 900; margin-bottom: 8px; }
.card-desc { font-size: 14px; color: #8b949e; line-height: 1.5; }
.conclusion { text-align: center; padding: 28px 40px; background: rgba(22, 27, 40, 0.6); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 16px; width: 100%; max-width: 900px; opacity: 0; animation: cardIn 0.8s ease-out forwards 0.8s;}
.conclusion-line { font-size: 22px; font-weight: 900; line-height: 1.8; background: linear-gradient(90deg, #7c3aed, #38bdf8, #34d399, #f97316, #ec4899, #fbbf24); background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: gradient-shift 5s ease infinite; }
@keyframes gradient-shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
'''
body_05 = '''
<div class="summary-grid">
  <div class="summary-card">
    <span class="card-icon">🚀</span><div class="card-name">시스템 재설계</div><div class="card-desc">단순 툴 도입이 아닌 비즈니스 병목 해결</div>
  </div>
  <div class="summary-card">
    <span class="card-icon">📈</span><div class="card-name">비즈니스 임팩트</div><div class="card-desc">시간과 비용 등 숫자로 증명하는 가치 창출</div>
  </div>
  <div class="summary-card">
    <span class="card-icon">👑</span><div class="card-name">리더십 결단</div><div class="card-desc">프로세스 이해도와 과감한 Risk Taking</div>
  </div>
  <div class="summary-card">
    <span class="card-icon">🛡️</span><div class="card-name">Harness Engineering</div><div class="card-desc">영구적 통제 규칙으로 퀄리티 보장 및 표준화</div>
  </div>
  <div class="summary-card">
    <span class="card-icon">🤖</span><div class="card-name">Human-on-the-loop</div><div class="card-desc">에이전트가 95% 주도, 인간은 5% 치명적 결정만</div>
  </div>
  <div class="summary-card">
    <span class="card-icon">🔁</span><div class="card-name">자체 피드백 루프</div><div class="card-desc">스스로 실패 원인을 분석하고 개선하는 체계</div>
  </div>
</div>
<div class="conclusion">
  <div class="conclusion-line">AX는 도입이 아니라 운영이다.</div>
</div>
'''
write_html('05-summary.html', '요약 및 마무리', css_05, body_05,
           '<a href="04-human-loop.html" onclick="event.preventDefault(); navigateTo(this.href)">&larr; 이전</a>',
           '<a href="index.html">05 / 05</a>',
           '<span class="nav-disabled">다음 &rarr;</span>',
           "document.addEventListener('keydown', function(e) { if(e.key==='ArrowLeft') navigateTo('04-human-loop.html'); });")

print('All HTML slide files have been generated.')
