#!/usr/bin/env python3
"""
Test script for AI Research API integration.
This script tests the ability to fetch data from the API and process it.
"""

import os
import json
import requests
from datetime import datetime

# Configuration
API_URL = os.environ.get(
    "API_URL", "https://ai-research-api.vercel.app/api/research-data"
)
API_KEY = os.environ.get("AI_RESEARCH_API_KEY", "")
OUTPUT_FILE = "api_test_output.json"

def test_api_fetch():
    """Test fetching data from the API and saving it to a file."""
    print(f"Testing API fetch from: {API_URL}")
    
    # Set up headers
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
        print("Using API key from environment variable")
    
    try:
        # Make the request
        print("Making API request...")
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        print(f"Successfully fetched data from API")
        
        # Basic validation
        validate_data(data)
        
        # Save to file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved API response to {OUTPUT_FILE}")
        return True
    
    except requests.RequestException as e:
        print(f"Error fetching data from API: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return False

def validate_data(data):
    """Perform basic validation on the API response data."""
    print("Validating API response...")
    
    # Check if we have the expected sections
    expected_sections = [
        "AI Model Updates", 
        "Hardware Advancements",
        "Robotics",
        "Enterprise AI",
        "Regulatory News", 
        "Research",
        "Future Trends"
    ]
    
    # Count items in each section
    total_items = 0
    for section in expected_sections:
        if section not in data:
            print(f"Warning: Missing section '{section}' in API response")
            continue
            
        items = data[section]
        if not isinstance(items, list):
            print(f"Warning: Section '{section}' is not a list")
            continue
            
        section_count = len(items)
        total_items += section_count
        print(f"Section '{section}' has {section_count} items")
        
        # Check a few required fields for the first item if available
        if section_count > 0:
            first_item = items[0]
            for field in ['title', 'summary', 'date']:
                if field not in first_item:
                    print(f"Warning: Item in '{section}' missing required field '{field}'")
    
    print(f"Total items across all sections: {total_items}")
    print("Validation complete")

if __name__ == "__main__":
    print(f"=== API Test Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Run the test
    success = test_api_fetch()
    
    if success:
        print("API test completed successfully!")
    else:
        print("API test failed!")
        exit(1)  # Exit with error code
        
    print(f"=== API Test Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===") 