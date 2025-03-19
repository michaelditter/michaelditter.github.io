#!/usr/bin/env python3
import os
import sys
import json
import requests
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import re
import datetime

# Buttondown API configuration
BUTTONDOWN_API_KEY = os.environ.get("BUTTONDOWN_API_KEY")
BUTTONDOWN_API_URL = "https://api.buttondown.email/v1/emails"

def strip_markdown_links(text):
    """Convert markdown links to plain text, keeping the link text"""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

def convert_markdown_to_html(markdown_text):
    """Convert markdown to HTML for email"""
    # Use the Python markdown library
    html = markdown.markdown(markdown_text, extensions=['extra'])
    return html

def clean_html_content(html_content):
    """Clean HTML content for email newsletter formatting"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Add inline styles for better email client compatibility
    for h1 in soup.find_all('h1'):
        h1['style'] = 'font-size: 28px; color: #333; margin-top: 30px; margin-bottom: 10px;'
    
    for h2 in soup.find_all('h2'):
        h2['style'] = 'font-size: 24px; color: #333; margin-top: 25px; margin-bottom: 10px;'
    
    for h3 in soup.find_all('h3'):
        h3['style'] = 'font-size: 20px; color: #333; margin-top: 20px; margin-bottom: 10px;'
    
    for p in soup.find_all('p'):
        p['style'] = 'font-size: 16px; line-height: 1.6; margin-bottom: 15px; color: #444;'
    
    for ul in soup.find_all('ul'):
        ul['style'] = 'margin-bottom: 15px; padding-left: 20px;'
    
    for li in soup.find_all('li'):
        li['style'] = 'font-size: 16px; line-height: 1.6; margin-bottom: 5px; color: #444;'
    
    for a in soup.find_all('a'):
        a['style'] = 'color: #0066cc; text-decoration: underline;'
    
    for strong in soup.find_all('strong'):
        strong['style'] = 'font-weight: bold; color: #333;'
    
    return str(soup)

def send_newsletter(newsletter_data_file):
    """Send a newsletter via Buttondown API"""
    if not BUTTONDOWN_API_KEY:
        print("Error: BUTTONDOWN_API_KEY environment variable is required.")
        return False
    
    try:
        with open(newsletter_data_file, 'r') as f:
            newsletter_data = json.load(f)
        
        title = newsletter_data.get("title")
        content = newsletter_data.get("content")
        description = newsletter_data.get("description")
        url = newsletter_data.get("url")
        
        if not all([title, content, url]):
            print("Error: Missing required newsletter data (title, content, or URL).")
            return False
        
        # Create email subject
        email_subject = title
        
        # Create email body - first convert markdown to HTML, then clean the HTML
        html_content = convert_markdown_to_html(content)
        cleaned_html = clean_html_content(html_content)
        
        # Add a header with the title
        header = f'<h1 style="font-size: 32px; color: #333; margin-bottom: 20px;">{title}</h1>'
        
        # Add a preheader (intro text)
        preheader = f'<p style="font-size: 18px; font-style: italic; color: #666; margin-bottom: 25px;">{description}</p>'
        
        # Add a footer with link to full article
        footer = f'''
        <hr style="margin: 30px 0; border: 0; border-top: 1px solid #eee;">
        <p style="font-size: 16px; color: #666;">
            <em>This is an excerpt from my latest article. 
            <a href="{url}" target="_blank" style="color: #0066cc; font-weight: bold;">Read the full post on my website</a>.</em>
        </p>
        <p style="font-size: 14px; color: #999; margin-top: 30px;">
            © {datetime.datetime.now().year} Michael J Ditter. All rights reserved.<br>
            <a href="https://www.michaelditter.com" target="_blank" style="color: #999;">michaelditter.com</a>
        </p>
        '''
        
        # Combine all parts
        full_email_content = f'{header}\n{preheader}\n{cleaned_html}\n{footer}'
        
        # Prepare data for Buttondown API
        api_data = {
            "subject": email_subject,
            "body": full_email_content,
            "status": "draft"  # Set to "draft" to review before sending
        }
        
        # Add tags if available
        if tags := newsletter_data.get("tags"):
            api_data["tags"] = tags
        
        # Send to Buttondown API
        headers = {
            "Authorization": f"Token {BUTTONDOWN_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            BUTTONDOWN_API_URL,
            headers=headers,
            json=api_data
        )
        
        if response.status_code in (200, 201):
            result = response.json()
            print(f"Newsletter draft created successfully!")
            print(f"Draft ID: {result.get('id')}")
            print(f"Status: {result.get('status')}")
            print(f"Preview URL: {result.get('preview_url')}")
            return True
        else:
            print(f"Error creating newsletter: {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print(f"Error sending newsletter: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_buttondown_newsletter.py <newsletter_data_file>")
        sys.exit(1)
    
    newsletter_data_file = sys.argv[1]
    if not os.path.exists(newsletter_data_file):
        print(f"Error: Newsletter data file not found: {newsletter_data_file}")
        sys.exit(1)
    
    success = send_newsletter(newsletter_data_file)
    sys.exit(0 if success else 1) 