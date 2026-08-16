import pytest
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError

# 모듈이 위치한 경로를 sys.path에 추가하여 main.py를 임포트할 수 있게 함
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import safe_summarize_news, summarize_news

def test_safe_summarize_news_retries_on_failure(mocker):
    """
    429 에러가 발생했을 때 tenacity가 정상적으로 재시도하는지 검증하는 단위 테스트.
    처음 2번은 에러를 발생시키고, 3번째에 성공하도록 설정.
    """
    # google.genai.Client를 모킹
    mock_client_class = mocker.patch('main.genai.Client')
    mock_client_instance = mock_client_class.return_value
    
    def side_effect(*args, **kwargs):
        side_effect.call_count += 1
        if side_effect.call_count <= 2:
            # 2번의 실패 (429 에러)
            raise ClientError(message="429 Quota Exceeded", code=429)
        else:
            # 3번째 성공
            mock_response = MagicMock()
            mock_response.text = "성공적인 요약 결과"
            return mock_response
            
    side_effect.call_count = 0
    mock_client_instance.models.generate_content.side_effect = side_effect
    
    # 함수 실행
    result = safe_summarize_news(
        category_name="Test Category",
        focus="Test Focus",
        articles=[{"title": "Test News 1", "link": "http://test", "published": "today"}]
    )
    
    # 3번째에 성공했으므로 총 3번 호출되었어야 함
    assert mock_client_instance.models.generate_content.call_count == 3
    assert result == "성공적인 요약 결과"
    print("단위 테스트(Unit Test) 성공: 429 에러 발생 시 정상적으로 재시도(Exponential Backoff)를 수행했습니다.")
