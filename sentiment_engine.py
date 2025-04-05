import nltk
import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Tuple
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD

# Set up a logger
logger = logging.getLogger('sentiment_engine')

# Download VADER lexicon (only needed once)
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    logger.info("Downloading VADER lexicon (first-time setup)")
    nltk.download('vader_lexicon')

class SentimentEngine:
    def __init__(self):
        """Initialize the VADER sentiment analyzer"""
        self.analyzer = SentimentIntensityAnalyzer()
    
    def score_text(self, text: str) -> float:
        """
        Score a single text using VADER
        
        Args:
            text: Text to analyze
            
        Returns:
            Compound sentiment score (-1 to 1)
        """
        if not text or not isinstance(text, str):
            return 0.0
        
        sentiment = self.analyzer.polarity_scores(text)
        return sentiment['compound']  # Compound score is between -1 (negative) and 1 (positive)
    
    def classify_sentiment(self, score: float) -> str:
        """
        Classify sentiment score into positive, negative, or neutral
        
        Args:
            score: Compound sentiment score
            
        Returns:
            String classification
        """
        if score >= POSITIVE_THRESHOLD:
            return "positive"
        elif score <= NEGATIVE_THRESHOLD:
            return "negative"
        else:
            return "neutral"
    
    def analyze_news(self, news_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a list of news items
        
        Args:
            news_items: List of news dictionaries (from Finnhub)
            
        Returns:
            Dictionary with average score, count, and sentiment label
        """
        if not news_items:
            return {
                "avg_score": 0.0,
                "sentiment": "neutral",
                "count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0
            }
        
        scores = []
        sentiments = []
        
        for item in news_items:
            # Get headline and summary
            headline = item.get('headline', '')
            summary = item.get('summary', '')
            
            # Score headline (more weight) and summary
            headline_score = self.score_text(headline) * 1.5  # More weight to headline
            summary_score = self.score_text(summary) 
            
            # Average the scores (with headline having more weight)
            combined_score = (headline_score + summary_score) / 2.5
            scores.append(combined_score)
            
            sentiment = self.classify_sentiment(combined_score)
            sentiments.append(sentiment)
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        overall_sentiment = self.classify_sentiment(avg_score)
        
        positive_count = sentiments.count("positive")
        negative_count = sentiments.count("negative")
        neutral_count = sentiments.count("neutral")
        
        return {
            "avg_score": avg_score,
            "sentiment": overall_sentiment,
            "count": len(news_items),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }
    
    def process_batch_data(self, batch_data: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Process batch data from Finnhub client and return a DataFrame with sentiment
        
        Args:
            batch_data: Dictionary of ticker data from FinnhubClient.get_batch_data()
            
        Returns:
            DataFrame with sentiment analysis results
        """
        results = []
        
        for ticker, data in batch_data.items():
            news = data.get('news', [])
            profile = data.get('profile', {})
            quote = data.get('quote', {})
            
            sentiment_data = self.analyze_news(news)
            
            results.append({
                'ticker': ticker,
                'name': profile.get('name', ticker),
                'sector': profile.get('finnhubIndustry', 'Unknown'),
                'sentiment_score': sentiment_data['avg_score'],
                'sentiment': sentiment_data['sentiment'],
                'mentions': sentiment_data['count'],
                'positive_mentions': sentiment_data['positive_count'],
                'negative_mentions': sentiment_data['negative_count'],
                'neutral_mentions': sentiment_data['neutral_count'],
                'current_price': quote.get('c', 0),
                'price_change': quote.get('d', 0),
                'price_change_pct': quote.get('dp', 0),
            })
        
        return pd.DataFrame(results) 