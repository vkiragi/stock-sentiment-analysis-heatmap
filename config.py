import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Finnhub API key
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# App configuration
DEFAULT_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]
DEFAULT_TIME_WINDOW = 7  # days
DEFAULT_NEWS_COUNT = 50  # number of news to fetch per stock

# Sentiment thresholds
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

# Sectors for filtering
SECTORS = [
    "Technology", 
    "Healthcare", 
    "Consumer Cyclical", 
    "Financial Services",
    "Communication Services", 
    "Industrials", 
    "Consumer Defensive",
    "Energy", 
    "Basic Materials", 
    "Real Estate", 
    "Utilities"
] 