#!/usr/bin/env python3
"""
Update the Bitcoin Twitter card in index.html to point to the latest report.
"""

import os
import re
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bitcoin_card_updater')

# Try to load formatting configuration
CONFIG_PATH = Path(".github/config/report_format.json")
try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
    logger.info(f"Loaded configuration from {CONFIG_PATH}")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.warning(f"Could not load configuration: {e}")
    # Default configuration if file not found or invalid
    CONFIG = {
        "emojis": {
            "price": "📈",
            "key_points": "🔑",
            "analysis": "📊",
            "outlook": "🔮",
            "bullish": "🚀",
            "bearish": "📉",
            "neutral": "⏺️",
            "point1": "1️⃣",
            "point2": "2️⃣",
            "point3": "3️⃣"
        },
        "styling": {
            "use_color_coding": True,
            "positive_color": "#28a745",
            "negative_color": "#dc3545",
            "neutral_color": "#6c757d"
        },
        "twitter_card": {
            "update_frequency": "Daily",
            "max_points": 2,
            "include_outlook": True
        }
    }

def get_change_class(price_change):
    """Determine the CSS class for price change."""
    if not price_change:
        return "neutral"
    
    # Extract numeric value from formatted price change string
    # E.g., "(+3.60%)" -> "+3.60" -> 3.60
    change_str = re.search(r'([+-]?\d+\.?\d*)', price_change)
    if not change_str:
        return "neutral"
    
    change = float(change_str.group(1))
    if change > 0:
        return "positive"
    elif change < 0:
        return "negative"
    else:
        return "neutral"

def get_sentiment_emoji(price_change):
    """Get appropriate emoji based on price change."""
    if not price_change:
        return CONFIG["emojis"]["neutral"]
    
    # Extract numeric value
    change_str = re.search(r'([+-]?\d+\.?\d*)', price_change)
    if not change_str:
        return CONFIG["emojis"]["neutral"]
    
    change = float(change_str.group(1))
    if change > 3:
        return CONFIG["emojis"]["very_bullish"] if "very_bullish" in CONFIG["emojis"] else CONFIG["emojis"]["bullish"]
    elif change > 0:
        return CONFIG["emojis"]["bullish"]
    elif change < -3:
        return CONFIG["emojis"]["very_bearish"] if "very_bearish" in CONFIG["emojis"] else CONFIG["emojis"]["bearish"]
    elif change < 0:
        return CONFIG["emojis"]["bearish"]
    else:
        return CONFIG["emojis"]["neutral"]

def update_index_html(report_date, report_slug, report_data=None):
    """
    Update the Bitcoin Twitter card in index.html to point to the latest report.
    
    Args:
        report_date (str): The date of the report in format "Mar DD, YYYY"
        report_slug (str): The slug of the report (e.g., bitcoin-market-report-2025-03-21)
        report_data (dict, optional): Report data to update the card content
    """
    # Get the index.html path
    index_path = Path("index.html")
    if not index_path.exists():
        logger.error(f"Error: {index_path} not found")
        return False
    
    # Read the file
    with open(index_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    logger.debug("Reading index.html content for update")
    
    # First, locate the Bitcoin Research card specifically
    content_parts = content.split('<!-- Bitcoin Research Index Card -->')
    
    if len(content_parts) < 2:
        logger.error("Could not find Bitcoin Research card section")
        return False
    
    # Get the pre-Bitcoin card content and the Bitcoin card + remaining content
    pre_card_content = content_parts[0]
    post_section = content_parts[1]
    
    # Find the closing div for the Bitcoin card container
    card_end_match = re.search(r'</div>\s*<!-- Bitcoin Research Index Card -->', post_section)
    if not card_end_match:
        card_end_match = re.search(r'</div>\s*<div class="insight-card">', post_section)
    
    if not card_end_match:
        # Try to find the end of the card section
        card_section_match = re.search(r'<div class="twitter-card-container">.*?</div>\s*\n\s*<div', post_section, re.DOTALL)
        if card_section_match:
            bitcoin_card = card_section_match.group(0)
            bitcoin_card = bitcoin_card[:-4]  # Remove the trailing <div
        else:
            logger.error("Could not find the end of the Bitcoin card")
            return False
    else:
        # Extract just the card container
        end_index = card_end_match.start() + 6  # Add 6 to include the closing </div>
        bitcoin_card = post_section[:end_index]
    
    logger.info(f"Found Bitcoin card section of length {len(bitcoin_card)}")
    logger.debug(f"Bitcoin card starts with: {bitcoin_card[:200]}...")
    
    # Update the link to the latest report
    updated_card = re.sub(
        r'<a href="/blog/bitcoin-market-report-[^"]+"',
        f'<a href="/blog/{report_slug}/"',
        bitcoin_card
    )
    
    # Update the date in the card
    update_frequency = CONFIG.get("twitter_card", {}).get("update_frequency", "Daily")
    updated_card = re.sub(
        r'<span>Updated (Daily|Weekly) · Latest: .+?</span>',
        f'<span>Updated {update_frequency} · Latest: {report_date}</span>',
        updated_card
    )
    
    # If we have report data, update the content of the card
    if report_data:
        # Get data for the card
        price = report_data.get('price', '$84,570')
        price_change = report_data.get('price_change_24h', '(+3.60%)')
        change_class = get_change_class(price_change)
        sentiment_emoji = get_sentiment_emoji(price_change)
        
        # Get the key points (or use defaults if not available)
        key_points = report_data.get('key_points', [
            "Positive regulatory moves & pending SEC Bitcoin ETF decision",
            "Institutional adoption with Fidelity & BlackRock"
        ])
        
        # Format key points for Twitter card
        max_points = min(CONFIG.get("twitter_card", {}).get("max_points", 2), len(key_points))
        formatted_points = []
        for i, point in enumerate(key_points[:max_points]):
            point_num = i + 1
            emoji = CONFIG["emojis"].get(f"point{point_num}", f"{point_num}.")
            formatted_points.append(f"{emoji} {point}")
        
        # Get outlook or use default
        outlook = report_data.get('outlook', "Bullish with support at $80K & resistance at $100K")
        include_outlook = CONFIG.get("twitter_card", {}).get("include_outlook", True)
        
        # Create the new content with proper formatting
        new_content = f"""<p>{CONFIG['emojis']['price']} #Bitcoin update:<br>
Price: {price} <span class="{change_class}">{price_change}</span><br>
{('<br>'.join(formatted_points))}<br>
{CONFIG['emojis']['outlook']} Outlook: {outlook}. #BTC #Crypto</p>"""
        
        # Replace the content using regex - carefully matching the structure
        updated_card = re.sub(
            r'<div class="twitter-content">[\s\S]*?</div>',
            f'<div class="twitter-content">\n                        {new_content}\n                    </div>',
            updated_card
        )
    
    # Replace the entire Bitcoin card in the original content
    updated_content = pre_card_content + '<!-- Bitcoin Research Index Card -->' + updated_card
    
    # Properly join with the rest of the content
    rest_of_content = post_section[len(bitcoin_card):]
    updated_content += rest_of_content
    
    # Write the updated content back to the file
    with open(index_path, "w", encoding="utf-8") as file:
        file.write(updated_content)
    
    logger.info(f"Successfully updated index.html Bitcoin card to point to {report_slug}")
    return True

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Update Bitcoin Twitter card on the website")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--data-file", type=str, help="Path to the JSON data file")
    parser.add_argument("--report-slug", type=str, help="Report slug (format: bitcoin-market-report-YYYY-MM-DD)")
    parser.add_argument("--report-date", type=str, help="Report date (format: Mar DD, YYYY)")
    args = parser.parse_args()
    
    # Set up debug mode if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Get the report slug
    report_slug = args.report_slug or os.environ.get("POST_SLUG")
    
    # If still not available, generate it based on current date
    if not report_slug:
        today = datetime.now()
        report_slug = f"bitcoin-market-report-{today.strftime('%Y-%m-%d')}"
        logger.info(f"Generated report slug: {report_slug}")
    
    # Get the report date
    report_date = args.report_date
    
    # If not provided, format from slug or use current date
    if not report_date:
        date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", report_slug)
        if date_match:
            year, month, day = date_match.groups()
            date_obj = datetime(int(year), int(month), int(day))
            report_date = date_obj.strftime("%b %d, %Y")
        else:
            report_date = datetime.now().strftime("%b %d, %Y")
        logger.info(f"Using report date: {report_date}")
    
    # Get the data file path
    json_data_file = args.data_file or os.environ.get("NEWSLETTER_DATA_FILE")
    
    # Load report data if available
    report_data = None
    if json_data_file and os.path.exists(json_data_file):
        try:
            with open(json_data_file, 'r') as f:
                report_data = json.load(f)
            logger.info(f"Loaded report data from {json_data_file}")
            
            # Debug the data
            logger.info(f"Report data: price={report_data.get('price')}, change={report_data.get('price_change_24h')}")
            if 'key_points' in report_data:
                logger.info(f"Key points: {report_data['key_points'][:2]}")
            
        except json.JSONDecodeError:
            logger.warning(f"Could not parse JSON from {json_data_file}")
    else:
        logger.warning(f"Data file not found or not specified: {json_data_file}")
    
    # Update the index.html file
    success = update_index_html(report_date, report_slug, report_data)
    if not success:
        logger.error("Failed to update index.html")
        sys.exit(1)
    
    logger.info("Bitcoin Twitter card updated successfully")

if __name__ == "__main__":
    main() 