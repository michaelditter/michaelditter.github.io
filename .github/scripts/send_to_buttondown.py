#!/usr/bin/env python3
"""
Send Bitcoin report to Buttondown newsletter.
This script takes the generated Bitcoin report and sends it as a newsletter through Buttondown's API.
"""

import os
import json
import sys
import requests
from datetime import datetime

def main():
    # Get API key from environment variable
    api_key = os.environ.get('BUTTONDOWN_API_KEY')
    if not api_key:
        print("Error: BUTTONDOWN_API_KEY environment variable not found")
        sys.exit(1)
    
    # Get the newsletter data file from input argument
    if len(sys.argv) < 2:
        print("Error: Please provide the path to the newsletter data JSON file")
        sys.exit(1)
    
    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"Error: Newsletter data file not found: {data_file}")
        sys.exit(1)
    
    # Load the newsletter data
    try:
        with open(data_file, 'r') as f:
            newsletter_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in newsletter data file: {data_file}")
        sys.exit(1)
    
    # Extract data
    date_str = newsletter_data.get('date', datetime.now().strftime("%B %d, %Y"))
    title = newsletter_data.get('title', f"Bitcoin Market Report: {date_str}")
    
    # Construct HTML content
    html_content = f"""
    <h1>Bitcoin Market Report: {date_str}</h1>
    
    <h2>Market Summary</h2>
    <p><strong>Current Price:</strong> {newsletter_data.get('price', 'Not available')}</p>
    <p><strong>24h Change:</strong> {newsletter_data.get('price_change_24h', 'Not available')}</p>
    
    <h2>Key Developments</h2>
    <ul>
    """
    
    # Add key developments
    for point in newsletter_data.get('key_points', []):
        html_content += f"<li>{point}</li>\n"
    
    html_content += """
    </ul>
    
    <h2>Market Analysis</h2>
    """
    
    # Add market analysis
    for section in newsletter_data.get('analysis', []):
        html_content += f"<p>{section}</p>\n"
    
    # Add footer with link to full report and FAQ guide
    post_slug = os.path.basename(data_file).replace('-newsletter-data.json', '')
    
    html_content += f"""
    <p><a href="https://www.michaelditter.com/blog/{post_slug}/">Read the full report on my website</a></p>
    
    <hr>
    
    <p><em>P.S. New subscribers receive my comprehensive 
    <a href="https://www.michaelditter.com/assets/private/guides/ai7fx92d5e/?source=newsletter">AI Marketing FAQ Guide</a></em></p>
    """
    
    # Prepare the API request
    url = "https://api.buttondown.email/v1/emails"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "subject": title,
        "body": html_content,
        "status": "draft"  # Set to "draft" so you can review before sending
    }
    
    # Send the request
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Successfully created newsletter draft in Buttondown!")
        print(f"Newsletter ID: {response.json().get('id')}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Buttondown API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 