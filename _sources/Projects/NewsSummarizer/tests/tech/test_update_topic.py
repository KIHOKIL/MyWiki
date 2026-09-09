import sys
import os
import json
from unittest.mock import MagicMock

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.tech import update_topic

def test_update_config_gemini_success(mocker):
    mocker.patch("time.sleep")
    """Gemini API가 Issue를 파싱하여 성공적으로 config.json을 반환하는지 검증"""
    # config.json 읽기/쓰기 Mock
    mocker.patch("builtins.open", mocker.mock_open(read_data='{"categories": []}'))
    
    # Gemini API 응답 Mock
    mock_response = MagicMock()
    mock_response.text = '{"categories": [{"name": "AI", "queries": ["AI", "LLM"], "focus": "Tech updates"}]}'
    
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    
    mocker.patch("agents.tech.update_topic.genai.Client", return_value=mock_client)
    mock_openai = mocker.patch("agents.tech.update_topic.OpenAI") # Should not be called
    
    # 실행
    update_topic.update_config("이슈 제목: AI 추가", "내용: AI 뉴스 추가해줘")
    
    # 검증
    mock_client.models.generate_content.assert_called_once()
    mock_openai.assert_not_called()
    
def test_update_config_gemini_fail(mocker, monkeypatch):
    mocker.patch("time.sleep")
    import pytest
    mocker.patch("builtins.open", mocker.mock_open(read_data='{"categories": []}'))
    
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("Gemini Rate Limit")
    mocker.patch("agents.tech.update_topic.genai.Client", return_value=mock_client)
    
    with pytest.raises(SystemExit):
        update_topic.update_config("이슈 제목: Quantum 추가", "")

