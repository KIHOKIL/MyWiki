import pytest
import os
import sys

# 모듈이 위치한 경로를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import safe_summarize_news
from dotenv import load_dotenv

load_dotenv()

def test_integration_gemini_api():
    """
    실제 Gemini API와 연동하여 프롬프트가 정상 처리되고 요약이 반환되는지 검증하는 통합 테스트.
    API Key가 없으면 스킵합니다.
    """
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY 환경 변수가 설정되어 있지 않아 통합 테스트를 스킵합니다.")
        
    dummy_articles = [
        {"title": "OpenAI, 새로운 초거대 AI 모델 공개", "link": "http://example.com/1", "published": "2026-08-16"},
        {"title": "구글, 제미나이 2.5 플래시 발표... 추론 속도 10배 향상", "link": "http://example.com/2", "published": "2026-08-16"}
    ]
    
    # 2.5-flash 모델로 변경된 코드가 실제 동작하는지 확인
    result = safe_summarize_news(
        category_name="AI Integration Test",
        focus="글로벌 AI 모델 트렌드와 속도 향상에 초점",
        articles=dummy_articles
    )
    
    assert result is not None
    assert "AI" in result or "OpenAI" in result or "구글" in result or "제미나이" in result
    print("\n통합 테스트 성공: 실제 Gemini API 연동이 정상적으로 작동하며 요약이 생성되었습니다.")
    print(f"결과 미리보기:\n{result[:100]}...")
