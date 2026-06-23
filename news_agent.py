import feedparser
import requests
import os
from openai import OpenAI

# API Keys
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

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

def summarize(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the news in 1 simple sentence for exam preparation."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return text  # fallback


def get_news():
    categorized_news = {}

    for category, urls in rss_feeds.items():
        categorized_news[category] = []

        for url in urls:
            feed = feedparser.parse(url)

            for entry in feed.entries[:2]:  # reduce due to API usage
                summary = summarize(entry.title)
                news = f"• {summary}\n{entry.link}"
                categorized_news[category].append(news)

    return categorized_news


def format_message(news_dict):
    message = "🔥 *AI Powered 3-Hour News Update*\n\n"

    for category, news_list in news_dict.items():
        if news_list:
            message += f"*{category}*\n"
            message += "\n".join(news_list)
            message += "\n\n"

    return message


def send_to_slack(message):
    if not WEBHOOK_URL:
        print("❌ Slack Webhook Missing")
        return

    payload = {"text": message}
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("✅ Sent to Slack")
    else:
        print("❌ Error:", response.text)


def job():
    print("🚀 Running AI News Agent...")
    news = get_news()
    message = format_message(news)
    send_to_slack(message)


if __name__ == "__main__":
    job()
