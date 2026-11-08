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

# 2. Page Number Canvas Class (Watermark & Footer)
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
        self.drawString(20 * mm, 285 * mm, "CONFIDENTIAL · 2nd Brain & AI Agent Evaluation Report")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(20 * mm, 282 * mm, 190 * mm, 282 * mm)

        # Bottom Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(190 * mm, 12 * mm, page_str)
        self.drawString(20 * mm, 12 * mm, "Generated via PaperPilot Rust/MCP Specification Standard")
        self.line(20 * mm, 16 * mm, 190 * mm, 16 * mm)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=22 * mm,
    bottomMargin=22 * mm,
)

# 3. Styles
styles = getSampleStyleSheet()

h1_style = ParagraphStyle(
    "CustomH1",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=18,
    leading=24,
    textColor=colors.HexColor("#0f172a"),
    spaceAfter=6,
)

h2_style = ParagraphStyle(
    "CustomH2",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=13,
    leading=18,
    textColor=colors.HexColor("#1e293b"),
    spaceBefore=10,
    spaceAfter=4,
)

body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontName=body_font,
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor("#334155"),
    spaceAfter=6,
)

badge_style = ParagraphStyle(
    "BadgeStyle",
    parent=styles["Normal"],
    fontName=title_font,
    fontSize=8,
    leading=10,
    textColor=colors.HexColor("#2563eb"),
)

story = []

# Title & Metadata Banner
badge_text = "<font color='#2563eb'><b>[ EXECUTIVE TECH WHITEPAPER · METADATA SANITIZED ]</b></font>"
story.append(Paragraph(badge_text, badge_style))
story.append(Spacer(1, 4 * mm))

title_text = "AI 에이전트를 위한 2nd Brain과 Eval 프레임워크 아키텍처"
story.append(Paragraph(title_text, h1_style))

meta_text = "<b>작성:</b> Mobile PHY SW 그룹 / 2nd Brain 팀 &nbsp;|&nbsp; <b>출처:</b> Meta 8년차 시니어 엔지니어 세미나 전수 분석"
story.append(Paragraph(meta_text, body_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=5 * mm))

# Executive Summary Box
summary_html = (
    "<b>[요약: AI 코딩의 진짜 병목과 하네스 패러다임]</b><br/>"
    "AI 에이전트 도입 이후 코드 작성 속도는 수배 빨라졌으나, 대형 PR의 범람으로 인해 "
    "<b>'검증(Verification)과 코드 이해(Context)'</b>가 새로운 조직적 병목으로 부상했습니다. "
    "에이전트에게 매번 프롬프트를 다듬어 설명하는 것은 시스템의 실패이며, "
    "<b>코드베이스 지도(Code Graph)와 설계 맥락(Code Memory)을 먹여주는 2nd Brain</b> 및 "
    "<b>품질을 숫자로 증명하는 Eval 파이프라인</b>의 결합이 필수적입니다."
)
summary_table = Table([[Paragraph(summary_html, body_style)]], colWidths=[170 * mm])
summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BORDER", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ])
)
story.append(summary_table)
story.append(Spacer(1, 6 * mm))

# Section 1: 2nd Brain Two Pillars
story.append(Paragraph("1. Developer's 2nd Brain: 두 개의 핵심 기둥", h2_style))
p1_text = (
    "새로운 세션이 열릴 때마다 AI에게 프로젝트 아키텍처를 사람이 설명하는 것은 낭비입니다. "
    "개발자용 2nd Brain은 컴파일러가 생성하는 <b>정밀한 그래프(Codebase Graph)</b>와 "
    "코드만으로는 유추하기 어려운 <b>의사결정 역사(Code Memory)</b>가 합쳐져 완성됩니다."
)
story.append(Paragraph(p1_text, body_style))

# Two Column Table for Pillars
col1_html = "<b>🕸️ 기둥 1: Codebase Graph</b><br/>• 컴파일러 AST 기반 정밀 심볼 링킹<br/>• 단순 grep/벡터 RAG의 환각 원천 차단<br/>• k-Hop 전파를 통한 파급 반경(Blast Radius) 자동 계산"
col2_html = "<b>🧠 기둥 2: Code Memory</b><br/>• '왜(Why) 이렇게 구현했는가?'에 대한 암묵지<br/>• 아키텍처 결정(ADR) 및 과거 장애 회고록<br/>• 신입 시니어 온보딩처럼 AI에게 프로젝트 맥락 자동 제공"
pillar_table = Table([[Paragraph(col1_html, body_style), Paragraph(col2_html, body_style)]], colWidths=[83 * mm, 83 * mm])
pillar_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#f8fafc")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#f8fafc")),
        ("BORDER", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])
)
story.append(pillar_table)
story.append(Spacer(1, 5 * mm))

# Section 2: Eval-Driven Development
story.append(Paragraph("2. Eval: AI 에이전트 스킬 품질의 정량적 증명", h2_style))
p2_text = (
    "단위 테스트 없이 코드를 배포하지 않듯, <b>통계적 검증(Eval) 없는 에이전트는 프로덕션에 쓸 수 없습니다.</b> "
    "에이전트가 내놓은 답이 기존 대비 얼마나 나아졌는지, 다른 곳을 망가뜨리지 않았는지 CI 상에서 숫자로 판정해야 합니다."
)
story.append(Paragraph(p2_text, body_style))

# Evaluation Criteria Table
eval_data = [
    [Paragraph("<b>평가 지표 (Dimension)</b>", body_style), Paragraph("<b>검증 방식 및 기준</b>", body_style), Paragraph("<b>실무 적용점 (PHY SW)</b>", body_style)],
    [Paragraph("<b>Trigger Accuracy</b>", body_style), Paragraph("스킬이 필요한 순간에만 정확히 발동하는가?", body_style), Paragraph("W1C 레지스터/ISR 수정 시 전담 Auditor 자동 소환", body_style)],
    [Paragraph("<b>Quality Gain</b>", body_style), Paragraph("기존 대비 성능과 결함 검출율이 향상되었는가?", body_style), Paragraph("5-Layer 불변조건 위반 탐지율 95% 이상 달성", body_style)],
    [Paragraph("<b>Zero Regression</b>", body_style), Paragraph("새로운 규칙이 정상 코드를 오탐(False Positive)으로 막지 않는가?", body_style), Paragraph("반증(Disproving) 패스를 통해 오탐 0% 달성", body_style)],
]
eval_table = Table(eval_data, colWidths=[38 * mm, 66 * mm, 66 * mm])
eval_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ])
)
story.append(eval_table)
story.append(Spacer(1, 5 * mm))

# Section 3: Visual Chart Integration
story.append(Paragraph("3. 2nd Brain 오피스/문서화 도구 벤치마크 지표", h2_style))
chart_path = r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval\assets\benchmark_comparison_chart.png"
if os.path.exists(chart_path):
    story.append(Image(chart_path, width=165 * mm, height=75 * mm))

# Build Document
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PaperPilot-standard Executive Whitepaper successfully built: {pdf_path}")
