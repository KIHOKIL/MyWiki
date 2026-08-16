import os
import pytest

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """모든 테스트가 실행될 때 자동으로 가짜 환경변수를 주입합니다. (비용/실수 방지)"""
    monkeypatch.setenv("GEMINI_API_KEY", "fake_gemini_key")
    monkeypatch.setenv("OPENAI_API_KEY", "fake_openai_key")
    monkeypatch.setenv("EMAIL_SENDER", "test@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "fakepassword")
    monkeypatch.setenv("EMAIL_RECEIVER", "receiver@example.com")
