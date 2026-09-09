import re

with open('agents/tech/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. replace 'gemini-3.1-flash-lite' with 'gemini-2.5-flash'
code = code.replace("'gemini-3.1-flash-lite'", "'gemini-2.5-flash'")

# 2. Add time.sleep to safe_summarize_news
code = re.sub(r'(@retry.*?)\n(def safe_summarize_news.*?:\n\s*print\(f"  \[.*?\] Gemini 분석 요청 중..."\))', r'\1\n\2\n    import time; time.sleep(5)', code)

# 3. Add time.sleep to safe_analyze_github_trending
code = re.sub(r'(@retry.*?)\n(def safe_analyze_github_trending.*?:\n\s*print\("  \[GitHub Trending\] Gemini 4대 분야 분석 요청 중..."\))', r'\1\n\2\n    import time; time.sleep(5)', code)

# 4. Add time.sleep to safe_generate_executive_summary
code = re.sub(r'(@retry.*?)\n(def safe_generate_executive_summary.*?:\n\s*print\("  \[Executive Summary\] Gemini 종합 분석 요청 중..."\))', r'\1\n\2\n    import time; time.sleep(5)', code)

# 5. Remove retry exponential, replace with wait_fixed
code = re.sub(r'wait=wait_exponential\(multiplier=2, min=4, max=60\)', 'wait=wait_fixed(10)', code)
code = re.sub(r'stop=stop_after_attempt\(5\)', 'stop=stop_after_attempt(3)', code)

# 6. Remove openai fallback logic from main
code = re.sub(r'(\s*)try:\n\s*summary = safe_summarize_news\(cat_name, focus, unique_articles\)\n\s*except Exception as e:\n\s*try:\n\s*summary = safe_summarize_news_openai\(cat_name, focus, unique_articles\)\n\s*except Exception as e2:\n\s*summary = "요약 실패"', r'\1try:\n\1    summary = safe_summarize_news(cat_name, focus, unique_articles)\n\1except Exception as e:\n\1    summary = "요약 실패"', code)

code = re.sub(r'(\s*)try:\n\s*github_summary_text = safe_analyze_github_trending\(focus_str, cur_candidates\)\n\s*except Exception as e:\n\s*try:\n\s*github_summary_text = safe_analyze_github_trending_openai\(focus_str, cur_candidates\)\n\s*except Exception as e2:\n\s*github_summary_text = ""', r'\1try:\n\1    github_summary_text = safe_analyze_github_trending(focus_str, cur_candidates)\n\1except Exception as e:\n\1    github_summary_text = ""', code)

code = re.sub(r'(\s*)try:\n\s*executive_summary = safe_generate_executive_summary\(articles_summary_text, github_summary_text\)\n\s*except Exception as e:\n\s*try:\n\s*executive_summary = safe_generate_executive_summary_openai\(articles_summary_text, github_summary_text\)\n\s*except Exception as e2:\n\s*executive_summary = ""', r'\1try:\n\1    executive_summary = safe_generate_executive_summary(articles_summary_text, github_summary_text)\n\1except Exception as e:\n\1    executive_summary = ""', code)

with open('agents/tech/main.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Tech agent patched!")
