---
name: galaxy-todo-sync
description: Manage and sync daily to-do checklists and time-based reminders to Google Tasks and Samsung Calendar on Galaxy phones. Trigger this skill whenever the user asks to add, list, or schedule daily tasks (e.g. "오늘 할 일 등록해줘", "투두 추가해줘", "할 일 목록 보여줘", "몇 시에 알림 걸어줘", "To-Do 동기화").
---

# Galaxy To-Do Sync Skill

이 스킬은 사용자가 PC(Antigravity)에서 작성한 할 일(To-Do) 목록을 `kiho.kil@gmail.com`의 **Google Tasks** 및 **Google Calendar**에 동기화하여, **Galaxy 스마트폰(삼성 캘린더 / Google Tasks 위젯 및 알림음)**에서 실시간으로 체크리스트를 확인하고 관리할 수 있도록 지원합니다.

## 실행 도구 위치
- 스크립트 경로: `c:\Users\kihok\내 드라이브\MyWiki\scripts\galaxy_todo_sync.py`
- 토큰 및 인증 파일 위치: `C:\Users\kihok\.google_todo_sync\`

## 사용 가능한 명령어 및 패턴

### 1. 할 일 목록 조회
```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\galaxy_todo_sync.py" list
```

### 2. 일반 할 일 등록 (체크리스트)
```powershell
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\galaxy_todo_sync.py" add "할 일 제목" --notes "세부 내용"
```

### 3. 특정 시간 마감 및 스마트폰 캘린더 팝업 알림 동시 등록
시간이 지정된 작업은 `--alarm` 플래그를 붙여 Google Calendar 이벤트로도 동시 등록되어, Galaxy 폰에서 10분 전 및 정각에 강력한 팝업 알림이 울립니다.
```powershell
# 오늘 오후 3시 30분 알림
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\galaxy_todo_sync.py" add "회의 자료 검토" --time "15:30" --alarm --notes "1층 회의실"

# 특정 날짜 및 시간
python "c:\Users\kihok\내 드라이브\MyWiki\scripts\galaxy_todo_sync.py" add "보고서 제출" --time "2026-11-09T18:00:00" --alarm
```

## 에이전트 행동 지침
- 사용자가 "오늘 할 일 3가지 등록해줘: 1. ... 2. ... 3. ..."라고 요청하면, 목록을 파악하여 각각 `add` 명령어로 즉시 등록합니다.
- 알림 시간(예: "오후 2시에 알려줘")이 언급된 경우 `--time`과 `--alarm` 옵션을 함께 전달합니다.
- 등록 완료 후 등록된 항목과 Galaxy 폰에서 체크박스로 확인하는 방법을 사용자에게 간결하게 브리핑합니다.
