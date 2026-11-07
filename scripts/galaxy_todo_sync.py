#!/usr/bin/env python3
"""
Galaxy To-Do Sync: Google Tasks & Google Calendar Integration
=============================================================
Manages daily checklist tasks with Google Tasks API and optional time reminders
via Google Calendar API for sync with Samsung Calendar / Galaxy phone.
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scope definitions: Tasks and Calendar
SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/calendar.events",
]

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = Path.home() / ".google_todo_sync"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"


def get_credentials() -> Credentials:
    """Load or authenticate OAuth2 credentials."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    creds = None

    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"[WARN] Failed to load existing token: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
                return creds
            except Exception as e:
                print(f"[WARN] Failed to refresh token: {e}")

        if not CREDENTIALS_FILE.exists():
            print("\n" + "=" * 65)
            print("❌ [OAuth 인증 오류] credentials.json 파일을 찾을 수 없습니다!")
            print(f"👉 파일 위치: {CREDENTIALS_FILE}")
            print("\n[발급 및 배치 방법]")
            print("1. Google Cloud Console (https://console.cloud.google.com/) 접속")
            print("2. 'Google Tasks API' 및 'Google Calendar API' 활성화")
            print("3. '사용자 인증 정보' -> 'OAuth 클라이언트 ID 만들기'")
            print("   (애플리케이션 유형: '데스크톱 앱' 또는 'Desktop App')")
            print(f"4. 다운로드한 JSON 파일을 다음 경로에 저장해주세요:")
            print(f"   {CREDENTIALS_FILE}")
            print("=" * 65 + "\n")
            sys.exit(1)

        print("\n🌐 브라우저를 열어 Google 계정 1회 인증을 진행합니다...")
        print("💡 고정 포트 8088에서 인증 리스너를 시작합니다.")
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(host="localhost", port=8088, open_browser=True)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print(f"✅ 인증 성공! 토큰이 저장되었습니다: {TOKEN_FILE}\n")

    return creds


def get_tasks_service(creds: Credentials):
    return build("tasks", "v1", credentials=creds)


def get_calendar_service(creds: Credentials):
    return build("calendar", "v3", credentials=creds)


def list_today_tasks():
    """List open tasks in the primary tasklist."""
    creds = get_credentials()
    service = get_tasks_service(creds)
    try:
        results = service.tasks().list(tasklist="@default", showCompleted=False).execute()
        items = results.get("items", [])
        if not items:
            print("📋 현재 등록된 미완료 할 일이 없습니다.")
            return

        print(f"📋 [Google Tasks 목록] 총 {len(items)}개 미완료:")
        for idx, task in enumerate(items, 1):
            title = task.get("title", "제목 없음")
            notes = task.get("notes", "")
            due = task.get("due", "")
            due_str = f" (마감: {due[:10]})" if due else ""
            print(f"  {idx}. [ ] {title}{due_str}")
            if notes:
                print(f"      ㄴ 📝 {notes}")
    except HttpError as err:
        print(f"❌ Tasks 조회 오류: {err}")


def add_task(title: str, notes: Optional[str] = None, due_time: Optional[str] = None, add_calendar_alarm: bool = False):
    """
    Add a task to Google Tasks, and optionally schedule a Calendar event for phone alarm.
    due_time format: YYYY-MM-DDTHH:MM:SS (ISO) or HH:MM (defaults to today)
    """
    creds = get_credentials()
    tasks_svc = get_tasks_service(creds)

    task_body: Dict[str, Any] = {"title": title}
    if notes:
        task_body["notes"] = notes

    dt_target = None
    if due_time:
        today = datetime.date.today()
        if len(due_time) == 5 and ":" in due_time:  # HH:MM format
            h, m = map(int, due_time.split(":"))
            dt_target = datetime.datetime.combine(today, datetime.time(h, m))
        else:
            try:
                dt_target = datetime.datetime.fromisoformat(due_time)
            except Exception:
                pass

        if dt_target:
            # Google Tasks due date in RFC3339 format (UTC)
            task_body["due"] = dt_target.astimezone(datetime.timezone.utc).isoformat()

    try:
        result = tasks_svc.tasks().insert(tasklist="@default", body=task_body).execute()
        print(f"✅ [Google Tasks 등록 완료]")
        print(f"   - 할 일: {result.get('title')}")
        if notes:
            print(f"   - 메모: {notes}")
        if dt_target:
            print(f"   - 시간: {dt_target.strftime('%Y-%m-%d %H:%M')}")
        print(f"   - 상태: Galaxy 폰 Google Tasks 및 삼성 캘린더 동기화 대기 중")

        if add_calendar_alarm and dt_target:
            cal_svc = get_calendar_service(creds)
            end_dt = dt_target + datetime.timedelta(minutes=30)
            event_body = {
                "summary": f"[To-Do] {title}",
                "description": notes or "Antigravity에서 등록된 할 일 리마인더",
                "start": {"dateTime": dt_target.isoformat(), "timeZone": "Asia/Seoul"},
                "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Seoul"},
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 10},
                        {"method": "popup", "minutes": 0},
                    ],
                },
            }
            cal_event = cal_svc.events().insert(calendarId="primary", body=event_body).execute()
            print(f"⏰ [Google Calendar 알림 등록 완료]")
            print(f"   - 캘린더 이벤트: {cal_event.get('summary')} (10분 전/정각 스마트폰 팝업 알림)")

    except HttpError as err:
        print(f"❌ 작업 등록 실패: {err}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Galaxy To-Do Sync CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    subparsers.add_parser("list", help="오늘의 미완료 할 일 목록 조회")

    # Add command
    add_p = subparsers.add_parser("add", help="할 일 등록")
    add_p.add_argument("title", help="할 일 제목")
    add_p.add_argument("--notes", "-n", help="상세 메모")
    add_p.add_argument("--time", "-t", help="마감 또는 실행 시간 (예: 15:30 또는 2026-11-08T15:30:00)")
    add_p.add_argument("--alarm", "-a", action="store_true", help="스마트폰 캘린더 팝업 알림 동시 등록")

    # Auth check command
    subparsers.add_parser("auth", help="OAuth 인증 테스트 및 토큰 생성")

    args = parser.parse_args()

    if args.command == "list":
        list_today_tasks()
    elif args.command == "add":
        add_task(args.title, notes=args.notes, due_time=args.time, add_calendar_alarm=args.alarm)
    elif args.command == "auth":
        get_credentials()
        print("✅ 인증 및 토큰 검증이 완료되었습니다.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

