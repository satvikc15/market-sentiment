from fastapi import FastAPI
from data_sources.news_fetcher import get_latest_news

app = FastAPI()

@app.get("/market_context")
def market_context(stock: str):
    return {
        "stock": stock,
        "news": get_latest_news(stock),
        "source": "MCP Server",
        "timestamp": "real-time"
    }
