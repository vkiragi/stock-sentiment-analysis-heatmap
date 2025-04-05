import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('stock_sentiment_app')

from finnhub_client import FinnhubClient
from sentiment_engine import SentimentEngine
from data_utils import (
    filter_df_by_sector,
    filter_df_by_sentiment,
    sort_df_by_column,
    create_color_scale,
    format_df_for_display,
    get_sector_counts,
    get_sentiment_stats
)
from config import DEFAULT_STOCKS, DEFAULT_TIME_WINDOW, SECTORS

# Page configuration
st.set_page_config(
    page_title="Stock Sentiment Heatmap",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create cache directory if it doesn't exist
if not os.path.exists('./cache'):
    os.makedirs('./cache')

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'lookback_days' not in st.session_state:
    st.session_state.lookback_days = DEFAULT_TIME_WINDOW

# Function to load data
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def load_data(tickers, days):
    """Load data from Finnhub API and analyze sentiment"""
    cache_key = f"tickers={'_'.join(sorted(tickers))}_days={days}"
    logger.info(f"Cache key: {cache_key}")
    
    try:
        st.info(f"🕒 Fetching news with lookback period: {days} days")
        
        finnhub_client = FinnhubClient()
        sentiment_engine = SentimentEngine()
        
        batch_data = finnhub_client.get_batch_data(tickers, days)
        
        # Log the total number of news articles for verification
        total_news = 0
        news_counts = {}
        for ticker, data in batch_data.items():
            news_count = len(data.get('news', []))
            total_news += news_count
            news_counts[ticker] = news_count
            logger.info(f"Found {news_count} news items for {ticker}")
        
        logger.info(f"Total news articles fetched: {total_news}")
        # Show a simplified summary in the UI
        counts_str = ", ".join([f"{t}: {c}" for t, c in news_counts.items()])
        st.info(f"📊 News articles found: {total_news} total ({counts_str})")
        
        df = sentiment_engine.process_batch_data(batch_data)
        
        # Save data to cache
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df.to_csv(f'./cache/sentiment_data_{timestamp}.csv', index=False)
        
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error(f"Error loading data: {e}")
        return None

# Sidebar
st.sidebar.title("📈 Stock Sentiment Analyzer")

# Ticker input
ticker_input = st.sidebar.text_area(
    "Enter stock tickers (comma-separated)",
    value=", ".join(DEFAULT_STOCKS),
    help="Enter comma-separated stock symbols (e.g., AAPL, MSFT, GOOGL)"
)

# Parse tickers
tickers = [ticker.strip().upper() for ticker in ticker_input.split(',') if ticker.strip()]

# Time window selection
time_window = st.sidebar.slider(
    "News lookback period (days)",
    min_value=1,
    max_value=30,
    value=DEFAULT_TIME_WINDOW,
    help="Number of days to look back for news headlines"
)

# If lookback period changed, clear cache
if time_window != st.session_state.lookback_days:
    st.sidebar.warning(f"Lookback period changed from {st.session_state.lookback_days} to {time_window} days. Click 'Fetch Latest Data' to apply.")
    st.session_state.lookback_days = time_window

# Fetch data button
if st.sidebar.button("Fetch Latest Data"):
    # Clear cache to ensure fresh data
    st.cache_data.clear()
    with st.spinner("Fetching data from Finnhub and analyzing sentiment..."):
        st.session_state.data = load_data(tickers, time_window)
        st.session_state.last_update = datetime.now()
        
# Show last update time
if st.session_state.last_update:
    st.sidebar.info(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    # Load data on first run
    if st.session_state.data is None:
        with st.spinner("Loading initial data..."):
            st.session_state.data = load_data(tickers, time_window)
            st.session_state.last_update = datetime.now()

# Divider
st.sidebar.markdown("---")

# Filters section
st.sidebar.subheader("Filters")

# Sector filter
all_sectors = ["All"] + SECTORS
sector_filter = st.sidebar.selectbox("Filter by Sector", all_sectors)

# Sentiment filter
sentiment_filter = st.sidebar.selectbox(
    "Filter by Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

# Sort options
sort_options = {
    "Sentiment Score": "sentiment_score",
    "News Mentions": "mentions",
    "Price Change (%)": "price_change_pct",
    "Ticker": "ticker"
}

sort_by = st.sidebar.selectbox("Sort by", list(sort_options.keys()))
sort_order = st.sidebar.radio("Sort order", ["Descending", "Ascending"])

# Main content
st.title("Stock Sentiment Heatmap")

# Show current settings
st.write(f"**Data settings**: Analyzing {len(tickers)} stocks with a {st.session_state.lookback_days}-day lookback period")

# Check if data is loaded
if st.session_state.data is not None:
    df = st.session_state.data
    
    # Apply filters
    df = filter_df_by_sector(df, sector_filter)
    df = filter_df_by_sentiment(df, sentiment_filter)
    
    # Sort data
    df = sort_df_by_column(
        df, 
        sort_options[sort_by], 
        ascending=(sort_order == "Ascending")
    )
    
    # Display Stats in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Get sentiment stats
    stats = get_sentiment_stats(df)
    
    with col1:
        st.metric("Total Stocks", stats['total'])
    
    with col2:
        st.metric("Positive Sentiment", f"{stats['positive']} ({stats['positive_pct']:.1f}%)")
    
    with col3:
        st.metric("Neutral Sentiment", f"{stats['neutral']} ({stats['neutral_pct']:.1f}%)")
    
    with col4:
        st.metric("Negative Sentiment", f"{stats['negative']} ({stats['negative_pct']:.1f}%)")
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["Heatmap", "Data Table", "Charts"])
    
    with tab1:
        st.subheader("Sentiment & Price Change Heatmap")
        
        if not df.empty:
            # Create a copy of the DataFrame for display
            display_df = format_df_for_display(df)
            
            # Debug messages removed
            
            # Select columns for heatmap
            heatmap_cols = ['Ticker', 'Company', 'Sector', 'Sentiment Score', 'News Mentions', 'Change (%)']
            
            # Ensure all columns exist
            missing_cols = [col for col in heatmap_cols if col not in display_df.columns]
            if missing_cols:
                st.error(f"Missing columns in DataFrame: {missing_cols}")
                # Use available columns only
                heatmap_cols = [col for col in heatmap_cols if col in display_df.columns]
            
            # Create a styled dataframe for the heatmap
            heatmap_df = display_df[heatmap_cols].copy()
            
            # Create a background color dataframe with the same shape
            bg_colors = pd.DataFrame('', index=heatmap_df.index, columns=heatmap_df.columns)
            
            # Set colors for sentiment score
            try:
                sentiment_scores = df['sentiment_score'].tolist()
                for i, score in enumerate(sentiment_scores):
                    red = int(255 * (1 - max(0, score)))
                    green = int(255 * max(0, score))
                    bg_colors.loc[i, 'Sentiment Score'] = f'background-color: rgba({red}, {green}, 0, 0.7)'
            except Exception as e:
                st.error(f"Error styling sentiment scores: {e}")
            
            # Set colors for price change
            try:
                price_changes = df['price_change_pct'].tolist()
                for i, change in enumerate(price_changes):
                    red = int(255 * (1 - min(1, max(0, (change + 5) / 10))))
                    green = int(255 * min(1, max(0, (change + 5) / 10)))
                    bg_colors.loc[i, 'Change (%)'] = f'background-color: rgba({red}, {green}, 0, 0.7)'
            except Exception as e:
                st.error(f"Error styling price changes: {e}")
            
            # Apply styles
            st.dataframe(
                heatmap_df.style.apply(lambda _: bg_colors, axis=None),
                use_container_width=True,
                height=400
            )
            
            # Explanation for colors
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Sentiment Score Color**: 🟢 Green = Positive, 🔴 Red = Negative")
            with col2:
                st.markdown("**Price Change Color**: 🟢 Green = Positive, 🔴 Red = Negative")
            
        else:
            st.warning("No data available for the selected filters.")
    
    with tab2:
        st.subheader("Stock Sentiment Data Table")
        
        if not df.empty:
            # Add information about news counts
            st.info(f"Number of news articles analyzed: {df['mentions'].sum()} total " +
                    f"({df['mentions'].mean():.1f} articles per stock on average)")
            
            # Format DataFrame for display
            display_df = format_df_for_display(df)
            
            # Display as an interactive table
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600
            )
        else:
            st.warning("No data available for the selected filters.")
    
    with tab3:
        st.subheader("Sentiment and Price Analysis")
        
        if not df.empty:
            # Create charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Sentiment distribution by sector
                sector_fig = px.bar(
                    df.groupby('sector')['sentiment_score'].mean().reset_index(),
                    x='sector',
                    y='sentiment_score',
                    title="Average Sentiment by Sector",
                    color='sentiment_score',
                    color_continuous_scale=['red', 'yellow', 'green'],
                    labels={'sentiment_score': 'Avg. Sentiment', 'sector': 'Sector'}
                )
                sector_fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(sector_fig, use_container_width=True)
            
            with col2:
                # Scatter plot of sentiment vs price change
                scatter_fig = px.scatter(
                    df,
                    x='sentiment_score',
                    y='price_change_pct',
                    color='sector',
                    size='mentions',
                    hover_name='ticker',
                    title="Sentiment vs Price Change",
                    labels={
                        'sentiment_score': 'Sentiment Score', 
                        'price_change_pct': 'Price Change (%)',
                        'mentions': 'News Mentions'
                    }
                )
                st.plotly_chart(scatter_fig, use_container_width=True)
            
            # Top positive and negative sentiment stocks
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Positive Sentiment Stocks")
                top_positive = df.sort_values('sentiment_score', ascending=False).head(5)
                positive_fig = px.bar(
                    top_positive,
                    x='ticker',
                    y='sentiment_score',
                    color='sentiment_score',
                    color_continuous_scale=['yellow', 'green'],
                    labels={'sentiment_score': 'Sentiment Score', 'ticker': 'Ticker'},
                    hover_data=['mentions']
                )
                st.plotly_chart(positive_fig, use_container_width=True)
            
            with col2:
                st.subheader("Top Negative Sentiment Stocks")
                top_negative = df.sort_values('sentiment_score').head(5)
                negative_fig = px.bar(
                    top_negative,
                    x='ticker',
                    y='sentiment_score',
                    color='sentiment_score',
                    color_continuous_scale=['red', 'yellow'],
                    labels={'sentiment_score': 'Sentiment Score', 'ticker': 'Ticker'},
                    hover_data=['mentions']
                )
                st.plotly_chart(negative_fig, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")
else:
    st.info("No data loaded. Please click 'Fetch Latest Data' to get started.")

# Footer
st.markdown("---")
st.caption("Powered by Finnhub API and VADER Sentiment Analysis. Data refreshes every hour.")
st.caption("© Stock Sentiment Heatmap " + str(datetime.now().year)) 