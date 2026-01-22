import requests
import os
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def get_latest_news(stock: str, max_articles: int = 5) -> list[dict]:
    """
    Fetch latest news articles for a given stock/company using GNews API.
    Returns list of articles with title, description, and source.
    """
    try:
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": f"{stock} stock market",
            "lang": "en",
            "country": "us,in",
            "max": max_articles,
            "apikey": GNEWS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
                "publishedAt": article.get("publishedAt", "")
            })
        
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        # Return mock data for demo if API fails
        return get_mock_news(stock)


def get_mock_news(stock: str) -> list[dict]:
    """Fallback mock news for demo purposes"""
    return [
        {
            "title": f"{stock} Reports Strong Quarterly Earnings, Stock Surges 5%",
            "description": f"{stock} exceeded analyst expectations with record revenue growth driven by strong demand in key markets.",
            "source": "Financial Times",
            "url": "#",
            "publishedAt": "2026-01-22T10:00:00Z"
        },
        {
            "title": f"Analysts Upgrade {stock} Rating to 'Buy' After Positive Outlook",
            "description": f"Major investment banks have upgraded {stock} citing robust fundamentals and growth potential.",
            "source": "Bloomberg",
            "url": "#",
            "publishedAt": "2026-01-22T08:30:00Z"
        },
        {
            "title": f"{stock} Announces New Strategic Partnership",
            "description": f"The partnership is expected to drive innovation and expand market reach for {stock}.",
            "source": "Reuters",
            "url": "#",
            "publishedAt": "2026-01-21T15:00:00Z"
        }
    ]
