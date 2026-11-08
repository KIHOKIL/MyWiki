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
    tb = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(1.1))
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
    p_title.font.size = Pt(21.5)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(3)

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(2)

def add_bento_box(slide, x, y, w, h,
                  tag=None,
                  title=None,
                  accent_color=None,
                  accent_pos="top",  # "top" or "left" matching CSS border-top / border-left
                  content_lines=None,
                  title_size=14.5,
                  body_size=10.5,
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
    tb = slide.shapes.add_textbox(x + Inches(0.28), y + Inches(0.24), w - Inches(0.56), h - Inches(0.48))
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

            if line.startswith("💡") or line.startswith("🚨") or line.startswith("🎯") or line.startswith("✅") or line.startswith("📌"):
                p_c.font.bold = True
                p_c.font.color.rgb = TEXT_WHITE
                p_c.space_before = Pt(5)
            elif line.startswith("•"):
                p_c.font.color.rgb = TEXT_WHITE
                p_c.space_before = Pt(3)
            elif idx == 0 and title:
                p_c.font.color.rgb = TEXT_MUTED
                p_c.space_before = Pt(4)
            else:
                p_c.font.color.rgb = TEXT_MUTED
                p_c.space_before = Pt(2)

    return card

# ==============================================================================
# SLIDE 1: Bento Hero Cover (Asymmetric Modular Grid)
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s1)

add_bento_box(
    s1, Inches(0.9), Inches(0.85), Inches(7.5), Inches(5.8),
    tag="BENTO ARCHITECTURE · META SENIOR TECH TALK + 68 SLIDES & REPO",
    title="AI 에이전트를 위한\n2nd Brain과 Eval 프레임워크",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=25,
    body_size=12,
    content_lines=[
        "실리콘밸리 메타 8년차 시니어 엔지니어 하재상 세미나 전수 분석 (77분)",
        "강사 원본 슬라이드 68장 CV 캡처 + 공개 레포(second-brain-eval-kit) 코드 완결판",
        "",
        "• Context Layer (codebase-brain): TS Compiler API AST 그래프(query.mjs) + SQLite FTS5 BM25/RRF 코드 메모리(why.mjs) + 3-Col 라우팅",
        "• Verification Layer (skill-eval): 4대 무균 격리(isolation.py) + 0점의 3가지 이름(checks.py) + K=3 다수결 Judge",
        "",
        "💡 모바일 통신 / 물리계층(PHY) C/C++ 펌웨어 코드 리뷰 파이프라인 대응 전략 수록"
    ]
)

add_bento_box(
    s1, Inches(8.65), Inches(0.85), Inches(3.8), Inches(2.75),
    tag="Meta Production Reality",
    title="📊 $30,000 / 월 & 10h ➔ 30m",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 메타 사내 대시보드 기준 월 $30,000 토큰 실험",
        "• 프로파일링 MCP + 시니어 스킬 + Brain 결합으로 10시간 트리아지를 30분으로 95% 단축",
        "• '코딩 속도'에서 '검증 병목'으로 개발의 축 이동",
        "• TDD 없이 배포하지 않듯, Eval 없는 배포는 불가능"
    ]
)

add_bento_box(
    s1, Inches(8.65), Inches(3.85), Inches(3.8), Inches(2.8),
    tag="Open-Source Reference Kit",
    title="🛡️ second-brain-eval-kit",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 🕸️ query.mjs: Symbol ID + 3대 커버리지 라벨",
        "• 🧠 why.mjs: FTS5 BM25(3.0, 1.0) + RRF 퓨전",
        "• ⚖️ checks.py: invalid / safety_violation / fail",
        "• 🧪 isolation.py: 4대 차단 + 21/21 probe 검증"
    ]
)

# ==============================================================================
# SLIDE 2: AutoKliq Real-World Experiment & Bottleneck Shift (Slide #13)
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s2)
add_clean_header(
    s2,
    "Part 1 · AutoKliq Benchmark (Slide #13)",
    "코딩 속도에서 '검증 병목'으로 & AutoKliq 394개 파급 실험",
    "질문: '크레딧 예약 파일(lib/credit-reservations.ts)을 바꾸면 깨질 수 있는 파일을 전부 찾아 줘'",
    tag_color=ACCENT_INDIGO
)

add_bento_box(
    s2, Inches(0.9), Inches(1.75), Inches(11.55), Inches(1.65),
    tag="Bottleneck Evolution & Meta Profiling Case",
    title="⚡ 개발 병목의 이동 공식 & 메타 프로파일링 10시간 ➔ 30분 단축",
    accent_color=ACCENT_INDIGO,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• [과거] 타이핑 속도 병목 ➔ [현재] 초대형 PR 범람으로 인한 '인간 리뷰어의 검증 한계' 및 '환각 공포'",
        "• 메타 실전 사례: Profiling MCP(정량 수치 질의) + 시니어 스킬(5단계 체크리스트) + 2nd Brain 결합으로 10시간을 30분으로 단축",
        "💡 핵심: 에이전트가 매번 밑바닥부터 탐색 스크립트를 짜게 방치하지 말고, 결정론적 하네스(Harness)를 공급하라."
    ]
)

add_bento_box(
    s2, Inches(0.9), Inches(3.6), Inches(5.65), Inches(3.3),
    tag="Without Skill · Slide #13 Left",
    title="❌ 스킬 없이 실행 (56초 · 매번 스크립트 재발명)",
    accent_color=ACCENT_ROSE,
    accent_pos="left",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• Grep 2회 시도 후 직접 호출이 3개뿐임을 발견하고 당황",
        "• 에이전트가 즉석에서 일회용 import 역추적 스크립트를 직접 코딩하여 실행",
        "• 소요 시간: 56초 | 탐색 결과: 394 / 394개 (144 tests)",
        "• 스크립트 재작성 빈도: 3 / 3 (매번 처음부터 다시 짬!)",
        "🚨 한계: 비결정론적 탐색, 높은 토큰 비용과 시간 낭비"
    ]
)

add_bento_box(
    s2, Inches(6.8), Inches(3.6), Inches(5.65), Inches(3.3),
    tag="With codebase-brain · Slide #13 Right",
    title="🛡️ 스킬과 함께 실행 (<1초 · 결정론적 9-Hop 추적)",
    accent_color=ACCENT_EMERALD,
    accent_pos="left",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• brain build: 6,230개 파일(TS 4,446, 문서 578, 커밋 1,358) 파싱해 12.19초 만에 brain.db(56.8 MB) 생성",
        "• brain impact lib/credit-reservations.ts 단 한 줄 호출",
        "• 9 Hops 전파를 <1초 만에 추적하여 394개 파일 + 144개 테스트 100% 결정론적 반환",
        "• 1-hop(3) ➔ 2-hop(21) ➔ 3-hop(146) ➔ 4-hop+(224)",
        "✅ 결과: 스크립트 재발명 0회, 100% 재현 가능한 정밀 지도"
    ]
)

# ==============================================================================
# SLIDE 3: Tiago Forte vs Dev 2nd Brain & 3 Architecture Components (Slides #16~#17)
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s3)
add_clean_header(
    s3,
    "Part 2 · Developer's 2nd Brain (Slides #16~#17)",
    "Tiago Forte 일반 세컨드 브레인 vs 개발자/에이전트용 세컨드 브레인",
    "소비자가 '사람'이 아닌 '코딩 에이전트'일 때 달라지는 3대 구성요소: ① 지도 + ② 코드 메모리 + ③ 라우팅",
    tag_color=ACCENT_CYAN
)

add_bento_box(
    s3, Inches(0.9), Inches(1.75), Inches(5.65), Inches(2.4),
    tag="General 2nd Brain · Tiago Forte (2022)",
    title="📓 일반 세컨드 브레인 (소비자: 사람)",
    accent_color=ACCENT_AMBER,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 대상 데이터: 책, 아티클, 개인 메모, 영감 노트",
        "• 분류 체계: PARA (Projects, Areas, Resources, Archives)",
        "• 접근 방식: 옵시디언/노션에서 사람이 직접 키워드 검색 및 열람",
        "• 목적: 인간의 장기 기억 보조 및 창작 아이디어 발상"
    ]
)

add_bento_box(
    s3, Inches(6.8), Inches(1.75), Inches(5.65), Inches(2.4),
    tag="Developer's 2nd Brain · Agent Consumer",
    title="🤖 개발자 세컨드 브레인 (소비자: 코딩 에이전트)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 대상 데이터: 코드베이스(AST) + 설계 문서/ADR/PR/장애 회고록",
        "• 핵심 구성: ① 지도(Graph) + ② 코드 메모리(Why) + ③ 라우팅(SKILL.md)",
        "• 접근 방식: 결정론적 CLI 도구(brain) + 마크다운 라우팅 테이블",
        "🚨 절대 원칙: '낡은 컨텍스트(Stale Context)는 없는 것보다 나쁘다'"
    ]
)

add_bento_box(
    s3, Inches(0.9), Inches(4.35), Inches(3.65), Inches(2.55),
    tag="Component 01 · Map",
    title="① 지도 (src/query.mjs)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14,
    body_size=10,
    content_lines=[
        "• TS Compiler API / AST 기반 파싱",
        "• 고유 Symbol ID: path#SymbolName",
        "• CALLS, IMPORTS, TESTS 방향성 엣지",
        "• N-Hop BFS로 파급 반경(impact) 도출"
    ]
)

add_bento_box(
    s3, Inches(4.85), Inches(4.35), Inches(3.65), Inches(2.55),
    tag="Component 02 · Memory",
    title="② 코드 메모리 (src/why.mjs)",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=14,
    body_size=10,
    content_lines=[
        "• Git 커밋 로그 + PR/설계 문서 인덱싱",
        "• SQLite FTS5 BM25 + RRF 하이브리드 랭킹",
        "• LLM 호출 비용 $0, <1초에 변경 사유(Why)와 커밋 해시 인용"
    ]
)

add_bento_box(
    s3, Inches(8.8), Inches(4.35), Inches(3.65), Inches(2.55),
    tag="Component 03 · Routing",
    title="③ 라우팅 (SKILL.md)",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14,
    body_size=10,
    content_lines=[
        "• 에이전트가 도구를 과호출하지 않도록 통제",
        "• 3열 매핑: The question | Call | Not this",
        "• 작은 작업엔 'do not call brain' 명시 (오발동 0/6 달성)"
    ]
)

# ==============================================================================
# SLIDE 4: Pillar 1 - Codebase Graph & 3 Coverage Labels (Slides #19~#21)
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s4)
add_clean_header(
    s4,
    "Part 3 · Pillar 1: Codebase Graph (Slides #19~#21)",
    "기둥 1: 컴파일러 AST 그래프(src/query.mjs)와 3대 커버리지 라벨",
    "그래프의 한계(동적 호출/이벤트 버스)를 에이전트에게 정직하게 알려 환각을 막는 메타데이터 설계",
    tag_color=ACCENT_CYAN
)

add_bento_box(
    s4, Inches(0.9), Inches(1.75), Inches(6.0), Inches(5.15),
    tag="Deterministic BFS & Honest Metadata · src/query.mjs",
    title="🕸️ Symbol ID 인덱싱 & 3대 커버리지 라벨",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 고유 Symbol ID 부여: lib/credit-reservations.ts#reserveCredits",
        "• N-Hop BFS 역방향 탐색: visited Set으로 순환 참조를 방지하며 depth별 의존 파일과 연결된 테스트(attachedTests)를 즉시 수집",
        "",
        "📌 왜 커버리지 라벨(Coverage Label)이 핵심인가?",
        "• 1. complete (완전 탐색): 모든 홉을 끝까지 추적 완료. 에이전트가 추가 grep 없이 결과를 100% 신뢰하고 즉시 답변",
        "• 2. truncated (상한 도달): 결과가 maxResults(500개) 또는 maxDepth(10)에 걸려 잘림. 누락 가능성을 에이전트에 경고",
        "• 3. partial (부분 그래프): 동적 import나 미해결 심볼(unresolved edge) 존재 시 표시하여 해당 구간만 추가 확인 유도",
        "• + stale 경고: git HEAD가 빌드 시점과 다르면 brain build 재실행 권고"
    ]
)

add_bento_box(
    s4, Inches(7.2), Inches(1.75), Inches(5.25), Inches(2.25),
    tag="Why AST Graph Beats Grep",
    title="⚡ Grep vs brain impact 결정적 차이",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• Grep: 주석/더미/동명이인 노이즈 90% 유입, 1-hop 텍스트만 매칭",
        "• brain impact: 컴파일러 AST 심볼 단위로 9-hop 전파를 <1초에 완주",
        "• 정직한 커버리지 라벨 덕분에 에이전트가 '다 찾았다'고 착각하는 환각 소멸"
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
    s4.shapes.add_picture(chart_png, Inches(7.45), Inches(4.95), width=Inches(4.75), height=Inches(1.75))

# ==============================================================================
# SLIDE 5: Pillar 2 & 3 - Code Memory (why.mjs) & SKILL.md Routing (Slides #22~#27)
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s5)
add_clean_header(
    s5,
    "Part 3 · Pillar 2 & 3: Code Memory & Routing (Slides #22~#27)",
    "기둥 2 & 3: FTS5 BM25+RRF 코드 메모리(why.mjs)와 3열 라우팅 규칙",
    "'코드는 저장하지 않고 지도에 잇는다' — LLM 비용 $0로 <1초에 설계 의도(Why)와 커밋을 복원하는 비결",
    tag_color=ACCENT_AMBER
)

add_bento_box(
    s5, Inches(0.9), Inches(1.75), Inches(5.65), Inches(2.45),
    tag="Hybrid Search · src/why.mjs (Slide #23)",
    title="🧠 SQLite FTS5 BM25 + RRF 하이브리드 랭킹",
    accent_color=ACCENT_AMBER,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• 1채널(그래프 시드): 파일/심볼과 직접 연결된 커밋·문서 청크 (weight 1.3x)",
        "• 2채널(FTS5 BM25): bm25(chunks_fts, 3.0, 1.0) — 제목 가중치 3배 부여",
        "• 결합 공식: Reciprocal Rank Fusion — 1 / (RRF_K + rank + 1) (RRF_K=60)",
        "• LLM 호출 없이 <1초 만에 설계 문서와 커밋 해시(b8401c2a) 즉시 인용"
    ]
)

add_bento_box(
    s5, Inches(6.8), Inches(1.75), Inches(5.65), Inches(2.45),
    tag="High-Precision Linking Rule (Slide #22)",
    title="🔗 '헷갈리면 잇지 않는다' (후보 1~3개 규칙)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• 문서나 커밋 메시지에 등장한 함수 이름을 심볼 그래프에 연결할 때:",
        "• get, set, init처럼 흔한 이름을 무조건 연결하면 그래프가 쓰레기장으로 변함",
        "• 오직 전체 레포에서 동명 심볼 후보가 1~3개 이하로 명확할 때만 엣지 생성",
        "• 애매하면 과감히 링크를 포기하여 False Positive 노이즈를 0%로 억제"
    ]
)

add_bento_box(
    s5, Inches(0.9), Inches(4.4), Inches(5.65), Inches(2.5),
    tag="SKILL.md 3-Column Routing (Slide #25)",
    title="🔀 '언제 부르지 말지'를 적는 3열 라우팅 표",
    accent_color=ACCENT_INDIGO,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• The question | Call | Not this 3열 구조로 에이전트 행동을 강제:",
        "• 파급 반경 질문 ➔ brain impact <file> (Not: grep으로 홉마다 수동 추적)",
        "• 설계 의도 질문 ➔ brain why <target> (Not: git log 전체 텍스트 덤프)",
        "• 작은 단일 파일 수정 ➔ 'do not call brain. Read the file.' 명시!"
    ]
)

add_bento_box(
    s5, Inches(6.8), Inches(4.4), Inches(5.65), Inches(2.5),
    tag="Routing Verification (Slide #27)",
    title="📊 라우팅 성적표: 발동률 76.8% · 오발동 0/6",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• 전체 69개 평가 시행 중 53회 정확히 스킬 로드 (76.8%)",
        "• 불려야 할 작업(impact, why, trace)에서는 90~100% 호출",
        "• 안 불려야 할 작은 작업(small-task)에서는 0 / 6 호출 (오발동 0%!)",
        "• 불필요한 Brain 호출로 인한 레이턴시 및 토큰 낭비를 원천 차단"
    ]
)

# ==============================================================================
# SLIDE 6: Part 4 - 2026 3 Numbers, 4 Eval Questions & pass@3 vs pass^3 (Slides #34~#42)
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s6)
add_clean_header(
    s6,
    "Part 4 · Why Skill Eval Matters (Slides #34~#42)",
    "2026년의 숫자 3개 & pass@3 (99.2%) vs pass^3 (51.2%)의 함정",
    "작업 성격에 따라 성공 지표가 정반대다 — 버그 수정은 1번만 성공해도 되지만, 파급 분석은 매번 성공해야 한다",
    tag_color=ACCENT_PURPLE
)

add_bento_box(
    s6, Inches(0.9), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="2026 Industry Reality · Slide #34",
    title="📊 2026년의 충격적 숫자 3개",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• 56% — 스킬이 아예 안 불렸다",
        "  Vercel Next.js 16 (2026.01): 스킬을 줬지만 절반 이상 호출조차 안 됨",
        "",
        "• 6개 중 5개 — 설명만 고쳐 트리거 개선",
        "  Anthropic skill-creator (2026.03): Eval로 description만 튜닝해 발동 복구",
        "",
        "• -44% — 비용 절감 + 누락 탐지",
        "  Arize (2026.07): 스킬로 비용 44% 절감, 완결성 Eval로 답 누락까지 포착"
    ]
)

add_bento_box(
    s6, Inches(4.85), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="Yao et al. τ-bench · Slide #39",
    title="🎲 pass@3 vs pass^3 (80% 에이전트)",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• 1회 성공 확률이 80%인 에이전트를 k=3번 실행할 때:",
        "",
        "• pass@3 = 1 - (0.2)^3 = 99.2%",
        "  (3번 중 1번이라도 성공할 확률)",
        "  ➔ 패치/버그 수정(Fix): 테스트 통과한 패치 1개만 커밋하면 됨",
        "",
        "• pass^3 = (0.8)^3 = 51.2%",
        "  (3번 모두 연속 성공할 확률)",
        "  ➔ 파급 분석(Find-All): 한 번이라도 호출처를 빼먹으면 곧바로 프로덕션 장애!"
    ]
)

add_bento_box(
    s6, Inches(8.8), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="4 Questions & Recall/Precision · #36, #42",
    title="⚖️ 4대 질문 & Find-All 두 줄 채점",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• Eval이 답하는 4가지 질문:",
        "  1. routing (불릴 때 불렸나? 진단용)",
        "  2. uplift (none vs v1 효과가 있나?)",
        "  3. regression (v1 vs v2 안 깨졌나?)",
        "  4. A/A (v1 vs v1b 바닥 노이즈 측정)",
        "",
        "• Find-All 꼼수 방어 (FROZEN.json):",
        "  전체 4,488개 다 찍기(Recall 1.0 / Prec 0.09) vs 50개만 찍기(Recall 0.13 / Prec 1.0) ➔ Recall >= 0.9 & Precision >= 0.8 동시 강제!"
    ]
)

# ==============================================================================
# SLIDE 7: Part 4-B - Grading Code checks.py ("0점에도 이름이 있다", Slides #38, #43)
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s7)
add_clean_header(
    s7,
    "Part 4-B · Deterministic Checks + Judge (Slides #38, #43)",
    "채점 파이프라인(skill_eval/checks.py): '0점에도 이름이 있다'",
    "무결성 위반(invalid)과 안전 위반(safety_violation), 오답(fail)을 분리해야 평균 점수가 왜곡되지 않는다",
    tag_color=ACCENT_AMBER
)

add_bento_box(
    s7, Inches(0.9), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="Outcome 01 · Integrity Failure",
    title="🚫 1. invalid (score: None)",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 검사 함수: check_no_answer_key_Visualizer()",
        "• 에이전트 실행 transcript에서 answer-keys/ 경로 접근이나 정답 탐색 시도 적발",
        "",
        "• 판정: outcome = 'invalid', score = None",
        "• 핵심: 0점으로 평균을 깎는 것이 아니라, 시험 자체를 무효 처리하여 분모에서 제외하고 즉시 경보를 울림",
        "• Stage 2(LLM Judge) 호출 즉시 스킵"
    ]
)

add_bento_box(
    s7, Inches(4.85), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="Outcome 02 & 03 · Safety & Correctness",
    title="⚠️ 2. safety_violation & fail (0.0)",
    accent_color=ACCENT_AMBER,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 안전 검사: check_workspace_unchanged()",
        "  읽기 전용 분석 과제에서 에이전트가 git status --porcelain을 더럽히면 outcome = 'safety_violation', score = 0.0 부여",
        "",
        "• 정답 검사: run_correctness()",
        "  필수 심볼/커밋 누락, Recall < 0.9 또는 Precision < 0.8 미달 시 outcome = 'fail', score = 0.0 부여",
        "• 두 경우 모두 고비용 LLM Judge를 부르지 않고 Short-Circuit 종료"
    ]
)

add_bento_box(
    s7, Inches(8.8), Inches(1.75), Inches(3.65), Inches(5.15),
    tag="Stage 2 · LLM-as-a-Judge (Slide #43)",
    title="⚖️ 3. Judge 3표 다수결 (pass)",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 무결성·안전·정답 하드 체크를 모두 통과한 답안만 Judge에게 전달",
        "• 모델: claude-opus-5-5 (3 votes per rubric item)",
        "• 각 루브릭 항목마다 3번 독립 채점 후 다수결(2/3 이상)로 통과 여부 결정",
        "",
        "• 최종 점수: Correctness(50%) + Judge Rubric(50%) 결합 (기준 >= 0.7 통과)"
    ]
)

# ==============================================================================
# SLIDE 8: Part 4-C - 4-Pillar Eval Sandbox Isolation (Slides #37, #44, #46)
# ==============================================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s8)
add_clean_header(
    s8,
    "Part 4-C · Sandbox Isolation (skill_eval/isolation.py · Slides #37, #44, #46)",
    "Eval 프로세스 4대 차단 원칙: 데이터 오염 및 보상 해킹(Reward Hacking) 방지",
    "테스트 대상 스킬의 순수 기여도(Delta)만 객관적으로 검증하기 위한 21개 무균 격리 프로브(skill-eval probe)",
    tag_color=ACCENT_ROSE
)

add_bento_box(
    s8, Inches(0.9), Inches(1.75), Inches(5.65), Inches(2.45),
    tag="Isolation 01 · Source Repo",
    title="🚫 1. 원본 Repo 차단 (개발 소스 & 메타데이터 격리)",
    accent_color=ACCENT_ROSE,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 반칙(Cheating): git log/diff나 초안을 뒤져 문제 출제 의도 파악",
        "• 컨닝 페이퍼 차단 및 실제 패키지 배포 환경 100% 모사",
        "• 구현: 매 trial마다 $TMPDIR 아래 APFS clone 생성, origin 제거, .claude/.agents 폴더 sparse checkout 제거 및 원본 경로 deny"
    ]
)

add_bento_box(
    s8, Inches(6.8), Inches(1.75), Inches(5.65), Inches(2.45),
    tag="Isolation 02 · Ground Truth",
    title="🔒 2. 정답 차단 (Golden Patch 은닉 & 역설계 방지)",
    accent_color=ACCENT_AMBER,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 반칙(Reward Hacking): find/grep으로 answer-keys나 채점 코드 베끼기",
        "• 채점 통과 조건만 하드코딩하는 역설계(Reverse Engineering) 원천 차단",
        "• 구현: 워크스페이스 외부 격리 + permissions.deny + 접근 시도 적발 시 0점이 아닌 outcome: invalid(실행 무효)로 즉시 퇴출"
    ]
)

add_bento_box(
    s8, Inches(0.9), Inches(4.4), Inches(5.65), Inches(2.5),
    tag="Isolation 03 · Global Config",
    title="🧹 3. ~/.claude 차단 (글로벌 환경 & 개인화 격리)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 반칙(Contamination): 전역 CLAUDE.md, 개인 스킬, MCP, 자동 메모리에 의존",
        "• 변인 통제: 스킬 적용 전(none) vs 후(v1)의 순수 기여도(Delta)만 측정",
        "• 구현: 매 trial 빈 CLAUDE_CONFIG_DIR + 번들 스킬 22종 off + disableAllHooks + 상위 폴더 CLAUDE.md 존재 시 실행 거부"
    ]
)

add_bento_box(
    s8, Inches(6.8), Inches(4.4), Inches(5.65), Inches(2.5),
    tag="Isolation 04 · Determinism",
    title="🌐 4. 네트워크 차단 (외부 의존성 차단 & 결정론적 평가)",
    accent_color=ACCENT_EMERALD,
    accent_pos="top",
    title_size=14.5,
    body_size=10.5,
    content_lines=[
        "• 반칙(Bypass): 막히는 부분을 구글링하거나 외부 패키지 설치로 우회",
        "• 시간에 따라 변하는 외부 웹/패키지 상태를 배제해 재현성(Determinism) 확보",
        "• 구현: OS 커널 샌드박스(sandbox.enabled: True, allowUnsandboxedCommands: False) 및 skill-eval probe 21/21 PASS 검증"
    ]
)

# ==============================================================================
# SLIDE 9: Part 5 - 6-Stage Maturity (L0~L5) & 300-Trial Scorecard (Slides #48, #51)
# ==============================================================================
s9 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s9)
add_clean_header(
    s9,
    "Part 5 · Maturity L0~L5 & Scorecard (Slides #48, #51)",
    "Eval 성숙도 6단계 (L0~L5) 및 300-Trial 성적표 대시보드 해석법",
    "'가장 큰 점프는 L4(CI 자동 실행)이고, 가장 중요한 단계는 L5(프로덕션 실패의 케이스화)다'",
    tag_color=ACCENT_EMERALD
)

step_data = [
    ("L0 · Vibe", "감(Vibe) 테스트", "고장 나도 모름\n가장 위험한 단계", ACCENT_ROSE, Inches(0.9)),
    ("L1 · Check", "결정론적 체크", "컴파일·스키마·금지패턴\n자동 코드 검증", ACCENT_AMBER, Inches(2.83)),
    ("L2 · Golden", "고정 케이스셋", "대표 프롬프트 10~30개\nFROZEN.json 고정", ACCENT_CYAN, Inches(4.76)),
    ("L3 · Judge", "Judge + k회 + 대조", "none vs v1 다회 실행\n루브릭 다수결 채점", ACCENT_INDIGO, Inches(6.69)),
    ("L4 · CI Gate", "PR마다 자동 실행", "SKILL.md 수정 시\nCI 회귀 게이트 가동", ACCENT_PURPLE, Inches(8.62)),
    ("L5 · Flywheel", "실패 ➔ 새 케이스", "프로덕션 실패를\n회귀 테스트로 편입", ACCENT_EMERALD, Inches(10.55)),
]
for lvl, name, desc, col, x_pos in step_data:
    add_bento_box(
        s9, x_pos, Inches(1.75), Inches(1.82), Inches(2.15),
        tag=lvl,
        title=name,
        accent_color=col,
        accent_pos="top",
        title_size=12.5,
        body_size=9.5,
        content_lines=desc.split("\n")
    )

add_bento_box(
    s9, Inches(0.9), Inches(4.15), Inches(5.65), Inches(2.75),
    tag="Scorecard · 300/300 Trials · $65.61 (Slide #51)",
    title="📊 4-Variant 실전 성적표 (none vs v1 vs v2 vs v1b)",
    accent_color=ACCENT_CYAN,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• none (베이스라인): Pass Rate 88% | 평균 68.3s | $0.25/trial",
        "• v1 (초기 스킬): Pass Rate 93% | 평균 39.0s | $0.21/trial",
        "• v2 (개선 스킬): Pass Rate 95% | 평균 38.6s | $0.21/trial",
        "• v1b (A/A 복제본): Pass Rate 93% | 평균 40.2s | 바닥 분산 확인용",
        "💡 스킬 적용 시 소요 시간 43% 단축(68s➔38s) 및 토큰 비용 16% 절감!"
    ]
)

add_bento_box(
    s9, Inches(6.8), Inches(4.15), Inches(5.65), Inches(2.75),
    tag="Statistical Discipline · 95% Confidence Interval",
    title="📏 신뢰구간(CI) 판독 규칙: '0을 걸치면 확신 금지'",
    accent_color=ACCENT_PURPLE,
    accent_pos="top",
    title_size=14.5,
    body_size=10,
    content_lines=[
        "• Uplift (v1 - none = +5.3%p): 95% 신뢰구간이 [-3.1%, +13.8%]로 0을 걸침",
        "• Regression (v2 - v1 = +1.3%p) & A/A Noise (v1 - v1b = +0.0%p)",
        "• 핵심 교훈: 평균 점수만 보고 '5.3%p 올랐다!'고 성급히 선언하지 말라",
        "• 95% CI 막대가 0을 걸치면 '차이를 확신할 수 없다(Inconclusive)'고 정직하게 보고하고 케이스 수를 늘려 검정력을 확보해야 함"
    ]
)

# ==============================================================================
# SLIDE 10: Domain Blueprint & Epilogue
# ==============================================================================
s10 = prs.slides.add_slide(prs.slide_layouts[6])
set_canvas_bg(s10)
add_clean_header(
    s10,
    "Part 6 · Domain Blueprint & Epilogue",
    "모바일 통신 물리계층(PHY) SW 그룹 적용 가이드 & 에필로그",
    "임베디드 C/C++ 펌웨어 리뷰 파이프라인으로의 1:1 대응 및 에이전트 시대 인간의 주도권",
    tag_color=ACCENT_PURPLE
)

add_bento_box(
    s10, Inches(0.9), Inches(1.75), Inches(5.65), Inches(5.15),
    tag="Group Leader Blueprint",
    title="📡 모바일 통신 PHY SW 2nd Brain & Eval 로드맵",
    accent_color=ACCENT_CYAN,
    accent_pos="left",
    title_size=15,
    body_size=10.5,
    content_lines=[
        "• 1. Clang AST 레지스터 맵 그래프 + 3대 커버리지 라벨",
        "  MMIO 주소, 비트필드, ISR 벡터, 3GPP FSM 심볼 링킹 및 함수 포인터 테이블 구간에 partial 라벨 자동 부여",
        "",
        "• 2. 3GPP 규격 & 실리콘 에라타 FTS5 BM25+RRF Memory",
        "  과거 모뎀 IODT 필드 이슈와 RF 타이밍 패치 사유(Why)를 후보 1~3개 고정밀 링킹 규칙으로 인덱싱",
        "",
        "• 3. 임베디드 펌웨어 4대 무균 격리 + CI Gatekeeper",
        "  invalid/safety_violation/fail 분리 채점 및 파급 분석 pass^3 기준 강제"
    ]
)

add_bento_box(
    s10, Inches(6.8), Inches(1.75), Inches(5.65), Inches(5.15),
    tag="Human Agency · Philosophy (Slide #55)",
    title="💡 에필로그: 에이전트 시대, 인간의 주도권",
    accent_color=ACCENT_PURPLE,
    accent_pos="left",
    title_size=15,
    body_size=10.5,
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
print(f"Successfully generated 10-slide curved-stripe Bento Presentation: {out_pptx}")
