import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_sentiment(articles: list[dict], stock: str) -> dict:
    """
    Analyze sentiment of news articles using Groq LLM.
    Returns sentiment score, recommendation, and detailed analysis.
    """
    
    # Prepare news content for analysis
    news_text = "\n\n".join([
        f"**{article['title']}** ({article['source']})\n{article['description']}"
        for article in articles
    ])
    
    prompt = f"""You are an expert financial analyst. Analyze the following news articles about {stock} and provide investment sentiment analysis and base you evalauation on below topics:
    Financial Performance Metrics
Profitability: Net Profit Margin, Gross Profit Margin, Earnings Per Share (EPS), and Return on Equity (ROE).
Liquidity: Current Ratio and Quick Ratio, which measure the ability to meet short-term obligations.
Solvency/Leverage: Debt-to-Equity Ratio, assessing long-term debt management.
Efficiency: Inventory Turnover and Accounts Receivable Turnover. 

NEWS ARTICLES:
{news_text}

Provide your analysis in the following JSON format ONLY (no other text):
{{
    "sentiment_score": <number between -1 (very bearish) and 1 (very bullish)>,
    "sentiment_label": "<Strongly Bullish|Bullish|Neutral|Bearish|Strongly Bearish>",
    "recommendation": "<Strong Buy|Buy|Hold|Sell|Strong Sell>",
    "confidence": <number between 0 and 100>,
    "key_insights": ["<insight 1>", "<insight 2>", "<insight 3>"],
    "risks": ["<risk 1>", "<risk 2>"],
    "summary": "<2-3 sentence summary of the analysis>"
}}"""

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst AI. Always respond with valid JSON only."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        if not result_text:
            raise ValueError("Empty response from LLM")
            
        # Clean up the response to find JSON
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = result_text[start_idx:end_idx+1]
            try:
                result = json.loads(json_str)
                return result
            except json.JSONDecodeError:
                # If direct parsing fails, try to repair common issues
                pass
        
        # Fallback if standard parsing fails
        result = json.loads(result_text)
        return result
        
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON Parse Error: {str(e)}")
        print(f"Raw Response: {result_text}")
        return {
            "sentiment_score": 0,
            "sentiment_label": "Neutral",
            "recommendation": "Hold",
            "confidence": 0,
            "key_insights": ["Error parsing AI response"],
            "risks": ["Please try again"],
            "summary": f"The AI response couldn't be parsed. It might have returned unstructured text."
        }
    except Exception as e:
        return {
            "sentiment_score": 0,
            "sentiment_label": "Error",
            "recommendation": "Hold",
            "confidence": 0,
            "key_insights": ["API error occurred"],
            "risks": ["Unable to complete analysis"],
            "summary": f"Error: {str(e)}"
        }
