import sys
import os
from unittest.mock import MagicMock

# Add parent directory to sys.path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

def test_fallback_logic_in_main(mocker):
    """Gemini API가 5회 재시도 후 최종 실패할 때 OpenAI로 자동 Fallback 되는지 검증"""
    mocker.patch("main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}],
        "github_trend": {"queries": ["test"], "focus": "test focus"}
    })
    
    mock_article = {"title": "Test Title", "link": "http://test.com", "published": "2026-08-16"}
    mocker.patch("main.fetch_google_news", return_value=[mock_article])
    mocker.patch("main.fetch_github_trending", return_value=[{
        "full_name": "test/repo", "html_url": "http://github.com/test/repo",
        "description": "test", "stars": 100, "language": "Python", "topics": []
    }])
    
    mock_gemini = mocker.patch("main.safe_summarize_news", side_effect=Exception("Gemini Rate Limit"))
    mock_openai = mocker.patch("main.safe_summarize_news_openai", return_value="OpenAI Summary")
    
    mocker.patch("main.safe_analyze_github_trending", return_value="GitHub Trending Analysis")
    mocker.patch("main.safe_generate_executive_summary", return_value="Executive Summary Analysis")
    
    mock_send_email = mocker.patch("main.send_email")
    mock_save = mocker.patch("main.save_to_markdown")
    mocker.patch("time.sleep")
    mocker.patch("main.OPENAI_API_KEY", "fake_key")
    
    main.main()
    
    mock_gemini.assert_called_once()
    mock_openai.assert_called_once()
    
    called_subject = mock_send_email.call_args[0][0]
    called_body = mock_send_email.call_args[0][1]
    
    assert "[요약 일부 실패]" not in called_subject
    assert "OpenAI Summary" in called_body
    assert "Section 1: Executive Summary" in called_body
    assert "Section 2: 오늘의 GitHub 트렌드 큐레이션" in called_body

def test_all_api_fail_in_main(mocker):
    """Gemini, OpenAI 모두 실패했을 때 [요약 일부 실패] 에러 핸들링 검증"""
    mocker.patch("main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}]
    })
    mocker.patch("main.fetch_google_news", return_value=[{"title": "Fail", "link": "link", "published": "date"}])
    mocker.patch("main.fetch_github_trending", return_value=[])
    mocker.patch("time.sleep")
    
    mock_gemini = mocker.patch("main.safe_summarize_news", side_effect=Exception("Gemini Fail"))
    mock_openai = mocker.patch("main.safe_summarize_news_openai", side_effect=Exception("OpenAI Fail"))
    mocker.patch("main.safe_analyze_github_trending", return_value="GitHub Trending Analysis")
    mocker.patch("main.safe_generate_executive_summary", return_value="Executive Summary Analysis")
    
    mock_send_email = mocker.patch("main.send_email")
    mocker.patch("main.save_to_markdown")
    mocker.patch("main.OPENAI_API_KEY", "fake_key")
    
    main.main()
    
    mock_gemini.assert_called_once()
    mock_openai.assert_called_once()
    
    called_subject = mock_send_email.call_args[0][0]
    called_body = mock_send_email.call_args[0][1]
    
    assert "[요약 일부 실패]" in called_subject
    assert "API 연동 문제로 AI 요약 생성에 실패했습니다" in called_body

def test_three_sections_and_html_email_generation(mocker):
    """Section 1, Section 2, Section 3 및 반응형 HTML 이메일 포맷 생성 검증"""
    mocker.patch("main.load_config", return_value={
        "categories": [
            {"name": "Group 2nd Brain", "queries": ["2nd brain"], "focus": "Brain focus"},
            {"name": "Codebase Understanding", "queries": ["code review"], "focus": "Codebase focus"}
        ],
        "github_trend": {"queries": ["second-brain"], "focus": "GitHub focus"}
    })
    
    mocker.patch("main.fetch_google_news", return_value=[
        {"title": "Sample News Title", "link": "https://sample.com/news", "published": "2026-09-06"}
    ])
    mocker.patch("main.fetch_github_trending", return_value=[
        {
            "full_name": "tinyhumansai/openhuman",
            "html_url": "https://github.com/tinyhumansai/openhuman",
            "description": "OpenHuman personal AI",
            "stars": 39400,
            "language": "Python",
            "topics": ["second-brain"]
        }
    ])
    mocker.patch("time.sleep")
    
    mocker.patch("main.safe_summarize_news", side_effect=lambda name, focus, arts: f"Summary for {name}")
    mocker.patch("main.safe_analyze_github_trending", return_value="### 1위. [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) (★ 39,400)\n- **🎯 한 줄 정의**: 오픈소스 개인용 AI")
    mocker.patch("main.safe_generate_executive_summary", return_value="### 🚀 오늘 주목해야 할 핵심 혁신 (Key Innovations)\n- 사내 지식 그래프와 로컬 에이전트 결합")
    
    mock_send_email = mocker.patch("main.send_email")
    mock_save = mocker.patch("main.save_to_markdown")
    
    main.main()
    
    # 1. Email calls verification
    mock_send_email.assert_called_once()
    called_args = mock_send_email.call_args
    subject = called_args[0][0]
    plain_body = called_args[0][1]
    html_body = called_args[1].get("html_content")
    
    assert "Group 2nd Brain & Tech Horizon 브리핑" in subject
    
    # Check Section 1 in plain text & html
    assert "Section 1: Executive Summary" in plain_body
    assert "사내 지식 그래프와 로컬 에이전트 결합" in plain_body
    
    # Check Section 2 in plain text & html
    assert "Section 2: 오늘의 GitHub 트렌드 큐레이션" in plain_body
    assert "tinyhumansai/openhuman" in plain_body
    
    # Check Section 3 in plain text & html
    assert "Section 3: 관심 분야별 심층 뉴스" in plain_body
    assert "Group 2nd Brain" in plain_body
    assert "Codebase Understanding" in plain_body
    
    # Check HTML email formatting
    assert html_body is not None
    assert "<!DOCTYPE html>" in html_body
    assert "DAILY INTELLIGENCE &amp; KNOWLEDGE BRIEFING" in html_body or "DAILY INTELLIGENCE & KNOWLEDGE BRIEFING" in html_body
    assert "tinyhumansai/openhuman" in html_body
    assert "Group 2nd Brain" in html_body
    
    # 2. Markdown save verification
    mock_save.assert_called_once()
    saved_content = mock_save.call_args[0][1]
    assert "Section 1: Executive Summary" in saved_content
    assert "Section 2: 오늘의 GitHub 트렌드 큐레이션" in saved_content
    assert "Section 3: 관심 분야별 심층 뉴스" in saved_content
