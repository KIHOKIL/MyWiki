---
name: youtube-summarizer
description: YouTube 영상 URL을 받아 자막을 추출하고, 핵심 내용을 요약하여 옵시디언 위키 포맷의 마크다운 파일로 저장합니다. '유튜브 요약', 'youtube 요약' 등의 요청 시 트리거됩니다.
---

# YouTube Summarizer Skill

이 스킬은 YouTube URL을 입력받아 영상의 전체 자막(Transcript)을 추출하고, 이를 기반으로 구조화된 요약 노트를 생성하여 위키에 추가(Ingest)하는 작업을 수행합니다.

## Prerequisites
- 파이썬 환경에 `youtube-transcript-api` 패키지가 설치되어 있어야 합니다.
- 설치 여부를 모른다면 다음 명령어로 미리 설치하세요: `pip install youtube-transcript-api`

## Workflow

### 1. URL 확인 및 자막 추출
- 사용자가 제공한 YouTube URL에서 Video ID를 추출합니다. (예: `v=VIDEO_ID`)
- `run_command` 도구를 사용하여 임시 디렉토리에 파이썬 스크립트를 작성하고 실행하여 자막을 추출합니다. (또는 터미널에서 `-c` 로 직접 실행합니다.)
```bash
python -c "
from youtube_transcript_api import YouTubeTranscriptApi
import sys
try:
    transcript = YouTubeTranscriptApi.get_transcript('VIDEO_ID', languages=['ko', 'en'])
    print(' '.join([t['text'] for t in transcript]))
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
"
```
*(주의: `VIDEO_ID` 부분을 실제 ID로 치환하세요)*

### 2. 요약 및 인사이트 도출
- 추출된 자막 데이터를 바탕으로, 다음 내용을 포함하는 마크다운 요약본을 작성합니다:
  - 💡 **핵심 요약 (1~2줄)**
  - 📌 **주요 내용 (불릿 포인트 형식으로 구조화)**
  - 🎯 **인사이트 및 배울 점**

### 3. 마크다운 파일 생성 (Wiki Ingest)
- 요약된 내용을 사용자의 옵시디언 위키 경로(`_source/Study/AI-Lectures/` 등 적절한 폴더)에 마크다운 파일로 저장합니다.
- 반드시 `llm-wiki` 스킬의 규칙에 따라 필수 Frontmatter(`title`, `category`, `tags`, `sources`, `created`, `updated`)를 포함해야 합니다.

### 4. 완료 보고 및 후속 작업 연계
- 사용자에게 요약이 완료되었음을 알립니다.
- 만약 사용자가 후속으로 요약된 내용을 바탕으로 강의 자료나 슬라이드를 원할 경우, `presentation_slides` 스킬 등과 연계하여 다음 작업을 진행합니다.
