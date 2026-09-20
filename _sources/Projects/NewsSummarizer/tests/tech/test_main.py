import sys
import os
from unittest.mock import MagicMock

# Add parent directory to sys.path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.tech import main

def test_fallback_logic_in_main(mocker):
    """Gemini API가 5회 재시도 후 최종 실패할 때 OpenAI로 자동 Fallback 되는지 검증"""
    mocker.patch("agents.tech.main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}],
        "github_trend": {"queries": ["test"], "focus": "test focus"}
    })
    
    mock_article = {"title": "Test Title", "link": "http://test.com", "published": "2026-08-16"}
    mocker.patch("agents.tech.main.fetch_google_news", return_value=[mock_article])
    mocker.patch("agents.tech.main.fetch_github_trending", return_value=[{
        "full_name": "test/repo", "html_url": "http://github.com/test/repo",
        "description": "test", "stars": 100, "language": "Python", "topics": []
    }])
    
    mock_gemini = mocker.patch("agents.tech.main.safe_summarize_news", side_effect=Exception("Gemini Rate Limit"))
    mock_openai = mocker.patch("agents.tech.main.safe_summarize_news_openai", return_value="OpenAI Summary")
    
    mocker.patch("agents.tech.main.safe_analyze_github_trending", return_value="GitHub Trending Analysis")
    mocker.patch("agents.tech.main.safe_generate_executive_summary", return_value="Executive Summary Analysis")
    
    mock_send_email = mocker.patch("agents.tech.main.send_email")
    mock_save = mocker.patch("agents.tech.main.save_to_markdown")
    mocker.patch("time.sleep")
    mocker.patch("agents.tech.main.OPENAI_API_KEY", "fake_key")
    
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
    mocker.patch("agents.tech.main.load_config", return_value={
        "categories": [{"name": "Tech", "queries": ["AI"], "focus": "Test"}]
    })
    mocker.patch("agents.tech.main.fetch_google_news", return_value=[{"title": "Fail", "link": "link", "published": "date"}])
    mocker.patch("agents.tech.main.fetch_github_trending", return_value=[])
    mocker.patch("time.sleep")
    
    mock_gemini = mocker.patch("agents.tech.main.safe_summarize_news", side_effect=Exception("Gemini Fail"))
    mock_openai = mocker.patch("agents.tech.main.safe_summarize_news_openai", side_effect=Exception("OpenAI Fail"))
    mocker.patch("agents.tech.main.safe_analyze_github_trending", return_value="GitHub Trending Analysis")
    mocker.patch("agents.tech.main.safe_generate_executive_summary", return_value="Executive Summary Analysis")
    
    mock_send_email = mocker.patch("agents.tech.main.send_email")
    mocker.patch("agents.tech.main.save_to_markdown")
    mocker.patch("agents.tech.main.OPENAI_API_KEY", "fake_key")
    
    main.main()
    
    mock_gemini.assert_called_once()
    mock_openai.assert_called_once()
    
    called_subject = mock_send_email.call_args[0][0]
    called_body = mock_send_email.call_args[0][1]
    
    assert "[요약 일부 실패]" in called_subject
    assert "API 연동 문제로 AI 요약 생성에 실패했습니다" in called_body

def test_three_sections_and_html_email_generation(mocker):
    """Section 1, Section 2, Section 3 및 반응형 HTML 이메일 포맷 생성 검증"""
    mocker.patch("agents.tech.main.load_config", return_value={
        "categories": [
            {"name": "Group 2nd Brain", "queries": ["2nd brain"], "focus": "Brain focus"},
            {"name": "Codebase Understanding", "queries": ["code review"], "focus": "Codebase focus"}
        ],
        "github_trend": {"queries": ["second-brain"], "focus": "GitHub focus"}
    })
    
    mocker.patch("agents.tech.main.fetch_google_news", return_value=[
        {"title": "Sample News Title", "link": "https://sample.com/news", "published": "2026-09-06"}
    ])
    mocker.patch("agents.tech.main.fetch_github_trending", return_value=[
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
    
    mocker.patch("agents.tech.main.safe_summarize_news", side_effect=lambda name, focus, arts: f"Summary for {name}")
    mocker.patch("agents.tech.main.safe_analyze_github_trending", return_value="### 1위. [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) (★ 39,400)\n- **🎯 한 줄 정의**: 오픈소스 개인용 AI")
    mocker.patch("agents.tech.main.safe_generate_executive_summary", return_value="### 🚀 오늘 주목해야 할 핵심 혁신 (Key Innovations)\n- 사내 지식 그래프와 로컬 에이전트 결합")
    
    mock_send_email = mocker.patch("agents.tech.main.send_email")
    mock_save = mocker.patch("agents.tech.main.save_to_markdown")
    
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


def test_fetch_jesusiswithus_github_parsing(mocker):
    """'매일의 IT뉴스' HTML 본문에서 추천 GitHub 저장소가 정상 추출되는지 검증"""
    mock_html = """
    <html>
    <h2 id=오늘의-추천-github-리포>오늘의 추천 GitHub 리포</h2>
    <h3 id=1-cua--플랫폼>1. cua — 컴퓨터 사용 에이전트 플랫폼</h3>
    <ul>
        <li><strong>GitHub</strong>: <a href=https://github.com/trycua/cua target=_blank>trycua/cua</a></li>
        <li><strong>한 줄 설명</strong>: 컴퓨터 사용 AI 에이전트 학습 플랫폼입니다.</li>
        <li><strong>수치</strong>: 별 24,000개 · MIT 라이선스</li>
        <li><strong>어디서/왜</strong>: GitHub 트렌딩 상위 랭크</li>
    </ul>
    <h3 id=2-pizza-bot--받은편지함>2. Pizza Bot — 받은편지함</h3>
    <ul>
        <li><strong>GitHub</strong>: <a href=https://github.com/pizza-bot-app/pizza-bot target=_blank>pizza-bot-app/pizza-bot</a></li>
        <li><strong>한 줄 설명</strong>: AI 에이전트를 위한 로컬 인박스 도구입니다.</li>
        <li><strong>수치</strong>: 별 320개</li>
    </ul>
    <h2 id=오늘의-일반사역용-추천-리포>오늘의 일반사역용 추천 리포</h2>
    </html>
    """
    mock_resp = MagicMock()
    mock_resp.read.return_value = mock_html.encode('utf-8')
    mock_resp.__enter__.return_value = mock_resp
    mocker.patch("urllib.request.urlopen", return_value=mock_resp)

    repos = main.fetch_jesusiswithus_github("2026-09-20")
    assert len(repos) == 2
    assert repos[0]["full_name"] == "trycua/cua"
    assert repos[0]["stars"] == 24000
    assert "컴퓨터 사용" in repos[0]["description"]
    assert repos[1]["full_name"] == "pizza-bot-app/pizza-bot"
    assert repos[1]["stars"] == 320


def test_fetch_jesusiswithus_github_fallback(mocker):
    """당일 IT뉴스 404 시 메인 목록에서 최신 일자 포스트를 찾아 Fallback 하는지 검증"""
    main_html = """
    <html>
    <a href="/digest/daily-it-news/2026/2026-09-20/">2026년 9월 20일 IT뉴스</a>
    </html>
    """
    post_html = """
    <html>
    <h2 id=오늘의-추천-github-리포>오늘의 추천 GitHub 리포</h2>
    <h3 id=1-librechat>1. LibreChat</h3>
    <ul>
        <li><strong>GitHub</strong>: <a href=https://github.com/danny-avila/LibreChat target=_blank>danny-avila/LibreChat</a></li>
        <li><strong>한 줄 설명</strong>: 자체 호스팅 오픈소스 챗GPT 대안</li>
        <li><strong>수치</strong>: 별 44,000개</li>
    </ul>
    </html>
    """

    def mock_urlopen_side_effect(req, timeout=10):
        url = req.get_full_url() if hasattr(req, "get_full_url") else str(req)
        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        if "2026-09-25" in url:
            import urllib.error
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        elif url.endswith("/digest/daily-it-news/"):
            mock_resp.read.return_value = main_html.encode('utf-8')
            return mock_resp
        else:
            mock_resp.read.return_value = post_html.encode('utf-8')
            return mock_resp

    mocker.patch("urllib.request.urlopen", side_effect=mock_urlopen_side_effect)

    repos = main.fetch_jesusiswithus_github("2026-09-25")
    assert len(repos) == 1
    assert repos[0]["full_name"] == "danny-avila/LibreChat"
    assert repos[0]["stars"] == 44000


def test_shared_github_history_deduplication(tmp_path, mocker):
    """최근 14일 이내 브리핑에 공유된 저장소는 중복 추천에서 제외되는지 검증"""
    fake_history_file = str(tmp_path / "shared_github_history.json")
    mocker.patch("agents.tech.main.get_shared_github_history_file", return_value=fake_history_file)

    # 1. 저장소 기록 저장
    main.save_shared_github_history(["old-owner/old-repo", "already-seen/repo"])

    # 2. 이력 로드 검증
    history = main.load_shared_github_history(max_age_days=14)
    assert "old-owner/old-repo" in history
    assert "already-seen/repo" in history

    # 3. fetch_github_trending 호출 시 중복 저장소 제외 검증
    mocker.patch("agents.tech.main.fetch_jesusiswithus_github", return_value=[
        {"full_name": "already-seen/repo", "html_url": "http://...", "description": "seen", "stars": 100, "category_id": "second_brain", "category_name": "Second-Brain", "category_icon": "🧠"},
        {"full_name": "fresh-owner/fresh-repo", "html_url": "http://...", "description": "fresh", "stars": 200, "category_id": "second_brain", "category_name": "Second-Brain", "category_icon": "🧠"}
    ])
    
    # GitHub Search API는 빈 리스트 반환
    mock_resp = MagicMock()
    mock_resp.read.return_value = b'{"items": []}'
    mock_resp.__enter__.return_value = mock_resp
    mocker.patch("urllib.request.urlopen", return_value=mock_resp)
    mocker.patch("time.sleep")

    # 캐시 무효화
    real_exists = os.path.exists
    mocker.patch("os.path.exists", side_effect=lambda p: False if "github_cache.json" in str(p) else real_exists(p))

    candidates = main.fetch_github_trending(categories_or_queries=[{"id": "second_brain", "name": "Second-Brain", "icon": "🧠", "queries": ["query"]}])
    
    candidate_names = [c["full_name"] for c in candidates]
    assert "already-seen/repo" not in candidate_names
    assert "fresh-owner/fresh-repo" in candidate_names

