#!/usr/bin/env python3
"""
Fetch Bitcoin market data from reliable sources with fallback mechanisms.
"""

import requests
import json
import os
import random
import time
import logging
from datetime import datetime, timedelta
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('bitcoin_data_fetcher')

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'

if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    logger.debug("Running in DEBUG mode")


def fetch_from_coingecko():
    """Fetch Bitcoin data from CoinGecko API."""
    logger.info("Attempting to fetch data from CoinGecko API")
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false"
    }
    headers = {"Accept": "application/json"}
    
    try:
        logger.debug(f"Making request to: {url}")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            price = data['market_data']['current_price']['usd']
            price_formatted = f"${price:,.0f}" if price >= 1000 else f"${price:.2f}"
            
            price_change_24h = data['market_data']['price_change_percentage_24h']
            price_change_formatted = f"({'+' if price_change_24h >= 0 else ''}{price_change_24h:.2f}%)"
            
            # Extract other key metrics
            market_cap = data['market_data']['market_cap']['usd']
            volume = data['market_data']['total_volume']['usd']
            
            # Determine sentiment based on price change
            sentiment = "bullish" if price_change_24h > 1 else "bearish" if price_change_24h < -1 else "neutral"
            
            logger.info(f"Successfully fetched data from CoinGecko: {price_formatted} {price_change_formatted}")
            
            return {
                "price": price_formatted,
                "raw_price": price,
                "price_change_24h": price_change_formatted,
                "raw_price_change": price_change_24h,
                "market_cap": f"${market_cap:,.0f}",
                "volume_24h": f"${volume:,.0f}",
                "timestamp": datetime.now().isoformat(),
                "source": "CoinGecko",
                "sentiment": sentiment
            }
        else:
            logger.warning(f"CoinGecko API returned status code {response.status_code}")
            if DEBUG_MODE:
                logger.debug(f"Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching from CoinGecko: {e}")
        return None


def fetch_from_coinmarketcap():
    """Fetch Bitcoin data from CoinMarketCap API (requires API key)."""
    api_key = os.environ.get('COINMARKETCAP_API_KEY')
    if not api_key:
        logger.warning("No CoinMarketCap API key found")
        return None
        
    logger.info("Attempting to fetch data from CoinMarketCap API")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": "BTC",
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key
    }
    
    try:
        logger.debug(f"Making request to: {url}")
        response = requests.get(url, headers=headers, params=parameters, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            btc_data = data['data']['BTC']
            price = btc_data['quote']['USD']['price']
            price_formatted = f"${price:,.0f}" if price >= 1000 else f"${price:.2f}"
            
            price_change_24h = btc_data['quote']['USD']['percent_change_24h']
            price_change_formatted = f"({'+' if price_change_24h >= 0 else ''}{price_change_24h:.2f}%)"
            
            # Extract other key metrics
            market_cap = btc_data['quote']['USD']['market_cap']
            volume = btc_data['quote']['USD']['volume_24h']
            
            # Determine sentiment based on price change
            sentiment = "bullish" if price_change_24h > 1 else "bearish" if price_change_24h < -1 else "neutral"
            
            logger.info(f"Successfully fetched data from CoinMarketCap: {price_formatted} {price_change_formatted}")
            
            return {
                "price": price_formatted,
                "raw_price": price,
                "price_change_24h": price_change_formatted,
                "raw_price_change": price_change_24h,
                "market_cap": f"${market_cap:,.0f}",
                "volume_24h": f"${volume:,.0f}",
                "timestamp": datetime.now().isoformat(),
                "source": "CoinMarketCap",
                "sentiment": sentiment
            }
        else:
            logger.warning(f"CoinMarketCap API returned status code {response.status_code}")
            if DEBUG_MODE:
                logger.debug(f"Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching from CoinMarketCap: {e}")
        return None


def fetch_from_binance():
    """Fetch Bitcoin data from Binance API."""
    logger.info("Attempting to fetch data from Binance API")
    url = "https://api.binance.com/api/v3/ticker/24hr"
    params = {"symbol": "BTCUSDT"}
    
    try:
        logger.debug(f"Making request to: {url}")
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant information
            price = float(data['lastPrice'])
            price_formatted = f"${price:,.0f}" if price >= 1000 else f"${price:.2f}"
            
            price_change_24h = float(data['priceChangePercent'])
            price_change_formatted = f"({'+' if price_change_24h >= 0 else ''}{price_change_24h:.2f}%)"
            
            # Extract other key metrics
            volume = float(data['volume']) * price
            
            # Determine sentiment based on price change
            sentiment = "bullish" if price_change_24h > 1 else "bearish" if price_change_24h < -1 else "neutral"
            
            logger.info(f"Successfully fetched data from Binance: {price_formatted} {price_change_formatted}")
            
            return {
                "price": price_formatted,
                "raw_price": price,
                "price_change_24h": price_change_formatted,
                "raw_price_change": price_change_24h,
                "volume_24h": f"${volume:,.0f}",
                "timestamp": datetime.now().isoformat(),
                "source": "Binance",
                "sentiment": sentiment
            }
        else:
            logger.warning(f"Binance API returned status code {response.status_code}")
            if DEBUG_MODE:
                logger.debug(f"Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching from Binance: {e}")
        return None


def get_news_and_insights():
    """Get Bitcoin news and insights (placeholder, could use a news API)."""
    logger.info("Generating news and insights")
    # This would be replaced with a real implementation fetching news
    insights = [
        {
            "title": "Institutional adoption continues to grow",
            "summary": "Major financial institutions are increasingly adding Bitcoin to their portfolios",
            "sentiment": "bullish"
        },
        {
            "title": "Bitcoin ETF inflows remain strong",
            "summary": "ETFs continue to attract significant capital, indicating growing mainstream interest",
            "sentiment": "bullish"
        },
        {
            "title": "Technical indicators suggest consolidation phase",
            "summary": "After recent gains, on-chain metrics show a period of consolidation may be ahead",
            "sentiment": "neutral"
        }
    ]
    
    # In a real implementation, you would fetch from sources like
    # CryptoCompare News API, Messari, CoinDesk, etc.
    
    return insights


def fetch_bitcoin_data_with_retries():
    """Fetch Bitcoin data with multiple data sources and retry logic."""
    # Try each source with retries
    data_sources = [
        fetch_from_coingecko,
        fetch_from_binance,
        fetch_from_coinmarketcap
    ]
    
    bitcoin_data = None
    
    for source_func in data_sources:
        source_name = source_func.__name__.replace("fetch_from_", "")
        logger.info(f"Trying data source: {source_name}")
        
        for attempt in range(MAX_RETRIES):
            try:
                bitcoin_data = source_func()
                if bitcoin_data:
                    logger.info(f"Successfully fetched data from {bitcoin_data['source']}")
                    return bitcoin_data
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed for {source_name}: {e}")
                
            # Exponential backoff
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY * (2 ** attempt)
                logger.info(f"Retrying {source_name} in {delay} seconds...")
                time.sleep(delay)
        
        logger.warning(f"All {MAX_RETRIES} attempts failed for {source_name}")
    
    logger.error("All data sources failed to fetch Bitcoin data")
    return None


def get_bitcoin_sentiment(data=None):
    """Get overall Bitcoin market sentiment."""
    if data and "raw_price_change" in data:
        # Determine from data
        change = data["raw_price_change"]
        if change > 5:
            return "very bullish"
        elif change > 1:
            return "bullish"
        elif change < -5:
            return "very bearish"
        elif change < -1:
            return "bearish"
        else:
            return "neutral"
    else:
        # Fallback - could use social media sentiment analysis
        sentiments = ["bullish", "neutral", "bearish"]
        weights = [0.5, 0.3, 0.2]  # More likely to be bullish
        return random.choices(sentiments, weights)[0]


def generate_key_points(data, insights):
    """Generate key points for the report based on data and insights."""
    key_points = []
    
    # Add points based on price action
    if data and "raw_price_change" in data:
        change = data["raw_price_change"]
        if change > 3:
            key_points.append(f"Bitcoin is showing strong upward momentum with a {data['price_change_24h']} increase in 24 hours")
        elif change > 1:
            key_points.append(f"Bitcoin is trending upward with a {data['price_change_24h']} gain in the last day")
        elif change < -3:
            key_points.append(f"Bitcoin is experiencing significant downward pressure, falling {data['price_change_24h']} in 24 hours")
        elif change < -1:
            key_points.append(f"Bitcoin is in a slight downtrend, down {data['price_change_24h']} over 24 hours")
        else:
            key_points.append(f"Bitcoin price remains relatively stable with a {data['price_change_24h']} change in 24 hours")
    
    # Add points based on insights
    for insight in insights[:2]:  # Only take the first two insights
        key_points.append(f"{insight['title']}: {insight['summary']}")
    
    # Add additional market context
    if data:
        if "volume_24h" in data:
            key_points.append(f"Trading volume in the last 24 hours: {data['volume_24h']}")
        
        if "market_cap" in data:
            key_points.append(f"Bitcoin's current market cap stands at {data['market_cap']}")
    
    # Ensure we have at least two key points
    while len(key_points) < 2:
        key_points.append("Bitcoin continues to be the leading cryptocurrency by market capitalization")
    
    return key_points[:4]  # Return max 4 key points


def generate_analysis(data, insights):
    """Generate analysis paragraphs for the report."""
    analysis = []
    
    # Add analysis based on price action
    if data and "raw_price_change" in data and "raw_price" in data:
        price = data["raw_price"]
        change = data["raw_price_change"]
        
        # Price action analysis
        if change > 3:
            analysis.append(f"Bitcoin's price has surged significantly, indicating strong buying pressure. The {data['price_change_24h']} increase suggests renewed market optimism.")
        elif change > 1:
            analysis.append(f"Bitcoin is maintaining positive momentum with a {data['price_change_24h']} gain. This moderate increase suggests steady accumulation by investors.")
        elif change < -3:
            analysis.append(f"Bitcoin has seen a sharp correction of {data['price_change_24h']}, potentially indicating profit-taking or a shift in market sentiment. Buyers may look for support levels to establish new positions.")
        elif change < -1:
            analysis.append(f"Bitcoin is experiencing a minor pullback of {data['price_change_24h']}, which is normal within the context of a broader trend. This could present a buying opportunity for those looking to accumulate.")
        else:
            analysis.append(f"Bitcoin's price has remained relatively stable with a {data['price_change_24h']} change, suggesting a consolidation phase where the market is seeking direction.")
        
        # Technical analysis (simplified)
        key_levels = {
            "support_1": round(price * 0.95, -3),  # 5% below current price, rounded
            "support_2": round(price * 0.9, -3),   # 10% below current price, rounded
            "resistance_1": round(price * 1.05, -3),  # 5% above current price, rounded
            "resistance_2": round(price * 1.1, -3)    # 10% above current price, rounded
        }
        
        analysis.append(f"Key technical levels to watch include support at ${key_levels['support_1']:,.0f} and ${key_levels['support_2']:,.0f}, with resistance at ${key_levels['resistance_1']:,.0f} and ${key_levels['resistance_2']:,.0f}.")
    
    # Add analysis based on insights
    insight_analysis = []
    for insight in insights:
        if insight['sentiment'] == 'bullish':
            insight_analysis.append(f"Bullish Factor: {insight['title']} - {insight['summary']}")
        elif insight['sentiment'] == 'bearish':
            insight_analysis.append(f"Bearish Factor: {insight['title']} - {insight['summary']}")
        else:
            insight_analysis.append(f"{insight['title']} - {insight['summary']}")
    
    if insight_analysis:
        analysis.append("Market Factors: " + " ".join(insight_analysis))
    
    return analysis


def generate_outlook(data, insights):
    """Generate market outlook based on data and insights."""
    sentiment = get_bitcoin_sentiment(data)
    
    # Count the sentiment in insights
    sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
    for insight in insights:
        if insight['sentiment'] in sentiment_counts:
            sentiment_counts[insight['sentiment']] += 1
    
    # Determine the dominant sentiment from insights
    max_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    
    # Combine data sentiment with insight sentiment
    if sentiment == max_sentiment:
        # Strong consensus
        strength = "strongly" if sentiment in ["very bullish", "very bearish"] else "moderately"
    else:
        # Mixed signals
        strength = "cautiously"
    
    # Generate appropriate outlook statement
    if sentiment in ["very bullish", "bullish"]:
        outlook = f"{strength.capitalize()} bullish with upward momentum likely to continue. Support at ${data['raw_price']*0.9:,.0f} & resistance around ${data['raw_price']*1.1:,.0f}"
    elif sentiment in ["very bearish", "bearish"]:
        outlook = f"{strength.capitalize()} bearish with further consolidation possible. Support at ${data['raw_price']*0.85:,.0f} & resistance at current levels around ${data['raw_price']:,.0f}"
    else:
        outlook = f"Neutral with {strength} optimistic bias. Market in consolidation phase between ${data['raw_price']*0.95:,.0f} and ${data['raw_price']*1.05:,.0f}"
    
    return outlook


def prepare_report_data(fetch_data=True):
    """Prepare complete report data structure."""
    # Initialize with timestamp
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%B %d, %Y")
    }
    
    # Fetch Bitcoin market data
    bitcoin_data = None
    if fetch_data:
        bitcoin_data = fetch_bitcoin_data_with_retries()
    
    if not bitcoin_data:
        logger.warning("Could not fetch real Bitcoin data, using fallback values")
        # Fallback values
        bitcoin_data = {
            "price": "$84,570",
            "raw_price": 84570,
            "price_change_24h": "(+3.60%)",
            "raw_price_change": 3.60,
            "market_cap": "$1,650,000,000,000",
            "volume_24h": "$48,000,000,000",
            "source": "Fallback",
            "sentiment": "bullish"
        }
    
    # Get news and insights
    insights = get_news_and_insights()
    
    # Generate key points, analysis and outlook
    key_points = generate_key_points(bitcoin_data, insights)
    analysis = generate_analysis(bitcoin_data, insights)
    outlook = generate_outlook(bitcoin_data, insights)
    
    # Combine all data
    report_data.update({
        "price": bitcoin_data["price"],
        "price_change_24h": bitcoin_data["price_change_24h"],
        "market_cap": bitcoin_data.get("market_cap", "N/A"),
        "volume_24h": bitcoin_data.get("volume_24h", "N/A"),
        "data_source": bitcoin_data["source"],
        "sentiment": bitcoin_data["sentiment"],
        "key_points": key_points,
        "analysis": analysis,
        "outlook": outlook,
        "insights": insights
    })
    
    return report_data


def save_report_data(report_data):
    """Save report data to files and set GitHub environment variables."""
    # Create necessary directories
    os.makedirs(".github/tmp", exist_ok=True)
    
    # Set environment variables for the workflow
    today = datetime.now().strftime("%Y-%m-%d")
    post_slug = f"bitcoin-market-report-{today}"
    post_title = f"Bitcoin Market Report - {datetime.now().strftime('%B %d, %Y')}"
    newsletter_data_file = f".github/tmp/{post_slug}-newsletter-data.json"
    
    # Create the social content file
    with open(".github/tmp/social_content.txt", "w") as f:
        f.write(f"📈 #Bitcoin update:\n")
        f.write(f"Price: {report_data['price']} {report_data['price_change_24h']}\n")
        
        # Add key points (using only the first two)
        for i, point in enumerate(report_data['key_points'][:2], 1):
            f.write(f"{i}. {point}\n")
        
        # Add outlook
        f.write(f"Outlook: {report_data['outlook']}. #BTC #Crypto")
    
    logger.info(f"Created social content at .github/tmp/social_content.txt")
    
    # Write data to JSON file for other scripts to use
    with open(newsletter_data_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"Saved report data to {newsletter_data_file}")
    
    # Set environment variables if running in GitHub Actions
    github_env = os.environ.get('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a') as env_file:
            env_file.write(f"TODAY={today}\n")
            env_file.write(f"POST_SLUG={post_slug}\n")
            env_file.write(f"POST_TITLE={post_title}\n")
            env_file.write(f"NEWSLETTER_DATA_FILE={newsletter_data_file}\n")
            env_file.write(f"BITCOIN_PRICE={report_data['price']}\n")
            env_file.write(f"BITCOIN_CHANGE={report_data['price_change_24h']}\n")
        
        logger.info(f"Set environment variables in GitHub Actions")
    else:
        # For local testing
        print(f"TODAY={today}")
        print(f"POST_SLUG={post_slug}")
        print(f"POST_TITLE={post_title}")
        print(f"NEWSLETTER_DATA_FILE={newsletter_data_file}")
    
    return True


def validate_fetched_data(data):
    """Validate that the fetched data contains expected fields."""
    required_fields = ["price", "price_change_24h", "timestamp", "source"]
    
    if not data:
        logger.error("Data validation failed: No data provided")
        return False
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.error(f"Data validation failed: Missing fields {missing_fields}")
        return False
    
    logger.info("Data validation passed")
    return True


def main():
    """Main function to run the Bitcoin data fetcher."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Fetch Bitcoin market data')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--test', action='store_true', help='Use test data instead of fetching')
    args = parser.parse_args()
    
    # Set debug mode if requested
    if args.debug:
        global DEBUG_MODE
        DEBUG_MODE = True
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled via command line")
    
    try:
        # Prepare report data
        logger.info("Starting Bitcoin data fetching process")
        report_data = prepare_report_data(fetch_data=not args.test)
        
        # Save the data
        success = save_report_data(report_data)
        
        if success:
            logger.info("Bitcoin data fetching and processing completed successfully")
            logger.info(f"Price: {report_data['price']} {report_data['price_change_24h']}")
            logger.info(f"Key point 1: {report_data['key_points'][0]}")
            logger.info(f"Source: {report_data['data_source']}")
            return 0
        else:
            logger.error("Failed to save report data")
            return 1
            
    except Exception as e:
        logger.error(f"Unhandled exception in main: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 