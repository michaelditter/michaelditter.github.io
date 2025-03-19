#!/usr/bin/env python3
import re
import os
from pathlib import Path

def clean_content(content):
    """Clean and validate the content before posting to Twitter/X."""
    # Strip any leading/trailing whitespace
    content = content.strip()
    
    # Remove any environment file commands if they exist
    content = re.sub(r'file command \'env\'.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'Error: Unable to process file.*$', '', content, flags=re.MULTILINE)
    
    # Remove any error messages about format
    content = re.sub(r'Error: Invalid format.*$', '', content, flags=re.MULTILINE)
    
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
    price_pattern = r'Price: \$([0-9,]+)(?:\.\d+)? \(([+-]\d+\.\d+%)(?: in 24h)?\)'
    match = re.search(price_pattern, content)
    
    if match:
        price = match.group(1)
        change = match.group(2)
        print(f"Detected Bitcoin price: ${price} {change}")
        return True
    else:
        print("Could not detect price information in the content")
        # Try alternative formats
        alt_pattern = r'\$([0-9,]+)(?:\.\d+)?.*?([+-]\d+\.\d+%)'
        alt_match = re.search(alt_pattern, content)
        if alt_match:
            price = alt_match.group(1)
            change = alt_match.group(2)
            print(f"Detected Bitcoin price (alternative format): ${price} {change}")
            return True
    
    return False

def main():
    print("Simple Twitter Content Test")
    print("==========================")
    
    # Sample content from the report generation
    sample_content = """📈 #Bitcoin update:
Price: $84,556 (+3.52% in 24h)
Key developments: SEC's Bitcoin ETF decision pending, institutional adoption grows
Outlook: Potential move to $90,000, watch $80,000 support
Stay updated! 🚀💰 #BTC #Crypto
Error: Unable to process file command 'env' successfully.
Error: Invalid format 'Price: $84,556 (+3.52% in 24h)'"""
    
    # Check if we have a real social content file to use
    content_file = Path("..") / "tmp" / "social_content.txt"
    if content_file.exists():
        print(f"Found actual social content file: {content_file}")
        try:
            with open(content_file, "r") as f:
                file_content = f.read()
                print("\nACTUAL CONTENT FROM FILE:")
                print("-" * 40)
                print(file_content)
                print("-" * 40)
                
                # Process the actual content
                print("\nCLEANED ACTUAL CONTENT:")
                print("-" * 40)
                cleaned_file_content = clean_content(file_content)
                print(cleaned_file_content)
                print("-" * 40)
                print(f"Character count: {len(cleaned_file_content)}")
                extract_price_info(cleaned_file_content)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
    
    # Process the sample content
    print("\nCLEANED SAMPLE CONTENT:")
    print("-" * 40)
    cleaned_content = clean_content(sample_content)
    print(cleaned_content)
    print("-" * 40)
    print(f"Character count: {len(cleaned_content)}")
    extract_price_info(cleaned_content)
    
    print("\nTest completed. If you see the content above without error messages, the cleaning is working correctly.")
    print("\nTo enable Twitter posting, you need to add your Twitter API credentials to GitHub Secrets:")
    print("TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET")

if __name__ == "__main__":
    main() 