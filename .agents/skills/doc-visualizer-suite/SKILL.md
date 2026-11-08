---
name: doc-visualizer-suite
description: Comprehensive document & visual presentation suite for Antigravity and Obsidian 2nd Brain. Generates Bento Grid PPTX decks (with concentric curved accent bars & COM visual QA), Presenton-style PPTX decks, Bento single-file HTML slides, PaperPilot executive PDF whitepapers, interactive dark-theme Wiki reports, and extracts original instructor slides from YouTube lecture videos into PDF/PPTX slidebooks. Trigger when the user asks to create presentations, slides, PDFs, format documents, or extract lecture slides ("PPT 만들어줘", "Bento PPT", "슬라이드 제작", "PDF 백서 생성", "보고서 포맷팅", "문서 시각화", "강사 슬라이드 캡처/추출").
---

# 🎨 Doc Visualizer Suite (2nd Brain 멀티포맷 문서 시각화 & 슬라이드 추출 스위트)

사용자의 명시적 선호와 실전 렌더링 검증(Visual Harmony QA)을 통해 확립된 **6대 표준 문서/슬라이드 빌더 파이프라인**입니다.

---

## 🏆 확정된 포맷별 표준 빌더 및 역할 분담

| 포맷 / 모드 | 채택된 표준 엔진 | 주요 출력물 및 핵심 디자인 특징 | 표준 스크립트 위치 |
| :--- | :--- | :--- | :--- |
| **1. PPTX (Bento Grid)** | **`Bento Grid` 네이티브 PPTX** *(기본 추천)* | • 애플/모던 웹 Bento 모듈러 그리드 레이아웃 (`16:9`)<br>• **동심원 이중 라운드 박스 기법**으로 둥근 모서리를 따라 완벽히 휘어지는 상단/좌측 네온 액센트 바 (`border-top` / `border-left` 재현)<br>• 깔끔한 도트 프리픽스 헤더 (`● PART X · TITLE`)<br>• **PowerPoint COM 이미지 렌더링 시각 검수 필수** | `scripts/build_bento_pptx.py` |
| **2. PPTX (Presenton)** | **`Presenton` 스타일 PPTX** | • Gamma/Canva형 딥 슬레이트 다크 카드 레이아웃<br>• 상단 필 뱃지, 3단 요약 카드, 벤치마크 차트 결합<br>• 실제 편집 가능한 네이티브 텍스트/도형 | `scripts/build_presenton_deck.py` |
| **3. HTML (슬라이드)** | **`Bento` 단일 파일 HTML** | • 외부 CDN 의존성 없는 순수 Standalone HTML 슬라이드<br>• **키보드 방향키(`←` / `→` / `Space`)** 발표 모드<br>• CSS Grid Bento 박스 + 상단/좌측 컬러 보더 스트라이프 | `04_Bento_Presentation.html` 템플릿 |
| **4. HTML (리포트)** | **`MyWiki` 다크 리포트** | • 한 페이지로 완독하는 심층 기술 블로그 / 위키 아티클<br>• 좌측 고정 목차(ScrollSpy), Mermaid.js 아키텍처 다이어그램, 원클릭 프롬프트 복사 | `lecture-html-curator` 연계 (`02_Lecture_Report_WikiSkill.html`) |
| **5. PDF (백서)** | **`PaperPilot` 스타일 PDF** | • A4 규격 엔터프라이즈 테크니컬 이그제큐티브 백서<br>• Windows `맑은 고딕`(`malgun.ttf`/`malgunbd.ttf`) 벡터 내장<br>• 2-Pass 페이지 번호(`Page X of Y`), 정밀 표/차트 | `scripts/build_paperpilot_pdf.py` |
| **6. YouTube 원본 슬라이드 추출** | **`CV Slide Extractor`** | • 강의 영상에서 강사가 직접 작성/띄운 원본 슬라이드만 자동 추출<br>• 토킹헤드 필터링 + 웹캠 PiP 마스킹 + 256-bit `dHash` 중복 제거 + Lookahead 애니메이션 완성본 캡처<br>• 고화질 원본 JPG 폴더 + **원본 슬라이드북 PDF & PPTX** 자동 생성 | `scripts/extract_lecture_slides.py` |

---

## 📐 핵심 아키텍처 및 구현 디테일 (필수 준수 규칙)

### 1. Bento Grid PPTX — 동심원 이중 라운드 박스 기법 (`scripts/build_bento_pptx.py`)

파워포인트(`python-pptx`)에서 둥근 사각형(`ROUNDED_RECTANGLE`) 내부에 직선 사각형(`RECTANGLE`)으로 상단 바를 그리면 **둥근 모서리와 직선이 충돌하여 조화가 깨지는 시각적 결함**이 발생합니다. 이를 해결하기 위해 반드시 **동심원 이중 라운드 사각형 마스킹(Concentric Rounded Rectangle Masking)** 기법을 사용합니다.

```python
BENTO_RADIUS_PT = 12.0       # 모든 Bento 카드의 절대 모서리 반경 (12pt = ~16px 통일)
STRIPE_THICKNESS_PT = 3.5    # 상단(top) 또는 좌측(left) 액센트 바 두께

def apply_corner_radius(shape, radius_pt=BENTO_RADIUS_PT):
    """카드 크기가 달라도 모든 카드의 모서리 곡률 반경(12pt)이 100% 동일하게 보이도록 역산"""
    min_dim_pt = min(shape.width.pt, shape.height.pt)
    if min_dim_pt > 0:
        shape.adjustments[0] = radius_pt / min_dim_pt
```

- **구현 원리 (`add_bento_box`):**
  1. **하단 베이스 도형 (`accent_base`):** `(x, y, w, h)` 위치에 `accent_color`로 채운 `ROUNDED_RECTANGLE`을 배치하고 `apply_corner_radius`를 적용합니다.
  2. **상단 본체 도형 (`card`):**
     - `accent_pos="top"`일 때: `(x, y + Pt(3.5), w, h - Pt(3.5))` 위치에 다크 배경(`#12151F`)의 `ROUNDED_RECTANGLE`을 덮어씌웁니다.
     - `accent_pos="left"`일 때: `(x + Pt(3.5), y, w - Pt(3.5), h)` 위치에 덮어씌웁니다.
  3. **주의사항 (`python-pptx` EMU 연산):** `Inches()`에서 `Pt()`를 뺀 결과는 순수 `int`(EMU)이므로 `(h - Pt(3.5)).pt`를 호출하면 `AttributeError`가 발생합니다. 반드시 생성된 `card.width.pt`, `card.height.pt` 속성을 사용해 `apply_corner_radius(card)`를 호출하세요.
- **슬라이드 헤더 규칙 (`add_clean_header`):**
  - 슬라이드 상단 헤더에는 캡슐/필(Pill) 도형을 쓰지 않고(하단 Bento 박스와 시각적 충돌 방지), 깔끔한 타이포그래피 도트 프리픽스(`●  PART 1 · OVERVIEW`)만 사용합니다.

---

### 2. 필수 시각 조화 검수 (Mandatory Visual Harmony QA via PowerPoint COM)

PPTX 파일을 생성하거나 수정한 직후에는 **반드시 실제 PowerPoint 렌더링 엔진으로 슬라이드 전체를 JPG 이미지로 추출한 뒤, 에이전트가 `read_file` 도구로 모든 슬라이드 이미지를 직접 눈으로 확인**해야 합니다.

```powershell
# 1. GoogleDriveFS 또는 이전 PowerPoint 프로세스 파일 잠금 해제
Stop-Process -Name "POWERPNT" -Force -ErrorAction SilentlyContinue

# 2. PowerPoint 스크립트 실행 후 슬라이드 전체를 JPG로 익스포트 (Format 17 = ppSaveAsJPG)
$deckPath = Resolve-Path "<생성된_PPTX_경로>"
$outDir = "<검수용_이미지_폴더_절대경로>"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
# 주의: $ppt.Visible = msoFalse 설정 시 일부 Office 환경에서 예외가 발생하므로 생략하고 Open의 WithWindow 인자($false)를 사용
$pres = $ppt.Presentations.Open($deckPath.Path, $true, $false, $false)
$pres.SaveAs($outDir, 17)
$pres.Close()
$ppt.Quit()
```

- **시각 검수 체크리스트 (`read_file`로 `슬라이드1.JPG` ~ `슬라이드N.JPG` 확인):**
  - [ ] 둥근 모서리와 액센트 바가 삐져나오거나 직선과 충돌하지 않고 매끄러운 초승달 곡선을 이루는가?
  - [ ] 카드 크기가 달라도 모든 Bento 박스의 모서리 곡률(`12pt`)이 균일한가?
  - [ ] 텍스트가 카드 하단 경계선 밖으로 넘치거나(Overflow) 차트/이미지와 겹치지 않는가?

---

### 3. YouTube 강사 원본 슬라이드 자동 추출 파이프라인 (`scripts/extract_lecture_slides.py`)

강사가 직접 작성한 장표가 화면에 나오는 세미나/강의 영상에서 **강사 얼굴(토킹헤드)을 걸러내고 완성된 원본 슬라이드만 고화질로 추출**하여 PDF 및 PPTX로 패키징합니다.

```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\extract_lecture_slides.py"
```

- **4단계 Computer Vision 파이프라인 핵심 로직:**
  1. **스트림 다운로드 (`yt_dlp`):** `bestvideo[height<=720][ext=mp4]` 포맷으로 빠르게 비디오 스트림 확보.
  2. **토킹헤드 vs 슬라이드 판별기 (`is_slide_frame`):**
     - 좌측 75% 영역(우측 하단 웹캠 PiP 제외)에 대해 Sobel 엣지 밀도(`edge_ratio < 0.16`)와 평탄 배경 픽셀 비율(`flat_ratio > 0.62`)을 계산하여 강사 단독 카메라 샷을 100% 배제.
  3. **웹캠 PiP 마스킹 + 256-bit `dHash` + Lookahead 완성본 캡처:**
     - 우측 웹캠 영역(가로 76% 이후)에서 강사가 손짓/고개를 움직여도 해시가 변하지 않도록 좌측 76% ROI만 크롭하여 16×16(`256-bit`) Difference Hash 계산 (`HAMMING_THRESHOLD = 14`).
     - **Lookahead Slide Completion:** 불릿 포인트가 한 줄씩 등장하는 애니메이션 슬라이드에서 첫 프레임이 아닌 **다음 슬라이드로 넘어가기 직전의 마지막 안정 프레임(`last_frame`)**을 채택하여 모든 텍스트가 다 뜬 완성본 장표만 저장.
  4. **유니코드 안전 저장 및 PDF/PPTX 패키징:**
     - Windows 한글 경로(`내 드라이브`, `실밸개발자` 등)에서 `cv2.imwrite`가 실패하는 문제를 방지하기 위해 반드시 `PIL.Image.fromarray(rgb).save(fpath, format="JPEG", quality=92)`로 저장.
     - 추출된 슬라이드와 타임스탬프 자막을 결합하여 **`09_Instructor_Original_Slides_Book.pdf`** (ReportLab A4 가로형 슬라이드북) 및 **`10_Instructor_Original_Slides_Deck.pptx`** (슬라이드 노트 영역에 해당 시간대 강사 설명 자막 자동 주입) 생성.

---

### 4. PaperPilot 스타일 최고급 PDF 백서 생성 (`scripts/build_paperpilot_pdf.py`)

```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\build_paperpilot_pdf.py"
```
- ReportLab `NumberedCanvas` 2-Pass 렌더링으로 상단 러닝 헤더 및 하단 `Page X of Y` 자동 표기.
- Windows 시스템 폰트(`C:\Windows\Fonts\malgun.ttf`, `malgunbd.ttf`) 등록으로 한글 깨짐 0%.
- Executive Summary 콜아웃 박스, 구조화 비교 테이블, 고해상도 벤치마크 차트 결합.

---

## 💡 에이전트 행동 지침 (Routing Rules)
- 사용자가 *"Bento 스타일로 PPT 만들어줘"* 또는 *"PPT 만들어줘"*라고 하면 ➔ **`scripts/build_bento_pptx.py` (동심원 곡선 액센트 바 + PowerPoint COM 시각 검수)** 및 **`scripts/build_presenton_deck.py`**를 생성합니다.
- 사용자가 *"가볍게 브라우저로 발표할 슬라이드 만들어줘"*라고 하면 ➔ **Bento 단일 파일 HTML (`04_Bento_Presentation.html`)**을 생성합니다.
- 사용자가 *"출력하거나 공유할 정식 보고서/PDF 백서로 만들어줘"*라고 하면 ➔ **PaperPilot PDF (`07_PaperPilot_Executive_Whitepaper.pdf`)**를 생성합니다.
- 사용자가 *"위키 정리글/대시보드 형태로 만들어줘"*라고 하면 ➔ **MyWiki 네이티브 다크테마 HTML 리포트 (`02_Lecture_Report_WikiSkill.html`)**를 생성합니다.
- 사용자가 *"강사가 화면에 띄운 원본 강의자료/장표를 캡처해서 뽑아줘"*라고 하면 ➔ **`scripts/extract_lecture_slides.py`**를 실행하여 고화질 슬라이드 이미지 세트 + 원본 슬라이드북 PDF(`09`) + 발표자 노트 포함 PPTX(`10`)를 생성합니다.
