import os
import re
import cv2
import numpy as np
import yt_dlp
from PIL import Image as PILImage
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

VIDEO_URL = "https://youtu.be/AyKq4zFfrlc"
BASE_DIR = os.path.abspath(r"_sources\Study\AI-Lectures\실밸개발자\20261108_2ndBrain_and_Eval")
SLIDES_DIR = os.path.join(BASE_DIR, "assets", "captured_slides")
VTT_PATH = os.path.join(BASE_DIR, "yt_sub_AyKq4zFfrlc.ko.vtt")
TEMP_VIDEO = os.path.join(BASE_DIR, "temp_lecture_720p.mp4")
OUT_PDF = os.path.join(BASE_DIR, "09_Instructor_Original_Slides_Book.pdf")
OUT_PPTX = os.path.join(BASE_DIR, "10_Instructor_Original_Slides_Deck.pptx")

os.makedirs(SLIDES_DIR, exist_ok=True)

def save_frame_unicode(frame, fpath, quality=92):
    """Safely saves an OpenCV BGR frame to a Windows path containing Korean characters."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    PILImage.fromarray(rgb).save(fpath, format="JPEG", quality=quality)

# 1. Parse VTT subtitles into (sec, ts, text) list
def parse_vtt_to_timeline(vtt_path):
    if not os.path.exists(vtt_path):
        return []
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2})\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n([\s\S]*?)(?=\n\n|\Z)')
    timeline = []
    last_txt = ""
    for m in pattern.finditer(content):
        ts, txt = m.groups()
        txt = re.sub(r'<[^>]+>', '', txt).replace('\n', ' ').strip()
        txt = re.sub(r'align:[^\s]+|position:[^\s]+', '', txt).strip()
        if txt and txt != last_txt:
            sec = int(ts[:2]) * 3600 + int(ts[3:5]) * 60 + int(ts[6:8])
            timeline.append((sec, ts, txt))
            last_txt = txt
    return timeline

def get_transcript_window(timeline, start_sec, end_sec):
    snippets = []
    w_start = max(0, start_sec - 4)
    w_end = max(start_sec + 25, min(end_sec, start_sec + 45))
    for sec, ts, txt in timeline:
        if w_start <= sec <= w_end:
            if not snippets or txt not in snippets[-1]:
                snippets.append(txt)
    joined = " ".join(snippets)
    return joined[:420] + ("..." if len(joined) > 420 else "")

# 2. Compute perceptual difference hash (dHash) on slide region (masking out webcam area)
def compute_slide_dhash(frame, hash_size=16):
    h, w, _ = frame.shape
    roi = frame[int(h*0.05):int(h*0.92), int(w*0.03):int(w*0.76)]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
    diff = resized[:, 1:] > resized[:, :-1]
    return diff.flatten()

def hamming_dist(h1, h2):
    return np.count_nonzero(h1 != h2)

def is_slide_frame(frame):
    h, w, _ = frame.shape
    roi = frame[int(h*0.08):int(h*0.88), int(w*0.05):int(w*0.75)]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    gx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    flat_pixels = np.mean(mag < 8.0)
    sharp_edges = np.mean(mag > 60.0)
    return flat_pixels > 0.54 and sharp_edges > 0.008

# 3. Download lightweight 720p stream
if not os.path.exists(TEMP_VIDEO):
    print("Downloading lightweight 720p lecture stream...")
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]/best[height<=720]',
        'outtmpl': TEMP_VIDEO,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VIDEO_URL])
    print("Download complete!")

# 4. Scan video and group consecutive similar frames so we capture the COMPLETED slide state
print("Scanning lecture frames and grouping slide build animations...")
timeline = parse_vtt_to_timeline(VTT_PATH)
cap = cv2.VideoCapture(TEMP_VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_sec = int(total_frames / fps)

for old_f in os.listdir(SLIDES_DIR):
    if old_f.endswith(".jpg"):
        os.remove(os.path.join(SLIDES_DIR, old_f))

raw_candidates = []
step_sec = 10

for sec in range(90, duration_sec - 50, step_sec):
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    ret, frame = cap.read()
    if not ret or frame is None:
        continue
    if not is_slide_frame(frame):
        continue
    cur_hash = compute_slide_dhash(frame)
    raw_candidates.append((sec, frame, cur_hash))

cap.release()

# Group candidates into distinct slides (keep the LAST frame of each slide segment so all bullet builds are visible!)
distinct_groups = []
for sec, frame, cur_hash in raw_candidates:
    if not distinct_groups:
        distinct_groups.append({"start_sec": sec, "end_sec": sec, "frame": frame, "hash": cur_hash})
    else:
        prev = distinct_groups[-1]
        dist = hamming_dist(cur_hash, prev["hash"])
        if dist < 38:  # Same slide (or minor bullet addition): update end_sec & keep latest completed frame
            prev["end_sec"] = sec
            prev["frame"] = frame
            prev["hash"] = cur_hash
        else:
            # Check if this slide is a revisit of any earlier slide
            is_revisit = any(hamming_dist(cur_hash, g["hash"]) < 30 for g in distinct_groups[:-1])
            if not is_revisit:
                distinct_groups.append({"start_sec": sec, "end_sec": sec, "frame": frame, "hash": cur_hash})

captured_slides = []
for idx, g in enumerate(distinct_groups, start=1):
    sec = g["start_sec"]
    m, s = divmod(sec, 60)
    h_val, m = divmod(m, 60)
    ts_str = f"{h_val:02d}:{m:02d}:{s:02d}"
    fname = f"slide_{idx:02d}_{h_val:02d}h{m:02d}m{s:02d}s.jpg"
    fpath = os.path.join(SLIDES_DIR, fname)
    save_frame_unicode(g["frame"], fpath, quality=92)
    
    transcript_text = get_transcript_window(timeline, g["start_sec"], g["end_sec"])
    captured_slides.append({
        "idx": idx,
        "sec": sec,
        "ts_str": ts_str,
        "img_path": fpath,
        "fname": fname,
        "transcript": transcript_text
    })

print(f"Successfully saved {len(captured_slides)} completed instructor slides to {SLIDES_DIR}!")

# Remove temp video after confirming slides exist
if os.path.exists(TEMP_VIDEO) and len(captured_slides) > 0:
    try:
        os.remove(TEMP_VIDEO)
        print("Removed temporary video file.")
    except Exception:
        pass

# 5. Build Slidebook PDF (09_Instructor_Original_Slides_Book.pdf)
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

doc = SimpleDocTemplate(
    OUT_PDF,
    pagesize=A4,
    leftMargin=16 * mm,
    rightMargin=16 * mm,
    topMargin=16 * mm,
    bottomMargin=16 * mm,
)
styles = getSampleStyleSheet()
h1_s = ParagraphStyle("H1", parent=styles["Normal"], fontName=title_font, fontSize=16, leading=22, textColor=colors.HexColor("#0f172a"), spaceAfter=4)
sub_s = ParagraphStyle("Sub", parent=styles["Normal"], fontName=body_font, fontSize=9.5, leading=14, textColor=colors.HexColor("#475569"), spaceAfter=10)
slide_hdr_s = ParagraphStyle("SHdr", parent=styles["Normal"], fontName=title_font, fontSize=11, leading=15, textColor=colors.HexColor("#1e40af"), spaceAfter=4)
cap_s = ParagraphStyle("Cap", parent=styles["Normal"], fontName=body_font, fontSize=8.5, leading=13, textColor=colors.HexColor("#334155"))

story = []
story.append(Paragraph("메타 시니어 엔지니어 세미나: 강사 원본 슬라이드 캡처 북 (Slidebook)", h1_s))
story.append(Paragraph(f"원본 영상: {VIDEO_URL}  |  자동 장면 전환 감지(dHash + Lookahead Completion)로 추출된 {len(captured_slides)}장의 원본 슬라이드 및 발화 자막 매핑", sub_s))

for i, item in enumerate(captured_slides):
    story.append(Paragraph(f"Slide #{item['idx']:02d}  —  타임스탬프 [{item['ts_str']}]", slide_hdr_s))
    img_flow = RLImage(item["img_path"], width=175 * mm, height=98.4 * mm)
    story.append(img_flow)
    story.append(Spacer(1, 2 * mm))
    
    txt_clean = item["transcript"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    box_data = [[Paragraph(f"<b>[강사 발화 요약 · {item['ts_str']}]</b><br/>{txt_clean}", cap_s)]]
    t = Table(box_data, colWidths=[175 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 5 * mm))
    if (i + 1) % 2 == 0 and (i + 1) < len(captured_slides):
        story.append(PageBreak())

doc.build(story)
print(f"Generated Slidebook PDF: {OUT_PDF}")

# 6. Build Slidebook PPTX (10_Instructor_Original_Slides_Deck.pptx)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BG_DARK = RGBColor(9, 10, 15)
CARD_BG = RGBColor(18, 21, 31)
CARD_BORDER = RGBColor(36, 42, 58)
ACCENT_CYAN = RGBColor(56, 189, 248)
TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)

for item in captured_slides:
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    bg = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()

    # Header bar
    tb = sl.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.45))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = f"●  INSTRUCTOR ORIGINAL SLIDE #{item['idx']:02d}   |   TIMESTAMP [{item['ts_str']}]"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Original Slide Image (Left/Center Large: 9.2" x 5.175")
    sl.shapes.add_picture(item["img_path"], Inches(0.6), Inches(0.95), width=Inches(9.2))

    # Right Bento Transcript Note Card with Curved Top Accent Bar
    bx, by, bw, bh = Inches(10.0), Inches(0.95), Inches(2.8), Inches(5.175)
    accent_base = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
    accent_base.fill.solid()
    accent_base.fill.fore_color.rgb = ACCENT_CYAN
    accent_base.line.fill.background()
    accent_base.adjustments[0] = 12.0 / min(bw.pt, bh.pt)

    card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by + Pt(3.5), bw, bh - Pt(3.5))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.0)
    card.adjustments[0] = 12.0 / min(card.width.pt, card.height.pt)

    ntb = sl.shapes.add_textbox(Inches(10.22), Inches(1.2), Inches(2.36), Inches(4.7))
    ntf = ntb.text_frame
    ntf.word_wrap = True
    np1 = ntf.paragraphs[0]
    np1.text = f"🎙️ [{item['ts_str']}] 강사 발화"
    np1.font.size = Pt(12)
    np1.font.bold = True
    np1.font.color.rgb = TEXT_WHITE

    np2 = ntf.add_paragraph()
    np2.text = item["transcript"]
    np2.font.size = Pt(9.5)
    np2.font.color.rgb = TEXT_MUTED
    np2.space_before = Pt(8)

    notes_slide = sl.notes_slide
    notes_slide.notes_text_frame.text = f"[{item['ts_str']}] {item['transcript']}"

prs.save(OUT_PPTX)
print(f"Generated Slidebook PPTX: {OUT_PPTX}")
