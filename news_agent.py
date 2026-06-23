import feedparser
import requests
import os

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

rss_feeds = {
    "🛡 DEFENCE": [
        "https://news.google.com/rss/search?q=defence+india"
    ],
    "🌍 WORLD AFFAIRS": [
        "https://news.google.com/rss/search?q=world+news"
    ],
    "📜 GOVERNMENT POLICIES": [
        "https://news.google.com/rss/search?q=india+government+policy"
    ],
    "🤖 AI & TECHNOLOGY": [
        "https://news.google.com/rss/search?q=artificial+intelligence+news",
        "https://news.google.com/rss/search?q=latest+technology"
    ],
    "💼 JOB ALERTS": [
        "https://news.google.com/rss/search?q=ssc+gate+jobs+india",
        "https://news.google.com/rss/search?q=government+jobs+india"
    ],
    "🇮🇳 STATE NEWS": [
        "https://news.google.com/rss/search?q=state+news+india"
    ]
}

def get_news():
    categorized_news = {}

    for category, urls in rss_feeds.items():
        categorized_news[category] = []

        for url in urls:
            feed = feedparser.parse(url)

            for entry in feed.entries[:3]:  # limit per category
                news = f"• {entry.title}\n{entry.link}"
                categorized_news[category].append(news)

    return categorized_news


def format_message(news_dict):
    message = "🔥 *3-Hour News Update*\n\n"

    for category, news_list in news_dict.items():
        if news_list:
            message += f"*{category}*\n"
            message += "\n".join(news_list)
            message += "\n\n"

    return message


def send_to_slack(message):
    payload = {"text": message}
    requests.post(WEBHOOK_URL, json=payload)


def job():
    news = get_news()
    message = format_message(news)
    send_to_slack(message)
