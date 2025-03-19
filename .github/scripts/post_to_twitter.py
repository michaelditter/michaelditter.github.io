#!/usr/bin/env python3
import os
import sys
import requests
import json
from requests_oauthlib import OAuth1

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
        return False
    
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
    
    if len(sys.argv) > 1:
        content = sys.argv[1]
    
    if not content:
        print("Error: No content provided for Twitter/X post.")
        print("Usage: python post_to_twitter.py 'Your tweet content' OR set SOCIAL_CONTENT env var")
        sys.exit(1)
    
    # Enforce Twitter character limit
    if len(content) > 280:
        print(f"Warning: Content exceeds Twitter's 280 character limit ({len(content)} chars). Truncating...")
        content = content[:277] + "..."
    
    # Post to Twitter
    success = post_to_twitter(content)
    sys.exit(0 if success else 1) 