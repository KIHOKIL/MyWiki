import sys
import os
from unittest.mock import MagicMock

# Add parent directory to sys.path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

def test_fallback_logic_in_main(mocker):
    """Gemini API가 5회 재시도 후 최종 실패할 때 OpenAI로 자동 Fallback 되는지 검증"""
    # 1. Mock config
    mocker.patch("main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}]
    })
    
    # 2. Mock RSS fetching (return 1 article)
    mock_article = {"title": "Test Title", "link": "http://test.com", "published": "2026-08-16"}
    mocker.patch("main.fetch_google_news", return_value=[mock_article])
    
    # 3. Mock safe_summarize_news (Gemini) to fail instantly without sleeping
    mock_gemini = mocker.patch("main.safe_summarize_news", side_effect=Exception("Gemini Rate Limit"))
    
    # 4. Mock safe_summarize_news_openai to succeed
    mock_openai = mocker.patch("main.safe_summarize_news_openai", return_value="OpenAI Summary")
    
    # 5. Mock send_email and save_to_markdown
    mock_send_email = mocker.patch("main.send_email")
    mock_save = mocker.patch("main.save_to_markdown")
    
    # 6. Mock time.sleep
    mocker.patch("time.sleep")
    
    # 7. Provide fake OpenAI key
    mocker.patch("main.OPENAI_API_KEY", "fake_key")
    
    # Run main loop
    main.main()
    
    # Verify fallback happened
    mock_gemini.assert_called_once()
    mock_openai.assert_called_once()
    
    # Verify email was sent without error flag in subject
    called_subject = mock_send_email.call_args[0][0]
    called_body = mock_send_email.call_args[0][1]
    
    assert "[요약 일부 실패]" not in called_subject
    assert "OpenAI Summary" in called_body

def test_all_api_fail_in_main(mocker):
    """Gemini, OpenAI 모두 실패했을 때 [요약 일부 실패] 에러 핸들링 검증"""
    mocker.patch("main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}]
    })
    mocker.patch("main.fetch_google_news", return_value=[{"title": "Fail", "link": "link", "published": "date"}])
    mocker.patch("time.sleep")
    
    mock_gemini = mocker.patch("main.safe_summarize_news", side_effect=Exception("Gemini Fail"))
    mock_openai = mocker.patch("main.safe_summarize_news_openai", side_effect=Exception("OpenAI Fail"))
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
