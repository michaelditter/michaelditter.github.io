#!/usr/bin/env python3
"""
Update the Bitcoin Twitter card in index.html to point to the latest report.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

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
        print(f"Error: {index_path} not found")
        return False
    
    # Read the file
    with open(index_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Update the link to the latest report
    content = re.sub(
        r'<a href="/blog/bitcoin-market-report-\d{4}-\d{2}-\d{2}/" class="twitter-card">',
        f'<a href="/blog/{report_slug}/" class="twitter-card">',
        content
    )
    
    # Update the date in the card
    content = re.sub(
        r'<span>Updated (Daily|Weekly) · Latest: .+?</span>',
        f'<span>Updated Daily · Latest: {report_date}</span>',
        content
    )
    
    # If we have report data, update the content of the card
    if report_data:
        # Create the Twitter content with the latest data
        price = report_data.get('price', '$84,570')
        price_change = report_data.get('price_change_24h', '(+3.60%)')
        
        # Get the key points (or use defaults if not available)
        key_points = report_data.get('key_points', [
            "Positive regulatory moves & pending SEC Bitcoin ETF decision",
            "Institutional adoption with Fidelity & BlackRock"
        ])
        
        # Format first two key points for Twitter card
        point1 = key_points[0] if len(key_points) > 0 else ""
        point2 = key_points[1] if len(key_points) > 1 else ""
        
        # Get outlook or use default
        outlook = report_data.get('outlook', "Bullish with support at $80K & resistance at $100K")
        
        # Update the Twitter content
        twitter_content = f"""<p>📈 #Bitcoin update:<br>
                        Price: {price} {price_change}<br>
                        1. {point1}<br>
                        2. {point2}<br>
                        Outlook: {outlook}. #BTC #Crypto</p>"""
        
        # Replace the content using regex
        content = re.sub(
            r'<div class="twitter-content">[\s\S]*?</div>',
            f'<div class="twitter-content">\n                        {twitter_content}\n                    </div>',
            content,
            count=1  # Only replace the first occurrence after the previous replacements
        )
    
    # Write the updated content back to the file
    with open(index_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"Successfully updated index.html Bitcoin card to point to {report_slug}")
    return True

def main():
    # Get the report slug from command line argument or environment variable
    report_slug = None
    report_date = None
    json_data_file = None
    
    # Check command line arguments
    if len(sys.argv) > 1:
        report_slug = sys.argv[1]
    
    # If not provided via command line, check environment variables
    if not report_slug:
        report_slug = os.environ.get("POST_SLUG")
    
    # If still not available, generate it based on current date
    if not report_slug:
        today = datetime.now()
        report_slug = f"bitcoin-market-report-{today.strftime('%Y-%m-%d')}"
    
    # Check for JSON data file
    if len(sys.argv) > 2:
        json_data_file = sys.argv[2]
    else:
        json_data_file = os.environ.get("NEWSLETTER_DATA_FILE")
    
    # Format the date as "Mar DD, YYYY"
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", report_slug)
    if date_match:
        year, month, day = date_match.groups()
        date_obj = datetime(int(year), int(month), int(day))
        report_date = date_obj.strftime("%b %d, %Y")
    else:
        report_date = datetime.now().strftime("%b %d, %Y")
    
    # Load report data if available
    report_data = None
    if json_data_file and os.path.exists(json_data_file):
        import json
        try:
            with open(json_data_file, 'r') as f:
                report_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from {json_data_file}")
    
    # Update the index.html file
    success = update_index_html(report_date, report_slug, report_data)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 