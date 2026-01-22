# 📈 Market Sentiment Analyzer - Project Documentation

## 1. Proposed Solution

### The Problem
In the fast-paced world of stock trading, vast amounts of news and financial data are generated every second. For retail investors and analysts, manually reading and interpreting thousands of articles to gauge market sentiment is impossible. Missing a critical piece of news or misinterpreting the overall mood can lead to poor investment decisions.

### The Solution
The **Market Sentiment Analyzer** is an AI-powered tool designed to democratize financial intelligence. It automates the process of:
1.  **Aggregating** real-time news from credible financial sources.
2.  **Analyzing** the underlying sentiment (Bullish/Bearish) using advanced Large Language Models (LLMs).
3.  **Synthesizing** this information into actionable insights, investment recommendations, and risk assessments.

This solution provides users with an instant, data-driven "second opinion" on any stock, helping them make more informed decisions with higher confidence.

---

## 2. System Architecture

The system follows a modular **Microservices-inspired Architecture**, separating data fetching, intelligence, and presentation layers.

### Data Flow
1.  **User Input**: User selects a stock (e.g., "AAPL") via the Streamlit UI.
2.  **Data Ingestion**: The `NewsFetcher` module queries the **GNews API** to retrieve the latest 5-10 relevant articles.
3.  **Prompt Engineering**: Articles are combined into a structured prompt context, instructing the LLM to act as a financial analyst.
4.  **Intelligence Processing**: The prompt is sent to the **Groq API** (running Qwen/Llama models), which processes the text at high speed.
5.  **Structured Output**: The LLM returns a JSON object containing scores, labels, and justifications.
6.  **Visualization**: Streamlit renders the JSON data into interactive metrics, charts, and summary cards.

### Architecture Diagram
```mermaid
graph TD
    User[User] -->|Input Stock Symbol| UI[Streamlit Frontend]
    UI -->|Request Data| Fetcher[News Fetcher Module]
    Fetcher -->|Query (HTTP)| NewsAPI[GNews API]
    NewsAPI -->|JSON Articles| Fetcher
    Fetcher -->|Raw Articles| Engine[Sentiment Engine]
    Engine -->|Context + Prompt| LLM[Groq API (LLM)]
    LLM -->|Analysis (JSON)| Engine
    Engine -->|Parsed Results| UI
    UI -->|Visual Dashboard| User
```

---

## 3. Technology Stack

### Core Technologies
*   **Programming Language**: Python 3.11+
    *   Chosen for its rich ecosystem of data and AI libraries.

### Frontend
*   **Framework**: **Streamlit**
    *   Allows for rapid development of interactive data dashboards.
    *   Provides built-in widgets for input, metrics, and layout management.

### Artificial Intelligence (LLM)
*   **Inference Engine**: **Groq**
    *   Selected for its industry-leading inference speed (LPU™ Inference Engine), crucial for real-time applications.
*   **Model**: **Qwen 2.5/3 (32B)** or **Llama 3.3 (70B)**
    *   High-performance open-source models capable of nuanced financial reasoning and adhering to strict JSON output formats.

### Data sources
*   **News Provider**: **GNews API**
    *   Provides real-time access to global news sources with filtering capabilities.

### Key Libraries
*   `requests`: For handling HTTP calls to external APIs.
*   `python-dotenv`: For secure environment variable management (API keys).
*   `json`: For parsing structured LLM outputs.

---

## 4. Planning

### Phase 1: Foundation & Setup ✅
*   [x] Define project structure and environment.
*   [x] Secure API keys for Groq and GNews.
*   [x] Establish basic GitHub/local repository structure.

### Phase 2: Core Implementation ✅
*   [x] **News Fetcher**: Implement `get_latest_news()` to retrieve and format articles.
*   [x] **Sentiment Engine**: Implement `analyze_sentiment()` to interface with Groq.
*   [x] **Prompt Engineering**: Design system prompts to ensure consistent JSON outputs and financial persona.

### Phase 3: Interface & UX ✅
*   [x] **UI Development**: Build Streamlit dashboard with input fields and loading states.
*   [x] **Visualization**: Design metric cards for Sentiment Score, Confidence, and Recommendations.
*   [x] **Formatting**: Apply styling (colors, emojis) to differentiate Bullish vs. Bearish signals.

### Phase 4: Reliability & Robustness ✅
*   [x] **Error Handling**: Manage API timeouts and rate limits.
*   [x] **Parser Logic**: Implement robust JSON extraction to handle LLM "thinking" traces or markdown wrapping.
*   [x] **Dependency Management**: Lock compatible versions (`groq`, `httpx`) to prevent environment conflicts.

### Phase 5: Future Enhancements 🚀
*   [ ] **Portfolio Mode**: Analyze multiple stocks simultaneously.
*   [ ] **Historical Analysis**: Track sentiment trends over time (requires database).
*   [ ] **Multi-Agent System**: Use separate agents for "Risk Analysis", "Technical Analysis", and "Fundamental Analysis" and merge their insights.
*   [ ] **PDF Report Generation**: Export analysis as a downloadable PDF for presentation.
