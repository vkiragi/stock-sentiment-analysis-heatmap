import requests
import json
import datetime
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

if not API_KEY:
    raise ValueError("FINNHUB_API_KEY not found in .env file")

# Set up parameters
ticker = "AAPL"  # Example ticker
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

# Define the endpoint URL
url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={start_date}&to={end_date}&token={API_KEY}"

print(f"Calling endpoint: {url.replace(API_KEY, 'YOUR_API_KEY')}")

# Make the API request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    news_data = response.json()
    
    # Print the total number of articles
    print(f"Found {len(news_data)} news articles for {ticker}")
    
    # Print detailed info for first 3 articles
    for i, article in enumerate(news_data[:3]):
        print(f"\nArticle {i+1}:")
        print(f"  Headline: {article.get('headline', 'N/A')}")
        print(f"  Summary: {article.get('summary', 'N/A')[:100]}...")  # First 100 chars
        print(f"  Source: {article.get('source', 'N/A')}")
        print(f"  URL: {article.get('url', 'N/A')}")
        print(f"  Date: {article.get('datetime', 'N/A')}")
        
    # Save full response to a JSON file for further inspection
    with open(f"{ticker}_news.json", "w") as f:
        json.dump(news_data, f, indent=2)
    print(f"\nFull data saved to {ticker}_news.json")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text) 