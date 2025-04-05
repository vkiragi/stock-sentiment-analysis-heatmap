import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from config import SECTORS

def filter_df_by_sector(df: pd.DataFrame, sector: str) -> pd.DataFrame:
    """
    Filter DataFrame by sector
    
    Args:
        df: DataFrame containing stock data
        sector: Sector to filter by
        
    Returns:
        Filtered DataFrame
    """
    if sector == "All":
        return df
    
    return df[df['sector'] == sector]

def filter_df_by_sentiment(df: pd.DataFrame, sentiment: str) -> pd.DataFrame:
    """
    Filter DataFrame by sentiment
    
    Args:
        df: DataFrame containing stock data
        sentiment: Sentiment to filter by (positive, negative, neutral, all)
        
    Returns:
        Filtered DataFrame
    """
    if sentiment.lower() == "all":
        return df
    
    return df[df['sentiment'] == sentiment.lower()]

def sort_df_by_column(df: pd.DataFrame, column: str, ascending: bool = False) -> pd.DataFrame:
    """
    Sort DataFrame by a column
    
    Args:
        df: DataFrame containing stock data
        column: Column to sort by
        ascending: Sort ascending (True) or descending (False)
        
    Returns:
        Sorted DataFrame
    """
    return df.sort_values(by=column, ascending=ascending)

def create_color_scale(df: pd.DataFrame, column: str) -> List[str]:
    """
    Create a color scale for a column based on values
    
    Args:
        df: DataFrame containing stock data
        column: Column to create color scale for
        
    Returns:
        List of hex color strings corresponding to DataFrame rows
    """
    # For sentiment score column
    if column == 'sentiment_score':
        return [
            f"rgb({int(255 * (1 - max(0, row[column])))}, {int(255 * max(0, row[column]))}, 0)"
            for _, row in df.iterrows()
        ]
    
    # For price change column
    elif column == 'price_change_pct':
        return [
            f"rgb({int(255 * (1 - min(1, max(0, (row[column] + 5) / 10))))}, {int(255 * min(1, max(0, (row[column] + 5) / 10)))}, 0)"
            for _, row in df.iterrows()
        ]
    
    # Default to no color scaling
    else:
        return ["rgb(240, 240, 240)"] * len(df)

def format_df_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format DataFrame for display in Streamlit
    
    Args:
        df: DataFrame containing stock data
        
    Returns:
        Formatted DataFrame for display
    """
    display_df = df.copy()
    
    # Format percentage columns
    if 'price_change_pct' in display_df.columns:
        display_df['price_change_pct'] = display_df['price_change_pct'].apply(lambda x: f"{x:.2f}%")
    
    # Format sentiment score
    if 'sentiment_score' in display_df.columns:
        display_df['sentiment_score'] = display_df['sentiment_score'].apply(lambda x: f"{x:.2f}")
    
    # Rename columns for better display
    column_map = {
        'ticker': 'Ticker',
        'name': 'Company',
        'sector': 'Sector',
        'sentiment_score': 'Sentiment Score',
        'sentiment': 'Sentiment',
        'mentions': 'News Mentions',
        'current_price': 'Price ($)',
        'price_change': 'Change ($)',
        'price_change_pct': 'Change (%)'
    }
    
    display_df = display_df.rename(columns=column_map)
    
    return display_df

def get_sector_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    Get count of stocks by sector
    
    Args:
        df: DataFrame containing stock data
        
    Returns:
        Dictionary of sector counts
    """
    sector_counts = df['sector'].value_counts().to_dict()
    return sector_counts

def get_sentiment_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get statistics about sentiment in DataFrame
    
    Args:
        df: DataFrame containing stock data
        
    Returns:
        Dictionary of sentiment statistics
    """
    total_stocks = len(df)
    positive_stocks = len(df[df['sentiment'] == 'positive'])
    negative_stocks = len(df[df['sentiment'] == 'negative'])
    neutral_stocks = len(df[df['sentiment'] == 'neutral'])
    
    return {
        'total': total_stocks,
        'positive': positive_stocks,
        'negative': negative_stocks,
        'neutral': neutral_stocks,
        'positive_pct': (positive_stocks / total_stocks) * 100 if total_stocks > 0 else 0,
        'negative_pct': (negative_stocks / total_stocks) * 100 if total_stocks > 0 else 0,
        'neutral_pct': (neutral_stocks / total_stocks) * 100 if total_stocks > 0 else 0
    } 