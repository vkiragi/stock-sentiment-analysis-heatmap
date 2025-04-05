import requests
import json
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

if not API_KEY:
    raise ValueError("FINNHUB_API_KEY not found in .env file")

# Set up parameters
ticker = "AAPL"  # Example ticker

# Define the endpoint URL for quote
url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"

print(f"Calling endpoint: {url.replace(API_KEY, 'YOUR_API_KEY')}")

# Make the API request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    quote_data = response.json()
    
    # Print the quote data with explanations
    print("\nStock Quote:")
    if 'c' in quote_data:
        print(f"  Current Price: ${quote_data['c']}")
    if 'h' in quote_data:
        print(f"  High Price (Today): ${quote_data['h']}")
    if 'l' in quote_data:
        print(f"  Low Price (Today): ${quote_data['l']}")
    if 'o' in quote_data:
        print(f"  Open Price: ${quote_data['o']}")
    if 'pc' in quote_data:
        print(f"  Previous Close: ${quote_data['pc']}")
    if 'd' in quote_data:
        print(f"  Change: ${quote_data['d']}")
    if 'dp' in quote_data:
        print(f"  Percent Change: {quote_data['dp']}%")
    
    # Show all raw data
    print("\nRaw Quote Data:")
    for key, value in quote_data.items():
        print(f"  {key}: {value}")
    
    # Save full response to a JSON file for further inspection
    with open(f"{ticker}_quote.json", "w") as f:
        json.dump(quote_data, f, indent=2)
    print(f"\nFull data saved to {ticker}_quote.json")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text) 