import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

out_pptx = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\06_Presenton_Modern_Deck.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)  # 16:9

# Presenton Modern Gamma Palette
BG_DARK = RGBColor(15, 18, 25)          # #0f1219 (Deep Navy Black)
CARD_BG = RGBColor(26, 31, 46)          # #1a1f2e (Subtle Slate Blue Card)
CARD_BORDER = RGBColor(45, 55, 80)      # #2d3750
ACCENT_CYAN = RGBColor(56, 189, 248)    # #38bdf8 (Sky Cyan)
ACCENT_PURPLE = RGBColor(168, 85, 247)  # #a855f7 (Purple Glow)
ACCENT_EMERALD = RGBColor(52, 211, 153) # #34d399 (Emerald Green)
ACCENT_AMBER = RGBColor(251, 191, 36)   # #fbbf24 (Warm Amber)
TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)

def set_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_pill="⚡ META SENIOR ENGINEERING LECTURE"):
    # Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.55), Inches(4.5), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 69)
    pill.line.color.rgb = ACCENT_CYAN
    tf_p = pill.text_frame
    tf_p.text = category_pill
    tf_p.paragraphs[0].font.size = Pt(10)
    tf_p.paragraphs[0].font.bold = True
    tf_p.paragraphs[0].font.color.rgb = ACCENT_CYAN

    # Title
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.95), Inches(11.3), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 1: Cover / Hero
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s1)

pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(4.8), Inches(0.45))
pill1.fill.solid()
pill1.fill.fore_color.rgb = RGBColor(30, 41, 69)
pill1.line.color.rgb = ACCENT_CYAN
tf_p1 = pill1.text_frame
tf_p1.text = "⚡ META SENIOR LECTURE · FULL BLUEPRINT"
tf_p1.paragraphs[0].font.size = Pt(11)
tf_p1.paragraphs[0].font.bold = True
tf_p1.paragraphs[0].font.color.rgb = ACCENT_CYAN

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(2.3))
tf1 = tb1.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "AI 에이전트를 위한 2nd Brain과 Eval"
p1.font.size = Pt(40)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE

p1_sub = tf1.add_paragraph()
p1_sub.text = "메타 시니어 엔지니어 하재상 세미나 전수 분석: 맥락 주입(Context)과 자동 검증(Verification)"
p1_sub.font.size = Pt(18)
p1_sub.font.color.rgb = TEXT_MUTED
p1_sub.space_before = Pt(12)

pill_items = [
    ("🕸️ Codebase Graph", "컴파일러/AST 기반 정밀 지도\nBFS Hopping으로 Blast Radius 계산", Inches(1.2)),
    ("🧠 Code Memory", "Git 커밋/PR의 'Why' 추적\nBM25 희귀 엔지니어링 용어 인덱싱", Inches(5.1)),
    ("⚖️ Eval (EDD)", "Hard Check + K-Judge Majority Voting\nCI Gatekeeper로 머지 차단", Inches(9.0))
]
for title, desc, x_pos in pill_items:
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(4.9), Inches(3.6), Inches(1.9))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    ctf = card.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = ACCENT_CYAN
    cp2 = ctf.add_paragraph()
    cp2.text = desc
    cp2.font.size = Pt(12)
    cp2.font.color.rgb = TEXT_MUTED
    cp2.space_before = Pt(6)

# ==============================================================================
# SLIDE 2: 병목의 이동 & 하네스의 필요성
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s2)
add_header(s2, "AI 코딩 패러다임의 전환: 코딩 속도에서 '검증 병목'으로")

c2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.8))
c2_l.fill.solid()
c2_l.fill.fore_color.rgb = CARD_BG
c2_l.line.color.rgb = RGBColor(239, 68, 68)
t2_l = c2_l.text_frame
t2_l.word_wrap = True
tp2_l = t2_l.paragraphs[0]
tp2_l.text = "🚨 프롬프팅 중심 코딩의 붕괴"
tp2_l.font.size = Pt(18)
tp2_l.font.bold = True
tp2_l.font.color.rgb = RGBColor(248, 113, 113)

sub_l = t2_l.add_paragraph()
sub_l.text = (
    "\n• 코드 타이핑 병목 소멸\n"
    "  LLM이 1초 만에 수백 줄의 코드를 작성하지만, 대규모 PR이 쏟아져 인간 리뷰어의 뇌에 극한의 병목 유발\n\n"
    "• 환각(Hallucination) 공포\n"
    "  결과물을 신뢰할 수 없어 인간이 코드를 일일이 대조 검증해야 하므로 실제 생산성은 정체\n\n"
    "• 세션 컨텍스트 리셋\n"
    "  새로운 에이전트 대화창을 열 때마다 매번 프로젝트 아키텍처와 규칙을 사람이 재설명하는 낭비 발생"
)
sub_l.font.size = Pt(13)
sub_l.font.color.rgb = TEXT_WHITE

c2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.8))
c2_r.fill.solid()
c2_r.fill.fore_color.rgb = CARD_BG
c2_r.line.color.rgb = ACCENT_EMERALD
t2_r = c2_r.text_frame
t2_r.word_wrap = True
tp2_r = t2_r.paragraphs[0]
tp2_r.text = "🛡️ 시스템 하네스(Harness)의 해결 공식"
tp2_r.font.size = Pt(18)
tp2_r.font.bold = True
tp2_r.font.color.rgb = ACCENT_EMERALD

sub_r = t2_r.add_paragraph()
sub_r.text = (
    "\n• 메타의 $30,000/월 실험 결론\n"
    "  규칙, 툴, 프롬프트를 아무리 잘 줘도 자동 검증(Eval) 체계가 없으면 자율 위임은 불가능\n\n"
    "• Context Layer (2nd Brain)\n"
    "  사람이 설명하지 않아도 시스템이 컴파일러 AST 그래프와 Git 히스토리에서 맥락을 자동 공급\n\n"
    "• Verification Layer (Eval)\n"
    "  Deterministic Hard Check + K-Judge Majority Voting으로 통계적 신뢰성을 확보한 후 CI에서 자동 머지"
)
sub_r.font.size = Pt(13)
sub_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 3: 메타 실전 사례 (10시간 ➔ 30분)
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s3)
add_header(s3, "메타 프로덕션 실전 사례: 성능 프로파일링 10시간 ➔ 30분 단축")

cards_s3 = [
    ("1. 문제 상황 (Pain Point)", "• 대규모 분산 백엔드 서비스 레이턴시 급증\n• 수천 개 모듈 간 상호 호출로 원인 추적 난해\n• 시니어 엔지니어가 Flame Graph 및 Trace 데이터를 수작업 대조하며 10시간 소모", RGBColor(239, 68, 68), Inches(1.0)),
    ("2. 하네스 결합 솔루션", "• Profiling MCP: Flame Graph 지표 질의 툴\n• Senior Skill: 메타 시니어 진단 매뉴얼 패키징\n• 2nd Brain Graph: 의존 함수 및 데이터 흐름 역추적\n• 에이전트가 가설 수립 및 코드 검증을 자율 병렬 수행", ACCENT_CYAN, Inches(4.9)),
    ("3. 성과 및 핵심 교훈", "• 진단 및 패치 시간: 10시간 ➔ 30분 (95% 단축)\n• 단순 Grep 검색은 90% 이상 무관한 주석/더미 반환\n• '표준 MCP 도구' + '시니어 노하우(Skill)' + '코드 지도(Brain)' 3자 결합이 자율화의 핵심", ACCENT_EMERALD, Inches(8.8))
]
for title, body, border_c, x_pos in cards_s3:
    c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(2.0), Inches(3.6), Inches(4.8))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = border_c
    ctf = c.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = border_c
    cp2 = ctf.add_paragraph()
    cp2.text = f"\n{body}"
    cp2.font.size = Pt(12)
    cp2.font.color.rgb = TEXT_WHITE
    cp2.space_before = Pt(4)

# ==============================================================================
# SLIDE 4: 세컨드 브레인 아키텍처 - Codebase Graph
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s4)
add_header(s4, "세컨드 브레인 기둥 1: 컴파일러/AST 기반 Codebase Graph")

c4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.8))
c4_l.fill.solid()
c4_l.fill.fore_color.rgb = CARD_BG
c4_l.line.color.rgb = ACCENT_CYAN
t4_l = c4_l.text_frame
t4_l.word_wrap = True
tp4_l = t4_l.paragraphs[0]
tp4_l.text = "🕸️ Grep vs Compiler AST 비교"
tp4_l.font.size = Pt(18)
tp4_l.font.bold = True
tp4_l.font.color.rgb = ACCENT_CYAN
sp4_l = t4_l.add_paragraph()
sp4_l.text = (
    "\n• 텍스트 Grep의 치명적 한계\n"
    "  - 키워드 매칭 시 주석, 테스트 더미, 이름만 같은 무관 변수 대량 유입\n"
    "  - 컨텍스트 윈도우 폭증으로 모델 추론 정확도 급락\n\n"
    "• 컴파일러/AST 그래프 구축 (`brain build`)\n"
    "  - TypeScript Compiler API, Clang AST 파서로 코드 분석\n"
    "  - 모든 함수/구조체/클래스에 고유 `Symbol ID` 부여\n"
    "  - `CALLS`, `IMPORTS`, `WRITES_TO` 관계를 방향성 엣지로 인덱싱\n\n"
    "• 결정론적 BFS Hopping\n"
    "  - A 함수 수정 시 파급되는 2차, 3차 영향권(Blast Radius)을 수학적으로 100% 정밀 도출"
)
sp4_l.font.size = Pt(13)
sp4_l.font.color.rgb = TEXT_WHITE

c4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.8))
c4_r.fill.solid()
c4_r.fill.fore_color.rgb = CARD_BG
c4_r.line.color.rgb = ACCENT_PURPLE
t4_r = c4_r.text_frame
t4_r.word_wrap = True
tp4_r = t4_r.paragraphs[0]
tp4_r.text = "📊 도구별 성능 및 벤치마크"
tp4_r.font.size = Pt(18)
tp4_r.font.bold = True
tp4_r.font.color.rgb = ACCENT_PURPLE

chart_img = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\assets\benchmark_comparison_chart.png"
if os.path.exists(chart_img):
    s4.shapes.add_picture(chart_img, Inches(7.0), Inches(2.6), width=Inches(5.1))

# ==============================================================================
# SLIDE 5: 세컨드 브레인 기둥 2 - Code Memory & Routing
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s5)
add_header(s5, "세컨드 브레인 기둥 2: 'Why'를 추적하는 Code Memory & 라우팅 규칙")

c5_l = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.8))
c5_l.fill.solid()
c5_l.fill.fore_color.rgb = CARD_BG
c5_l.line.color.rgb = ACCENT_AMBER
t5_l = c5_l.text_frame
t5_l.word_wrap = True
tp5_l = t5_l.paragraphs[0]
tp5_l.text = "🧠 Code Memory: 아키텍처 의도 복원"
tp5_l.font.size = Pt(18)
tp5_l.font.bold = True
tp5_l.font.color.rgb = ACCENT_AMBER
sp5_l = t5_l.add_paragraph()
sp5_l.text = (
    "\n• 그래프의 맹점: '현재 구조'만 알 뿐 'Why'를 모름\n"
    "  '이 함수는 왜 딜레이를 10us 주는가?', '왜 이 예외처리가 존재하는가?'\n\n"
    "• `why.mjs` & `query.mjs` 구현\n"
    "  - Git 커밋 히스토리, PR 리뷰 토론, ADR(의사결정 문서) 연동\n\n"
    "• BM25 키워드 랭킹 채택\n"
    "  - 일반 벡터 임베딩은 통신/하드웨어 전문 약어 매칭에 취약\n"
    "  - BM25는 희귀 엔지니어링 고유명사에 가중치를 부여해 정확한 변경 맥락을 즉각 적중"
)
sp5_l.font.size = Pt(13)
sp5_l.font.color.rgb = TEXT_WHITE

c5_r = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.8))
c5_r.fill.solid()
c5_r.fill.fore_color.rgb = CARD_BG
c5_r.line.color.rgb = ACCENT_CYAN
t5_r = c5_r.text_frame
t5_r.word_wrap = True
tp5_r = t5_r.paragraphs[0]
tp5_r.text = "🔀 Brain 트레이드오프와 라우팅 규칙"
tp5_r.font.size = Pt(18)
tp5_r.font.bold = True
tp5_r.font.color.rgb = ACCENT_CYAN
sp5_r = t5_r.add_paragraph()
sp5_r.text = (
    "\n• 무조건 Brain 조회 시 오버헤드 발생\n"
    "  단순 오탈자나 단일 파일의 자명한 수정에 Brain을 태우면 레이턴시와 토큰 비용만 낭비됨\n\n"
    "• 2원화 라우팅 규칙 (Routing Policy)\n"
    "  1. Fast Path (로컬 수정):\n"
    "     단일 파일 내 국소 수정 ➔ LLM 직접 편집 (No Brain)\n"
    "  2. Brain Path (구조적 수정):\n"
    "     공용 인터페이스 변경, 아키텍처 리팩토링, 레지스터 정의 수정 ➔ 반드시 Code Graph & Memory 선행 조회 의무화"
)
sp5_r.font.size = Pt(13)
sp5_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 6: Eval (평가 체계) - 2단계 검증 아키텍처
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s6)
add_header(s6, "Eval 체계: 결정론적 Hard Check + K-Judge Majority Voting")

cards_s6 = [
    ("Stage 1: Hard Check (결정론적)", "• 컴파일 검증: Clang / TS exit code == 0\n• 정적 린트: Clang-Tidy, ESLint 무결점\n• 단위 테스트: 100% Pass\n• 스키마 검증: 입출력 JSON 규격 일치\n\n🚨 단 1개라도 실패 시 즉시 0점 탈락 (Stage 2 생략)", RGBColor(239, 68, 68), Inches(1.0)),
    ("Stage 2: K-Judge Majority Voting", "• LLM-as-a-Judge 정성 평가\n• LLM의 확률적 변동성(Variance) 제거\n• K=3 독립 세션 실행 (3인의 교수 심사 모델)\n• 2표 이상 찬성(Pass) 시에만 최종 합격\n• 아키텍처 규칙 준수 및 엣지 케이스 점검", ACCENT_PURPLE, Inches(4.9)),
    ("CI Gatekeeper (자동화 머지)", "• 'CI에서 자동 실행되지 않는 Eval은 없는 것과 같다'\n• Pull Request 제출 시 GitHub Actions 연동\n• Hard Check + K-Judge 통과 시에만 머지 활성화\n• 주니어 엔지니어도 안심하고 에이전트 PR 생성 가능", ACCENT_EMERALD, Inches(8.8))
]
for title, body, border_c, x_pos in cards_s6:
    c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(2.0), Inches(3.6), Inches(4.8))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = border_c
    ctf = c.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = border_c
    cp2 = ctf.add_paragraph()
    cp2.text = f"\n{body}"
    cp2.font.size = Pt(12)
    cp2.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 7: 샌드박스 격리 & 메타의 5단계 성숙도 모델
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s7)
add_header(s7, "샌드박스 격리와 메타의 Eval 성숙도 5단계 (Levels 0 ~ 4)")

c7_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.8))
c7_l.fill.solid()
c7_l.fill.fore_color.rgb = CARD_BG
c7_l.line.color.rgb = ACCENT_CYAN
t7_l = c7_l.text_frame
t7_l.word_wrap = True
tp7_l = t7_l.paragraphs[0]
tp7_l.text = "🧪 Sandbox Isolation (무균 격리)"
tp7_l.font.size = Pt(18)
tp7_l.font.bold = True
tp7_l.font.color.rgb = ACCENT_CYAN
sp7_l = t7_l.add_paragraph()
sp7_l.text = (
    "\n• 오염 방지 격리 원칙\n"
    "  - 에이전트가 Ground Truth(정답 파일)를 읽지 못하도록 차단\n"
    "  - 로컬의 글로벌 설정(~/.claude/settings) 유입 차단\n"
    "  - 매 실행마다 독립 임시 컨테이너에서 무균 실행\n\n"
    "• 골든 프롬프트 (Golden Prompts) 벤치마크\n"
    "  - 실무 핵심 시나리오 20~30개 엄선\n"
    "  - Baseline(No-Skill) vs Skill 적용군의 통계적 점수 비교"
)
sp7_l.font.size = Pt(13)
sp7_l.font.color.rgb = TEXT_WHITE

c7_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.8))
c7_r.fill.solid()
c7_r.fill.fore_color.rgb = CARD_BG
c7_r.line.color.rgb = ACCENT_EMERALD
t7_r = c7_r.text_frame
t7_r.word_wrap = True
tp7_r = t7_r.paragraphs[0]
tp7_r.text = "📈 메타의 Eval 성숙도 5단계"
tp7_r.font.size = Pt(18)
tp7_r.font.bold = True
tp7_r.font.color.rgb = ACCENT_EMERALD
sp7_r = t7_r.add_paragraph()
sp7_r.text = (
    "\n• Level 0: 느낌 (Vibe) ➔ '어? 잘 되는 것 같은데?' (위험)\n"
    "• Level 1: 단위 테스트 & 린트 ➔ 기본적인 하드 체크 자동화\n"
    "• Level 2: 오프라인 Eval ➔ 골든 프롬프트 벤치마크 점수화\n"
    "• Level 3: CI Gatekeeper ➔ PR 머지 전 자동 통과 의무화\n"
    "• Level 4: Self-Improving Loop ➔ 실패 사례 분석 후 프롬프트/스킬 자체 자동 개선\n\n"
    "🎯 스킬의 3대 필수 질문: 호출 정확도 / 성능 향상 / 무리그레션"
)
sp7_r.font.size = Pt(13)
sp7_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 8: 모바일 통신 PHY SW 적용 & 인간의 주도권
# ==============================================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s8)
add_header(s8, "모바일 통신/물리계층(PHY) SW 그룹 적용 가이드 & 에필로그")

c8_l = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.8))
c8_l.fill.solid()
c8_l.fill.fore_color.rgb = CARD_BG
c8_l.line.color.rgb = ACCENT_CYAN
t8_l = c8_l.text_frame
t8_l.word_wrap = True
tp8_l = t8_l.paragraphs[0]
tp8_l.text = "📡 모바일 통신 PHY SW 2nd Brain 로드맵"
tp8_l.font.size = Pt(18)
tp8_l.font.bold = True
tp8_l.font.color.rgb = ACCENT_CYAN
sp8_l = t8_l.add_paragraph()
sp8_l.text = (
    "\n1. ARM Clang AST 기반 레지스터 맵 그래프 구축\n"
    "   - MMIO 주소, 비트필드, ISR, FSM 상태 머신 심볼 링킹\n\n"
    "2. 3GPP 규격 및 실리콘 에라타(Silicon Errata) Memory\n"
    "   - '왜 이 10us 딜레이가 존재하는가?' ➔ 과거 IODT 실패 이력 주입\n\n"
    "3. 임베디드 펌웨어 Eval CI 게이트\n"
    "   - Hard Check: Cross-Compiler 빌드 + SRAM/D-Cache 사용량\n"
    "   - Domain Judge: ISR 동시성 경합 및 us 실시간 데드라인 검증"
)
sp8_l.font.size = Pt(13)
sp8_l.font.color.rgb = TEXT_WHITE

c8_r = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.8))
c8_r.fill.solid()
c8_r.fill.fore_color.rgb = CARD_BG
c8_r.line.color.rgb = ACCENT_PURPLE
t8_r = c8_r.text_frame
t8_r.word_wrap = True
tp8_r = t8_r.paragraphs[0]
tp8_r.text = "💡 에필로그: 에이전트 시대, 인간의 주도권"
tp8_r.font.size = Pt(18)
tp8_r.font.bold = True
tp8_r.font.color.rgb = ACCENT_PURPLE
sp8_r = t8_r.add_paragraph()
sp8_r.text = (
    "\n\"에이전트에게 주도권을 뺏기지 마세요.\"\n\n"
    "• 에이전트를 돌리느라 24시간 쉬지 못하고 건강과 가족을 해치는 것은 도구의 본질을 잃은 것\n\n"
    "• 나의 1번 가치(가족, 건강, 엔지니어링의 본질)를 확고히 세우고, 에이전트는 나를 그 가치로 데려다주는 강력한 지렛대로 부려야 함\n\n"
    "• 설계, 전략, 아키텍처 판단은 인간 테크리드가 쥐고, 구현과 검증은 견고한 하네스(2nd Brain + Eval)에 위임하라"
)
sp8_r.font.size = Pt(13)
sp8_r.font.color.rgb = TEXT_WHITE

prs.save(out_pptx)
print(f"Successfully generated expanded 8-slide Presenton deck: {out_pptx}")
