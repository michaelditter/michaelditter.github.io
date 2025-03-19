#!/usr/bin/env python3
import os
import sys
import requests
import json
import re
from requests_oauthlib import OAuth1

def clean_content(content):
    """Clean and validate the content before posting to Twitter/X."""
    # Strip any leading/trailing whitespace
    content = content.strip()
    
    # First, remove any lines that start with "Error:"
    lines = content.split('\n')
    cleaned_lines = [line for line in lines if not line.startswith('Error:')]
    content = '\n'.join(cleaned_lines)
    
    # Remove any environment file commands if they exist
    content = re.sub(r'file command \'env\'.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'Unable to process file.*$', '', content, flags=re.MULTILINE)
    
    # Remove any error messages about format
    content = re.sub(r'Invalid format.*$', '', content, flags=re.MULTILINE)
    
    # Remove lines related to GitHub Actions environment variables
    content = re.sub(r'GITHUB_ENV=.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'>>.*GITHUB_ENV.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'::set-output.*$', '', content, flags=re.MULTILINE)
    
    # Clean up any empty lines from removed content
    content = re.sub(r'\n\s*\n+', '\n\n', content)
    
    # Ensure the content is under Twitter's character limit
    if len(content) > 280:
        print(f"Warning: Content exceeds Twitter's 280 character limit ({len(content)} chars). Truncating...")
        content = content[:277] + "..."
    
    return content

def extract_price_info(content):
    """Extract price information for logging purposes."""
    # Updated pattern to handle "in 24h" format
    price_pattern = r'Price: \$([0-9,]+)(?:\.\d+)? \(([+-]\d+\.\d+%)(?: in 24h)?\)'
    match = re.search(price_pattern, content)
    
    if match:
        price = match.group(1)
        change = match.group(2)
        print(f"Detected Bitcoin price: ${price} {change}")
    else:
        print("Could not detect price information in the content using main pattern")
        # Try alternative formats
        alt_pattern = r'\$([0-9,]+)(?:\.\d+)?.*?([+-]\d+\.\d+%)'
        alt_match = re.search(alt_pattern, content)
        if alt_match:
            price = alt_match.group(1)
            change = alt_match.group(2)
            print(f"Detected Bitcoin price (alternative format): ${price} {change}")
        else:
            print("Could not detect price information with alternative pattern either")
    
    return content

def post_to_twitter(content):
    """Post content to Twitter/X using API v1.1"""
    # Get API credentials from environment variables
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET")
    
    # Validate credentials
    if not all([api_key, api_secret, access_token, access_secret]):
        print("Error: Twitter API credentials are missing. Cannot post update.")
        print("Debug: Would have posted the following content:")
        print("=" * 40)
        print(content)
        print("=" * 40)
        print("To enable posting, set the following GitHub Secrets:")
        print("TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET")
        # Return True to avoid workflow failure when credentials are missing
        return True
    
    # Create OAuth session
    auth = OAuth1(
        api_key,
        client_secret=api_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_secret
    )
    
    # Twitter API v1.1 endpoint for posting tweets
    url = "https://api.twitter.com/1.1/statuses/update.json"
    
    # Prepare the payload
    payload = {
        "status": content
    }
    
    # Make the request
    try:
        response = requests.post(url, auth=auth, data=payload)
        
        # Check if successful
        if response.status_code == 200:
            tweet_data = response.json()
            tweet_id = tweet_data.get("id_str")
            print(f"Successfully posted to Twitter/X! Tweet ID: {tweet_id}")
            print(f"View at: https://twitter.com/i/web/status/{tweet_id}")
            return True
        else:
            print(f"Error posting to Twitter/X: HTTP {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print(f"Exception when posting to Twitter/X: {str(e)}")
        return False

if __name__ == "__main__":
    # Read content from environment variable or command line
    content = os.environ.get("SOCIAL_CONTENT")
    
    # If not found in environment, try command line argument
    if not content and len(sys.argv) > 1:
        content = sys.argv[1]
    
    # If still no content, check for a file with the content
    if not content and os.path.exists(".github/tmp/social_content.txt"):
        try:
            with open(".github/tmp/social_content.txt", "r") as f:
                content = f.read().strip()
        except Exception as e:
            print(f"Error reading from social content file: {str(e)}")
    
    if not content:
        print("Error: No content provided for Twitter/X post.")
        print("Usage: python post_to_twitter.py 'Your tweet content' OR set SOCIAL_CONTENT env var")
        sys.exit(1)
    
    # Clean and process the content
    content = clean_content(content)
    content = extract_price_info(content)
    
    print("Prepared content for posting:")
    print("=" * 40)
    print(content)
    print("=" * 40)
    print(f"Character count: {len(content)}/280")
    
    # Post to Twitter
    success = post_to_twitter(content)
    sys.exit(0 if success else 1) 