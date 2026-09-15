import os
import sys
from unittest.mock import MagicMock, patch
from email.message import EmailMessage

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.finance import main

def test_generate_html_email_output():
    date_str = "2026-09-06"
    report_md = "### 1. 🌐 Global Macro & Policy\n- 테스트 내용\n\n### 💡 Snowball Insight\n- 전략 제언"
    form_url = "https://example.com/form"

    html = main.generate_html_email(date_str, report_md, form_url)

    assert "<!DOCTYPE html>" in html
    assert "DAILY INTELLIGENCE & KNOWLEDGE BRIEFING" in html or "DAILY INTELLIGENCE &amp; KNOWLEDGE BRIEFING" in html
    assert "2026-09-06" in html
    assert "Money Snowball Macro Briefing" in html
    assert "📌 📊 Money Snowball Daily Macro Briefing" in html
    assert "Global Macro & Policy" in html
    assert "Snowball Insight" in html
    assert "https://example.com/form" in html
    assert "max-width:680px" in html

def test_send_email_multipart_construction(mocker):
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL")
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    mocker.patch("agents.finance.main.EMAIL_SENDER", "test_sender@gmail.com")
    mocker.patch("agents.finance.main.EMAIL_PASSWORD", "app_password_1234")
    mocker.patch("agents.finance.main.EMAIL_RECEIVER", "receiver1@gmail.com, receiver2@gmail.com")
    mocker.patch("agents.finance.main.get_additional_subscribers", return_value=["receiver3@gmail.com"])

    subject = "[Money Snowball] Daily Macro Briefing"
    plain_content = "플레인 텍스트 본문"
    html_content = "<p>HTML 본문</p>"

    main.send_email(subject, plain_content, html_content=html_content)

    mock_smtp_instance.login.assert_called_once_with("test_sender@gmail.com", "app_password_1234")
    mock_smtp_instance.send_message.assert_called_once()

    sent_msg = mock_smtp_instance.send_message.call_args[0][0]
    assert sent_msg["Subject"] == subject
    assert sent_msg["From"] == "test_sender@gmail.com"
    assert sent_msg["To"] == "test_sender@gmail.com"
    
    bcc = sent_msg["Bcc"]
    assert "receiver1@gmail.com" in bcc
    assert "receiver2@gmail.com" in bcc
    assert "receiver3@gmail.com" in bcc

    body_payloads = [part.get_content_type() for part in sent_msg.walk()]
    assert "text/plain" in body_payloads
    assert "text/html" in body_payloads

def test_send_email_skips_when_credentials_missing(mocker):
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL")
    mocker.patch("agents.finance.main.EMAIL_SENDER", "your_email@gmail.com")
    mocker.patch("agents.finance.main.EMAIL_PASSWORD", "")

    main.send_email("제목", "내용")
    mock_smtp_class.assert_not_called()

def test_send_email_handles_smtp_exception(mocker):
    mock_smtp_class = mocker.patch("smtplib.SMTP_SSL", side_effect=Exception("SMTP Connection Error"))
    mocker.patch("agents.finance.main.EMAIL_SENDER", "test@gmail.com")
    mocker.patch("agents.finance.main.EMAIL_PASSWORD", "pwd")
    mocker.patch("agents.finance.main.EMAIL_RECEIVER", "rec@gmail.com")

    main.send_email("제목", "내용", html_content="<p>내용</p>")
    mock_smtp_class.assert_called_once()

def test_get_additional_subscribers_regex(mocker):
    csv_mock_content = "Name,Email,Date\n홍길동,hong@test.com,2026-09-01\n이순신,lee@test.com,2026-09-02\n중복,hong@test.com,2026-09-03"
    
    mocker.patch("agents.finance.main.SUBSCRIBERS_CSV_URL", "https://example.com/subscribers.csv")
    
    mock_resp = MagicMock()
    mock_resp.read.return_value = csv_mock_content.encode('utf-8')
    mock_resp.__enter__.return_value = mock_resp
    mocker.patch("urllib.request.urlopen", return_value=mock_resp)

    emails = main.get_additional_subscribers()
    assert len(emails) == 2
    assert "hong@test.com" in emails
    assert "lee@test.com" in emails

def test_get_additional_subscribers_google_sheets_discovery(mocker):
    """Google Sheets URL(/pub?output=csv 등)에서 pubhtml로 여러 시트 gid를 자동 탐색하여 이메일을 수집하는지 검증"""
    mocker.patch("agents.finance.main.SUBSCRIBERS_CSV_URL", "https://docs.google.com/spreadsheets/d/e/2PACX-test/pub?output=csv")
    
    html_mock = '<html><body><a href="?gid=12345">Sheet1</a><a href="?gid=67890">Sheet2</a></body></html>'
    csv1_mock = "Name,Email\nUser1,user1@test.com"
    csv2_mock = "Name,Email\nUser2,user2@test.com"

    def mock_urlopen(req, timeout=10):
        url = req.full_url if hasattr(req, 'full_url') else req
        resp = MagicMock()
        if "pubhtml" in url:
            resp.read.return_value = html_mock.encode('utf-8')
        elif "gid=12345" in url:
            resp.read.return_value = csv1_mock.encode('utf-8')
        elif "gid=67890" in url:
            resp.read.return_value = csv2_mock.encode('utf-8')
        else:
            resp.read.return_value = b""
        resp.__enter__.return_value = resp
        return resp

    mocker.patch("urllib.request.urlopen", side_effect=mock_urlopen)

    emails = main.get_additional_subscribers()
    assert len(emails) == 2
    assert "user1@test.com" in emails
    assert "user2@test.com" in emails

def test_markdown_to_clean_html_table_parsing():
    md_table = """### 📊 다각화 매트릭스

**1. 핵심 요약 (Executive Summary)**
- 5G 스마트폰 AP 시장 정체로 새로운 현금창출원 모색

**3. 매트릭스**
| 자산명 | 비중 | 기대 수익 | 리스크 |
|---|---|---|---|
| TLT | 40% | 5% | 금리 인상 |
| GLD | 10% | 8% | 인플레이션 |
"""
    html = main.markdown_to_clean_html(md_table)
    
    assert "<table" in html
    assert "<thead" in html
    assert "<th" in html
    assert "자산명" in html
    assert "기대 수익" in html
    assert "<tbody" in html
    assert "<td" in html
    assert "TLT" in html
    assert "GLD" in html
