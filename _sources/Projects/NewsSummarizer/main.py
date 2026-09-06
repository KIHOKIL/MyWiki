import sys
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

# Windows 콘솔 환경(CP949) 이모지 및 유니코드 출력 호환성 보장
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

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

# 4대 필수 탐색 주제별 검증된 실존 레포지토리 (All-time Classics & High-quality Curations)
DEFAULT_CURATED_REPOS = {
    "second_brain": {
        "name": "Second-Brain",
        "icon": "🧠",
        "repos": [
            {
                "full_name": "logseq/logseq",
                "html_url": "https://github.com/logseq/logseq",
                "description": "A privacy-first, open-source platform for knowledge management and collaboration.",
                "stars": 34200,
                "language": "Clojure / JavaScript",
                "category_id": "second_brain",
                "category_name": "Second-Brain",
                "category_icon": "🧠",
                "role_type": "스테디셀러"
            },
            {
                "full_name": "tinyhumansai/openhuman",
                "html_url": "https://github.com/tinyhumansai/openhuman",
                "description": "Local-first private memory and agent orchestration for personal/team knowledge bases.",
                "stars": 39500,
                "language": "Python / TypeScript",
                "category_id": "second_brain",
                "category_name": "Second-Brain",
                "category_icon": "🧠",
                "role_type": "루키"
            }
        ]
    },
    "code_review_ai": {
        "name": "Code Review AI",
        "icon": "🔍",
        "repos": [
            {
                "full_name": "qodo-ai/pr-agent",
                "html_url": "https://github.com/qodo-ai/pr-agent",
                "description": "An AI-powered tool for automated pull request review, feedback, and suggestions.",
                "stars": 6500,
                "language": "Python",
                "category_id": "code_review_ai",
                "category_name": "Code Review AI",
                "category_icon": "🔍",
                "role_type": "스테디셀러"
            },
            {
                "full_name": "tirth8205/code-review-graph",
                "html_url": "https://github.com/tirth8205/code-review-graph",
                "description": "Local-first context reduction graph for PR code review and agentic workflows.",
                "stars": 31200,
                "language": "TypeScript / Python",
                "category_id": "code_review_ai",
                "category_name": "Code Review AI",
                "category_icon": "🔍",
                "role_type": "루키"
            }
        ]
    },
    "codebase_understanding": {
        "name": "Codebase understanding",
        "icon": "🧭",
        "repos": [
            {
                "full_name": "ast-grep/ast-grep",
                "html_url": "https://github.com/ast-grep/ast-grep",
                "description": "A CLI tool for code structural search, lint, and rewriting based on abstract syntax tree.",
                "stars": 11200,
                "language": "Rust",
                "category_id": "codebase_understanding",
                "category_name": "Codebase understanding",
                "category_icon": "🧭",
                "role_type": "스테디셀러"
            },
            {
                "full_name": "DeusData/codebase-memory-mcp",
                "html_url": "https://github.com/DeusData/codebase-memory-mcp",
                "description": "Zero-dependency C AST graph MCP server providing fast persistent codebase intelligence.",
                "stars": 42000,
                "language": "C",
                "category_id": "codebase_understanding",
                "category_name": "Codebase understanding",
                "category_icon": "🧭",
                "role_type": "루키"
            }
        ]
    },
    "embedded_sw": {
        "name": "Embedded SW implementation",
        "icon": "⚡",
        "repos": [
            {
                "full_name": "FreeRTOS/FreeRTOS-Kernel",
                "html_url": "https://github.com/FreeRTOS/FreeRTOS-Kernel",
                "description": "FreeRTOS kernel files and ports for real-time embedded systems architecture.",
                "stars": 5600,
                "language": "C",
                "category_id": "embedded_sw",
                "category_name": "Embedded SW implementation",
                "category_icon": "⚡",
                "role_type": "스테디셀러"
            },
            {
                "full_name": "embassy-rs/embassy",
                "html_url": "https://github.com/embassy-rs/embassy",
                "description": "Modern async embedded runtime and HAL drivers in Rust for microcontrollers.",
                "stars": 5800,
                "language": "Rust",
                "category_id": "embedded_sw",
                "category_name": "Embedded SW implementation",
                "category_icon": "⚡",
                "role_type": "루키"
            }
        ]
    }
}

def is_valid_github_repo(item):
    """스팸성, 어뷰징 및 알맹이 없는 Awesome-list 저장소를 필터링합니다."""
    name = (item.get("name") or "").lower()
    full_name = (item.get("full_name") or "").lower()
    desc = (item.get("description") or "").lower()
    
    # Awesome-list 필터링
    if name.startswith("awesome-") or full_name.startswith("awesome-") or "awesome list" in desc:
        return False
    # 빈 설명 필터링
    if not desc or len(desc.strip()) < 5:
        return False
    return True

def fetch_github_trending(categories_or_queries=None, max_candidates=16):
    """
    GitHub Search API를 사용하여 4대 관심 주제별 최상위 오픈소스 저장소를 수집합니다.
    categories_or_queries: config.json의 카테고리 설정(list of dicts) 또는 쿼리 리스트(list of strings)
    """
    default_cat_list = [
        {"id": "second_brain", "name": "Second-Brain", "icon": "🧠", "queries": ["topic:second-brain", "personal knowledge management AI", "obsidian agent"]},
        {"id": "code_review_ai", "name": "Code Review AI", "icon": "🔍", "queries": ["code review AI", "PR agent LLM", "automated code review"]},
        {"id": "codebase_understanding", "name": "Codebase understanding", "icon": "🧭", "queries": ["codebase intelligence", "code graph AST", "codebase understanding MCP"]},
        {"id": "embedded_sw", "name": "Embedded SW implementation", "icon": "⚡", "queries": ["embedded RTOS", "firmware driver HAL", "embedded software architecture", "real-time embedded"]}
    ]

    # 입력 형태 판별 (카테고리 딕셔너리 리스트 vs 단순 쿼리 문자열 리스트)
    if isinstance(categories_or_queries, list) and categories_or_queries and isinstance(categories_or_queries[0], dict):
        cat_configs = categories_or_queries
    elif isinstance(categories_or_queries, list) and categories_or_queries and isinstance(categories_or_queries[0], str):
        cat_configs = [{"id": "custom", "name": "Custom Topic", "icon": "⭐", "queries": categories_or_queries}]
    else:
        cat_configs = default_cat_list

    candidates = []
    seen_repos = set()
    headers = {
        'User-Agent': 'DailyNewsSummarizer/2.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f"token {GITHUB_TOKEN}"

    for cat in cat_configs:
        cat_id = cat.get("id", "general")
        cat_name = cat.get("name", "General")
        cat_icon = cat.get("icon", "⭐")
        queries = cat.get("queries", [])
        cat_repos = []

        for query in queries:
            try:
                encoded_query = urllib.parse.quote(query)
                url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=4"
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    for item in data.get("items", []):
                        if not is_valid_github_repo(item):
                            continue
                        full_name = item.get("full_name")
                        if full_name and full_name not in seen_repos:
                            seen_repos.add(full_name)
                            repo_obj = {
                                "full_name": full_name,
                                "html_url": item.get("html_url", ""),
                                "description": item.get("description") or "설명 없음",
                                "stars": item.get("stargazers_count", 0),
                                "language": item.get("language") or "General",
                                "topics": item.get("topics", []),
                                "category_id": cat_id,
                                "category_name": cat_name,
                                "category_icon": cat_icon
                            }
                            cat_repos.append(repo_obj)
                            candidates.append(repo_obj)
            except Exception as e:
                print(f"  [Warning] GitHub API 검색 실패 ('{query}'): {e}")
            time.sleep(1)

        # 해당 카테고리 검색 결과가 0건인 경우 검증된 실존 Fallback 추가
        if not cat_repos and cat_id in DEFAULT_CURATED_REPOS:
            for fallback_repo in DEFAULT_CURATED_REPOS[cat_id]["repos"]:
                if fallback_repo["full_name"] not in seen_repos:
                    seen_repos.add(fallback_repo["full_name"])
                    candidates.append(fallback_repo)

    # 전체 후보가 전혀 없는 경우 전체 Fallback 통합 주입
    if not candidates:
        print("  [Notice] GitHub API 결과 부재 또는 요청 제한으로 4대 카테고리 기본 큐레이션 저장소를 활용합니다.")
        for cat_id, cat_info in DEFAULT_CURATED_REPOS.items():
            for repo in cat_info["repos"]:
                if repo["full_name"] not in seen_repos:
                    seen_repos.add(repo["full_name"])
                    candidates.append(repo)

    return candidates[:max_candidates]

# ==========================================
# 2. LLM 요약 및 분석 모듈
# ==========================================

# --- 카테고리 뉴스 분석 ---
def _build_news_prompt(category_name, focus, articles):
    cat_lower = category_name.lower()
    if "mobile communication" in cat_lower or "telecom" in cat_lower or "mobility" in cat_lower:
        sys_instruction = """# 💎 Name: Telecom & Mobility Strategy C-Pilot (통신·모빌리티 전략 분석기)
# 🎯 슬로건: "기술의 변화를 비즈니스의 수익 모델과 생존 전략으로 번역합니다."

## 1. 역할 및 정체성 (Role & Identity)
- 당신은 글로벌 최고 수준의 **'통신 및 스마트 모빌리티 신사업 전략 분석가(C-Level Strategy Advisor)'**입니다.
- 통신사, UE/네트워크 벤더, 반도체 기업들이 모바일(Mobile)과 셀룰러(Cellular)의 수익성 한계를 극복하기 위해 비-모바일(Non-mobile), 맞춤형 반도체(Custom SoC), CPE/Broadband, Wi-Fi 오프로딩 등으로 **'사업을 어떻게 다각화하고 있는지'**를 정밀하게 추적하고 분석합니다.
- 당신의 보고서를 읽는 대상은 **전략 기획 및 신사업 발굴을 담당하는 임원진(C-Level)**입니다. 따라서 기술 용어 자체의 나열보다는 "이 기술이 비즈니스 모델(BM)과 수익성에 어떤 영향을 미치는가(SWOT/위협과 기회)"를 중심으로 보고해야 합니다.

## 2. 핵심 임무 (Core Mission)
- 수집된 뉴스 기사들을 분석하여 노이즈를 제거하고 핵심 비즈니스 지표만 추출합니다.
- 분석된 결과를 바탕으로 기업별 다각화 전략 매트릭스가 포함된 **[주간/이슈별 전략 인텔리전스 브리핑]**을 생성하는 것이 유일한 목표입니다.
- **주요 모니터링 타겟 기업군 (항상 예의주시할 것):**
  1. 커스텀 SoC/인프라 칩: Broadcom, Marvell, Qualcomm, MediaTek, NXP
  2. 모듈/CPE/FWA 제조사: Fibocom, Quectel, WNC, Arcadyan, Sierra Wireless
  3. 네트워크 장비 벤더: Ericsson, Nokia, Cisco, Juniper, Huawei
  4. 혁신 망/모빌리티: Starlink, Wi-Fi 7 및 UWB 벤더, 전통 통신사업자(Telco)

## 3. 작업 프로세스 (Step-by-Step Workflow)
사용자의 요청(기사 입력 등)을 받으면 반드시 다음 순서로 사고하고 실행하십시오:
1. **[필터링 및 팩트 추출]:** 입력된 데이터가 통신/모빌리티 산업의 다각화 전략과 관련이 있는지 검증하고, 주요 팩트(투자 규모, 제휴사, 출시 스펙 등)를 추출합니다.
2. **[비즈니스 임팩트 번역]:** 추출된 기술적 사실이 벤더의 수익 모델이나 시장 점유율에 미칠 영향을 분석합니다.
3. **[매트릭스 맵핑]:** 해당 기업의 '기존 주력 사업'과 '신규 다각화 영역'을 비교 분석합니다.
4. **[출력 및 후속 제안]:** 지정된 마크다운 포맷에 따라 보고서를 출력하고, 심층 분석을 위한 후속 질문 2~3개를 생성합니다.

## 4. 엄격한 규칙 및 제약 (Strict Constraints)
- ❌ **숫자/재무 지표 환각(Hallucination) 절대 금지:** 기사에 명시되지 않은 매출, 투자 규모, 상세 스펙 등은 절대 임의로 추측하지 않으며, 알 수 없는 경우 "미상(N/A)"으로 표기합니다.
- ❌ **맥락 없는 기술 용어 나열 금지:** 기술적 사실(예: "Wi-Fi 7 MAC 계층 변경")만 언급하지 말고, 반드시 비즈니스 영향(예: "이로 인해 B2B 망 구축 TCO 절감")을 병기하십시오.
- 💡 **언어 및 표기법:** 보고서의 기본 언어는 100% 한국어로 작성하되 비즈니스 현장감을 살리기 위해 핵심 고유명사와 전문 용어는 영문을 병기합니다. (예: 고객 구내 설비(CPE), 맞춤형 시스템 반도체(Custom SoC))

## 5. 예외 및 오류 처리 (Edge Case Handling)
- 만약 수집된 기사 중 통신/모빌리티 사업 다각화와 직접 관련된 기사가 적더라도, 수집된 기사들에서 사업적 다각화 및 기술 변화 시사점을 최대한 도출하여 표준 포맷을 유지하십시오. 기사가 전무한 경우에만 알림을 남기십시오.

## 6. 출력 표준 포맷 (Output Format)
반드시 아래의 마크다운 구조를 단 한 치의 오차 없이 준수하십시오:

### 📊 [분석 대상 기업명 또는 주요 기술명] 전략 인텔리전스 브리핑

**1. 핵심 요약 (Executive Summary)**
- [3줄 이내의 Bullet Point로 기사의 가장 핵심적인 비즈니스 동향 요약]
- [기술 변화가 의미하는 시장의 흐름 요약]

**2. 전략적 임팩트 분석 (Business Impact Analysis)**
- **수익 모델 변화:** [셀룰러/모바일 한계 극복을 위한 새로운 캐시카우 분석]
- **시장 위협 및 기회 (SWOT 관점):** [해당 행보가 타 벤더나 통신망 생태계에 미칠 영향]

**3. 벤더 다각화 매트릭스 (Diversification Matrix)**
| 기업명 | 기존 핵심 캐시카우 (Legacy) | 신규 다각화 영역 (New Growth) | 핵심 파트너십 / 기술 자산 |
|---|---|---|---|
| [기업A] | [예: Mobile SoC] | [예: Custom ASIC, AI Infra] | [내용] |
| [기업B] | [예: Cellular Module] | [예: 5G FWA CPE, Edge AI] | [내용] |
*(기사에 등장하는 주요 플레이어 중심으로 작성)*

---
**💡 후속 심층 분석 제안 (Next Steps)**
*(더 깊게 파고들 수 있는 질문 2~3개를 아래와 같이 제안하십시오)*
- 🔍 [후속 질문 1]
- 🔍 [후속 질문 2]
"""
        prompt = f"""[특별 분석 포인트]
{focus}

[수집된 뉴스 기사 헤드라인 목록]
"""
        for i, article in enumerate(articles, 1):
            prompt += f"{i}. {article['title']}\n"
        return sys_instruction, prompt

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

# --- Section 2: GitHub Trending (시니어 멘토 개발자 4대 분야 큐레이션) ---
def _build_github_prompt(focus, candidates):
    sys_instruction = """# 데일리 GitHub 트렌드 큐레이터: 시니어 멘토 개발자

## 1. 역할 및 정체성 (Role & Identity)
- 당신은 트렌드에 민감하면서도 실무 적용의 가치를 최우선으로 생각하는 20년 차 시니어 개발자(멘토)입니다.
- 타겟 오디언스(실무 개발 리더 및 엔지니어)의 눈높이에 맞춰, 과장되지 않고 담백한 기술적 용어와 친근한 조언의 어조("오늘 흥미로운 프로젝트를 발견했습니다", "이 구조는 실무에 참고하기 좋겠네요")로 소통합니다.

## 2. 핵심 임무 (Core Mission)
- GitHub Search API 및 최신 데이터를 활용하여 사용자가 지정한 4가지 관심 주제에 부합하는, 인지도 높고 평가가 좋은 오픈소스 프로젝트를 엄선합니다.
- 매일 아침 이메일로 바로 발송할 수 있는 [카테고리 분류형 뉴스레터 초안]을 작성하는 것이 유일한 목표입니다.
- **필수 탐색 주제 4가지:**
  1. Second-Brain (지식 관리, 노트 연결 시스템 등)
  2. Code Review AI (자동화된 리뷰, 정적 분석, LLM 기반 리뷰어 등)
  3. Codebase understanding (대규모 코드 분석, 아키텍처 시각화, 컨텍스트 파악 도구 등)
  4. Embedded SW implementation (HW 가이드라인 기반 설계, 프로토콜 스택, 물리 계층/인터페이스 제어, 실시간(RTOS) 최적화 관련)

## 3. 작업 프로세스 (Step-by-Step Workflow)
1. **[데이터 확보 및 심층 검증]:** 제공된 4대 주제별 후보 저장소를 검토하고 스팸/Awesome-list를 배제합니다.
2. **[균형 큐레이션]:** 각 카테고리별로 가능하면 이미 검증된 '스테디셀러(Star 다수)' 1개와 최근 떠오르는 '루키(Trending)' 1개를 조합하여 선정합니다.
3. **[인사이트 도출]:** 단순 Readme 요약이 아닌, "왜 실제 개발자들이 이 프로젝트를 좋게 평가하는가?", "실무 도입 시 어떤 페인포인트(Pain-point)를 해결할 수 있는가?"를 분석합니다.
4. **[초안 작성]:** 이메일 템플릿에 맞추어 시니어 개발자의 톤으로 본문을 작성합니다.

## 4. 엄격한 규칙 및 제약 (Strict Constraints)
- ❌ **할루시네이션(환각) 절대 금지:** 제공된 후보 목록에 없는 가짜 GitHub 링크나 임의로 만들어낸 레포지토리 정보는 절대 출력하지 마십시오. 오직 팩트 기반으로 작성합니다.
- ❌ **버즈워드(Buzzword) 금지:** 지나치게 마케팅적이거나 과장된 표현("혁명적인", "세상을 바꿀")을 피하고, 철저히 개발자 친화적이고 담백한 기술 용어만 사용하십시오.
- ❌ **주제 이탈 금지:** 설정된 4가지 관심 주제를 벗어난 프로젝트는 아무리 인기가 많아도 절대 추천하지 않습니다.

## 5. 예외 및 오류 처리 (Edge Case Handling)
- 만약 특정 카테고리에서 오늘 추천할 만한 '새롭거나 퀄리티 높은' 루키를 찾지 못했다면 해당 섹션을 생략하지 마십시오.
- 대신 해당 분야의 **'불변의 명작(All-time Classic)' 프로젝트**를 소개하되, "이미 아시겠지만, 이 프로젝트의 [특정 아키텍처/코드 패턴]은 다시 볼 가치가 있습니다"라는 새로운 실무적 시각이나 리팩토링 관점의 인사이트를 덧붙여서 제안하십시오.

## 6. 출력 표준 포맷 (Output Format)
응답은 반드시 아래의 마크다운 구조를 단 한 치의 오차 없이 그대로 준수하여 출력하십시오:

## 📬 오늘의 GitHub 트렌드 큐레이션
안녕하세요. 오늘 아침 스캐닝한 흥미로운 오픈소스 프로젝트들을 정리해 드립니다. 바쁘시더라도 각 분야별로 실무에 영감을 줄 만한 코드들은 꼭 한 번 살펴보시길 권장합니다.

---
### 🧠 1. Second-Brain
**[프로젝트명 A (스테디셀러)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

**[프로젝트명 B (루키)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

### 🔍 2. Code Review AI
**[프로젝트명 A (스테디셀러)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

**[프로젝트명 B (루키)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

### 🧭 3. Codebase understanding
**[프로젝트명 A (스테디셀러)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

**[프로젝트명 B (루키)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

### ⚡ 4. Embedded SW implementation
**[프로젝트명 A (스테디셀러)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

**[프로젝트명 B (루키)]** - [GitHub URL]
- **Overview:** (1~2줄의 명확하고 기술적인 개요)
- **Senior's Insight:** (실제 개발자들이 좋게 평가하는 이유 및 실무 적용 팁)

---
오늘도 버그 없는 하루 되시길 바랍니다!
"""

    # 후보군을 4대 카테고리별로 분류/그룹화
    grouped = {
        "second_brain": [],
        "code_review_ai": [],
        "codebase_understanding": [],
        "embedded_sw": []
    }
    
    for c in candidates:
        cat_id = c.get("category_id")
        if cat_id in grouped:
            grouped[cat_id].append(c)
        else:
            # 카테고리가 명시되지 않은 경우 텍스트 기반 매핑
            desc = (c.get("description", "") + " " + c.get("full_name", "")).lower()
            if any(k in desc for k in ["embedded", "rtos", "hal", "firmware", "driver"]):
                grouped["embedded_sw"].append(c)
            elif any(k in desc for k in ["review", "pr-agent", "pull request", "linter"]):
                grouped["code_review_ai"].append(c)
            elif any(k in desc for k in ["ast", "codebase", "graph", "syntax", "intelligence"]):
                grouped["codebase_understanding"].append(c)
            else:
                grouped["second_brain"].append(c)

    prompt = "[수집된 4대 분야 GitHub 후보 저장소 목록]\n\n"
    category_meta = [
        ("second_brain", "🧠 1. Second-Brain"),
        ("code_review_ai", "🔍 2. Code Review AI"),
        ("codebase_understanding", "🧭 3. Codebase understanding"),
        ("embedded_sw", "⚡ 4. Embedded SW implementation")
    ]

    for cat_id, cat_title in category_meta:
        repos = grouped[cat_id]
        if not repos and cat_id in DEFAULT_CURATED_REPOS:
            repos = DEFAULT_CURATED_REPOS[cat_id]["repos"]
        
        prompt += f"### {cat_title}\n"
        for r in repos[:4]:
            role = f" ({r['role_type']})" if "role_type" in r else ""
            prompt += f"- [{r['full_name']}]({r['html_url']}) (Stars: {r.get('stars', 0):,}, Lang: {r.get('language', 'General')}){role}\n"
            prompt += f"  설명: {r.get('description', '설명 없음')}\n"
        prompt += "\n"

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
    print("  [GitHub Trending] Gemini 4대 분야 분석 요청 중...")
    return analyze_github_gemini(focus, candidates)

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_analyze_github_trending_openai(focus, candidates):
    print("  [GitHub Trending] OpenAI (Fallback) 4대 분야 분석 요청 중...")
    return analyze_github_openai(focus, candidates)

# --- Section 1: Executive Summary (2nd Brain, Codebase Loop & AI Frontier Strategy 종합) ---
def _build_executive_prompt(articles_summary_text, github_summary_text):
    sys_instruction = """당신은 글로벌 엔터프라이즈 AI 시스템 및 소프트웨어 엔지니어링 최고 임원(VP of Engineering & Chief AI Strategist)입니다.
오늘 수집된 글로벌 뉴스 및 GitHub 오픈소스 트렌드를 관통 분석하여, 데일리 브리핑 최상단에 위치할 [Executive Summary: 2nd Brain, Codebase Loop & Big Tech Strategy]를 작성하세요.

[핵심 분석 4대 렌즈]
1) **Group 2nd Brain 구축**: 사내 이메일, 메신저, Jira, Confluence 연동을 통한 팀 지식 허브 구축 및 보안/개인정보 거버넌스.
2) **Codebase 이해 기반 Implementation Loop & Code Review**: 대규모 코드베이스의 구조적 이해, AST 그래프, TDD 자동화, LLM 기반 정밀 코드 리뷰.
3) **Embedded SW Implementation**: HW 가이드라인 기반 설계, 프로토콜 스택, 물리 계층/인터페이스 제어, 실시간(RTOS) 최적화의 에이전틱 전환.
4) **Global Big Tech & AI Frontier 자본 흐름**: 빅테크 및 AI 프론티어(OpenAI, Anthropic, xAI, Databricks 등)의 M&A, 변형적 인수(Acqui-hire), 대규모 컴퓨팅 동맹 및 생태계 락인(Lock-in) 전략이 미치는 영향.

[필수 작성 구조]
반드시 다음 3가지 소제목으로 구성하고 글머리 기호(Bulleted list)를 활용해 명확하게 기술하세요:

### 🚀 오늘 주목해야 할 핵심 혁신 (Key Innovations)
- 2nd Brain 아키텍처, 코드베이스 분석/구현 루프, 임베디드 SW 최적화, 빅테크/AI 프론티어의 전략적 인수 및 인프라 도약 관점에서 오늘 포착된 주요 기술 혁신 요약.

### ⚠️ 핵심 리스크 및 과제 (Core Risks & Trade-offs)
- 사내 민감 데이터 연동 시의 보안/권한 누수, LLM Context 한계로 인한 코드베이스/임베디드 환각(Hallucination), 빅테크 플랫폼 종속성(Lock-in) 및 반독점/컴플라이언스 리스크 지적.

### 🎯 실무 적용 및 설계 시사점 (Actionable Takeaways)
- 현재 사내 Group 2nd Brain 설계, 코드 리뷰/구현 루프, 임베디드 및 엔터프라이즈 툴체인 선정에 즉시 반영해야 할 실행 지침 2~3가지 제시.
"""
    prompt = f"""[오늘의 카테고리별 뉴스 분석 내용]
{articles_summary_text}

[오늘의 GitHub 트렌드 큐레이션 내용 (시니어 멘토 개발자)]
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
    in_table = False
    is_table_header = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_table:
                html_lines.append("</tbody></table></div>")
                in_table = False
                is_table_header = True
            continue

        # 마크다운 테이블 처리 (| 로 시작하고 | 로 끝나는 행)
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            
            # 구분선 행 (|---|---|...) 감지 시 헤더 종료
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                is_table_header = False
                continue

            cells = [c.strip() for c in stripped.strip('|').split('|')]

            if not in_table:
                in_table = True
                is_table_header = True
                html_lines.append('<div style="overflow-x:auto; margin:14px 0 16px 0;"><table style="border-collapse:collapse; width:100%; min-width:480px; font-size:13px; border:1px solid #cbd5e1; border-radius:6px; background-color:#ffffff;">')
                html_lines.append('<thead><tr style="background-color:#f1f5f9;">')
                for cell in cells:
                    html_lines.append(f'<th style="padding:10px 12px; border:1px solid #cbd5e1; color:#0f172a; font-size:13px; font-weight:700; text-align:left;">{cell}</th>')
                html_lines.append('</tr></thead><tbody>')
            else:
                if is_table_header:
                    html_lines.append('<tr style="background-color:#f8fafc;">')
                    for cell in cells:
                        html_lines.append(f'<th style="padding:8px 12px; border:1px solid #cbd5e1; color:#0f172a; font-size:13px; font-weight:700; text-align:left;">{cell}</th>')
                    html_lines.append('</tr>')
                else:
                    html_lines.append('<tr>')
                    for cell in cells:
                        html_lines.append(f'<td style="padding:8px 12px; border:1px solid #e2e8f0; font-size:13px; color:#334155; line-height:1.5;">{cell}</td>')
                    html_lines.append('</tr>')
            continue

        # 테이블 밖으로 벗어난 경우 테이블 닫기
        if in_table:
            html_lines.append("</tbody></table></div>")
            in_table = False
            is_table_header = True

        # 수평 구분선
        if stripped in ["---", "***"]:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append('<hr style="border:0; border-top:1px dashed #cbd5e1; margin:18px 0;">')
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
            if "Second-Brain" in title or "🧠" in title:
                border_color = "#8b5cf6"
                bg_color = "#f5f3ff"
            elif "Code Review" in title or "🔍" in title:
                border_color = "#3b82f6"
                bg_color = "#eff6ff"
            elif "Codebase" in title or "🧭" in title:
                border_color = "#0ea5e9"
                bg_color = "#f0f9ff"
            elif "Embedded" in title or "⚡" in title:
                border_color = "#f59e0b"
                bg_color = "#fffbeb"
            elif "혁신" in title or "🚀" in title:
                border_color = "#10b981"
                bg_color = "#f0fdf4"
            elif "리스크" in title or "⚠️" in title:
                border_color = "#ef4444"
                bg_color = "#fef2f2"
            elif "시사점" in title or "🎯" in title or "적용" in title:
                border_color = "#3b82f6"
                bg_color = "#eff6ff"
            elif "전략 인텔리전스" in title or "📊" in title or "Telecom" in title or "Mobility" in title:
                border_color = "#0284c7"
                bg_color = "#f0f9ff"

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
    if in_table:
        html_lines.append("</tbody></table></div>")

    content_html = "\n".join(html_lines)

    # 볼드 체 처리
    content_html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#0f172a; font-weight:600;">\1</strong>', content_html)
    # Senior's Insight 및 Overview 뱃지 포인트 스타일링
    content_html = re.sub(r'<strong style="color:#0f172a; font-weight:600;">(Senior\'s Insight:?)</strong>', r'<span style="display:inline-block; background-color:#d1fae5; color:#065f46; font-size:12px; font-weight:700; padding:2px 6px; border-radius:4px; margin-right:4px;">💡 Senior\'s Insight</span>', content_html)
    content_html = re.sub(r'<strong style="color:#0f172a; font-weight:600;">(Overview:?)</strong>', r'<span style="display:inline-block; background-color:#e0e7ff; color:#3730a3; font-size:12px; font-weight:700; padding:2px 6px; border-radius:4px; margin-right:4px;">🎯 Overview</span>', content_html)
    # C-Pilot 뱃지 포인트 스타일링
    content_html = re.sub(r'<strong style="color:#0f172a; font-weight:600;">(수익 모델 변화:?)</strong>', r'<span style="display:inline-block; background-color:#e0f2fe; color:#0369a1; font-size:12px; font-weight:700; padding:2px 6px; border-radius:4px; margin-right:4px;">💰 수익 모델 변화</span>', content_html)
    content_html = re.sub(r'<strong style="color:#0f172a; font-weight:600;">(시장 위협 및 기회 \(SWOT 관점\):?)</strong>', r'<span style="display:inline-block; background-color:#fef3c7; color:#92400e; font-size:12px; font-weight:700; padding:2px 6px; border-radius:4px; margin-right:4px;">⚖️ SWOT 분석</span>', content_html)
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

              <!-- SECTION 2: GITHUB TRENDING (SENIOR MENTOR DEVELOPER) -->
              <div style="background-color:#ffffff; border:1px solid #cbd5e1; border-radius:10px; overflow:hidden; margin-bottom:28px;">
                <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color:#ffffff; padding:12px 18px; font-size:15px; font-weight:700;">
                  📬 Section 2: 오늘의 GitHub 트렌드 큐레이션 (시니어 멘토 개발자 Pick)
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
    # 단계 2: GitHub Trending 4대 분야 수집 및 심층 큐레이션 (Section 2용)
    # ----------------------------------------------------
    print("\n--- [Step 2] GitHub Trending 4대 분야 수집 및 심층 큐레이션 (시니어 멘토 개발자) ---")
    github_cfg = config.get("github_trend", {})
    categories_cfg = github_cfg.get("categories") or github_cfg.get("queries")
    github_focus = github_cfg.get("focus", "4대 필수 탐색 주제별 검증된 스테디셀러 1개와 신흥 루키 1개를 엄선하여 담백한 멘토링 인사이트 제공")
    
    candidates = fetch_github_trending(categories_cfg, max_candidates=16)
    print(f"  총 {len(candidates)}개 GitHub 후보 저장소 수집 완료. 4대 분야 심층 큐레이션 중...")
    
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
    
    markdown_body += "## 📬 Section 2: 오늘의 GitHub 트렌드 큐레이션 (시니어 멘토 개발자 Pick)\n"
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
