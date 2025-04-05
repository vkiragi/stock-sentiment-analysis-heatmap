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

# Define the endpoint URL for company profile
url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={API_KEY}"

print(f"Calling endpoint: {url.replace(API_KEY, 'YOUR_API_KEY')}")

# Make the API request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    profile_data = response.json()
    
    # Print the profile data with nice formatting
    print("\nCompany Profile:")
    for key, value in profile_data.items():
        print(f"  {key}: {value}")
    
    # Save full response to a JSON file for further inspection
    with open(f"{ticker}_profile.json", "w") as f:
        json.dump(profile_data, f, indent=2)
    print(f"\nFull data saved to {ticker}_profile.json")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text) 