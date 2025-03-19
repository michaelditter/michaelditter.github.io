#!/usr/bin/env python3
import os
import sys
import re

def clean_social_content(content):
    """Clean social content before saving to remove any potential issues."""
    # Strip any leading/trailing whitespace
    content = content.strip()
    
    # Remove any lines with error messages
    lines = content.split('\n')
    cleaned_lines = [line for line in lines if not line.startswith('Error:')]
    
    # Rejoin the lines
    content = '\n'.join(cleaned_lines)
    
    # Remove environment-related issues that might appear in GitHub Actions
    content = re.sub(r'Unable to process file command \'env\'.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'Invalid format.*$', '', content, flags=re.MULTILINE)
    
    # Ensure it's under Twitter's character limit
    if len(content) > 280:
        print(f"Warning: Social content exceeds Twitter's 280 character limit ({len(content)} chars). Truncating...")
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
        return True
    else:
        print("Could not detect price information using main pattern")
        # Try alternative formats
        alt_pattern = r'\$([0-9,]+)(?:\.\d+)?.*?([+-]\d+\.\d+%)'
        alt_match = re.search(alt_pattern, content)
        if alt_match:
            price = alt_match.group(1)
            change = alt_match.group(2)
            print(f"Detected Bitcoin price (alternative format): ${price} {change}")
            return True
    
    return False

# Test with problematic content examples
test_samples = [
    """📈 #Bitcoin Update: Price: $84,556 (+3.52% in 24h). Key points this week:
1. Regulatory updates worldwide could impact prices.
2. Growing institutional adoption incl. Apple & JP Morgan.
Outlook: Bullish sentiment prevails, watch SEC's ETF decision. #BTC #Crypto
Error: Unable to process file command 'env' successfully.
Error: Invalid format '1. Regulatory updates worldwide could impact prices.'""",

    """#Bitcoin Update:
Price: $84,570 (+3.60%)
1. Positive regulatory moves & pending SEC Bitcoin ETF decision
2. Institutional adoption with Fidelity & BlackRock
Outlook: Bullish with support at $80K & resistance at $100K. #BTC #Crypto""",

    """📈 Bitcoin now at $84,631 with +3.63% growth. Key developments: regulatory updates, institutional adoption. #BTC #Crypto"""
]

print("Testing Social Content Cleaning and Price Extraction")
print("==================================================")

for i, sample in enumerate(test_samples):
    print(f"\nTEST SAMPLE #{i+1}:")
    print("-" * 50)
    print(sample)
    print("-" * 50)
    
    cleaned = clean_social_content(sample)
    print("\nCLEANED CONTENT:")
    print("-" * 50)
    print(cleaned)
    print("-" * 50)
    print(f"Character count: {len(cleaned)}/280")
    
    success = extract_price_info(cleaned)
    print(f"Price extraction successful: {success}")
    
    print("\nTesting environment variable writing:")
    # Create a mock environment file
    mock_env_file = f"test_env_file_{i}.txt"
    try:
        with open(mock_env_file, "w") as env_file:
            env_file.write("POST_SLUG=test-slug\n")
            env_file.write("POST_TITLE=Test Title\n")
            
            # Use multi-line syntax for social content
            env_file.write("SOCIAL_CONTENT<<EOF\n")
            env_file.write(f"{cleaned}\n")
            env_file.write("EOF\n")
        
        # Read it back to verify
        with open(mock_env_file, "r") as env_file:
            env_content = env_file.read()
            print("\nEnvironment file content:")
            print("-" * 50)
            print(env_content)
            print("-" * 50)
            
        # Clean up
        os.remove(mock_env_file)
        print(f"Test for sample #{i+1} completed successfully")
    except Exception as e:
        print(f"Error in environment file test: {str(e)}")

print("\nAll tests completed.") 