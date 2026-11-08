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
DARK_BG = RGBColor(13, 17, 23)       # #0d1117
CARD_BG = RGBColor(22, 27, 34)       # #161b22
ACCENT_BLUE = RGBColor(88, 166, 255) # #58a6ff
ACCENT_GREEN = RGBColor(63, 185, 80) # #3fb950
ACCENT_PURPLE = RGBColor(188, 140, 255)
ACCENT_RED = RGBColor(248, 81, 73)
ACCENT_AMBER = RGBColor(210, 153, 34)
TEXT_WHITE = RGBColor(240, 246, 252)
TEXT_MUTED = RGBColor(139, 148, 158)

def apply_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = DARK_BG
    bg_shape.line.fill.background()
    return bg_shape

def add_slide_header(slide, title_text, color=ACCENT_BLUE):
    header_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.65), Inches(11.3), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = color

# --- Slide 1: Title ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide1)

title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11.0), Inches(3.6))
tf = title_box.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "AI 에이전트를 위한 2nd Brain & Eval 프레임워크"
p1.font.size = Pt(38)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE
p1.font.name = "Segoe UI"

p2 = tf.add_paragraph()
p2.text = "메타 8년차 시니어 엔지니어 세미나 + 강사 원본 슬라이드 68장 & second-brain-eval-kit 전수 분석"
p2.font.size = Pt(19)
p2.font.color.rgb = ACCENT_BLUE
p2.space_before = Pt(18)

p3 = tf.add_paragraph()
p3.text = "• codebase-brain: query.mjs (AST + 3대 커버리지 라벨) & why.mjs (SQLite FTS5 BM25 + RRF)\n• skill-eval: checks.py (invalid/safety_violation/fail) & isolation.py (4대 무균 샌드박스 차단)"
p3.font.size = Pt(14)
p3.font.color.rgb = TEXT_MUTED
p3.space_before = Pt(16)

# --- Slide 2: Bottleneck Shift & AutoKliq Benchmark ---
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide2)
add_slide_header(slide2, "1. 검증 병목으로의 이동 & AutoKliq 394개 파급 실험 (Slide #13)", ACCENT_BLUE)

card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
card1.fill.solid()
card1.fill.fore_color.rgb = CARD_BG
card1.line.color.rgb = ACCENT_RED
tf1 = card1.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "⚠️ 스킬 없이 실행 (56초 · 스크립트 3/3 재발명)"
p1.font.size = Pt(18)
p1.font.bold = True
p1.font.color.rgb = ACCENT_RED
p1_sub = tf1.add_paragraph()
p1_sub.text = "\n• 질문: 'lib/credit-reservations.ts 변경 시 깨질 수 있는 파일 전수 탐색'\n• Grep 2회 실패 후, 에이전트가 즉석에서 일회용 import 추적 스크립트를 직접 짜서 실행\n• 56초 소요, 394/394개 발견\n• 문제점: 3번 시키면 3번 다(3/3) 탐색 스크립트를 처음부터 다시 작성함 (비결정론적)"
p1_sub.font.size = Pt(13.5)
p1_sub.font.color.rgb = TEXT_WHITE

card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.4), Inches(4.9))
card2.fill.solid()
card2.fill.fore_color.rgb = CARD_BG
card2.line.color.rgb = ACCENT_GREEN
tf2 = card2.text_frame
tf2.word_wrap = True
p2 = tf2.paragraphs[0]
p2.text = "🛡️ codebase-brain 적용 (<1초 · 결정론적 9-Hop)"
p2.font.size = Pt(18)
p2.font.bold = True
p2.font.color.rgb = ACCENT_GREEN
p2_sub = tf2.add_paragraph()
p2_sub.text = "\n• brain build: 6,230개 파일(TS 4,446, 문서 578, 커밋 1,358)을 12.19초에 파싱해 brain.db(56.8MB) 생성\n• brain impact 단 한 줄로 9 Hops 전파를 <1초 만에 역추적 (394개 파일 + 144개 테스트 반환)\n• 메타 프로파일링 사례: MCP + 시니어 스킬 + Brain 결합으로 10시간을 30분으로 단축"
p2_sub.font.size = Pt(13.5)
p2_sub.font.color.rgb = TEXT_WHITE

# --- Slide 3: codebase-brain Architecture ---
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide3)
add_slide_header(slide3, "2. codebase-brain: 지도(query.mjs) + 메모리(why.mjs) + 라우팅", ACCENT_PURPLE)

c1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
c1.fill.solid()
c1.fill.fore_color.rgb = CARD_BG
c1.line.color.rgb = ACCENT_BLUE
t1 = c1.text_frame
t1.word_wrap = True
pt1 = t1.paragraphs[0]
pt1.text = "🕸️ ① 지도 (src/query.mjs) & 3대 커버리지 라벨"
pt1.font.size = Pt(17.5)
pt1.font.bold = True
pt1.font.color.rgb = ACCENT_BLUE
pt1_sub = t1.add_paragraph()
pt1_sub.text = "\n• 고유 Symbol ID (path#SymbolName) & N-Hop BFS\n• complete: 모든 홉 탐색 완료 (추가 grep 불필요)\n• truncated: 500개/10홉 상한 도달 경고\n• partial: 동적 호출/미해결 심볼 존재 경고\n• stale: git HEAD 불일치 경고 ('낡은 컨텍스트는 없는 것보다 나쁘다')"
pt1_sub.font.size = Pt(13)
pt1_sub.font.color.rgb = TEXT_WHITE

c2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.4), Inches(4.9))
c2.fill.solid()
c2.fill.fore_color.rgb = CARD_BG
c2.line.color.rgb = ACCENT_GREEN
t2 = c2.text_frame
t2.word_wrap = True
pt2 = t2.paragraphs[0]
pt2.text = "🧠 ② 코드 메모리 (src/why.mjs) & ③ 라우팅"
pt2.font.size = Pt(17.5)
pt2.font.bold = True
pt2.font.color.rgb = ACCENT_GREEN
pt2_sub = t2.add_paragraph()
pt2_sub.text = "\n• SQLite FTS5 bm25(chunks_fts, 3.0, 1.0) + RRF(1/(60+rank+1)) 하이브리드 랭킹 (LLM 비용 $0, <1초 응답)\n• '헷갈리면 잇지 않는다': 함수 이름은 후보 1~3개일 때만 연결\n• SKILL.md 3열 라우팅: 작은 작업엔 'do not call brain' 명시 (발동률 76.8%, 작은 작업 오발동 0/6)"
pt2_sub.font.size = Pt(13)
pt2_sub.font.color.rgb = TEXT_WHITE

# --- Slide 4: Skill Eval & 4-Pillar Isolation ---
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(slide4)
add_slide_header(slide4, "3. skill-eval: pass@3 vs pass^3, checks.py & 4대 무균 격리", ACCENT_AMBER)

c4_1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
c4_1.fill.solid()
c4_1.fill.fore_color.rgb = CARD_BG
c4_1.line.color.rgb = ACCENT_AMBER
tf4_1 = c4_1.text_frame
tf4_1.word_wrap = True
pf1 = tf4_1.paragraphs[0]
pf1.text = "⚖️ 2026 숫자 3개, pass^3 & '0점의 3가지 이름'"
pf1.font.size = Pt(17.5)
pf1.font.bold = True
pf1.font.color.rgb = ACCENT_AMBER
pf_sub1 = tf4_1.add_paragraph()
pf_sub1.text = "\n• 2026년 3대 숫자: 56%(미호출), 6개 중 5개(설명 개선), -44%(비용 절감)\n• 80% 에이전트 3회 실행: pass@3 = 99.2%(버그 패치) vs pass^3 = 51.2%(파급 분석 Find-All)\n• checks.py: invalid(정답 훔쳐보기, 분모 제외) / safety_violation(워크스페이스 훼손, 0점) / fail(오답, 0점)"
pf_sub1.font.size = Pt(13)
pf_sub1.font.color.rgb = TEXT_WHITE

c4_2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.4), Inches(4.9))
c4_2.fill.solid()
c4_2.fill.fore_color.rgb = CARD_BG
c4_2.line.color.rgb = ACCENT_RED
tf4_2 = c4_2.text_frame
tf4_2.word_wrap = True
pf2 = tf4_2.paragraphs[0]
pf2.text = "🧪 isolation.py 4대 샌드박스 차단 원칙"
pf2.font.size = Pt(17.5)
pf2.font.bold = True
pf2.font.color.rgb = ACCENT_RED
pf_sub2 = tf4_2.add_paragraph()
pf_sub2.text = "\n1. 원본 Repo 차단: $TMPDIR APFS clone, origin 제거, .claude 제거 (출제 의도 컨닝 차단)\n2. 정답 차단: answer-keys 외부 격리 + deny (보상 해킹 차단)\n3. ~/.claude 차단: 빈 CLAUDE_CONFIG_DIR + 번들 스킬 22종 off (순수 Delta 측정)\n4. 네트워크 차단: 커널 샌드박스 강제 + 21/21 probe 검증"
pf_sub2.font.size = Pt(13)
pf_sub2.font.color.rgb = TEXT_WHITE

prs.save(out_pptx)
print(f"Native PPTX generated successfully: {out_pptx}")
