import os
import json
import smtplib
from email.message import EmailMessage
import feedparser
from google import genai
from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv
import urllib.parse
import urllib.request
import csv
import io
import re
from datetime import datetime, timezone, timedelta
import time
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# 환경 변수 로드 (.env 우선순위: 스크립트 위치 .env 및 작업 디렉토리 .env)
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
load_dotenv()

# 설정값
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password").replace('\xa0', '').replace(' ', '')

EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver_email@gmail.com")
SUBSCRIBERS_CSV_URL = os.getenv("SUBSCRIBERS_CSV_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def load_config():
    """config.json 파일에서 카테고리, GitHub 트렌드 및 쿼리 설정을 로드합니다."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# 1. 뉴스 및 GitHub 데이터 수집 모듈
# ==========================================

def fetch_google_news(query, max_articles=2):
    """주어진 키워드로 Google News RSS를 검색하여 기사를 가져옵니다."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
            feed = feedparser.parse(xml_data)
            if feed and feed.entries:
                break
        except Exception as e:
            print(f"  [Warning] urllib request failed for '{query}' (Attempt {attempt+1}/3): {e}")
        time.sleep(2)
    
    if not feed or not hasattr(feed, 'entries'):
        print(f"  [Error] Failed to fetch or parse RSS for '{query}'.")
        return []

    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "")
        })
    return articles

def fetch_github_trending(queries=None, max_candidates=10):
    """GitHub Search API를 사용하여 사용자 관심 분야(2nd Brain, Code Review, Codebase)의 최상위 저장소를 수집합니다."""
    if not queries:
        queries = ["topic:second-brain", "code review AI", "codebase intelligence", "coding agent implementation"]
        
    candidates = []
    seen_repos = set()
    
    headers = {
        'User-Agent': 'DailyNewsSummarizer/2.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f"token {GITHUB_TOKEN}"

    for query in queries:
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=5"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                for item in data.get("items", []):
                    full_name = item.get("full_name")
                    if full_name and full_name not in seen_repos:
                        seen_repos.add(full_name)
                        candidates.append({
                            "full_name": full_name,
                            "html_url": item.get("html_url", ""),
                            "description": item.get("description") or "설명 없음",
                            "stars": item.get("stargazers_count", 0),
                            "language": item.get("language") or "General",
                            "topics": item.get("topics", [])
                        })
        except Exception as e:
            print(f"  [Warning] GitHub API 검색 실패 ('{query}'): {e}")
        time.sleep(1)

    # API 호출 실패 또는 후보가 없을 때를 대비한 검증된 큐레이션 기본값 (Fallback)
    if not candidates:
        print("  [Notice] GitHub API 결과 부재 또는 요청 제한으로 기본 큐레이션 저장소를 활용합니다.")
        candidates = [
            {
                "full_name": "tinyhumansai/openhuman",
                "html_url": "https://github.com/tinyhumansai/openhuman",
                "description": "OpenHuman is an open source personal AI for Mac, Windows and Linux — local-first memory, agent orchestration, and deep research.",
                "stars": 39400,
                "language": "Python / TypeScript",
                "topics": ["second-brain", "local-memory", "agent-orchestration"]
            },
            {
                "full_name": "tirth8205/code-review-graph",
                "html_url": "https://github.com/tirth8205/code-review-graph",
                "description": "Local-first code intelligence graph for MCP and CLI. Builds a persistent map of your codebase so AI coding tools read only what matters, with benchmarked context reductions on reviews and large-repo workflows.",
                "stars": 31200,
                "language": "TypeScript / Python",
                "topics": ["code-review", "codebase-graph", "mcp"]
            },
            {
                "full_name": "AgriciDaniel/claude-obsidian",
                "html_url": "https://github.com/AgriciDaniel/claude-obsidian",
                "description": "Self-organizing AI second brain for Obsidian + Claude Code. Drop any source and Claude reads, links, and files it into one connected knowledge graph of plain Markdown you own.",
                "stars": 14600,
                "language": "Markdown / Shell",
                "topics": ["obsidian", "second-brain", "pkm", "llm-wiki"]
            }
        ]

    candidates.sort(key=lambda x: x["stars"], reverse=True)
    return candidates[:max_candidates]

# ==========================================
# 2. LLM 요약 및 분석 모듈
# ==========================================

# --- 카테고리 뉴스 분석 ---
def _build_news_prompt(category_name, focus, articles):
    sys_instruction = f"""당신은 IT, 통신, AI 및 소프트웨어 엔지니어링 산업의 글로벌 최고 수준 애널리스트입니다.
아래에 수집된 뉴스 기사들을 바탕으로, **{category_name}** 분야의 최신 동향을 브리핑해 주셔야 합니다.

[특별 분석 포인트]
{focus}

단순히 기사를 나열하는 것이 아니라, 여러 기사들 사이의 맥락을 연결하고 위 분석 포인트에 부합하는 가장 중요한 산업적/기술적 의미를 도출해 주세요.
전문적이고 구조화된 리포트 형식(소제목, 글머리 기호 사용)으로 가독성 있게 작성해 주시고, 분량은 핵심만 압축하여 너무 길지 않게 작성하세요.

마지막으로, 오늘 수집된 뉴스들과 최신 글로벌 동향을 바탕으로, 사용자가 앞으로 새롭게 추적하면 좋을 만한 트렌디한 **추천 뉴스 키워드/주제**를 브리핑 맨 마지막에 '💡 오늘의 추천 신규 키워드' 라는 섹션으로 1~2개 정도 제안해주세요.
"""
    prompt = "[수집된 뉴스 기사 헤드라인 목록]\n\n"
    for i, article in enumerate(articles, 1):
        prompt += f"{i}. {article['title']}\n"
    return sys_instruction, prompt

def summarize_news_gemini(category_name, focus, articles):
    if not articles:
        return f"[{category_name}] 에 대한 최신 뉴스가 수집되지 않았습니다."
    sys_instruction, prompt = _build_news_prompt(category_name, focus, articles)
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruction,
            temperature=0.3
        ),
    )
    return response.text

def summarize_news_openai(category_name, focus, articles):
    if not articles:
        return f"[{category_name}] 에 대한 최신 뉴스가 수집되지 않았습니다."
    sys_instruction, prompt = _build_news_prompt(category_name, focus, articles)
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_summarize_news(category_name, focus, articles):
    print(f"  [{category_name}] Gemini 분석 요청 중...")
    return summarize_news_gemini(category_name, focus, articles)

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_summarize_news_openai(category_name, focus, articles):
    print(f"  [{category_name}] OpenAI (Fallback) 분석 요청 중...")
    return summarize_news_openai(category_name, focus, articles)

# --- Section 2: GitHub Trending Top 3 분석 ---
def _build_github_prompt(focus, candidates):
    sys_instruction = f"""당신은 글로벌 오픈소스 및 AI 아키텍처 수석 연구원입니다.
수집된 GitHub 후보 저장소 목록 중, 사용자 관심 분야({focus})에 가장 부합하는 **전 세계 Top 3 오픈소스 저장소**를 엄선하여 심층 분석해 주세요.

[분석 및 출력 포맷 가이드]
선정된 3개 저장소 각각에 대해 아래 양식을 엄격히 준수하여 마크다운으로 출력하세요:

### 1위. [저장소명](저장소링크) (★ 스타 수)
- **🎯 한 줄 정의 및 목적**: 무엇을 해결하는 도구/아키텍처인가?
- **💡 핵심 기술 및 차별점**: 로컬 우선(Local-first) 메모리, 그래프 AST, MCP 통합, 에이전트 오케스트레이션 등 기술적 포인트.
- **🛠️ 실무 적용 가치**: Group 2nd Brain 구축 또는 코드베이스 이해/구현 루프(Implementation Loop)/코드 리뷰에 어떻게 활용 가능한가?

(2위와 3위도 동일한 형식으로 순차 작성)
"""
    prompt = "[수집된 GitHub 후보 저장소 목록]\n\n"
    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. [{c['full_name']}]({c['html_url']}) (Stars: {c['stars']:,}, Lang: {c['language']})\n"
        prompt += f"   설명: {c['description']}\n\n"
    return sys_instruction, prompt

def analyze_github_gemini(focus, candidates):
    sys_instruction, prompt = _build_github_prompt(focus, candidates)
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruction,
            temperature=0.3
        ),
    )
    return response.text

def analyze_github_openai(focus, candidates):
    sys_instruction, prompt = _build_github_prompt(focus, candidates)
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_analyze_github_trending(focus, candidates):
    print("  [GitHub Trending] Gemini 분석 요청 중...")
    return analyze_github_gemini(focus, candidates)

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_analyze_github_trending_openai(focus, candidates):
    print("  [GitHub Trending] OpenAI (Fallback) 분석 요청 중...")
    return analyze_github_openai(focus, candidates)

# --- Section 1: Executive Summary (2nd Brain, Codebase Loop & AI Frontier Strategy 종합) ---
def _build_executive_prompt(articles_summary_text, github_summary_text):
    sys_instruction = """당신은 글로벌 엔터프라이즈 AI 시스템 및 소프트웨어 엔지니어링 최고 임원(VP of Engineering & Chief AI Strategist)입니다.
오늘 수집된 글로벌 뉴스 및 GitHub 오픈소스 트렌드를 관통 분석하여, 데일리 브리핑 최상단에 위치할 [Executive Summary: 2nd Brain, Codebase Loop & Big Tech Strategy]를 작성하세요.

[핵심 분석 3대 렌즈]
1) **Group 2nd Brain 구축**: 사내 이메일, 메신저, Jira, Confluence 연동을 통한 팀 지식 허브 구축 및 보안/개인정보 거버넌스.
2) **Codebase 이해 기반 Implementation Loop & Code Review**: 대규모 코드베이스의 구조적 이해, Harness Engineering, TDD 자동화, LLM 기반 정밀 코드 리뷰.
3) **Global Big Tech & AI Frontier 자본 흐름**: 빅테크(MS, 구글, 메타, 아마존, 애플, 엔비디아) 및 AI 프론티어 랩/유니콘(OpenAI, Anthropic, xAI, Databricks 등)의 M&A, 변형적 인수(Acqui-hire), 대규모 컴퓨팅 동맹(Stargate, 전력/클라우드) 및 생태계 락인(Lock-in) 전략이 기술 판도에 미치는 영향.

[필수 작성 구조]
반드시 다음 3가지 소제목으로 구성하고 글머리 기호(Bulleted list)를 활용해 명확하게 기술하세요:

### 🚀 오늘 주목해야 할 핵심 혁신 (Key Innovations)
- 2nd Brain 아키텍처, 코드베이스 분석/구현 루프, 빅테크/AI 프론티어의 전략적 인수 및 인프라 도약 관점에서 오늘 포착된 주요 기술 혁신 요약.

### ⚠️ 핵심 리스크 및 과제 (Core Risks & Trade-offs)
- 사내 민감 데이터 연동 시의 보안/권한 누수, LLM Context 한계로 인한 코드베이스 환각(Hallucination), 빅테크 플랫폼 종속성(Lock-in) 및 반독점/컴플라이언스 리스크 지적.

### 🎯 실무 적용 및 설계 시사점 (Actionable Takeaways)
- 현재 사내 Group 2nd Brain 설계, 코드 리뷰/구현 루프, 그리고 전략적 툴체인 선정에 즉시 반영해야 할 실행 지침 2~3가지 제시.
"""
    prompt = f"""[오늘의 카테고리별 뉴스 분석 내용]
{articles_summary_text}

[오늘의 GitHub 트렌드 Top 3 분석 내용]
{github_summary_text}
"""
    return sys_instruction, prompt

def generate_executive_gemini(articles_summary_text, github_summary_text):
    sys_instruction, prompt = _build_executive_prompt(articles_summary_text, github_summary_text)
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruction,
            temperature=0.3
        ),
    )
    return response.text

def generate_executive_openai(articles_summary_text, github_summary_text):
    sys_instruction, prompt = _build_executive_prompt(articles_summary_text, github_summary_text)
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_generate_executive_summary(articles_summary_text, github_summary_text):
    print("  [Executive Summary] Gemini 종합 분석 요청 중...")
    return generate_executive_gemini(articles_summary_text, github_summary_text)

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_generate_executive_summary_openai(articles_summary_text, github_summary_text):
    print("  [Executive Summary] OpenAI (Fallback) 종합 분석 요청 중...")
    return generate_executive_openai(articles_summary_text, github_summary_text)

# ==========================================
# 3. 이메일 및 마크다운 포맷 생성 모듈
# ==========================================

def markdown_to_clean_html(md_text):
    """마크다운 텍스트를 이메일 클라이언트에 호환되는 깔끔한 인라인 스타일 HTML로 변환합니다."""
    if not md_text:
        return ""
    lines = md_text.strip().split("\n")
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # 헤더 변환
        if stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = stripped[4:]
            
            # 소제목 아이콘에 따른 포인트 컬러 부여
            border_color = "#4f46e5"
            bg_color = "#f8fafc"
            if "혁신" in title or "🚀" in title:
                border_color = "#10b981"
                bg_color = "#f0fdf4"
            elif "리스크" in title or "⚠️" in title:
                border_color = "#f59e0b"
                bg_color = "#fffbeb"
            elif "시사점" in title or "🎯" in title or "적용" in title:
                border_color = "#3b82f6"
                bg_color = "#eff6ff"

            html_lines.append(f'<div style="margin:16px 0 8px 0; padding:8px 12px; background-color:{bg_color}; border-left:4px solid {border_color}; border-radius:4px;"><strong style="color:#0f172a; font-size:15px;">{title}</strong></div>')
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = stripped[3:]
            html_lines.append(f'<h3 style="color:#0f172a; margin:18px 0 8px 0; font-size:16px; font-weight:700;">{title}</h3>')
        elif stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = stripped[2:]
            html_lines.append(f'<h2 style="color:#0f172a; margin:22px 0 10px 0; font-size:18px; font-weight:800;">{title}</h2>')
        # 리스트 변환
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append('<ul style="margin:6px 0; padding-left:20px; color:#334155;">')
                in_list = True
            item_text = stripped[2:]
            html_lines.append(f'<li style="margin-bottom:6px; line-height:1.6; font-size:14px;">{item_text}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            match = re.match(r'^(\d+\.)\s+(.*)', stripped)
            num = match.group(1)
            item_text = match.group(2)
            html_lines.append(f'<div style="margin:6px 0; line-height:1.6; font-size:14px; color:#334155;"><strong style="color:#4f46e5;">{num}</strong> {item_text}</div>')
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<p style="margin:6px 0; line-height:1.6; font-size:14px; color:#334155;">{stripped}</p>')

    if in_list:
        html_lines.append("</ul>")

    content_html = "\n".join(html_lines)

    # 볼드 체 처리
    content_html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#0f172a; font-weight:600;">\1</strong>', content_html)
    # 이탤릭 체 처리
    content_html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', content_html)
    # 마크다운 링크 처리
    content_html = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" style="color:#4f46e5; text-decoration:none; font-weight:600; border-bottom:1px dashed #4f46e5;" target="_blank">\1</a>', content_html)

    return content_html

def generate_html_email(date_str, executive_summary, github_trending, category_sections, form_url):
    """모던하고 구조화된 프리미엄 반응형 HTML 이메일 템플릿을 생성합니다."""
    
    exec_html = markdown_to_clean_html(executive_summary)
    github_html = markdown_to_clean_html(github_trending)
    
    # 카테고리 카드 HTML 생성
    categories_html = ""
    for cat in category_sections:
        cat_name = cat["name"]
        cat_summary_html = markdown_to_clean_html(cat["summary"])
        
        # 참고 기사 링크 목록
        links_html = ""
        for art in cat["articles"][:4]:
            links_html += f'<li style="margin-bottom:4px; font-size:13px;"><a href="{art["link"]}" style="color:#475569; text-decoration:underline;" target="_blank">{art["title"]}</a></li>'
            
        categories_html += f"""
        <div style="background-color:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:20px; margin-bottom:20px;">
          <div style="display:inline-block; background:linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color:#ffffff; font-size:12px; font-weight:700; padding:4px 10px; border-radius:20px; text-transform:uppercase; margin-bottom:12px;">
            {cat_name}
          </div>
          <div style="font-size:14px; color:#334155; line-height:1.6;">
            {cat_summary_html}
          </div>
          <div style="margin-top:14px; padding-top:12px; border-top:1px dashed #e2e8f0;">
            <div style="font-size:12px; font-weight:700; color:#64748b; margin-bottom:6px;">🔗 주요 원문 기사</div>
            <ul style="margin:0; padding-left:18px; color:#64748b;">
              {links_html}
            </ul>
          </div>
        </div>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[{date_str}] 글로벌 IT/2nd Brain 산업 브리핑</title>
</head>
<body style="margin:0; padding:0; background-color:#f8fafc; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#1e293b; line-height:1.6;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed; background-color:#f8fafc;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:680px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
          
          <!-- 헤더 배너 -->
          <tr>
            <td style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%); padding: 32px 28px; text-align: left;">
              <div style="font-size:11px; font-weight:700; color:#818cf8; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                DAILY INTELLIGENCE & KNOWLEDGE BRIEFING
              </div>
              <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:800; letter-spacing:-0.5px;">
                Group 2nd Brain & Tech Horizon
              </h1>
              <div style="margin-top:10px; display:inline-block; background-color:rgba(255,255,255,0.12); color:#e2e8f0; font-size:12px; padding:4px 10px; border-radius:14px;">
                📅 {date_str} 리포트
              </div>
            </td>
          </tr>

          <!-- 메인 본문 -->
          <tr>
            <td style="padding: 28px 24px;">
              
              <!-- SECTION 1: EXECUTIVE SUMMARY -->
              <div style="background-color:#ffffff; border:2px solid #6366f1; border-radius:10px; overflow:hidden; margin-bottom:28px; box-shadow:0 2px 8px rgba(99,102,241,0.08);">
                <div style="background-color:#1e1b4b; color:#ffffff; padding:12px 18px; font-size:15px; font-weight:700;">
                  📌 Section 1: Executive Summary (2nd Brain & Codebase Loop)
                </div>
                <div style="padding:18px 20px;">
                  {exec_html}
                </div>
              </div>

              <!-- SECTION 2: GITHUB TRENDING TOP 3 -->
              <div style="background-color:#ffffff; border:1px solid #cbd5e1; border-radius:10px; overflow:hidden; margin-bottom:28px;">
                <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color:#ffffff; padding:12px 18px; font-size:15px; font-weight:700;">
                  ⭐ Section 2: GitHub Trending Top 3 (2nd Brain & Codebase Intelligence)
                </div>
                <div style="padding:18px 20px;">
                  {github_html}
                </div>
              </div>

              <!-- SECTION 3: CATEGORIZED NEWS -->
              <div style="margin-bottom:20px;">
                <div style="font-size:16px; font-weight:800; color:#0f172a; margin-bottom:16px; display:flex; align-items:center;">
                  📊 Section 3: 관심 분야별 심층 뉴스
                </div>
                {categories_html}
              </div>

              <!-- FOOTER / 구독 신청 -->
              <div style="background-color:#f1f5f9; border-radius:8px; padding:20px; text-align:center; margin-top:24px; border:1px solid #e2e8f0;">
                <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:6px;">
                  📬 뉴스레터 수신인 추가하기
                </div>
                <div style="font-size:12px; color:#64748b; margin-bottom:12px;">
                  동료 분들과 함께 이 브리핑을 받아보시려면 아래 링크에서 신청해 주세요.
                </div>
                <a href="{form_url}" style="display:inline-block; background-color:#4f46e5; color:#ffffff; font-size:13px; font-weight:600; padding:8px 18px; border-radius:6px; text-decoration:none;" target="_blank">
                  👉 수신인 추가 신청 링크
                </a>
              </div>

            </td>
          </tr>

          <!-- 저작권 및 안내 푸터 -->
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:18px 24px; text-align:center; font-size:11px; color:#94a3b8;">
              본 리포트는 Google Gemini & OpenAI 기반 자동화 지식 큐레이터 시스템에 의해 생성되었습니다.<br>
              MyWiki Active 2nd Brain Architecture | KIHOKIL
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return html_template

def get_additional_subscribers():
    """CSV URL(구글 스프레드시트 게시)에서 추가 구독자 이메일을 추출합니다."""
    if not SUBSCRIBERS_CSV_URL:
        return []
    try:
        req = urllib.request.Request(SUBSCRIBERS_CSV_URL)
        with urllib.request.urlopen(req, timeout=10) as response:
            csv_data = response.read().decode('utf-8')
        
        emails = set()
        reader = csv.reader(io.StringIO(csv_data))
        for row in reader:
            for cell in row:
                match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cell)
                if match:
                    emails.add(match.group(0).strip())
        return list(emails)
    except Exception as e:
        print(f"구독자 CSV 가져오기 실패: {e}")
        return []

def send_email(subject, content, html_content=None):
    """요약된 뉴스를 멀티파트(텍스트 + HTML) 이메일로 전송합니다."""
    if EMAIL_SENDER == "your_email@gmail.com" or not EMAIL_PASSWORD:
        print("이메일 설정이 되어있지 않아 전송을 건너뜁니다.")
        return

    receivers = set([e.strip() for e in EMAIL_RECEIVER.split(',') if e.strip()])
    additional_receivers = get_additional_subscribers()
    if additional_receivers:
        print(f"추가 구독자 {len(additional_receivers)}명을 확인했습니다.")
        receivers.update(additional_receivers)
    
    receivers_list = list(receivers)
    if not receivers_list:
        print("이메일 수신자가 설정되어 있지 않습니다.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_SENDER
    msg['Bcc'] = ", ".join(receivers_list)
    
    # 텍스트 본문 설정
    msg.set_content(content)
    
    # HTML 본문 추가 (지원 클라이언트용)
    if html_content:
        msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"이메일 전송 성공! (HTML 포맷 포함, 총 {len(receivers_list)}명 발송 완료)")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

def save_to_markdown(date_str, content):
    """요약된 내용을 MyWiki 내 Markdown 파일로 저장합니다."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    save_dir = os.path.join(base_dir, "News", "Daily_Summaries")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        
    KST = timezone(timedelta(hours=9))
    iso_date = datetime.now(KST).strftime("%Y-%m-%d")
    frontmatter = f"---\ntitle: \"[{iso_date}] Group 2nd Brain & Tech Horizon 브리핑\"\ncategory: News\ntags: [news, briefing, daily, second-brain, code-review]\ncreated: {iso_date}\nupdated: {iso_date}\nsources: []\n---\n\n"
    
    file_path = os.path.join(save_dir, f"{iso_date}_News_Briefing.md")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + content)
        print(f"Markdown 파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"Markdown 파일 저장 실패: {e}")

# ==========================================
# 4. 메인 실행 파이프라인
# ==========================================

def main():
    print("🚀 [Daily News & Tech Intelligence] 브리핑 자동화 파이프라인 가동...")
    config = load_config()
    
    KST = timezone(timedelta(hours=9))
    today_str = datetime.now(KST).strftime("%Y년 %m월 %d일")
    has_error = False
    
    # ----------------------------------------------------
    # 단계 1: 관심 분야별 뉴스 수집 및 분석 (Section 3용)
    # ----------------------------------------------------
    print("\n--- [Step 1] 관심 분야별 뉴스 수집 및 AI 요약 ---")
    category_results = []
    category_summary_texts = []
    
    for category in config.get("categories", []):
        cat_name = category["name"]
        queries = category["queries"]
        focus = category["focus"]
        
        print(f"\n[{cat_name}] 뉴스 기사 수집 중...")
        all_articles = []
        for q in queries:
            all_articles.extend(fetch_google_news(q, max_articles=2))
            time.sleep(1)
            
        unique_articles = []
        seen_titles = set()
        for article in all_articles:
            if article["title"] not in seen_titles:
                unique_articles.append(article)
                seen_titles.add(article["title"])
        unique_articles = unique_articles[:12]
        
        print(f"  총 {len(unique_articles)}개 고유 기사 수집 완료. AI 분석 중...")
        try:
            summary = safe_summarize_news(cat_name, focus, unique_articles)
        except Exception as e:
            print(f"  [{cat_name}] Gemini 재시도 실패: {e}")
            if OPENAI_API_KEY:
                try:
                    summary = safe_summarize_news_openai(cat_name, focus, unique_articles)
                    print(f"  [{cat_name}] OpenAI Fallback 요약 성공!")
                except Exception as oe:
                    print(f"  [{cat_name}] OpenAI Fallback 실패: {oe}")
                    summary = "⚠️ API 연동 문제로 AI 요약 생성에 실패했습니다. 아래 원문 기사 링크를 참고해 주세요."
                    has_error = True
            else:
                summary = "⚠️ API 연동 문제로 AI 요약 생성에 실패했습니다. (OPENAI_API_KEY 없음)"
                has_error = True
                
        category_results.append({
            "name": cat_name,
            "summary": summary,
            "articles": unique_articles
        })
        category_summary_texts.append(f"### 📊 {cat_name}\n{summary}")
        
        time.sleep(3) # Rate limit 방지

    combined_category_summary = "\n\n".join(category_summary_texts)

    # ----------------------------------------------------
    # 단계 2: GitHub Trending Top 3 수집 및 분석 (Section 2용)
    # ----------------------------------------------------
    print("\n--- [Step 2] GitHub Trending Top 3 수집 및 심층 분석 ---")
    github_cfg = config.get("github_trend", {})
    github_queries = github_cfg.get("queries", [
        "topic:second-brain", "code review AI", "codebase intelligence", "coding agent implementation"
    ])
    github_focus = github_cfg.get("focus", "2nd Brain 구축 및 Codebase 이해/Code Review/Implementation Loop 연관 글로벌 상위 저장소 3개 요약")
    
    candidates = fetch_github_trending(github_queries, max_candidates=8)
    print(f"  총 {len(candidates)}개 GitHub 후보 저장소 수집 완료. Top 3 선별 분석 중...")
    
    try:
        github_summary = safe_analyze_github_trending(github_focus, candidates)
    except Exception as ge:
        print(f"  [GitHub Trending] Gemini 실패: {ge}")
        if OPENAI_API_KEY:
            try:
                github_summary = safe_analyze_github_trending_openai(github_focus, candidates)
                print("  [GitHub Trending] OpenAI Fallback 성공!")
            except Exception as oe:
                print(f"  [GitHub Trending] OpenAI 마저 실패: {oe}")
                github_summary = "⚠️ GitHub 트렌드 AI 분석에 일시적 오류가 발생했습니다."
                has_error = True
        else:
            github_summary = "⚠️ GitHub 트렌드 AI 분석에 일시적 오류가 발생했습니다."
            has_error = True

    # ----------------------------------------------------
    # 단계 3: Executive Summary 종합 (Section 1용)
    # ----------------------------------------------------
    print("\n--- [Step 3] Executive Summary 종합 (2nd Brain & Codebase Loop) ---")
    try:
        exec_summary = safe_generate_executive_summary(combined_category_summary, github_summary)
    except Exception as ee:
        print(f"  [Executive Summary] Gemini 실패: {ee}")
        if OPENAI_API_KEY:
            try:
                exec_summary = safe_generate_executive_summary_openai(combined_category_summary, github_summary)
                print("  [Executive Summary] OpenAI Fallback 성공!")
            except Exception as oe:
                print(f"  [Executive Summary] OpenAI 실패: {oe}")
                exec_summary = "⚠️ Executive Summary 생성에 실패했습니다."
                has_error = True
        else:
            exec_summary = "⚠️ Executive Summary 생성에 실패했습니다."
            has_error = True

    # ----------------------------------------------------
    # 단계 4: 최종 마크다운 및 HTML 본문 조합
    # ----------------------------------------------------
    print("\n--- [Step 4] 마크다운 및 HTML 이메일 포맷 생성 ---")
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdPTpkieDY9RNHdJohQjH5cd4VYcQG2lCIfFWeI9dsmnKzcbQ/viewform?usp=dialog"
    
    # 1) Markdown Plain Text 본문
    markdown_body = f"# [{today_str}] Group 2nd Brain & Tech Horizon 브리핑\n\n"
    
    markdown_body += "## 📌 Section 1: Executive Summary (2nd Brain & Codebase Loop)\n"
    markdown_body += f"{exec_summary}\n\n"
    markdown_body += "="*50 + "\n\n"
    
    markdown_body += "## ⭐ Section 2: GitHub Trending Top 3 (2nd Brain & Codebase Intelligence)\n"
    markdown_body += f"{github_summary}\n\n"
    markdown_body += "="*50 + "\n\n"
    
    markdown_body += "## 📊 Section 3: 관심 분야별 심층 뉴스\n\n"
    for cat in category_results:
        markdown_body += f"### 🔹 {cat['name']}\n\n{cat['summary']}\n\n"
        markdown_body += "🔗 **참고 기사:**\n"
        for art in cat["articles"][:4]:
            markdown_body += f"- [{art['title']}]({art['link']})\n"
        markdown_body += "\n" + "-"*40 + "\n\n"
        
    markdown_body += "📬 **뉴스레터 수신인 추가하기**\n"
    markdown_body += f"이 브리핑을 다른 분들과 함께 받아보시려면 [수신인 추가 구글 폼]({form_url})에서 등록해 주세요.\n"

    # 2) 반응형 HTML 이메일 본문
    html_body = generate_html_email(today_str, exec_summary, github_summary, category_results, form_url)

    # ----------------------------------------------------
    # 단계 5: 발송 및 아카이브 저장
    # ----------------------------------------------------
    subject = f"📊 [{today_str}] Group 2nd Brain & Tech Horizon 브리핑"
    if has_error:
        subject = f"⚠️ [요약 일부 실패] [{today_str}] Group 2nd Brain & Tech Horizon 브리핑"
        
    print("\n이메일 발송을 시작합니다...")
    send_email(subject, markdown_body, html_content=html_body)
    
    print("\nMyWiki 내 Markdown 아카이브 파일 저장을 시작합니다...")
    save_to_markdown(today_str, markdown_body)
    
    print("\n✅ 모든 브리핑 생성 및 발송 작업이 성공적으로 완료되었습니다.")

if __name__ == "__main__":
    main()
