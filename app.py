import streamlit as st
from data_sources.news_fetcher import get_latest_news
from sentiment_engine.sentiment_llm import analyze_sentiment

# Page config
st.set_page_config(
    page_title="📈 Market Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sentiment-card {
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .bullish { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
    .bearish { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
    .neutral { background: linear-gradient(135deg, #636363 0%, #a2ab58 100%); color: white; }
    .metric-container {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .news-card {
        background: #2d2d2d;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📈 AI Stock Sentiment Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Powered by Groq LLM & Real-time News Analysis</p>', unsafe_allow_html=True)

st.divider()

# Popular stocks for quick selection
POPULAR_STOCKS = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN", "META", "TCS", "INFY", "RELIANCE"]

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    stock_input = st.text_input(
        "🔍 Enter Stock Symbol or Company Name",
        placeholder="e.g., AAPL, Tesla, TCS...",
        help="Enter a stock ticker symbol or company name"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze", type="primary", use_container_width=True)

# Quick select buttons
st.markdown("**Quick Select:**")
quick_cols = st.columns(len(POPULAR_STOCKS))
for i, stock in enumerate(POPULAR_STOCKS):
    if quick_cols[i].button(stock, key=f"quick_{stock}"):
        stock_input = stock
        analyze_btn = True

st.divider()

# Main analysis
if analyze_btn and stock_input:
    stock = stock_input.upper().strip()
    
    with st.spinner(f"🔄 Fetching latest news for {stock}..."):
        articles = get_latest_news(stock, max_articles=5)
    
    if articles:
        # Display news articles
        st.subheader(f"📰 Latest News for {stock}")
        
        news_cols = st.columns(min(len(articles), 3))
        for i, article in enumerate(articles[:3]):
            with news_cols[i]:
                st.markdown(f"""
                <div class="news-card">
                    <strong>{article['title'][:80]}...</strong><br>
                    <small style="color: #888;">📍 {article['source']}</small><br>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">{article['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Analyze sentiment
        with st.spinner("🤖 AI is analyzing sentiment..."):
            result = analyze_sentiment(articles, stock)
        
        # Display results
        st.subheader("📊 Sentiment Analysis Results")
        
        # Determine sentiment class for styling
        score = result.get("sentiment_score", 0)
        if score > 0.3:
            sentiment_class = "bullish"
            emoji = "🟢"
        elif score < -0.3:
            sentiment_class = "bearish"
            emoji = "🔴"
        else:
            sentiment_class = "neutral"
            emoji = "🟡"
        
        # Main metrics row
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric(
                label="Sentiment Score",
                value=f"{score:.2f}",
                delta=result.get("sentiment_label", "N/A")
            )
        
        with m2:
            st.metric(
                label="Recommendation",
                value=result.get("recommendation", "Hold")
            )
        
        with m3:
            st.metric(
                label="Confidence",
                value=f"{result.get('confidence', 0)}%"
            )
        
        with m4:
            st.metric(
                label="Signal",
                value=f"{emoji} {result.get('sentiment_label', 'N/A')}"
            )
        
        st.divider()
        
        # Detailed analysis
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("💡 Key Insights")
            for insight in result.get("key_insights", []):
                st.markdown(f"✅ {insight}")
        
        with col_right:
            st.subheader("⚠️ Risk Factors")
            for risk in result.get("risks", []):
                st.markdown(f"🔸 {risk}")
        
        st.divider()
        
        # Summary box
        st.subheader("📝 AI Summary")
        
        # Color-coded summary box
        if sentiment_class == "bullish":
            st.success(result.get("summary", "No summary available."))
        elif sentiment_class == "bearish":
            st.error(result.get("summary", "No summary available."))
        else:
            st.info(result.get("summary", "No summary available."))
        
        # Investment decision helper
        st.divider()
        st.subheader("🎯 Investment Decision Helper")
        
        rec = result.get("recommendation", "Hold")
        conf = result.get("confidence", 0)
        
        if rec in ["Strong Buy", "Buy"] and conf > 70:
            st.balloons()
            st.success(f"""
            ### ✅ Consider Investing
            Based on current news sentiment, **{stock}** shows positive signals.
            - Recommendation: **{rec}**
            - Confidence: **{conf}%**
            
            *Always do your own research before investing!*
            """)
        elif rec in ["Strong Sell", "Sell"] and conf > 70:
            st.warning(f"""
            ### ⚠️ Caution Advised
            Current news sentiment for **{stock}** is concerning.
            - Recommendation: **{rec}**
            - Confidence: **{conf}%**
            
            *Consider waiting for better market conditions.*
            """)
        else:
            st.info(f"""
            ### 🔍 Further Research Needed
            The sentiment for **{stock}** is mixed or uncertain.
            - Recommendation: **{rec}**
            - Confidence: **{conf}%**
            
            *Monitor the stock for clearer signals.*
            """)
    
    else:
        st.error("❌ Could not fetch news articles. Please try a different stock symbol.")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>⚠️ <strong>Disclaimer:</strong> This tool is for educational/demo purposes only. 
    Not financial advice. Always consult a qualified financial advisor before investing.</p>
    <p>Built with ❤️ using Streamlit & Groq LLM</p>
</div>
""", unsafe_allow_html=True)
