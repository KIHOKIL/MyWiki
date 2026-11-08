---
name: doc-visualizer-suite
description: Comprehensive document & visual presentation suite for Antigravity and Obsidian 2nd Brain. Generates Presenton-style PPTX decks, Bento single-file HTML slides, PaperPilot executive PDF whitepapers, and interactive dark-theme Wiki reports. Trigger when the user asks to create presentations, slides, PDFs, or format documents ("PPT 만들어줘", "슬라이드 제작", "PDF 백서 생성", "보고서 포맷팅", "문서 시각화").
---

# 🎨 Doc Visualizer Suite (2nd Brain 문서 시각화 스위트)

사용자의 명시적 선호와 실전 벤치마킹을 통해 확정된 **4대 문서 포맷 빌더 파이프라인**입니다.

## 🏆 확정된 포맷별 표준 빌더 및 역할 분담

| 포맷 | 채택된 표준 엔진 | 주요 출력물 및 특징 | 템플릿/스크립트 위치 |
| :--- | :--- | :--- | :--- |
| **PPTX** | **`Presenton` 스타일** | • Gamma/Canva형 다크 카드 레이아웃<br>• 상단 필 뱃지, 3단 요약 카드, 16:9 와이드<br>• 실제 편집 가능한 네이티브 텍스트/도형 | `scripts/build_presenton_deck.py` |
| **HTML (슬라이드)** | **`Bento` 스타일** | • 단일 HTML 오프라인 프레젠테이션<br>• **키보드 방향키(← / →)**로 넘기는 발표 모드<br>• 깔끔한 모던 미니멀 UI 및 반응형 카드 | `scripts/build_bento_slides.py` |
| **HTML (리포트)** | **`MyWiki` 네이티브** | • 기술 블로그 / 심층 위키 아티클<br>• 좌측 고정 목차(ScrollSpy), 인터랙티브 탭 | `lecture-html-curator` 스킬 연계 |
| **PDF** | **`PaperPilot` 스타일** | • A4 규격 엔터프라이즈 테크니컬 백서<br>• 한국어 벡터 폰트(맑은 고딕), 보안 워터마크<br>• 2-Pass 페이지 번호(Page X of Y), 정밀 표/차트 | `scripts/build_paperpilot_pdf.py` |

---

## 🛠️ 스크립트 실행 및 자동 생성 규칙

### 1. Presenton 스타일 파워포인트 (.pptx) 생성
```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\build_presenton_deck.py" --input <노트경로.md> --output <출력.pptx>
```
* 규칙:
  - 16:9 와이드스크린 (`13.333 x 7.5` 인치) 고정.
  - 배경색 `#0f1219`, 카드 배경 `#1a1f2e`, 테두리 `#2d3750`.
  - 핵심 키워드는 시안(`#38bdf8`), 에메랄드(`#34d399`), 퍼플(`#a855f7`) 강조.

### 2. Bento 스타일 단일 HTML 슬라이드 생성
```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\build_bento_slides.py" --input <노트경로.md> --output <출력.html>
```
* 규칙:
  - 외부 의존성(CDN) 없는 순수 Standalone HTML + CSS + JS.
  - 슬라이드 컨테이너 1100x620px 센터 정렬, `keydown` 리스너로 화살표 및 스페이스바 제어.

### 3. PaperPilot 스타일 최고급 PDF 백서 생성
```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\build_paperpilot_pdf.py" --input <노트경로.md> --output <출력.pdf>
```
* 규칙:
  - ReportLab `NumberedCanvas` 활용하여 상단 헤더선 및 하단 페이지 번호 통일.
  - Windows 시스템 맑은 고딕(`malgun.ttf`, `malgunbd.ttf`) 등록으로 한글 깨짐 0%.
  - 요약 박스(Executive Summary), 2열 구조화 표, 차트 이미지 결합.

---

## 💡 에이전트 행동 지침
- 사용자가 *"이 내용을 PPT로 만들어줘"*라고 하면 ➔ **Presenton 스타일 PPTX**를 기본으로 생성합니다.
- 사용자가 *"가볍게 브라우저로 발표할 슬라이드 만들어줘"*라고 하면 ➔ **Bento HTML**을 생성합니다.
- 사용자가 *"출력하거나 이메일로 첨부할 정식 보고서/PDF 백서로 만들어줘"*라고 하면 ➔ **PaperPilot PDF**를 생성합니다.
- 사용자가 *"위키 정리글 형태로 만들어줘"*라고 하면 ➔ **MyWiki 네이티브 다크테마 HTML 리포트**를 생성합니다.
