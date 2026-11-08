import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

out_pptx = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\06_Presenton_Modern_Deck.pptx"
out_pptx_style = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\06_Presenton_Style_Modern_Deck.pptx"

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
ACCENT_ROSE = RGBColor(244, 63, 94)     # #f43f5e (Rose Red)
TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)

def set_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_pill="⚡ META SENIOR LECTURE · 68 SLIDES + REPO COMPLETE"):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.5), Inches(5.4), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 69)
    pill.line.color.rgb = ACCENT_CYAN
    tf_p = pill.text_frame
    tf_p.text = category_pill
    tf_p.paragraphs[0].font.size = Pt(9.5)
    tf_p.paragraphs[0].font.bold = True
    tf_p.paragraphs[0].font.color.rgb = ACCENT_CYAN

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.92), Inches(11.3), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 1: Cover / Hero
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s1)

pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.3), Inches(5.8), Inches(0.45))
pill1.fill.solid()
pill1.fill.fore_color.rgb = RGBColor(30, 41, 69)
pill1.line.color.rgb = ACCENT_CYAN
tf_p1 = pill1.text_frame
tf_p1.text = "⚡ PRESENTON ENGINE · 68 SLIDES + SECOND-BRAIN-EVAL-KIT"
tf_p1.paragraphs[0].font.size = Pt(10.5)
tf_p1.paragraphs[0].font.bold = True
tf_p1.paragraphs[0].font.color.rgb = ACCENT_CYAN

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11.0), Inches(2.4))
tf1 = tb1.text_frame
tf1.word_wrap = True
p1 = tf1.paragraphs[0]
p1.text = "AI 에이전트를 위한 2nd Brain과 Eval"
p1.font.size = Pt(40)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE

p1_sub = tf1.add_paragraph()
p1_sub.text = "메타 시니어 엔지니어 하재상 세미나 + 강사 원본 슬라이드 68장 & 공개 레포(second-brain-eval-kit) 완결판"
p1_sub.font.size = Pt(17)
p1_sub.font.color.rgb = TEXT_MUTED
p1_sub.space_before = Pt(12)

pill_items = [
    ("🕸️ codebase-brain (지도)", "src/query.mjs: TS AST 그래프\n3대 커버리지 라벨(complete/truncated/partial)", Inches(1.2)),
    ("🧠 codebase-brain (메모리)", "src/why.mjs: FTS5 BM25 + RRF\nSKILL.md 3열 라우팅 (발동 76.8%, 오발동 0%)", Inches(5.1)),
    ("⚖️ skill-eval (검증 체계)", "checks.py (invalid/safety/fail)\nisolation.py 4대 차단 + K=3 Judge", Inches(9.0))
]
for title, desc, x_pos in pill_items:
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(4.8), Inches(3.6), Inches(1.95))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    ctf = card.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(15.5)
    cp1.font.bold = True
    cp1.font.color.rgb = ACCENT_CYAN
    cp2 = ctf.add_paragraph()
    cp2.text = desc
    cp2.font.size = Pt(11.5)
    cp2.font.color.rgb = TEXT_MUTED
    cp2.space_before = Pt(6)

# ==============================================================================
# SLIDE 2: AutoKliq 394-File Experiment & Bottleneck Shift (Slide #13)
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s2)
add_header(s2, "코딩 속도에서 '검증 병목'으로 & AutoKliq 394개 파급 실험 (Slide #13)")

c2_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.9))
c2_l.fill.solid()
c2_l.fill.fore_color.rgb = CARD_BG
c2_l.line.color.rgb = ACCENT_ROSE
t2_l = c2_l.text_frame
t2_l.word_wrap = True
tp2_l = t2_l.paragraphs[0]
tp2_l.text = "❌ 스킬 없이 실행 (Without Skill · 56초)"
tp2_l.font.size = Pt(17.5)
tp2_l.font.bold = True
tp2_l.font.color.rgb = ACCENT_ROSE

sub_l = t2_l.add_paragraph()
sub_l.text = (
    "\n• 질문: 'lib/credit-reservations.ts를 바꾸면 깨질 수 있는 파일을 전부 찾아 줘'\n\n"
    "• Grep 2회 시도 후 직접 호출이 3개뿐임을 보고 에이전트가 당황함\n\n"
    "• 즉석에서 일회용 import 추적 스크립트를 직접 짜서 실행 (56초 소요, 394/394 발견)\n\n"
    "• 결정적 문제: 3번 시키면 3번 다(3/3) 탐색 스크립트를 밑바닥부터 새로 짬! (비결정론적 낭비)"
)
sub_l.font.size = Pt(12.5)
sub_l.font.color.rgb = TEXT_WHITE

c2_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.9))
c2_r.fill.solid()
c2_r.fill.fore_color.rgb = CARD_BG
c2_r.line.color.rgb = ACCENT_EMERALD
t2_r = c2_r.text_frame
t2_r.word_wrap = True
tp2_r = t2_r.paragraphs[0]
tp2_r.text = "🛡️ codebase-brain 적용 (<1초 · 결정론적 9-Hop)"
tp2_r.font.size = Pt(17.5)
tp2_r.font.bold = True
tp2_r.font.color.rgb = ACCENT_EMERALD

sub_r = t2_r.add_paragraph()
sub_r.text = (
    "\n• brain build: 6,230개 파일(TS 4,446, 문서 578, 커밋 1,358)을 12.19초에 파싱해 brain.db(56.8 MB) 구축\n\n"
    "• brain impact lib/credit-reservations.ts 단 한 줄 실행\n\n"
    "• <1초 만에 9 Hops 전파를 역추적하여 394개 파일 + 144개 테스트를 100% 결정론적으로 반환\n\n"
    "• 메타 프로파일링 사례: MCP + 시니어 스킬 + Brain 결합으로 10시간 작업을 30분으로 95% 단축"
)
sub_r.font.size = Pt(12.5)
sub_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 3: Tiago Forte vs Dev 2nd Brain & 3 Coverage Labels (Slides #16~#21)
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s3)
add_header(s3, "개발자용 2nd Brain과 3대 커버리지 라벨 (Slides #16~#21)")

cards_s3 = [
    ("1. Tiago Forte vs 개발자 Brain", "• 일반 2nd Brain: 소비자=사람, PARA 노트 정리\n• 개발자 2nd Brain: 소비자=코딩 에이전트, AST 지도 + 코드 메모리 + 라우팅\n• 핵심 원칙: '낡은 컨텍스트(Stale)는 없는 것보다 나쁘다'", ACCENT_AMBER, Inches(1.0)),
    ("2. AST 그래프 (src/query.mjs)", "• 고유 Symbol ID: path#SymbolName\n• CALLS, IMPORTS, TESTS 방향성 엣지\n• N-Hop BFS 역방향 탐색으로 depth별 파급 파일과 연결 테스트 즉시 도출", ACCENT_CYAN, Inches(4.9)),
    ("3. 정직한 3대 커버리지 라벨", "• complete: 모든 홉 탐색 완료 (추가 grep 불필요)\n• truncated: 500개/10홉 상한 도달 경고\n• partial: 동적 호출/미해결 심볼 존재 경고\n• + stale: git HEAD 불일치 시 재빌드 권고", ACCENT_EMERALD, Inches(8.8))
]
for title, body, border_c, x_pos in cards_s3:
    c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.9), Inches(3.6), Inches(4.9))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = border_c
    ctf = c.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(15.5)
    cp1.font.bold = True
    cp1.font.color.rgb = border_c
    cp2 = ctf.add_paragraph()
    cp2.text = f"\n{body}"
    cp2.font.size = Pt(12)
    cp2.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 4: Code Memory (why.mjs) & SKILL.md Routing (Slides #22~#27)
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s4)
add_header(s4, "기둥 2 & 3: FTS5 BM25+RRF 코드 메모리(why.mjs)와 3열 라우팅 규칙")

c4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.9))
c4_l.fill.solid()
c4_l.fill.fore_color.rgb = CARD_BG
c4_l.line.color.rgb = ACCENT_AMBER
t4_l = c4_l.text_frame
t4_l.word_wrap = True
tp4_l = t4_l.paragraphs[0]
tp4_l.text = "🧠 src/why.mjs: SQLite FTS5 BM25 + RRF"
tp4_l.font.size = Pt(17.5)
tp4_l.font.bold = True
tp4_l.font.color.rgb = ACCENT_AMBER
sp4_l = t4_l.add_paragraph()
sp4_l.text = (
    "\n• '코드는 저장하지 않고 지도에 잇는다'\n"
    "  설계 문서(ADR/PR)와 커밋 로그를 청크로 쪼개어 심볼 그래프에 연결\n\n"
    "• 하이브리드 2채널 검색 (LLM 비용 $0, <1초 응답)\n"
    "  - 1채널: 파일/심볼 그래프 직접 연결 청크 (1.3x)\n"
    "  - 2채널: SQLite FTS5 bm25(chunks_fts, 3.0, 1.0)\n"
    "  - 결합: Reciprocal Rank Fusion 1/(60 + rank + 1)\n\n"
    "• 고정밀 링킹 규칙: '헷갈리면 잇지 않는다'\n"
    "  함수 이름은 전체 레포에서 후보가 1~3개 이하일 때만 연결하여 노이즈를 0%로 억제"
)
sp4_l.font.size = Pt(12)
sp4_l.font.color.rgb = TEXT_WHITE

c4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.9))
c4_r.fill.solid()
c4_r.fill.fore_color.rgb = CARD_BG
c4_r.line.color.rgb = ACCENT_CYAN
t4_r = c4_r.text_frame
t4_r.word_wrap = True
tp4_r = t4_r.paragraphs[0]
tp4_r.text = "🔀 SKILL.md 3열 라우팅 & 76.8% 성적표"
tp4_r.font.size = Pt(17.5)
tp4_r.font.bold = True
tp4_r.font.color.rgb = ACCENT_CYAN
sp4_r = t4_r.add_paragraph()
sp4_r.text = (
    "\n• 3열 매핑 표: The question | Call | Not this\n"
    "  - 파급 반경 ➔ brain impact (Not: 수동 grep 반복)\n"
    "  - 설계 의도 ➔ brain why (Not: git log 전체 덤프)\n"
    "  - 작은 단일 파일 수정 ➔ 'do not call brain. Read the file.' 명시!\n\n"
    "• 라우팅 평가 결과 (Slide #27):\n"
    "  - 전체 69개 시행 중 53회 스킬 로드 (76.8%)\n"
    "  - 작은 작업(small-task) 오발동: 0 / 6 (0%!)\n"
    "  - 불필요한 Brain 호출로 인한 레이턴시·토큰 낭비 완벽 차단"
)
sp4_r.font.size = Pt(12)
sp4_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 5: 2026 3 Numbers, pass@3 vs pass^3, checks.py (Slides #34~#43)
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s5)
add_header(s5, "Skill Eval: 2026년의 숫자 3개, pass@3 vs pass^3, '0점의 3가지 이름'")

cards_s5 = [
    ("1. 2026년의 숫자 3개 (#34)", "• 56%: 스킬을 줬지만 아예 안 불림 (Vercel Next.js 16)\n• 6개 중 5개: Eval로 설명만 고쳐 트리거 개선 (Anthropic)\n• -44%: 스킬로 비용 44% 절감 + 완결성 Eval로 누락 포착 (Arize)\n\n• 4대 질문: routing / uplift / regression / A/A", ACCENT_ROSE, Inches(1.0)),
    ("2. pass@3 vs pass^3 (#39)", "• 80% 정확도 에이전트를 3번 실행할 때:\n• pass@3 = 99.2% (1번이라도 성공): 버그 수정 패치용\n• pass^3 = 51.2% (3번 모두 성공): 파급 분석(Find-All)용 — 한 번이라도 놓치면 장애!\n• Find-All 채점: Recall >= 0.9 & Precision >= 0.8 동시 강제", ACCENT_PURPLE, Inches(4.9)),
    ("3. '0점에도 이름이 있다' (#38)", "• skill_eval/checks.py 3단계 분리:\n  1. invalid (score: None): 정답 훔쳐보기 적발 시 분모에서 제외\n  2. safety_violation (0.0): 읽기 전용 워크스페이스 훼손\n  3. fail (0.0): 정답 미달 (Judge 스킵)\n• 통과 시 claude-opus-5-5 3표 다수결", ACCENT_EMERALD, Inches(8.8))
]
for title, body, border_c, x_pos in cards_s5:
    c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.9), Inches(3.6), Inches(4.9))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = border_c
    ctf = c.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = title
    cp1.font.size = Pt(15.5)
    cp1.font.bold = True
    cp1.font.color.rgb = border_c
    cp2 = ctf.add_paragraph()
    cp2.text = f"\n{body}"
    cp2.font.size = Pt(11.5)
    cp2.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 6: 4-Pillar Eval Sandbox Isolation (skill_eval/isolation.py)
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s6)
add_header(s6, "Eval 4대 차단 원칙: 데이터 오염 및 보상 해킹(Reward Hacking) 방지 (#37, #44, #46)")

c6_l = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.9))
c6_l.fill.solid()
c6_l.fill.fore_color.rgb = CARD_BG
c6_l.line.color.rgb = ACCENT_ROSE
t6_l = c6_l.text_frame
t6_l.word_wrap = True
tp6_l = t6_l.paragraphs[0]
tp6_l.text = "🚫 1. 원본 Repo 차단 & 🔒 2. 정답 차단"
tp6_l.font.size = Pt(17)
tp6_l.font.bold = True
tp6_l.font.color.rgb = ACCENT_ROSE
sp6_l = t6_l.add_paragraph()
sp6_l.text = (
    "\n• 1. 원본 Repo 차단 (개발 소스 & 메타데이터 격리)\n"
    "  - 반칙: git log/diff나 초안을 뒤져 출제 의도 파악\n"
    "  - 구현: 매 trial마다 $TMPDIR APFS clone 생성, origin 제거, .claude/.agents 제거 및 원본 경로 deny\n\n"
    "• 2. 정답 차단 (Ground Truth 은닉 & 역설계 방지)\n"
    "  - 반칙: find/grep으로 answer-keys나 채점 코드 베끼기\n"
    "  - 구현: 워크스페이스 외부 격리 + permissions.deny + 적발 시 0점이 아닌 outcome: invalid(실행 무효) 처리"
)
sp6_l.font.size = Pt(12)
sp6_l.font.color.rgb = TEXT_WHITE

c6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.9))
c6_r.fill.solid()
c6_r.fill.fore_color.rgb = CARD_BG
c6_r.line.color.rgb = ACCENT_CYAN
t6_r = c6_r.text_frame
t6_r.word_wrap = True
tp6_r = t6_r.paragraphs[0]
tp6_r.text = "🧹 3. ~/.claude 차단 & 🌐 4. 네트워크 차단"
tp6_r.font.size = Pt(17)
tp6_r.font.bold = True
tp6_r.font.color.rgb = ACCENT_CYAN
sp6_r = t6_r.add_paragraph()
sp6_r.text = (
    "\n• 3. ~/.claude 차단 (글로벌 환경 & 개인화 격리)\n"
    "  - 반칙: 전역 CLAUDE.md, 개인 스킬, MCP, 자동 메모리에 의존해 베이스라인 오염\n"
    "  - 구현: 빈 CLAUDE_CONFIG_DIR + 번들 스킬 22종 off + 상위 폴더 CLAUDE.md 존재 시 실행 거부\n\n"
    "• 4. 네트워크 차단 (외부 의존성 차단 & 결정론적 평가)\n"
    "  - 반칙: 구글링이나 외부 패키지 설치로 결함 우회\n"
    "  - 구현: sandbox.enabled=True & skill-eval probe 21/21 PASS 무균 검증 후 본 실험 실행"
)
sp6_r.font.size = Pt(12)
sp6_r.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 7: 6-Stage Maturity (L0~L5), Scorecard & Domain Blueprint (Slides #48, #51, #55)
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s7)
add_header(s7, "Eval 성숙도 6단계(L0~L5), 300-Trial 성적표 & 모바일 PHY SW 청사진")

c7_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.9))
c7_l.fill.solid()
c7_l.fill.fore_color.rgb = CARD_BG
c7_l.line.color.rgb = ACCENT_EMERALD
t7_l = c7_l.text_frame
t7_l.word_wrap = True
tp7_l = t7_l.paragraphs[0]
tp7_l.text = "📈 L0~L5 성숙도 & 300-Trial 대시보드 (#48, #51)"
tp7_l.font.size = Pt(17)
tp7_l.font.bold = True
tp7_l.font.color.rgb = ACCENT_EMERALD
sp7_l = t7_l.add_paragraph()
sp7_l.text = (
    "\n• L0(감) ➔ L1(하드체크) ➔ L2(고정 케이스셋) ➔ L3(Judge+k회+대조) ➔ L4(PR마다 CI 자동 실행: 가장 큰 점프!) ➔ L5(프로덕션 실패를 새 케이스로 편입: 가장 중요!)\n\n"
    "• 300/300 Trials ($65.61): none(88%, 68.3s) vs v1(93%, 39.0s) vs v2(95%, 38.6s) vs v1b(93%, 40.2s)\n\n"
    "• 통계 규율: 95% 신뢰구간(CI) 막대가 0을 걸치면 '차이를 확신할 수 없다'고 정직하게 판독하라"
)
sp7_l.font.size = Pt(12)
sp7_l.font.color.rgb = TEXT_WHITE

c7_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.9))
c7_r.fill.solid()
c7_r.fill.fore_color.rgb = CARD_BG
c7_r.line.color.rgb = ACCENT_PURPLE
t7_r = c7_r.text_frame
t7_r.word_wrap = True
tp7_r = t7_r.paragraphs[0]
tp7_r.text = "📡 모바일 PHY SW 로드맵 & 인간의 주도권 (#55)"
tp7_r.font.size = Pt(17)
tp7_r.font.bold = True
tp7_r.font.color.rgb = ACCENT_PURPLE
sp7_r = t7_r.add_paragraph()
sp7_r.text = (
    "\n• 1. Clang AST 레지스터 맵 그래프 + partial 커버리지 라벨\n"
    "• 2. 3GPP 규격 & 실리콘 에라타 FTS5 BM25+RRF Memory (후보 1~3개 링킹 규칙)\n"
    "• 3. 펌웨어 4대 무균 샌드박스 + pass^3 CI 게이트\n\n"
    "💡 '에이전트에게 주도권을 뺏기지 마세요.'\n"
    "나의 1번 가치(가족, 건강, 엔지니어링 본질)를 세우고, 구현과 검증은 시스템 하네스에 위임하라."
)
sp7_r.font.size = Pt(12)
sp7_r.font.color.rgb = TEXT_WHITE

prs.save(out_pptx)
shutil.copyfile(out_pptx, out_pptx_style)
print(f"Successfully generated Presenton decks: {out_pptx} and {out_pptx_style}")
