import urllib.parse
import feedparser
import sys

query = "6G Standard"
if len(sys.argv) > 1:
    query = sys.argv[1]

encoded_query = urllib.parse.quote(query)
url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)
print(f"URL: {url}")
print(f"Entries: {len(feed.entries)}")
if feed.entries:
    print(f"Title 1: {feed.entries[0].title}")
    print(f"Published 1: {feed.entries[0].published}")
