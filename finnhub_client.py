import finnhub
import datetime
import pandas as pd
import logging
from typing import List, Dict, Any, Optional
from config import FINNHUB_API_KEY, DEFAULT_NEWS_COUNT

# Set up a logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('finnhub_client')

class FinnhubClient:
    def __init__(self):
        """Initialize Finnhub client with API key from config"""
        if not FINNHUB_API_KEY:
            raise ValueError("FINNHUB_API_KEY is not set. Please add it to your .env file.")
        self.client = finnhub.Client(api_key=FINNHUB_API_KEY)
    
    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get company profile for a ticker
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary containing company information
        """
        try:
            return self.client.company_profile2(symbol=ticker)
        except Exception as e:
            print(f"Error fetching company profile for {ticker}: {e}")
            return {}
    
    def get_quote(self, ticker: str) -> Dict[str, Any]:
        """
        Get current quote for a ticker
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary containing price information
        """
        try:
            return self.client.quote(ticker)
        except Exception as e:
            print(f"Error fetching quote for {ticker}: {e}")
            return {}
    
    def get_news(self, ticker: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get news for a ticker for specified number of days
        
        Args:
            ticker: Stock symbol
            days: Number of days to look back
            
        Returns:
            List of news items
        """
        try:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
            
            logger.info(f"Fetching news for {ticker} from {start_date} to {end_date} ({days} days lookback)")
            
            news = self.client.company_news(
                symbol=ticker,
                _from=start_date,
                to=end_date
            )
            
            news_count = len(news) if news else 0
            logger.info(f"Found {news_count} news items for {ticker}")
            
            # Limit the number of news items
            result = news[:DEFAULT_NEWS_COUNT] if news else []
            if news_count > DEFAULT_NEWS_COUNT:
                logger.info(f"Limiting to {DEFAULT_NEWS_COUNT} news items for {ticker}")
                
            return result
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []
    
    def get_batch_data(self, tickers: List[str], days: int = 7) -> Dict[str, Dict[str, Any]]:
        """
        Get all data for a list of tickers
        
        Args:
            tickers: List of stock symbols
            days: Number of days to look back for news
            
        Returns:
            Dictionary containing data for each ticker
        """
        results = {}
        
        for ticker in tickers:
            profile = self.get_company_profile(ticker)
            quote = self.get_quote(ticker)
            news = self.get_news(ticker, days)
            
            results[ticker] = {
                "profile": profile,
                "quote": quote,
                "news": news,
            }
        
        return results 