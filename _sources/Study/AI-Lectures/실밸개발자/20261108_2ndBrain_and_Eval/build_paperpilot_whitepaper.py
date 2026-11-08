import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
    KeepTogether,
    PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. Register Korean Font (Malgun Gothic)
font_path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "malgun.ttf")
font_bold_path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "malgunbd.ttf")

if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("Malgun", font_path))
    body_font = "Malgun"
else:
    body_font = "Helvetica"

if os.path.exists(font_bold_path):
    pdfmetrics.registerFont(TTFont("Malgun-Bold", font_bold_path))
    title_font = "Malgun-Bold"
else:
    title_font = body_font

pdf_path = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\07_PaperPilot_Executive_Whitepaper.pdf"

# 2. Numbered Canvas for Professional Headers & Footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(body_font, 8)
        self.setFillColor(colors.HexColor("#64748b"))
        # Top Header
        self.drawString(20 * mm, 285 * mm, "CONFIDENTIAL · 2nd Brain & AI Agent Evaluation Whitepaper (68 Slides + Repo Complete)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(20 * mm, 282 * mm, 190 * mm, 282 * mm)

        # Bottom Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(190 * mm, 12 * mm, page_str)
        self.drawString(20 * mm, 12 * mm, "Generated via PaperPilot Rust/MCP Specification Standard · Meta Senior SWE Lecture & second-brain-eval-kit")
        self.line(20 * mm, 16 * mm, 190 * mm, 16 * mm)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=18 * mm,
    rightMargin=18 * mm,
    topMargin=19 * mm,
    bottomMargin=19 * mm,
)

# 3. Styles
styles = getSampleStyleSheet()

h1_style = ParagraphStyle(
    "CustomH1",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=16.5,
    leading=22,
    textColor=colors.HexColor("#0f172a"),
    spaceAfter=4,
)

h2_style = ParagraphStyle(
    "CustomH2",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#1e293b"),
    spaceBefore=6.5,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontName=body_font,
    fontSize=8.6,
    leading=13,
    textColor=colors.HexColor("#334155"),
    spaceAfter=3.5,
)

badge_style = ParagraphStyle(
    "BadgeStyle",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=8,
    leading=10,
    textColor=colors.HexColor("#2563eb"),
)

callout_style = ParagraphStyle(
    "CalloutStyle",
    parent=styles["Normal"],
    fontName=body_font,
    fontSize=8.5,
    leading=13,
    textColor=colors.HexColor("#1e293b"),
)

table_header_style = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=8.2,
    leading=11,
    textColor=colors.white,
    alignment=1,
)

table_cell_style = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontName=body_font,
    fontSize=7.8,
    leading=11,
    textColor=colors.HexColor("#1e293b"),
)

table_cell_bold = ParagraphStyle(
    "TableCellBold",
    parent=table_cell_style,
    fontName=title_font,
)

story = []

# --- Title & Banner ---
story.append(Paragraph("<font color='#2563eb'><b>[ EXECUTIVE TECH WHITEPAPER · 68 INSTRUCTOR SLIDES + REPO SOURCE INTEGRATED ]</b></font>", badge_style))
story.append(Spacer(1, 2.5 * mm))
story.append(Paragraph("AI 에이전트를 위한 2nd Brain과 Eval 프레임워크 아키텍처", h1_style))
story.append(Paragraph(
    "<b>분석 대상:</b> 메타 시니어 엔지니어 하재상(실밸개발자) 77분 세미나 + 강사 원본 슬라이드 68장 + 공개 레포(<b>jha0313/second-brain-eval-kit</b>) 전수 분석<br/>"
    "<b>적용 분야:</b> 모바일 통신/물리계층(PHY) 임베디드 C/C++ SW 코드 리뷰 및 자율 검증 파이프라인", body_style
))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=3.5 * mm))

# --- Executive Summary Box ---
summary_text = (
    "<b>[핵심 요약 (Executive Summary)]</b><br/>"
    "본 백서는 메타 시니어 엔지니어 하재상님의 강연 보이스, CV로 캡처한 <b>원본 슬라이드 68장</b>, 그리고 오픈소스 레포지토리 "
    "(<b>github.com/jha0313/second-brain-eval-kit</b>)의 실제 구현 코드를 통합 분석한 엔터프라이즈 기술 백서이다. "
    "자율 코딩 에이전트 도입의 성패를 가르는 두 기둥인 <b>1) 컨텍스트 계층(codebase-brain: TS/Clang AST 그래프 query.mjs + SQLite FTS5 BM25/RRF 코드 메모리 why.mjs + 3열 라우팅 테이블)</b>과 "
    "<b>2) 검증 계층(skill-eval: 4대 무균 격리 isolation.py + 0점의 3가지 이름 checks.py + K=3 다수결 Judge + 95% 신뢰구간 판독)</b>을 규명하고, "
    "모바일 통신 물리계층(PHY) 임베디드 SW 그룹의 아키텍처로 1:1 매핑한다."
)
summary_table = Table([[Paragraph(summary_text, callout_style)]], colWidths=[174 * mm])
summary_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f7ff")),
    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
    ("PADDING", (0, 0), (-1, -1), 7),
]))
story.append(summary_table)
story.append(Spacer(1, 3.5 * mm))

# --- Section 1: Bottleneck Shift & AutoKliq Benchmark ---
story.append(Paragraph("1. 검증 병목으로의 이동 & AutoKliq 프로덕션 코드베이스 실전 실험 (Slide #13)", h2_style))
story.append(Paragraph(
    "LLM 도입 이후 코드 작성 속도는 폭발했으나, 초대형 PR 범람으로 인해 <b>'인간 리뷰어의 검증 한계'</b>가 새로운 병목이 되었다. "
    "메타 사내에서 <b>월 $30,000 상당의 토큰 실험</b>과 <b>성능 프로파일링 트리아지 단축(10시간 -> 30분, Profiling MCP + 시니어 스킬 + Brain 결합)</b>을 거치며 입증된 AutoKliq(6,230개 파일) 실전 파급 반경 실험 결과는 다음과 같다:", body_style
))

autokliq_data = [
    [
        Paragraph("비교 항목 (질문: lib/credit-reservations.ts 수정 시 파급 파일 전수 탐색)", table_header_style),
        Paragraph("스킬 없이 (Without Skill · Baseline)", table_header_style),
        Paragraph("codebase-brain 스킬 적용 (With Skill)", table_header_style)
    ],
    [
        Paragraph("<b>에이전트 행동 패턴</b>", table_cell_bold),
        Paragraph("Grep 2회 실패 후, <b>매번 일회용 import 역추적 스크립트를 즉석에서 새로 작성(3/3)</b>하여 실행", table_cell_style),
        Paragraph("<b>brain build</b>(12.19초, 56.8MB DB) 후 <b>brain impact</b> 명령 단 한 줄로 9-Hop BFS 즉시 추적", table_cell_style)
    ],
    [
        Paragraph("<b>소요 시간 및 탐색 결과</b>", table_cell_bold),
        Paragraph("<b>56초</b> (394 / 394개 파일 발견, 매번 스크립트 재발명)", table_cell_style),
        Paragraph("<b>&lt; 1초</b> (394개 파일 + 144개 테스트 100% 결정론적 반환: 1-hop 3 -> 2-hop 21 -> 3-hop 146 -> 4-hop+ 224)", table_cell_style)
    ]
]
autokliq_table = Table(autokliq_data, colWidths=[50 * mm, 62 * mm, 62 * mm])
autokliq_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 4),
]))
story.append(autokliq_table)
story.append(Spacer(1, 3 * mm))

# --- Section 2: Tiago Forte vs Dev 2nd Brain & 3 Pillars ---
story.append(Paragraph("2. 개발자용 2nd Brain (`codebase-brain`)의 3대 핵심 구성요소 (Slides #16~#27)", h2_style))
story.append(Paragraph(
    "Tiago Forte(2022)의 일반 세컨드 브레인은 소비자가 <b>'사람'</b>이고 PARA 폴더에 노트를 정리하지만, "
    "개발자용 세컨드 브레인은 소비자가 <b>'코딩 에이전트'</b>이며 핵심 원칙은 <b>\"낡은 컨텍스트(Stale Context)는 없는 것보다 나쁘다\"</b>이다.", body_style
))

brain_comp_data = [
    [
        Paragraph("구성요소", table_header_style),
        Paragraph("구현 파일 및 핵심 알고리즘", table_header_style),
        Paragraph("환각 및 노이즈 방지 메커니즘 (강사 슬라이드 핵심)", table_header_style)
    ],
    [
        Paragraph("<b>① 지도 (Map)</b>", table_cell_bold),
        Paragraph("<b>src/query.mjs</b><br/>TS Compiler API AST 파싱, 고유 Symbol ID(path#SymbolName), N-Hop BFS 역추적", table_cell_style),
        Paragraph("<b>3대 커버리지 라벨:</b> <b>complete</b>(완전 탐색), <b>truncated</b>(500개/10홉 상한 도달), <b>partial</b>(동적 호출/미해결 엣지 존재) + <b>stale</b>(커밋 불일치 경고)", table_cell_style)
    ],
    [
        Paragraph("<b>② 코드 메모리</b>", table_cell_bold),
        Paragraph("<b>src/why.mjs</b><br/>SQLite FTS5 <b>bm25(chunks_fts, 3.0, 1.0)</b> + <b>RRF(1/(60+rank+1))</b> 하이브리드 랭킹", table_cell_style),
        Paragraph("<b>\"코드는 저장하지 않고 지도에 잇는다\"</b> — LLM 비용 $0, &lt;1초에 문서/커밋(b8401c2a) 인용. <b>함수 이름은 후보 1~3개일 때만 연결(헷갈리면 잇지 않는다)</b>", table_cell_style)
    ],
    [
        Paragraph("<b>③ 라우팅</b>", table_cell_bold),
        Paragraph("<b>SKILL.md</b><br/>3열 테이블: <b>The question | Call | Not this</b>", table_cell_style),
        Paragraph("작은 단일 파일 수정에는 <b>\"do not call brain. Read the file.\"</b> 명시 -> 평가 결과 <b>필요 작업 발동률 76.8%(53/69), 작은 작업 오발동 0/6(0%)</b> 달성", table_cell_style)
    ]
]
brain_table = Table(brain_comp_data, colWidths=[28 * mm, 64 * mm, 82 * mm])
brain_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 4),
]))
story.append(brain_table)
story.append(Spacer(1, 3 * mm))

# --- Section 3: Skill Eval Metrics & pass@3 vs pass^3 ---
story.append(Paragraph("3. Skill Eval (`skill-eval`): 2026년의 숫자 3개 & pass@3 vs pass^3 (Slides #34~#43)", h2_style))
story.append(Paragraph(
    "• <b>2026년의 숫자 3개 (#34):</b> ① <b>56%</b>(스킬을 줬지만 절반 이상 안 불림 — Vercel Next.js 16, 2026.01), "
    "② <b>6개 중 5개</b>(Eval로 description만 고쳐 트리거 개선 — Anthropic skill-creator, 2026.03), "
    "③ <b>-44%</b>(스킬로 비용 44% 절감 + 완결성 Eval로 답 누락 포착 — Arize, 2026.07).<br/>"
    "• <b>Eval이 답하는 4가지 질문 (#36):</b> <b>routing</b>(진단용, 점수 제외), <b>uplift</b>(none vs v1), <b>regression</b>(v1 vs v2), <b>A/A</b>(v1 vs v1b 바닥 노이즈 확인).<br/>"
    "• <b>pass@3 vs pass^3 (#39, Yao et al. τ-bench):</b> 1회 정확도 80%인 에이전트를 3번 실행할 때, 적어도 1번 성공할 확률 <b>pass@3 = 99.2%</b>(버그 패치용)이지만, "
    "3번 모두 성공할 확률 <b>pass^3 = 51.2%</b>(파급 반경 find-all용: 한 번이라도 놓치면 장애)로 급락한다.<br/>"
    "• <b>Find-All 두 줄 채점 (#42):</b> 전체 4,488개 파일을 다 찍으면 Recall 1.00 / Precision 0.09가 된다. 꼼수를 막기 위해 <b>Recall &gt;= 0.9 AND Precision &gt;= 0.8</b>을 <b>FROZEN.json</b>에 사전 동결한다.<br/>"
    "• <b>\"0점에도 이름이 있다\" (skill_eval/checks.py, #38 & #43):</b> ① 정답 훔쳐보기 적발 시 <b>outcome: 'invalid', score: None</b>(분모에서 제외 및 경보), "
    "② 읽기 전용 워크스페이스 훼손 시 <b>outcome: 'safety_violation', score: 0.0</b>, ③ 정답 조건 미달 시 <b>outcome: 'fail', score: 0.0</b>(모두 LLM Judge 스킵). "
    "통과한 답안만 <b>claude-opus-5-5 Judge(항목당 3표 다수결)</b>로 채점한다.", body_style
))

# --- Section 4: 4-Pillar Sandbox Isolation ---
story.append(Paragraph("4. Eval 프로세스 4대 샌드박스 격리 원칙 (`skill_eval/isolation.py` · Slides #37, #44, #46)", h2_style))
story.append(Paragraph(
    "LLM 에이전트는 목표 달성을 위해 파일 시스템과 Git 로그를 뒤지는 <b>보상 해킹(Reward Hacking)</b> 특성이 있다. "
    "데이터 오염을 막고 오직 테스트 대상 스킬의 순수 기여도(Delta)만 검증하기 위해 다음 4가지를 원천 차단하며, 매 실행 전 <b>skill-eval probe (21/21 PASS)</b>로 무결성을 검증한다:", body_style
))

isolation_data = [
    [
        Paragraph("차단 항목", table_header_style),
        Paragraph("에이전트가 시도하는 반칙 (Cheating)", table_header_style),
        Paragraph("skill_eval/isolation.py 실제 구현 및 차단 효과", table_header_style)
    ],
    [
        Paragraph("<b>1. 원본 Repo 차단</b>", table_cell_bold),
        Paragraph("git log/diff나 개발 문서를 읽고 출제 의도 파악", table_cell_style),
        Paragraph("매 trial마다 <b>$TMPDIR 아래 APFS clone(cp -c -R)</b> 생성, <b>git remote remove origin</b>, .claude/.agents 제거 및 원본 스킬 경로 deny -> 실제 배포 상태 모사", table_cell_style)
    ],
    [
        Paragraph("<b>2. 정답 차단</b>", table_cell_bold),
        Paragraph("채점 스크립트나 정답 파일을 find/grep으로 베끼기", table_cell_style),
        Paragraph("<b>answer-keys/</b>를 워크스페이스 외부에 격리 + <b>permissions.deny</b> 등록 + 접근 시도 적발 시 0점이 아닌 <b>outcome: invalid</b>로 즉시 실격 처리", table_cell_style)
    ],
    [
        Paragraph("<b>3. ~/.claude 차단</b>", table_cell_bold),
        Paragraph("전역 CLAUDE.md 지침, 개인 스킬, MCP, 메모리에 의존", table_cell_style),
        Paragraph("매 trial 빈 <b>CLAUDE_CONFIG_DIR</b> 생성 + 번들 스킬 22종 전부 off + <b>disableAllHooks</b> + 상위 폴더에 CLAUDE.md 존재 시 실행 거부 -> 순수 Delta 측정", table_cell_style)
    ],
    [
        Paragraph("<b>4. 네트워크 차단</b>", table_cell_bold),
        Paragraph("막히는 부분을 구글링하거나 외부 패키지 설치로 해결", table_cell_style),
        Paragraph("OS 커널 샌드박스(<b>sandbox: {enabled: True, allowUnsandboxedCommands: False}</b>) 강제 -> 시간에 구애받지 않는 결정론적 재현성(Determinism) 확보", table_cell_style)
    ]
]
isolation_table = Table(isolation_data, colWidths=[30 * mm, 58 * mm, 86 * mm])
isolation_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#991b1b")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 4),
]))
story.append(isolation_table)
story.append(Spacer(1, 3 * mm))

# --- Section 5: 6-Stage Maturity Model & Scorecard ---
story.append(Paragraph("5. Eval 성숙도 6단계 (L0~L5) 및 300-Trial 성적표 대시보드 (Slides #48, #51)", h2_style))
maturity_text = (
    "• <b>성숙도 6단계 (#48):</b> <b>L0</b>(감/Vibe 테스트) -> <b>L1</b>(결정론적 체크) -> <b>L2</b>(고정 케이스셋 10~30개 FROZEN.json) -> "
    "<b>L3</b>(LLM Judge + k회 실행 + 베이스라인 대조) -> <b>L4</b>(PR마다 CI 자동 실행 — <b>가장 큰 점프</b>) -> "
    "<b>L5</b>(프로덕션 실패를 새 회귀 케이스로 편입 — <b>가장 중요한 단계</b>).<br/>"
    "• <b>300-Trial 성적표 (#51, $65.61):</b> <b>none</b>(88%, 68.3s, $0.25) vs <b>v1</b>(93%, 39.0s, $0.21) vs <b>v2</b>(95%, 38.6s, $0.21) vs <b>v1b</b>(93%, 40.2s). "
    "스킬 적용으로 소요 시간 <b>43% 단축(68.3s->38.6s)</b> 및 비용 <b>16% 절감</b>. 단, 95% 신뢰구간(CI) 막대가 0을 걸치면 <b>\"차이를 확신할 수 없다\"</b>고 정직하게 판독해야 한다."
)
story.append(Paragraph(maturity_text, body_style))

# --- Section 6: Mobile PHY SW Group Roadmap ---
story.append(Paragraph("6. 모바일 통신 물리계층(PHY) SW 그룹 2nd Brain & Eval 적용 청사진", h2_style))

phy_table_data = [
    [Paragraph("계층", table_header_style), Paragraph("second-brain-eval-kit 아키텍처", table_header_style), Paragraph("모바일 PHY / 임베디드 C/C++ SW 적용 모델", table_header_style)],
    [
        Paragraph("<b>Code Graph</b>", table_cell_bold),
        Paragraph("query.mjs: TS AST + complete/truncated/partial 라벨", table_cell_style),
        Paragraph("ARM Clang AST 기반 <b>MMIO 레지스터 맵, 비트필드, ISR 벡터, 3GPP FSM</b> 심볼 링킹 + 함수 포인터 테이블 구간 <b>partial</b> 라벨 자동 부여", table_cell_style)
    ],
    [
        Paragraph("<b>Code Memory</b>", table_cell_bold),
        Paragraph("why.mjs: SQLite FTS5 BM25(3.0, 1.0) + RRF + 후보 1~3개 규칙", table_cell_style),
        Paragraph("<b>3GPP 릴리즈 변경점, 실리콘 에라타(Silicon Errata), 과거 IODT 필드 이슈</b>를 BM25+RRF로 인덱싱하여 10us 딜레이 사유(Why) 즉시 복원", table_cell_style)
    ],
    [
        Paragraph("<b>Firmware Eval</b>", table_cell_bold),
        Paragraph("checks.py + isolation.py (4대 차단) + pass^3 기준", table_cell_style),
        Paragraph("<b>4대 무균 샌드박스</b> + <b>invalid/safety_violation/fail</b> 분리 채점 + 레지스터 파급 분석 시 <b>pass^3 &amp; Recall&gt;=0.9/Prec&gt;=0.8</b> CI 게이트 강제", table_cell_style)
    ]
]
phy_table = Table(phy_table_data, colWidths=[26 * mm, 64 * mm, 84 * mm])
phy_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("PADDING", (0, 0), (-1, -1), 4),
]))
story.append(phy_table)
story.append(Spacer(1, 3 * mm))

# --- Section 7: Philosophical Epilogue ---
story.append(Paragraph("7. 결론 및 엔지니어 철학: 에이전트 시대, 인간의 주도권 (Slide #55)", h2_style))
epilogue_text = (
    "<i>\"에이전트를 돌리느라 24시간 쉬지 못하고 건강과 가족을 해치는 것은 도구의 본질을 전도시키는 것입니다. "
    "<b>에이전트에게 주도권을 뺏기지 마세요.</b> 나의 1번 가치(가족, 건강, 엔지니어링의 본질)를 확고히 세우고, "
    "에이전트는 나를 그 가치로 데려다주는 강력한 지렛대로 부려야 합니다.\"</i> — <b>설계와 전략은 인간 테크리드가 쥐고, 구현과 검증은 시스템 하네스(2nd Brain + Eval CI)에 위임하라.</b>"
)
story.append(Paragraph(epilogue_text, callout_style))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Successfully generated PaperPilot Executive Whitepaper: {pdf_path}")
