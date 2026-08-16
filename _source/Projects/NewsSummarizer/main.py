import os
import json
import smtplib
from email.message import EmailMessage
import feedparser
from google import genai
from google.genai import types
from dotenv import load_dotenv
import urllib.parse
from datetime import datetime
import time
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# 환경 변수 로드
load_dotenv()

# 설정값
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver_email@gmail.com")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")

def load_config():
    """config.json 파일에서 카테고리 및 쿼리 설정을 로드합니다."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_google_news(query, max_articles=3):
    """주어진 키워드로 Google News RSS를 검색하여 기사를 가져옵니다."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    
    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return articles

def summarize_news(category_name, focus, articles):
    """Gemini API를 사용하여 기사들을 심층 분석하고 요약합니다."""
    if not articles:
        return f"[{category_name}] 에 대한 최신 뉴스가 수집되지 않았습니다."

    # 애널리스트 시스템 프롬프트 구성
    sys_instruction = f"""당신은 IT, 통신, AI 및 반도체 산업의 글로벌 최고 수준 애널리스트입니다.
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
    
    # 예외가 발생하면 tenacity가 재시도할 수 있도록 에러를 그대로 raise합니다.
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-flash-latest', # 404/429 에러를 피하기 위해 최신 범용 flash 모델 사용
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruction,
            temperature=0.3 # 분석의 일관성을 위해 낮은 온도 설정
        ),
    )
    return response.text

@retry(wait=wait_exponential(multiplier=2, min=4, max=60), stop=stop_after_attempt(5))
def safe_summarize_news(category_name, focus, articles):
    """API 제한을 방지하기 위해 지수 백오프(Exponential Backoff)를 적용한 래퍼 함수입니다."""
    print(f"  [{category_name}] AI 분석을 요청합니다...")
    return summarize_news(category_name, focus, articles)

def send_email(subject, content):
    """요약된 뉴스를 이메일로 전송합니다."""
    if EMAIL_SENDER == "your_email@gmail.com" or not EMAIL_PASSWORD:
        print("이메일 설정이 되어있지 않아 전송을 건너뜁니다.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("이메일 전송 성공!")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

def save_to_markdown(date_str, content):
    """요약된 내용을 MyWiki 내 Markdown 파일로 저장합니다."""
    # 현재 파일 기준 _source/News/Daily_Summaries 폴더 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    save_dir = os.path.join(base_dir, "News", "Daily_Summaries")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        
    # Obsidian Frontmatter 추가
    iso_date = datetime.now().strftime("%Y-%m-%d")
    frontmatter = f"---\ntitle: \"[{iso_date}] 산업 동향 심층 브리핑\"\ncategory: News\ntags: [news, briefing, daily]\ncreated: {iso_date}\nupdated: {iso_date}\nsources: []\n---\n\n"
    
    file_path = os.path.join(save_dir, f"{iso_date}_News_Briefing.md")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + content)
        print(f"Markdown 파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"Markdown 파일 저장 실패: {e}")

def main():
    print("전문가용 심층 뉴스 요약 자동화 시스템 시작...")
    config = load_config()
    
    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    email_body = f"[{today_str}] 글로벌 산업 동향 심층 브리핑\n\n"
    has_error = False
    
    for category in config.get("categories", []):
        cat_name = category["name"]
        queries = category["queries"]
        focus = category["focus"]
        
        print(f"[{cat_name}] 카테고리 기사 수집 중...")
        all_articles = []
        
        # 각 쿼리별로 기사 수집
        for q in queries:
            print(f"  - 검색: {q}")
            all_articles.extend(fetch_google_news(q, max_articles=2)) # 각 키워드별로 2개씩 가져옴
            
        # 중복 기사 제거 (제목 기준)
        unique_articles = []
        seen_titles = set()
        for article in all_articles:
            if article["title"] not in seen_titles:
                unique_articles.append(article)
                seen_titles.add(article["title"])
                
        # 너무 많으면 토큰 낭비 방지를 위해 최근 15개로 제한
        unique_articles = unique_articles[:15]
        
        print(f"총 {len(unique_articles)}개의 고유 기사 수집 완료. AI 분석 중...")
        
        try:
            summary = safe_summarize_news(cat_name, focus, unique_articles)
        except Exception as e:
            print(f"[{cat_name}] 최대 재시도 횟수 초과로 요약 실패: {e}")
            summary = "⚠️ API 연동 문제로 AI 요약 생성에 실패했습니다. 아래 원문 기사 링크를 참고해 주세요."
            has_error = True
            
        email_body += f"#"*3 + f" 📊 {cat_name}\n\n"
        email_body += f"{summary}\n\n"
        
        # (선택) 하단에 출처 링크 첨부
        email_body += "### 🔗 참고 기사 목록:\n"
        for article in unique_articles[:5]: # 너무 많으면 보기 불편하므로 상위 5개만 노출
            email_body += f"- {article['title']}\n  {article['link']}\n"
        email_body += "\n" + "="*50 + "\n\n"
        
        # API Rate Limit (15 RPM) 방지를 위해 카테고리 처리 간 5초 대기
        print("  API Rate Limit 방지를 위해 5초 대기합니다...")
        time.sleep(5)
    
    print("요약 리포트 생성 완료. 이메일 발송을 준비합니다.")
    subject = f"📊 [{today_str}] 글로벌 IT/통신/AI 산업 동향 브리핑"
    if has_error:
        subject = f"⚠️ [요약 일부 실패] [{today_str}] 글로벌 IT/통신/AI 산업 동향 브리핑"
    send_email(subject, email_body)
    
    print("MyWiki 저장소에 Markdown 파일로 저장을 준비합니다.")
    save_to_markdown(today_str, email_body)
    
    print("모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
