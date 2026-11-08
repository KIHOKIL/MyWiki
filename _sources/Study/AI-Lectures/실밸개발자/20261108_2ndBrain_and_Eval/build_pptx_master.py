import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

out_pptx = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\03_Generated_Presentation_PPTMaster.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5) # 16:9 Widescreen

# Colors
DARK_BG = RGBColor(13, 17, 23)      # #0d1117
CARD_BG = RGBColor(22, 27, 34)      # #161b22
ACCENT_BLUE = RGBColor(88, 166, 255) # #58a6ff
ACCENT_GREEN = RGBColor(63, 185, 80) # #3fb950
ACCENT_PURPLE = RGBColor(188, 140, 255)
TEXT_WHITE = RGBColor(240, 246, 252)
TEXT_MUTED = RGBColor(139, 148, 158)

def apply_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = DARK_BG
    bg_shape.line.fill.background()
    return bg_shape

# --- Slide 1: Title ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide1)

title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(3.0))
tf = title_box.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "AI 에이전트를 위한 2nd Brain & Eval 프레임워크"
p1.font.size = Pt(40)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE
p1.font.name = "Segoe UI"

p2 = tf.add_paragraph()
p2.text = "Meta 8년차 시니어 엔지니어(실밸개발자) 세미나 핵심 전수 분석 & 아키텍처"
p2.font.size = Pt(20)
p2.font.color.rgb = ACCENT_BLUE
p2.space_before = Pt(20)

p3 = tf.add_paragraph()
p3.text = "ppt-master 패턴 적용: Native Shapes, Dark Theme, 16:9 Widescreen"
p3.font.size = Pt(13)
p3.font.color.rgb = TEXT_MUTED
p3.space_before = Pt(15)

# --- Slide 2: The Bottleneck Shift ---
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide2)

header_box = slide2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = header_box.text_frame
p = tf.paragraphs[0]
p.text = "1. AI 코딩의 진짜 병목과 '하네스(Harness)' 전환"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

# Left Card: Old vs Current
card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
card1.fill.solid()
card1.fill.fore_color.rgb = CARD_BG
card1.line.color.rgb = RGBColor(48, 54, 61)
tf1 = card1.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "⚠️ 진짜 병목은 어디인가?"
p1.font.size = Pt(20)
p1.font.bold = True
p1.font.color.rgb = RGBColor(248, 81, 73)
p1_sub = tf1.add_paragraph()
p1_sub.text = "\n• 코드를 작성하는 것은 LLM이 1초 만에 수행\n• 그 결과 대형 PR이 쏟아져 나와 인간의 검증 부담 폭증\n• AI가 작성한 코드가 사내 아키텍처와 규칙을 지켰는지 확신할 수 없음\n• 결국 '검증과 리뷰'가 새로운 개발 병목으로 부상"
p1_sub.font.size = Pt(14)
p1_sub.font.color.rgb = TEXT_WHITE

# Right Card: Harness Solution
card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.0), Inches(5.4), Inches(4.5))
card2.fill.solid()
card2.fill.fore_color.rgb = CARD_BG
card2.line.color.rgb = RGBColor(48, 54, 61)
tf2 = card2.text_frame
tf2.word_wrap = True
p2 = tf2.paragraphs[0]
p2.text = "🛡️ 시스템 하네스(Harness)의 역할"
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = ACCENT_GREEN
p2_sub = tf2.add_paragraph()
p2_sub.text = "\n• 프롬프트를 매번 다듬는 것은 아마추어 방식\n• 시스템(하네스)이 맥락을 알아서 먹이고(2nd Brain)\n• 결과물의 신뢰성을 자동으로 증명(Eval)해야 함\n• AI 주도권을 사람이 쥐고 완전 위임하는 핵심 장치"
p2_sub.font.size = Pt(14)
p2_sub.font.color.rgb = TEXT_WHITE

# --- Slide 3: Second Brain ---
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide3)

header_box = slide3.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = header_box.text_frame
p = tf.paragraphs[0]
p.text = "2. Developer's 2nd Brain: 두 개의 기둥"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

# Card 1: Codebase Graph
c1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = RGBColor(48, 54, 61)
t1 = c1.text_frame
t1.word_wrap = True
pt1 = t1.paragraphs[0]
pt1.text = "🕸️ 기둥 1: Codebase Graph (지도)"
pt1.font.size = Pt(18)
pt1.font.bold = True
pt1.font.color.rgb = ACCENT_BLUE
pt1_sub = t1.add_paragraph()
pt1_sub.text = "\n• 컴파일러 AST 기반 정밀 심볼 링킹\n• 단순 grep이나 벡터 RAG의 환각 극복\n• k-Hop 전파를 통한 Blast Radius(파급 반경) 자동 계산\n• 변경된 코드가 시스템 전체에 미칠 영향 선행 파악"
pt1_sub.font.size = Pt(14)
pt1_sub.font.color.rgb = TEXT_WHITE

# Card 2: Code Memory
c2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.0), Inches(5.4), Inches(4.5))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = RGBColor(48, 54, 61)
t2 = c2.text_frame
t2.word_wrap = True
pt2 = t2.paragraphs[0]
pt2.text = "🧠 기둥 2: Code Memory (역사/맥락)"
pt2.font.size = Pt(18)
pt2.font.bold = True
pt2.font.color.rgb = ACCENT_GREEN
pt2_sub = t2.add_paragraph()
pt2_sub.text = "\n• '왜(Why) 이렇게 구현했는가?'에 대한 암묵지\n• 아키텍처 결정(ADR) 및 과거 장애 회고록\n• AI 에이전트가 신입 시니어처럼 즉시 온보딩\n• 코드만 보고 유추하기 불가능한 팀의 의사결정 보존"
pt2_sub.font.size = Pt(14)
pt2_sub.font.color.rgb = TEXT_WHITE

# --- Slide 4: Eval & Action ---
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide4)

header_box = slide4.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
tf = header_box.text_frame
p = tf.paragraphs[0]
p.text = "3. Eval & 실무(PHY SW) 액션 플랜"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = RGBColor(210, 153, 34)

c_full = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.5))
c_full.fill.solid()
c_full.fill.fore_color.rgb = CARD_BG
c_full.line.color.rgb = RGBColor(48, 54, 61)
tf_full = c_full.text_frame
tf_full.word_wrap = True

pf1 = tf_full.paragraphs[0]
pf1.text = "⚖️ Eval-Driven Development (EDD) 3대 검증 기준"
pf1.font.size = Pt(18)
pf1.font.bold = True
pf1.font.color.rgb = ACCENT_GREEN

pf_sub = tf_full.add_paragraph()
pf_sub.text = "1. Trigger Accuracy: 스킬이 필요한 순간에만 정확히 발동하는가?\n2. Quality Gain: 기존 방식 대비 성능과 검출율이 정량적으로 향상되었는가?\n3. Zero Regression: 새로운 규칙이 다른 정상 코드를 오탐(False Positive)으로 차단하지 않는가?\n\n🚀 우리 모뎀/PHY SW 그룹의 실천 적용점:\n• 이미 구축한 ARM Clang Code Graph에 반증(Disproving) 패스를 결합\n• GitHub Actions CI에 PR 자동 평가(Eval) 시스템을 정착시켜 병합 게이트 자동화"
pf_sub.font.size = Pt(15)
pf_sub.font.color.rgb = TEXT_WHITE
pf_sub.space_before = Pt(10)

prs.save(out_pptx)
print(f"Native PPTX generated successfully: {out_pptx}")

