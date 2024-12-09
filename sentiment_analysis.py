# sentiment_analysis.py

import requests
from llm_client import query_llm
from config import DATA_API_KEY
from logger import log_message


def get_news_sentiment(symbol):
    """
    Fetch news headlines for a stock and perform sentiment analysis.
    """
    try:
        API_URL = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={DATA_API_KEY}"
        response = requests.get(API_URL)
        articles = response.json().get("articles", [])

        sentiments = []
        for article in articles[:5]:  # Limit to top 5 articles
            text = article["title"] + " " + article["description"]
            sentiment_prompt = f"Analyze the sentiment of the following text: {text}. Return Positive, Negative, or Neutral."
            sentiment = query_llm(sentiment_prompt)
            sentiments.append(sentiment)

        # Aggregate sentiments
        positive = sentiments.count("Positive")
        negative = sentiments.count("Negative")
        neutral = sentiments.count("Neutral")

        if positive > negative and positive > neutral:
            overall_sentiment = "Positive"
        elif negative > positive and negative > neutral:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"

        log_message("INFO", f"Sentiment for {symbol}: {overall_sentiment}")
        return overall_sentiment
    except Exception as e:
        log_message("ERROR", f"Error fetching sentiment for {symbol}: {e}")
        return "Neutral"
