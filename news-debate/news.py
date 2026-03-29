# news.py
import feedparser

def get_headlines():
    feed = feedparser.parse("https://news.google.com/rss")
    articles = []
    
    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })
    
    return articles