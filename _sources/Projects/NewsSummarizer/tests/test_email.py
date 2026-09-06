import os
import sys
from unittest.mock import MagicMock, patch
from email.message import EmailMessage

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

def test_generate_html_email_output():
    """generate_html_email 함수가 680px 너비의 반응형 HTML 및 각 섹션 카드를 올바르게 생성하는지 검증"""
    date_str = "2026년 9월 6일"
    exec_summary = "### 🚀 오늘 주목해야 할 핵심 혁신 (Key Innovations)\n- 혁신 내용\n\n### ⚠️ 핵심 리스크 및 과제 (Core Risks & Trade-offs)\n- 리스크 내용"
    github_trending = "### 1위. [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) (★ 39,400)\n- **🎯 한 줄 정의**: 오픈소스 개인 AI"
    categories = [
        {
            "name": "Group 2nd Brain & Enterprise Agent Architecture",
            "summary": "사내 지식 관리 트렌드",
            "articles": [{"title": "기사 1", "link": "https://example.com/1"}]
        }
    ]
    form_url = "https://example.com/form"

    html = main.generate_html_email(date_str, exec_summary, github_trending, categories, form_url)

    assert "<!DOCTYPE html>" in html
    assert "DAILY INTELLIGENCE & KNOWLEDGE BRIEFING" in html or "DAILY INTELLIGENCE &amp; KNOWLEDGE BRIEFING" in html
    assert "2026년 9월 6일" in html
    assert "Section 1: Executive Summary" in html
    assert "Section 2: 오늘의 GitHub 트렌드 큐레이션" in html or "Section 2: GitHub Trending" in html
    assert "Section 3: 관심 분야별 심층 뉴스" in html
    assert "tinyhumansai/openhuman" in html
    assert "Group 2nd Brain" in html
    assert "https://example.com/form" in html
    assert "max-width:680px" in html

def test_send_email_multipart_construction(mocker):
    """send_email 호출 시 plain text와 HTML alternative가 모두 첨부되는지 검증"""
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL")
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    mocker.patch("main.EMAIL_SENDER", "test_sender@gmail.com")
    mocker.patch("main.EMAIL_PASSWORD", "app_password_1234")
    mocker.patch("main.EMAIL_RECEIVER", "receiver1@gmail.com, receiver2@gmail.com")
    mocker.patch("main.get_additional_subscribers", return_value=["receiver3@gmail.com"])

    subject = "[테스트] 3단계 브리핑 발송"
    plain_content = "플레인 텍스트 본문"
    html_content = "<p>HTML 본문</p>"

    main.send_email(subject, plain_content, html_content=html_content)

    # SMTP login 및 send_message 호출 검증
    mock_smtp_instance.login.assert_called_once_with("test_sender@gmail.com", "app_password_1234")
    mock_smtp_instance.send_message.assert_called_once()

    sent_msg = mock_smtp_instance.send_message.call_args[0][0]
    assert sent_msg["Subject"] == subject
    assert sent_msg["From"] == "test_sender@gmail.com"
    assert sent_msg["To"] == "test_sender@gmail.com"
    
    # Bcc에 기본 수신자 및 추가 구독자가 모두 포함되어 있는지 확인
    bcc = sent_msg["Bcc"]
    assert "receiver1@gmail.com" in bcc
    assert "receiver2@gmail.com" in bcc
    assert "receiver3@gmail.com" in bcc

    # Multipart 검증 (플레인 텍스트와 HTML 본문 모두 존재하는지)
    body_payloads = [part.get_content_type() for part in sent_msg.walk()]
    assert "text/plain" in body_payloads
    assert "text/html" in body_payloads

def test_send_email_skips_when_credentials_missing(mocker):
    """이메일 설정(발신자나 비밀번호)이 없을 때 전송을 안전하게 건너뛰는지 검증"""
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL")
    mocker.patch("main.EMAIL_SENDER", "your_email@gmail.com")
    mocker.patch("main.EMAIL_PASSWORD", "")

    main.send_email("테스트 제목", "내용")
    mock_smtp_class.assert_not_called()

def test_send_email_handles_smtp_exception(mocker):
    """SMTP 연결 중 예외 발생 시 프로그램이 비정상 종료되지 않고 에러를 안전하게 로깅하는지 검증"""
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL", side_effect=Exception("SMTP Connection Error"))
    mocker.patch("main.EMAIL_SENDER", "test@gmail.com")
    mocker.patch("main.EMAIL_PASSWORD", "pwd")
    mocker.patch("main.EMAIL_RECEIVER", "rec@gmail.com")

    # 예외가 발생해도 외부로 raise되지 않아야 함
    main.send_email("제목", "내용", html_content="<p>내용</p>")
    mock_smtp_class.assert_called_once()

def test_get_additional_subscribers_regex(mocker):
    """CSV 데이터로부터 이메일 주소를 정규식으로 정확히 추출하고 중복을 제거하는지 검증"""
    csv_mock_content = "Name,Email,Date\n홍길동,hong@test.com,2026-09-01\n이순신,lee@test.com,2026-09-02\n중복,hong@test.com,2026-09-03"
    
    mocker.patch("main.SUBSCRIBERS_CSV_URL", "https://example.com/subscribers.csv")
    
    mock_resp = MagicMock()
    mock_resp.read.return_value = csv_mock_content.encode('utf-8')
    mock_resp.__enter__.return_value = mock_resp
    mocker.patch("urllib.request.urlopen", return_value=mock_resp)


    emails = main.get_additional_subscribers()
    assert len(emails) == 2
    assert "hong@test.com" in emails
    assert "lee@test.com" in emails
