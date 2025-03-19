#!/usr/bin/env python3
import sys
from post_to_twitter import clean_content, extract_price_info

# Sample content with the problematic format
sample_content = """📈 #Bitcoin update:
Price: $84,556 (+3.52% in 24h)
Key developments: SEC's Bitcoin ETF decision pending, institutional adoption grows
Outlook: Potential move to $90,000, watch $80,000 support
Stay updated! 🚀💰 #BTC #Crypto
Error: Unable to process file command 'env' successfully.
Error: Invalid format 'Price: $84,556 (+3.52% in 24h)'"""

# Sample with GitHub environment variable messages
sample_with_env = """📈 #Bitcoin update:
Price: $84,556 (+3.52% in 24h)
Key developments: SEC's Bitcoin ETF decision pending, institutional adoption grows
Outlook: Potential move to $90,000, watch $80,000 support
Stay updated! 🚀💰 #BTC #Crypto
GITHUB_ENV=/home/runner/work/_temp/.runner_file_commands/set_env_cb066c13-f50d-4c9c-8cc0-1b1a0b74a0f0
echo "SOCIAL_CONTENT<<EOF" >> $GITHUB_ENV"""

# Clean the content
cleaned_content = clean_content(sample_content)
print("CLEANED CONTENT:")
print("-" * 40)
print(cleaned_content)
print("-" * 40)
print(f"Character count: {len(cleaned_content)}")
print()

# Check price extraction
extract_price_info(cleaned_content)
print()

# Test with env variables
cleaned_env_content = clean_content(sample_with_env)
print("CLEANED CONTENT WITH ENV VARS:")
print("-" * 40)
print(cleaned_env_content)
print("-" * 40)
print(f"Character count: {len(cleaned_env_content)}")

# Check price extraction on env content
extract_price_info(cleaned_env_content)

print("\nTest completed. If no errors are shown above, the cleaning is working correctly.") 