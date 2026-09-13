import os

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Herdr Slides</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background: #0a0f1a;
            color: #e2e8f0;
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}
        .slide {{
            background: rgba(139, 148, 158, 0.04);
            border: 1px solid rgba(139, 148, 158, 0.1);
            border-radius: 16px;
            padding: 4rem;
            width: 80%;
            max-width: 1000px;
            height: 60vh;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            justify-content: center;
            animation: fadeIn 0.5s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        h1 {{
            font-size: 3rem;
            background: linear-gradient(135deg, #7c3aed, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }}
        h2 {{ color: #38bdf8; font-size: 2rem; }}
        p, li {{ font-size: 1.5rem; line-height: 1.6; }}
        .nav {{
            position: absolute;
            bottom: 2rem;
            display: flex;
            gap: 1rem;
        }}
        a {{
            color: #fff;
            text-decoration: none;
            background: #7c3aed;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: 0.3s;
        }}
        a:hover {{ background: #38bdf8; }}
        a.disabled {{ background: #555; pointer-events: none; }}
    </style>
</head>
<body>
    <div class="slide">
        {content}
    </div>
    <div class="nav">
        <a href="{prev_link}" class="{prev_class}">Prev</a>
        <a href="{next_link}" class="{next_class}">Next</a>
    </div>
    <script>
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' && '{next_link}' !== '#') window.location.href = '{next_link}';
            if (e.key === 'ArrowLeft' && '{prev_link}' !== '#') window.location.href = '{prev_link}';
        }});
    </script>
</body>
</html>"""

slides_data = [
    {
        "filename": "index.html",
        "content": """<h1>에이전트 시대의 터미널 Herdr</h1>
                      <p>메타 시니어 엔지니어가 잘때도 에이전트를 돌리는 법</p>
                      <p style="margin-top:2rem; color:#94a3b8;">방향키(←, →)를 눌러 이동하세요</p>"""
    },
    {
        "filename": "01_background.html",
        "content": """<h2>1. 터미널 멀티플렉서의 귀환</h2>
                      <ul>
                        <li>에이전트가 오랫동안 돌기 시작하면서 tmux가 다시 필수품이 됨</li>
                        <li><strong>치명적 한계</strong>: tmux는 안에서 도는 게 '봇'인지 모름</li>
                        <li>에이전트가 승인을 기다려도 사람이 못 보면 멈춰 있음 (병목은 인간)</li>
                      </ul>"""
    },
    {
        "filename": "02_herdr_features.html",
        "content": """<h2>2. Herdr 핵심 강점 3가지</h2>
                      <ul>
                        <li><strong>상태 인식 (5 States)</strong>: Blocked, Working, Done 등 사이드바 표시</li>
                        <li><strong>에이전트 주도 조작</strong>: 에이전트가 명령어로 탭/Pane을 직접 분할</li>
                        <li><strong>세션 복원력</strong>: 터미널을 꺼도 <code>claude --resume</code>로 대화 복원</li>
                      </ul>"""
    },
    {
        "filename": "03_demo.html",
        "content": """<h2>3. 오케스트레이션 데모 (AutoKliq)</h2>
                      <ul>
                        <li>오케스트레이터 Claude Code가 <code>herdr split-pane</code> 실행</li>
                        <li>독립된 3개의 서브 에이전트를 백그라운드 구동</li>
                        <li>리더는 사이드바의 <strong><span style="color:#ef4444;">Blocked</span></strong> 알림만 보고 방향성 승인</li>
                      </ul>"""
    },
    {
        "filename": "04_next_action.html",
        "content": """<h2>4. 실무 도입 (Next Action)</h2>
                      <ul>
                        <li><strong>목표</strong>: Legacy C/C++ 리팩토링 및 레지스터 분석 파이프라인</li>
                        <li><strong>전략</strong>: Master 에이전트가 헤더 분석 / 파싱 에이전트를 개별 Pane에 띄움</li>
                        <li>비동기 최적화로 빌드 대기 시간 낭비 제로화</li>
                      </ul>"""
    }
]

def build():
    slides_dir = "slides"
    if not os.path.exists(slides_dir):
        os.makedirs(slides_dir)
        
    for i, slide in enumerate(slides_data):
        prev_link = slides_data[i-1]["filename"] if i > 0 else "#"
        next_link = slides_data[i+1]["filename"] if i < len(slides_data)-1 else "#"
        
        prev_class = "" if prev_link != "#" else "disabled"
        next_class = "" if next_link != "#" else "disabled"
        
        html = html_template.format(
            content=slide["content"],
            prev_link=prev_link,
            next_link=next_link,
            prev_class=prev_class,
            next_class=next_class
        )
        
        filepath = os.path.join(slides_dir, slide["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
            
    print(f"Generated {len(slides_data)} slides in '{slides_dir}' directory.")

if __name__ == "__main__":
    build()
