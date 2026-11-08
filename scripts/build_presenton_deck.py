import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

out_pptx = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\06_Presenton_Style_Modern_Deck.pptx"

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
TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)

def set_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

# --- SLIDE 1: Gamma / Presenton Hero Cover ---
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s1)

# Pill Badge
pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.8), Inches(4.2), Inches(0.45))
pill.fill.solid()
pill.fill.fore_color.rgb = RGBColor(30, 41, 69)
pill.line.color.rgb = ACCENT_CYAN
tf_p = pill.text_frame
tf_p.text = "⚡ PRESENTON AI PRESENTATION ENGINE"
tf_p.paragraphs[0].font.size = Pt(11)
tf_p.paragraphs[0].font.bold = True
tf_p.paragraphs[0].font.color.rgb = ACCENT_CYAN

# Big Hero Title
tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.5), Inches(11.0), Inches(2.2))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "AI 에이전트를 위한 2nd Brain과 Eval"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p_sub = tf1.add_paragraph()
p_sub.text = "메타 8년차 시니어 엔지니어가 밝히는 자율 에이전트의 두 기둥: 맥락(Context)과 검증(Verification)"
p_sub.font.size = Pt(18)
p_sub.font.color.rgb = TEXT_MUTED
p_sub.space_before = Pt(14)

# 3 Feature Pills at bottom
pill_items = [
    ("🕸️ Codebase Graph", "컴파일러 AST 기반 정밀 지도", Inches(1.2)),
    ("🧠 Code Memory", "의사결정 Why 및 아키텍처 맥락", Inches(5.1)),
    ("⚖️ Eval (EDD)", "GitHub CI 기반 통계적 정량 검증", Inches(9.0))
]
for title, desc, x_pos in pill_items:
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(5.0), Inches(3.6), Inches(1.6))
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

# --- SLIDE 2: Problem & Solution (Card Grid) ---
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s2)

h_box = s2.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(11.0), Inches(1.0))
htf = h_box.text_frame
hp = htf.paragraphs[0]
hp.text = "왜 단순 프롬프팅이 아닌 '하네스(Harness)'인가?"
hp.font.size = Pt(28)
hp.font.bold = True
hp.font.color.rgb = TEXT_WHITE

# Card Left: Problem
c_left = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.0), Inches(5.3), Inches(4.6))
c_left.fill.solid()
c_left.fill.fore_color.rgb = CARD_BG
c_left.line.color.rgb = RGBColor(239, 68, 68)
ltf = c_left.text_frame
ltf.word_wrap = True
lp1 = ltf.paragraphs[0]
lp1.text = "❌ AI 코딩의 새로운 병목"
lp1.font.size = Pt(20)
lp1.font.bold = True
lp1.font.color.rgb = RGBColor(248, 113, 113)

lp_sub = ltf.add_paragraph()
lp_sub.text = "\n1. 코드 작성이 빨라지면서 초대형 PR이 범람\n2. 리뷰어의 검증 부담이 기하급수적으로 폭증\n3. AI의 환각(Hallucination) 공포로 완전 위임 불가\n4. 매번 세션마다 프로젝트 맥락을 재설명하는 낭비"
lp_sub.font.size = Pt(14)
lp_sub.font.color.rgb = TEXT_WHITE

# Card Right: Solution
c_right = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.3), Inches(4.6))
c_right.fill.solid()
c_right.fill.fore_color.rgb = CARD_BG
c_right.line.color.rgb = ACCENT_EMERALD
rtf = c_right.text_frame
rtf.word_wrap = True
rp1 = rtf.paragraphs[0]
rp1.text = "🛡️ 시스템 하네스(Harness)의 해결책"
rp1.font.size = Pt(20)
rp1.font.bold = True
rp1.font.color.rgb = ACCENT_EMERALD

rp_sub = rtf.add_paragraph()
rp_sub.text = "\n1. 2nd Brain: 시스템이 맥락을 알아서 에이전트에 공급\n2. Code Graph: 컴파일러 수준에서 파급 반경(Blast Radius) 선행 계산\n3. Eval Layer: K번 실행 다수결 검증으로 통계적 신뢰도 확보\n4. CI Gate: 통과된 안전한 PR만 머지되도록 강제"
rp_sub.font.size = Pt(14)
rp_sub.font.color.rgb = TEXT_WHITE

# --- SLIDE 3: Architecture Diagram & Chart ---
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s3)

h_box3 = s3.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(11.0), Inches(1.0))
htf3 = h_box3.text_frame
hp3 = htf3.paragraphs[0]
hp3.text = "2nd Brain 및 Eval 아키텍처 비교 벤치마크"
hp3.font.size = Pt(28)
hp3.font.bold = True
hp3.font.color.rgb = TEXT_WHITE

# Left Side: Insert the generated chart PNG
chart_img = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\assets\benchmark_comparison_chart.png"
if os.path.exists(chart_img):
    s3.shapes.add_picture(chart_img, Inches(1.2), Inches(2.0), width=Inches(6.2))

# Right Side: Presenton Summary Card
c_stat = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(2.0), Inches(4.4), Inches(4.6))
c_stat.fill.solid()
c_stat.fill.fore_color.rgb = CARD_BG
c_stat.line.color.rgb = ACCENT_PURPLE
stf = c_stat.text_frame
stf.word_wrap = True

sp1 = stf.paragraphs[0]
sp1.text = "💡 시니어 테크리드 시사점"
sp1.font.size = Pt(18)
sp1.font.bold = True
sp1.font.color.rgb = ACCENT_PURPLE

sp_sub = stf.add_paragraph()
sp_sub.text = "\n• 에이전트 도입의 성공은 '프롬프트 문구'가 아닌 '컨텍스트 인프라'에 달려 있음\n\n• Code Graph는 함수 호출선만 그리는 것이 아니라, 레지스터 쓰기 및 ISR 잠금 상태까지 엣지에 담아야 함\n\n• Eval이 CI에 붙어야 비로소 주니어 엔지니어들도 안심하고 에이전트 코드를 프로덕션에 병합 가능"
sp_sub.font.size = Pt(13)
sp_sub.font.color.rgb = TEXT_WHITE

prs.save(out_pptx)
print(f"Successfully generated Presenton-style presentation: {out_pptx}")

