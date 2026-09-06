import sys
import os
import json
import smtplib
from email.message import EmailMessage
import urllib.parse
import urllib.request
import csv
import io
import re
from datetime import datetime, timezone, timedelta
from google import genai
from dotenv import load_dotenv

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").replace('\xa0', '').replace(' ', '')
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")
SUBSCRIBERS_CSV_URL = os.getenv("SUBSCRIBERS_CSV_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_google_news(query, max_articles=3):
    import feedparser
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            feed = feedparser.parse(response.read())
        return [{"title": e.title, "link": e.link} for e in feed.entries[:max_articles]]
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def generate_finance_report(news_data):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
# [Money Snowball]: 커스텀 매크로 투자 나침반 & 데일리 전략 브리핑 엔진

## 1. 역할 및 정체성 (Role & Identity)
- 당신은 10년 이상의 장기 자산 배분(US 주식 ETF, 금, 채권)을 운용하는 진지한 투자자를 돕는 수석 미국 주식 매크로 전략가 'Money Snowball'입니다.
- 워렌 버핏의 'Snowball(복리)' 철학과 오건영/하워드 마크스 수준의 '거시 경제(Macro) 통찰력'을 결합하여 시장을 분석합니다.
- 어떠한 사담이나 인사말 없이 즉시 마크다운 형식의 결과물만 출력하는 'One-shot' 봇입니다.

## 2. 수집된 뉴스 데이터
{json.dumps(news_data, ensure_ascii=False, indent=2)}

## 3. 출력 형식
반드시 아래의 형식을 지켜주세요.

```yaml
---
title: "US Market Daily Macro Briefing"
category: "Finance/Macro"
tags: [US-Market, Macro, ETF, Gold, Bonds]
created: "{datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')}"
---
```

# 📊 Money Snowball Daily Macro Briefing

## 1. 💡 Snowball Insight (오늘의 투자 나침반)
(장기 자산 배분 투자자를 위한 최종 요약 및 전략 제언)

## 2. 🌐 Global Macro & Policy (거시 경제 및 연준 정책)
(수집된 뉴스를 바탕으로 오건영/하워드 마크스 스타일의 분석을 제공하세요)

## 3. 📈 US Equity ETFs & Sectors (미국 주식 및 ETF 동향)
(자금 흐름과 섹터 로테이션, 장기 투자 관점의 시사점)

## 4. 🛡️ Safe Havens & Yields (안전 자산 및 채권 금리)
(금 가격 동향, 국채 금리 변동 및 채권 시장 시사점)
"""
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    return response.text

def markdown_to_clean_html(markdown_text):
    """주요 마크다운 요소를 이메일 친화적인 인라인 CSS 기반 HTML로 변환합니다."""
    html_lines = []
    lines = markdown_text.split('\n')
    
    in_list = False
    in_table = False
    is_table_header = False

    for line in lines:
        stripped = line.strip()
        
        # YAML Frontmatter 무시
        if stripped == "---" and not html_lines:
            continue
            
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_table:
                html_lines.append("</tbody></table></div>")
                in_table = False
                is_table_header = True
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            
            if re.match(r'^\|[-\s:]+\|', stripped):
                is_table_header = False
                continue

            cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
            
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

        if in_table:
            html_lines.append("</tbody></table></div>")
            in_table = False
            is_table_header = True

        if stripped in ["---", "***"]:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append('<hr style="border:0; border-top:1px dashed #cbd5e1; margin:18px 0;">')
            continue

        if stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            title = stripped[4:]
            
            border_color = "#4f46e5"
            bg_color = "#f8fafc"
            
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
            html_lines.append(f'<div style="margin:6px 0; line-height:1.6; font-size:14px; color:#334155;"><strong style="color:#059669;">{num}</strong> {item_text}</div>')
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
    content_html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#0f172a; font-weight:600;">\1</strong>', content_html)
    content_html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', content_html)
    content_html = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" style="color:#059669; text-decoration:none; font-weight:600; border-bottom:1px dashed #059669;" target="_blank">\1</a>', content_html)

    return content_html

def generate_html_email(date_str, report_md, form_url):
    """모던하고 구조화된 프리미엄 반응형 HTML 이메일 템플릿을 생성합니다."""
    
    # YAML 파트 제거 (디스플레이용)
    report_md = re.sub(r'```yaml.*?```', '', report_md, flags=re.DOTALL).strip()
    
    report_html = markdown_to_clean_html(report_md)
    
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[{date_str}] 글로벌 매크로 및 금융 시장 브리핑</title>
</head>
<body style="margin:0; padding:0; background-color:#f8fafc; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#1e293b; line-height:1.6;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed; background-color:#f8fafc;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:680px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.06); border:1px solid #e2e8f0;">
          
          <!-- 헤더 배너 -->
          <tr>
            <td style="background: linear-gradient(135deg, #064e3b 0%, #065f46 60%, #047857 100%); padding: 32px 28px; text-align: left;">
              <div style="font-size:11px; font-weight:700; color:#34d399; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                DAILY INTELLIGENCE & KNOWLEDGE BRIEFING
              </div>
              <h1 style="margin:0; color:#ffffff; font-size:22px; font-weight:800; letter-spacing:-0.5px;">
                Money Snowball Macro Briefing
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
              <div style="background-color:#ffffff; border:2px solid #10b981; border-radius:10px; overflow:hidden; margin-bottom:28px; box-shadow:0 2px 8px rgba(16,185,129,0.08);">
                <div style="background-color:#064e3b; color:#ffffff; padding:12px 18px; font-size:15px; font-weight:700;">
                  📌 📊 Money Snowball Daily Macro Briefing
                </div>
                <div style="padding:18px 20px;">
                  {report_html}
                </div>
              </div>

              <!-- FOOTER / 구독 신청 -->
              <div style="background-color:#f1f5f9; border-radius:8px; padding:20px; text-align:center; margin-top:24px; border:1px solid #e2e8f0;">
                <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:6px;">
                  📬 뉴스레터 수신인 추가하기
                </div>
                <div style="font-size:12px; color:#64748b; margin-bottom:12px;">
                  동료 분들과 함께 이 브리핑을 받아보시려면 아래 링크에서 신청해 주세요.
                </div>
                <a href="{form_url}" style="display:inline-block; background-color:#059669; color:#ffffff; font-size:13px; font-weight:600; padding:8px 18px; border-radius:6px; text-decoration:none;" target="_blank">
                  👉 수신인 추가 신청 링크
                </a>
              </div>

            </td>
          </tr>

          <!-- 저작권 및 안내 푸터 -->
          <tr>
            <td style="background-color:#f8fafc; border-top:1px solid #e2e8f0; padding:18px 24px; text-align:center; font-size:11px; color:#94a3b8;">
              본 리포트는 Google Gemini 기반 자동화 지식 큐레이터 시스템에 의해 생성되었습니다.<br>
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
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        print("Email credentials not set. Skipping email.")
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
    msg.set_content(content)
    
    if html_content:
        msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"이메일 전송 성공! (HTML 포맷 포함, 총 {len(receivers_list)}명 발송 완료)")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")

def main():
    print("Starting Finance Summarizer...")
    config = load_config()
    news_data = {}
    
    for category in config.get("categories", []):
        cat_name = category["name"]
        print(f"Fetching news for {cat_name}...")
        articles = []
        for q in category.get("queries", []):
            articles.extend(fetch_google_news(q, max_articles=2))
        news_data[cat_name] = articles

    print("Generating report via Gemini...")
    report_md = generate_finance_report(news_data)
    
    # Save to file
    today_str = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "News", "Finance")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"Finance_Briefing_{today_str}.md")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Saved report to {file_path}")
    
    # Generate HTML and Send Email
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdPTpkieDY9RNHdJohQjH5cd4VYcQG2lCIfFWeI9dsmnKzcbQ/viewform?usp=dialog"
    html_body = generate_html_email(today_str, report_md, form_url)
    send_email(f"🧭 [Money Snowball] Daily Macro Briefing ({today_str})", report_md, html_content=html_body)

if __name__ == "__main__":
    main()
