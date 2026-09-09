import os
import sys
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.finance import main

def test_fetch_google_news(mocker):
    mocker.patch("time.sleep")
    mock_resp = MagicMock()
    
    mock_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>Test Finance Article 1</title>
          <link>https://example.com/finance1</link>
        </item>
        <item>
          <title>Test Finance Article 2</title>
          <link>https://example.com/finance2</link>
        </item>
      </channel>
    </rss>
    """
    mock_resp.read.return_value = mock_xml
    mock_resp.__enter__.return_value = mock_resp
    mocker.patch("urllib.request.urlopen", return_value=mock_resp)

    articles = main.fetch_google_news("Macro", max_articles=2)
    assert len(articles) == 2
    assert articles[0]["title"] == "Test Finance Article 1"
    assert articles[0]["link"] == "https://example.com/finance1"

def test_generate_finance_report(mocker):
    mocker.patch("time.sleep")
    mock_client_class = mocker.patch("agents.finance.main.genai.Client")
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = "### 📊 Money Snowball Daily Macro Briefing\n\nGenerated Content"
    mock_client.models.generate_content.return_value = mock_response
    
    news_data = {"US Macro": [{"title": "Macro news", "link": "link"}]}
    mocker.patch("agents.finance.main.GEMINI_API_KEY", "fake_key")
    
    report = main.generate_finance_report(news_data)
    
    assert report == mock_response.text
    mock_client.models.generate_content.assert_called_once()
    
    call_args = mock_client.models.generate_content.call_args
    assert call_args[1]['model'] == 'gemini-3.6-flash'
    assert 'Macro news' in call_args[1]['contents']

def test_main_pipeline(mocker):
    mocker.patch("time.sleep")
    # Mock network & LLM dependencies
    mocker.patch("agents.finance.main.fetch_google_news", return_value=[{"title": "Test", "link": "http"}])
    mocker.patch("agents.finance.main.generate_finance_report", return_value="### Mocked Report")
    mocker.patch("agents.finance.main.send_email")
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    
    # Mock config
    mocker.patch("agents.finance.main.load_config", return_value={"categories": [{"name": "US Macro", "queries": ["Q1"]}]})
    
    # Run the main pipeline
    main.main()
    
    # Verify file was written
    mock_open.assert_called_once()
    handle = mock_open()
    handle.write.assert_called_once_with("### Mocked Report")
    
    # Verify email was sent
    main.send_email.assert_called_once()
    assert "Mocked Report" in main.send_email.call_args[0][1]
