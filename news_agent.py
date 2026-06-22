import feedparser
import requests
import schedule
import time

import os
  WEBHOOK_URL =os.getenv("SLACK_WEBHOOK_URL")

rss_feeds = [
    "https://news.google.com/rss/search?q=world+news",
    "https://news.google.com/rss/search?q=defence+india",
    "https://news.google.com/rss/search?q=india+government+policy",
    "https://news.google.com/rss/search?q=technology+ai",
    "https://news.google.com/rss/search?q=gate+ssc+jobs+india"
]

def get_news():
    all_news = []

    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            news = f"📰 {entry.title}\n{entry.link}"
            all_news.append(news)

    return all_news

def send_to_slack(news_list):
    message = "\n\n".join(news_list)

    payload = {
        "text": f"🔥 *3-Hour News Update*\n\n{message}"
    }

    requests.post(WEBHOOK_URL, json=payload)

def job():
    news = get_news()
    send_to_slack(news)

job()
# Run every 3 hours
schedule.every(3).hours.do(job)

print("Agent running...")

while True:
    schedule.run_pending()
    time.sleep(60)
