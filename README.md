# 📈 Stock Sentiment Heatmap

A real-time web app that displays sentiment scores and price movement for selected stocks using news data from Finnhub API and NLP sentiment analysis.

![Stock Sentiment Heatmap Demo](https://via.placeholder.com/800x400?text=Stock+Sentiment+Heatmap+Demo)

## 🌟 Features

- **Real-time Market Data**: Fetch stock quotes and company profiles via Finnhub API
- **News Sentiment Analysis**: Analyze news headlines using NLTK VADER sentiment analysis
- **Interactive Dashboard**: Visualize sentiment vs price movement with heatmaps and charts
- **Customizable Filters**: Filter by sector, sentiment, and sort by various metrics
- **Data Caching**: Save API calls with intelligent caching system

## 📊 Sample Output

The app displays a heatmap of stocks, colored by sentiment score (green for positive, red for negative) and provides detailed analysis:

| Ticker | Sector | Sentiment | Mentions | Price Change (1d) |
|--------|--------|-----------|----------|------------------|
| AAPL   | Tech   | +0.34     | 7        | -1.2%            |
| TSLA   | Auto   | -0.21     | 10       | +2.8%            |
| NVDA   | Tech   | +0.57     | 5        | +0.5%            |

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-heatmap.git
   cd stock-sentiment-heatmap
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Finnhub API key**
   - Create a `.env` file in the project root
   - Add your Finnhub API key: `FINNHUB_API_KEY=your_api_key_here`
   - You can get a free API key at [finnhub.io](https://finnhub.io/)

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
stock-sentiment-heatmap/
├── app.py                    # Streamlit frontend
├── finnhub_client.py         # Handles API calls to Finnhub
├── sentiment_engine.py       # Sentiment analysis logic (VADER)
├── data_utils.py             # Helper functions for formatting, filtering
├── config.py                 # API keys and constants
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview and setup
```

## 🚀 How It Works

1. User selects stocks or sectors to analyze
2. App fetches company profiles, current quotes, and recent news headlines
3. News headlines are analyzed using VADER sentiment analysis
4. Results are aggregated and displayed as interactive tables and charts
5. Data is cached locally to improve performance

## 📝 Future Enhancements

- [ ] Line chart of sentiment over time
- [ ] Email alerts for sentiment spikes
- [ ] Slack integration
- [ ] Comparison between sentiment and actual stock performance
- [ ] Additional data sources (Twitter, Reddit, etc.)

## 📄 License

MIT License

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/stock-sentiment-heatmap/issues).

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/stock-sentiment-heatmap](https://github.com/yourusername/stock-sentiment-heatmap) 