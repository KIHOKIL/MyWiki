import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

out_pptx = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\08_Bento_Grid_Presentation.pptx"
chart_png = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\assets\benchmark_comparison_chart.png"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)  # 16:9 Widescreen

# Bento Dark Theme Palette (Matching 04_Bento_Presentation.html)
CANVAS_BG = RGBColor(9, 10, 15)            # #090A0F
CARD_BG = RGBColor(18, 21, 31)             # #12151F
CARD_BORDER_DEFAULT = RGBColor(36, 42, 58) # Subtle border rgba(255,255,255,0.08)

# Vibrant Accents
ACCENT_CYAN = RGBColor(56, 189, 248)       # #38BDF8
ACCENT_INDIGO = RGBColor(99, 102, 241)     # #6366F1
ACCENT_EMERALD = RGBColor(52, 211, 153)    # #34D399
ACCENT_AMBER = RGBColor(251, 191, 36)      # #FBBF24
ACCENT_ROSE = RGBColor(244, 63, 94)        # #F43F5E
ACCENT_PURPLE = RGBColor(168, 85, 247)     # #A855F7

TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)

# Bento Box Corner Radius (12pt = ~16px in HTML Bento)
BENTO_RADIUS_PT = 12.0
STRIPE_THICKNESS_PT = 3.5

def set_canvas_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = CANVAS_BG
    bg.line.fill.background()
    return bg

def apply_corner_radius(shape, radius_pt=BENTO_RADIUS_PT):
    min_dim_pt = min(shape.width.pt, shape.height.pt)
    if min_dim_pt > 0:
        shape.adjustments[0] = radius_pt / min_dim_pt

def add_clean_header(slide, tag_text, title_text, subtitle_text=None, tag_color=ACCENT_CYAN):
    tb = slide.shapes.add_textbox(Inches(0.9), Inches(0.48), Inches(11.5), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_tag = tf.paragraphs[0]
    p_tag.text = f"●  {tag_text.upper()}"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = tag_color

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(3)

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_bento_box(slide, x, y, w, h,
                  tag=None,
                  title=None,
                  accent_color=None,
                  accent_pos="top",  # "top" or "left" matching CSS border-top / border-left
                  content_lines=None,
                  title_size=15,
                  body_size=11,
                  bg_color=CARD_BG):
    """
    Creates an authentic CSS-like Bento Box in PowerPoint:
    Uses a dual-layer concentric rounded rectangle technique so the top (or left)
    accent bar curves 100% seamlessly along the rounded corners of the box!
    """
    offset = Pt(STRIPE_THICKNESS_PT)

    if accent_color:
        # 1. Base Accent Shape (exposes a curved border-top or border-left crescent)
        accent_base = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        accent_base.fill.solid()
        accent_base.fill.fore_color.rgb = accent_color
        accent_base.line.fill.background()
        apply_corner_radius(accent_base, radius_pt=BENTO_RADIUS_PT)

        # 2. Foreground Card Surface shifted slightly to reveal the curved accent bar
        if accent_pos == "left":
            card_x = x + offset
            card_y = y
            card_w = w - offset
            card_h = h
        else:  # "top"
            card_x = x
            card_y = y + offset
            card_w = w
            card_h = h - offset

        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = CARD_BORDER_DEFAULT
        card.line.width = Pt(1.0)
        apply_corner_radius(card, radius_pt=BENTO_RADIUS_PT)
    else:
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = CARD_BORDER_DEFAULT
        card.line.width = Pt(1.0)
        apply_corner_radius(card, radius_pt=BENTO_RADIUS_PT)

    # 3. Inner Text Box
    tb = slide.shapes.add_textbox(x + Inches(0.32), y + Inches(0.28), w - Inches(0.64), h - Inches(0.56))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    first = True
    if tag:
        p_tag = tf.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = accent_color if accent_color else ACCENT_CYAN
        first = False

    if title:
        p_t = tf.paragraphs[0] if first else tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        if not first:
            p_t.space_before = Pt(3)
        first = False

    if content_lines:
        for idx, line in enumerate(content_lines):
            p_c = tf.add_paragraph()
            p_c.text = line
            p_c.font.size = Pt(body_size)
            
            if line.startswith("💡") or line.startswith("🚨") or line.startswith("🎯") or line.startswith("✅"):
                p_c.font.bold = True
                p_c.font.color.rgb = TEXT_WHITE
                p_c.space_before = Pt(6)
            elif line.startswith("•"):
                p_c.font.color.rgb = TEXT_WHITE
                p_c.space_before = Pt(3.5)
            elif idx == 0 and title:
                p_c.font.color.rgb = TEXT_MUTED
                p_c.space_before = Pt(5)
            else:
                p_c.font.color.rgb = TEXT_MUTED
                p_c.space_before = Pt(2.5)

    return card

# ==============================================================================
# SLIDE 1: Bento Hero Cover (Asymmetric Modular Grid)
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s1)

# Main Large Hero Box (Left 60%)
add_bento_box(
    s1, Inches(0.9), Inches(0.85), Inches(7.5), Inches(5.8),
    tag="BENTO ARCHITECTURE · META SENIOR TECH TALK",
    title="AI 에이전트를 위한\n2nd Brain과 Eval 프레임워크",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=26,
    body_size=12.5,
    content_lines=[
        "실리콘밸리 메타 8년차 시니어 엔지니어 하재상 세미나 전수 분석 (77분)",
        "",
        "자율 코딩 에이전트 도입의 성공을 결정하는 두 개의 절대적인 기둥:",
        "1. Context Layer (2nd Brain): 설명 없이 컴파일러 수준의 맥락을 자동 공급",
        "2. Verification Layer (Eval): 결정론적 하드 체크와 다수결 검증으로 신뢰도 보장",
        "",
        "💡 모바일 통신 / 물리계층(PHY) C/C++ 펌웨어 코드 리뷰 파이프라인 대응 전략 수록"
    ]
)

# Right Stack 1 (Top-Right)
add_bento_box(
    s1, Inches(8.65), Inches(0.85), Inches(3.8), Inches(2.75),
    tag="Meta Production Reality",
    title="📊 $30,000 / 월 에이전트 실험",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 메타 사내 대시보드 기준 월 $30,000 API 사용",
        "• 아무리 규칙과 도구를 잘 줘도 검증이 없으면 위임 불가",
        "• '코딩 속도'에서 '검증 병목'으로 개발의 축 이동",
        "• TDD 없이 배포하지 않듯, Eval 없는 배포는 자살행위"
    ]
)

# Right Stack 2 (Bottom-Right)
add_bento_box(
    s1, Inches(8.65), Inches(3.85), Inches(3.8), Inches(2.8),
    tag="Core Foundation",
    title="🛡️ 시스템 하네스(Harness)",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 🕸️ Codebase Graph: 컴파일러 AST 기반 정밀 지도",
        "• 🧠 Code Memory: 커밋/PR의 'Why' 추적 (BM25)",
        "• ⚖️ 2단계 Eval: Hard Check (0점 탈락) + K-Judge",
        "• 🧪 Sandbox & CI: 무균 격리 및 PR 머지 자동 차단"
    ]
)

# ==============================================================================
# SLIDE 2: Paradigm Shift (1-Wide + 2-Col)
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s2)
add_clean_header(s2, "Part 1 · Paradigm Shift", "AI 코딩 패러다임의 전환: 코딩 속도에서 '검증 병목'으로", "단순 프롬프트 엔지니어링의 한계와 시스템 하네스(Harness) 전환의 필연성", tag_color=ACCENT_INDIGO)

add_bento_box(
    s2, Inches(0.9), Inches(1.8), Inches(11.55), Inches(1.65),
    tag="Bottleneck Evolution",
    title="⚡ 개발 병목의 이동 공식",
    accent_color=ACCENT_INDIGO,
    accent_pos="top",
    title_size=15,
    body_size=11,
    content_lines=[
        "[과거] 코드 타이핑 및 구현 속도 병목  ➔  [LLM 도입] 초당 수백 줄 코드 작성 (생산성 착시)",
        "[현재의 진짜 병목] 초대형 PR 범람으로 인한 '인간 리뷰어의 검증 한계' 및 '환각(Hallucination) 공포'",
        "💡 결론: 프롬프트를 깎지 말고, 컨텍스트 주입과 자동 검증을 대행하는 '하네스(Harness)'를 구축하라."
    ]
)

add_bento_box(
    s2, Inches(0.9), Inches(3.65), Inches(5.65), Inches(3.25),
    tag="Legacy Problem",
    title="❌ 프롬프팅 중심 코딩의 붕괴",
    accent_color=ACCENT_ROSE,
    accent_pos="left",
    title_size=15,
    body_size=11,
    content_lines=[
        "• 초대형 PR 쏟아짐: 주니어/시니어 가리지 않고 검증 피로도 극대화",
        "• 세션 컨텍스트 리셋: 새 창을 열 때마다 매번 프로젝트 규칙 재설명",
        "• 침묵의 회귀(Regression): 프롬프트 한 줄 바꿨다가 기존 기능 파괴",
        "• 불안감으로 인한 수동 전수 검사: 결국 인간이 일일이 코드를 확인해야 함"
    ]
)

add_bento_box(
    s2, Inches(6.8), Inches(3.65), Inches(5.65), Inches(3.25),
    tag="Harness Engineering",
    title="🛡️ 시스템 하네스(Harness)의 해결책",
    accent_color=ACCENT_EMERALD,
    accent_pos="left",
    title_size=15,
    body_size=11,
    content_lines=[
        "• Context Layer (2nd Brain): 시스템이 컴파일러 AST와 Git에서 맥락 자동 주입",
        "• Blast Radius 선행 계산: 코드 변경 전 파급 반경을 수학적으로 먼저 도출",
        "• Verification Layer (Eval): 결정론적 코드 검사 + K=3 심사위원 다수결 채점",
        "• CI Gatekeeper: 검증된 안전한 코드만 프로덕션에 자동 병합 허용"
    ]
)

# ==============================================================================
# SLIDE 3: Meta Case Study (3-Box Trio with Curved Top Bars)
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s3)
add_clean_header(s3, "Part 2 · Meta Case Study", "메타 프로덕션 실전 사례: 성능 프로파일링 10시간 ➔ 30분 단축", "대규모 분산 백엔드 서비스의 레이턴시 트리아지를 에이전틱 하네스로 95% 단축한 비결", tag_color=ACCENT_CYAN)

add_bento_box(
    s3, Inches(0.9), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="Pain Point · 10 Hours",
    title="1. 기존 수작업의 한계",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=15,
    body_size=11,
    content_lines=[
        "• 분산 서비스의 응답 지연(Latency) 급증 발생",
        "• 수천 개 모듈 간 상호 호출로 원인 추적 난해",
        "• 시니어 엔지니어가 Flame Graph와 Trace 데이터를 수작업 대조",
        "• 단순 Grep 검색 시 90% 이상 무관한 주석/더미가 유입되어 LLM 환각 유발",
        "",
        "🚨 결과: 원인 규명에 평균 10시간 이상 소모"
    ]
)

add_bento_box(
    s3, Inches(4.85), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="3-Layer Solution",
    title="2. 하네스 3대 결합 솔루션",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=15,
    body_size=11,
    content_lines=[
        "• 🛠️ Profiling MCP Tool",
        "  Flame Graph 수치를 LLM이 정량 질의하는 표준화 도구",
        "• 📋 Senior Skill Manual",
        "  메타 시니어의 5단계 진단 체크리스트를 마크다운 화",
        "• 🕸️ 2nd Brain Graph",
        "  함수 호출선 및 데이터 흐름을 AST 수준에서 즉시 역추적",
        "",
        "🎯 에이전트가 가설 수립 및 코드 검증을 자율 병렬 수행"
    ]
)

add_bento_box(
    s3, Inches(8.8), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="Key Outcome · 30 Mins",
    title="3. 압도적 성과 & 교훈",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=15,
    body_size=11,
    content_lines=[
        "• ⏱️ 소요 시간 95% 단축",
        "  10시간의 고난도 트리아지가 30분 만에 패치 제안까지 완료",
        "• 🎯 노이즈 제로 컨텍스트",
        "  Grep의 쓰레기 데이터를 걸러내고 순수 의존 함수만 주입",
        "• 💡 핵심 교훈",
        "  '표준 도구(MCP)' + '시니어 노하우(Skill)' + '코드 지도(Brain)' 3자 결합이 자율화의 핵심"
    ]
)

# ==============================================================================
# SLIDE 4: Codebase Graph with Real Benchmark Chart Image
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s4)
add_clean_header(s4, "Part 3 · Second Brain Architecture", "세컨드 브레인 기둥 1: 컴파일러/AST 기반 Codebase Graph", "Grep의 텍스트 한계를 넘어 수학적으로 100% 결정론적인 파급 반경(Blast Radius) 도출", tag_color=ACCENT_CYAN)

add_bento_box(
    s4, Inches(0.9), Inches(1.8), Inches(6.0), Inches(5.1),
    tag="Precision Compiler Indexing",
    title="🕸️ Grep vs Compiler AST 비교",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=16,
    body_size=11,
    content_lines=[
        "• 텍스트 Grep의 치명적 결함:",
        "  - 정규표현식 단순 매칭으로 주석, 테스트 더미, 유사 이름 대량 유입",
        "  - 컨텍스트 윈도우 폭증으로 모델 추론 정확도 급락",
        "",
        "• `brain build` 컴파일러 AST 파싱:",
        "  - TypeScript Compiler API, Clang LibTooling 기반 AST 분석",
        "  - 모든 함수/구조체/클래스에 고유 'Symbol ID' 부여",
        "  - `CALLS`, `IMPORTS`, `WRITES_TO` 관계를 방향성 엣지로 인덱싱",
        "",
        "🎯 결과: 노이즈 90% 제거, 핵심 의존성만 컴팩트 주입"
    ]
)

add_bento_box(
    s4, Inches(7.2), Inches(1.8), Inches(5.25), Inches(2.2),
    tag="Algorithmic Traversal",
    title="⚡ BFS Hopping: Blast Radius 계산",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 함수 A 수정 시 영향받는 2차, 3차 호출 모듈 추적",
        "• 그래프 너비 우선 탐색(BFS)으로 파급 반경을 수학적으로 계산",
        "• 에이전트에게 '이 파일을 고치면 B, C 모듈이 깨집니다' 사전 경고"
    ]
)

add_bento_box(
    s4, Inches(7.2), Inches(4.2), Inches(5.25), Inches(2.7),
    tag="Benchmark Verification",
    title="📊 도구별 성능 및 토큰 효율",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14,
    body_size=10
)
if os.path.exists(chart_png):
    s4.shapes.add_picture(chart_png, Inches(7.45), Inches(5.0), width=Inches(4.75), height=Inches(1.75))

# ==============================================================================
# SLIDE 5: 2x2 Bento Matrix
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s5)
add_clean_header(s5, "Part 3 · Second Brain Architecture", "세컨드 브레인 기둥 2: 'Why'를 추적하는 Code Memory & 라우팅 규칙", "그래프의 구조적 한계를 보완하는 역사적 맥락과 2원화 실행 정책", tag_color=ACCENT_AMBER)

add_bento_box(
    s5, Inches(0.9), Inches(1.8), Inches(5.65), Inches(2.45),
    tag="Historical Context",
    title="🧠 Code Memory: 아키텍처 의도 복원",
    accent_color=ACCENT_AMBER,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 그래프의 맹점: '현재 구조'만 알 뿐 'Why'를 알지 못함",
        "• '이 함수는 왜 10us 딜레이를 주는가?' ➔ 과거 하드웨어 버그 회피 사유",
        "• `why.mjs` & `query.mjs`: Git 커밋, PR 리뷰, ADR 연동",
        "• 의사결정 맥락을 보존하여 에이전트의 성급한 리팩토링 방지"
    ]
)

add_bento_box(
    s5, Inches(6.8), Inches(1.8), Inches(5.65), Inches(2.45),
    tag="Retrieval Ranking",
    title="🔍 BM25 랭킹: 희귀 도메인 용어 적중",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 일반 벡터 임베딩은 통신/하드웨어 전문 약어 매칭에 취약",
        "• BM25는 희귀 엔지니어링 고유명사(IDF 가중치)를 최우선 랭킹",
        "• CPHY, DPHY, HARQ, MMIO 등 도메인 변경 맥락을 즉각 적중",
        "• 무관한 일반 단어 노이즈를 배제하여 검색 정밀도 극대화"
    ]
)

add_bento_box(
    s5, Inches(0.9), Inches(4.45), Inches(5.65), Inches(2.45),
    tag="Routing Policy · Local",
    title="⚡ Fast Path (로컬 수정 우회)",
    accent_color=ACCENT_INDIGO,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 모든 단순 작업에 Brain을 태우면 레이턴시와 토큰 낭비 발생",
        "• 단일 파일 내 자명한 타이포 및 로컬 버그 수정",
        "• LLM 직접 편집 (Brain 조회 바이패스)",
        "• 1초 이내 초고속 응답 달성 및 불필요한 토큰 소모 80% 절감"
    ]
)

add_bento_box(
    s5, Inches(6.8), Inches(4.45), Inches(5.65), Inches(2.45),
    tag="Routing Policy · Architecture",
    title="🏛️ Brain Path (구조적 수정 의무화)",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 공용 인터페이스 변경, 다중 모듈 리팩토링, 레지스터 정의 수정",
        "• 반드시 Code Graph BFS + Why 메모리 선행 조회 강제",
        "• 변경 전 파급 반경(Blast Radius) 확인 후 안전하게 코드 작성",
        "• 다른 팀 모듈을 깨뜨리는 침묵의 장애를 시스템 레벨에서 원천 차단"
    ]
)

# ==============================================================================
# SLIDE 6: Eval 2-Stage Verification Architecture
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s6)
add_clean_header(s6, "Part 4 · Verification Architecture", "Eval 체계: 결정론적 Hard Check + K-Judge Majority Voting", "Anthropic 프롬프트 업데이트 참사를 방지하는 2단계 검증 및 샌드박스 무균 격리", tag_color=ACCENT_PURPLE)

add_bento_box(
    s6, Inches(0.9), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="Stage 1 · Deterministic",
    title="1. Hard Check (하드 체크)",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 컴파일 성공 여부 (Clang exit code == 0)",
        "• 정적 분석 린트 무결점 (Clang-Tidy)",
        "• 단위 테스트 통과 (Unit Test Pass)",
        "• 입출력 JSON 스키마 규격 일치",
        "",
        "🚨 0점 탈락 규칙 (Short-Circuit):",
        "단 1개라도 실패 시 즉시 0점 탈락 처리하여 고비용 LLM 정성 평가를 생략"
    ]
)

add_bento_box(
    s6, Inches(4.85), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="Stage 2 · Qualitative",
    title="2. K-Judge Majority Voting",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• LLM-as-a-Judge 정성 평가",
        "• LLM 고유의 확률적 분산(Variance) 제거",
        "• K=3회 독립 세션 실행 (3인의 교수 심사 모델)",
        "• 2표 이상 찬성(Pass) 시에만 최종 합격",
        "",
        "🎯 평가 항목:",
        "아키텍처 규칙 준수, 가독성, 예외 처리 무결성"
    ]
)

add_bento_box(
    s6, Inches(8.8), Inches(1.8), Inches(3.65), Inches(5.1),
    tag="Infrastructure & Gate",
    title="3. Sandbox & CI Gate",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 🧪 무균 샌드박스 (Sandbox Isolation)",
        "  정답 파일(Ground Truth) 및 로컬 전역 설정(~/.claude) 오염 원천 차단",
        "• 🎯 골든 프롬프트 (Golden Prompts)",
        "  실무 전형 20~30개 시나리오 벤치마크",
        "• 🛡️ CI Gatekeeper",
        "  'CI에서 자동 실행되지 않는 Eval은 없는 것과 같다.' PR 머지 강제"
    ]
)

# ==============================================================================
# SLIDE 7: 5-Step Stepper + 3 Modular Question Bento Boxes
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s7)
add_clean_header(s7, "Part 5 · Maturity & Standards", "메타의 Eval 성숙도 5단계 (Levels 0 ~ 4) 및 스킬 3대 필수 질문", "감(Vibe)에 의존하는 단계에서 셀프 피드백 자가 교정 루프까지의 진화", tag_color=ACCENT_EMERALD)

step_data = [
    ("Level 0", "느낌 (Vibe)", "'어? 잘 되는 것 같은데?'\n가장 위험한 단계", ACCENT_ROSE, Inches(0.9)),
    ("Level 1", "단위 테스트", "기본적인 컴파일 & 린트\n결정론적 하드 체크", ACCENT_AMBER, Inches(3.25)),
    ("Level 2", "오프라인 Eval", "골든 프롬프트 20~30개\n정량적 점수 벤치마크", ACCENT_CYAN, Inches(5.6)),
    ("Level 3", "CI Gatekeeper", "PR 머지 전 자동 통과\n실패 시 머지 차단", ACCENT_INDIGO, Inches(7.95)),
    ("Level 4", "Self-Improving", "실패 피드백 분석 후\n스킬/프롬프트 자가 개선", ACCENT_EMERALD, Inches(10.3))
]
for lvl, name, desc, col, x_pos in step_data:
    add_bento_box(
        s7, x_pos, Inches(1.8), Inches(2.15), Inches(2.2),
        tag=lvl,
        title=name,
        accent_color=col,
        accent_pos="top",
        title_size=13.5,
        body_size=10,
        content_lines=desc.split("\n")
    )

add_bento_box(
    s7, Inches(0.9), Inches(4.3), Inches(3.65), Inches(2.6),
    tag="Rubric 01 · Trigger",
    title="🎯 1. 호출 정확도 (Triggering)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14,
    body_size=10.5,
    content_lines=[
        "• 불려야 할 상황에서 정확하게 호출되는가?",
        "• 무관한 요청에서 과도하게 호출되어 토큰과 시간을 낭비하지 않는가?",
        "• 프롬프트 트리거 설명(Description)의 정밀도 검증"
    ]
)

add_bento_box(
    s7, Inches(4.85), Inches(4.3), Inches(3.65), Inches(2.6),
    tag="Rubric 02 · Uplift",
    title="📈 2. 성능 향상 (Performance)",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14,
    body_size=10.5,
    content_lines=[
        "• 기존 Baseline(스킬 없음) 대비 성공률이 유의미하게 개선되었는가?",
        "• 복잡한 멀티스텝 작업의 완수 시간이 실질적으로 단축되었는가?",
        "• 골든 프롬프트 벤치마크 점수 상향 입증"
    ]
)

add_bento_box(
    s7, Inches(8.8), Inches(4.3), Inches(3.65), Inches(2.6),
    tag="Rubric 03 · Safety",
    title="🛡️ 3. 무리그레션 (Non-Regression)",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=14,
    body_size=10.5,
    content_lines=[
        "• 새 스킬 추가로 인해 기존에 잘 되던 기능이 깨지지 않는가?",
        "• 다른 스킬과의 충돌이나 예기치 않은 부작용이 없는가?",
        "• 전수 회귀 테스트 100% 통과 보장"
    ]
)

# ==============================================================================
# SLIDE 8: Domain Blueprint & Epilogue
# ==============================================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s8)
add_clean_header(s8, "Part 6 · Domain Blueprint & Epilogue", "모바일 통신 물리계층(PHY) SW 그룹 적용 가이드 & 에필로그", "임베디드 C/C++ 펌웨어 리뷰 파이프라인으로의 1:1 대응 및 에이전트 시대 인간의 주도권", tag_color=ACCENT_PURPLE)

add_bento_box(
    s8, Inches(0.9), Inches(1.8), Inches(5.65), Inches(5.1),
    tag="Group Leader Blueprint",
    title="📡 모바일 통신 PHY SW 2nd Brain 로드맵",
    accent_color=ACCENT_CYAN,
    accent_pos="left",
    title_size=15,
    body_size=11,
    content_lines=[
        "• 1. Clang AST 기반 하드웨어 레지스터 맵 그래프",
        "  MMIO 주소, 비트필드 구조체, ISR 인터럽트 벡터, 3GPP FSM 상태 머신을 심볼 링킹하여 레지스터 쓰기 경로 즉각 추적",
        "",
        "• 2. 3GPP 규격 및 실리콘 에라타(Silicon Errata) Memory",
        "  과거 모뎀 IODT 필드 이슈 이력과 칩셋 호환성 패치 사유(Why)를 BM25로 인덱싱하여 무환각 코드 리뷰 지원",
        "",
        "• 3. 임베디드 펌웨어 Eval CI 게이트",
        "  Hard Check(ARM GCC Cross-Compile + SRAM/D-Cache 사용량) + Domain Judge(ISR 동시성 경합 및 us 실시간 데드라인 규격 다수결 판정)"
    ]
)

add_bento_box(
    s8, Inches(6.8), Inches(1.8), Inches(5.65), Inches(5.1),
    tag="Human Agency · Philosophy",
    title="💡 에필로그: 에이전트 시대, 인간의 주도권",
    accent_color=ACCENT_PURPLE,
    accent_pos="left",
    title_size=15,
    body_size=11,
    content_lines=[
        "\"에이전트에게 주도권을 뺏기지 마세요.\"",
        "",
        "• 에이전트를 돌리느라 24시간 쉬지 못하고 가족과 건강을 해치는 것은 도구의 본질을 전도시키는 것",
        "",
        "• 나의 1번 가치(가족, 건강, 엔지니어링 본질)를 확고히 세우고, 에이전트는 나를 그 가치로 데려다주는 강력한 지렛대로 부려야 함",
        "",
        "• 설계와 전략, 아키텍처 판단 ➔ 인간 테크리드",
        "• 구현과 검증 ➔ 견고한 시스템 하네스(2nd Brain + Eval CI)"
    ]
)

prs.save(out_pptx)
print(f"Successfully generated curved-stripe Bento Presentation: {out_pptx}")
