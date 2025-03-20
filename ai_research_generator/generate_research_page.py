#!/usr/bin/env python3
"""
AI Research Index Page Generator

This script fetches the latest AI research data from either an API or local JSON file,
processes it, and generates a static HTML page that presents AI research updates across
multiple categories.

The script can be scheduled via cron to automatically update the index page at regular intervals.
"""

import json
import os
import requests
import datetime
from pathlib import Path
from markdown import markdown
from jinja2 import Environment, FileSystemLoader

# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed, skipping .env loading")

# Override configuration from environment variables if present
def get_env_var(name, default):
    return os.environ.get(name, default)

# Configuration
CONFIG = {
    "data_source": {
        "type": get_env_var("DATA_SOURCE_TYPE", "api"),  # "file" or "api"
        "file_path": get_env_var("DATA_FILE_PATH", "ai_research_generator/data/research_data.json"),
        "api_url": get_env_var("API_URL", "https://ai-research-api.michaelditter.com/api/research-data"),
        "api_key_env": get_env_var("API_KEY_ENV", "AI_RESEARCH_API_KEY")  # Name of env var holding API key
    },
    "output": {
        "html_path": get_env_var("OUTPUT_HTML_PATH", "blog/ai-research-index.html"),
        "canonical_url": get_env_var("CANONICAL_URL", "https://www.michaelditter.com/blog/ai-research-index.html")
    },
    "template": {
        "dir": get_env_var("TEMPLATE_DIR", "ai_research_generator/templates"),
        "file": get_env_var("TEMPLATE_FILE", "research_index.html")
    }
}

def fetch_data():
    """
    Fetch AI research data from either a local JSON file or an API.
    
    Returns:
        dict: The structured AI research data
    """
    print(f"Fetching AI research data...")
    
    if CONFIG["data_source"]["type"] == "file":
        # Load from local JSON file
        try:
            file_path = CONFIG["data_source"]["file_path"]
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Successfully loaded data from {file_path}")
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data file: {str(e)}")
            # Fall back to API if file not found or invalid
            print(f"Falling back to API data source...")
            CONFIG["data_source"]["type"] = "api"
            return fetch_data()
    else:
        # Fetch from API
        api_url = CONFIG["data_source"]["api_url"]
        # Securely get API key from environment variable
        api_key_env = CONFIG["data_source"]["api_key_env"]
        api_key = os.environ.get(api_key_env)
        
        # Check if API key is required - explicitly handle string "false"
        require_api_key = os.environ.get("REQUIRE_API_KEY", "true").lower() != "false"
        
        headers = {}
        if api_key and require_api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            print(f"Using API key from environment variable {api_key_env}")
        elif require_api_key and not api_key:
            print(f"Error: API key required but not found in environment variable {api_key_env}")
            raise ValueError(f"Missing required API key (set {api_key_env} environment variable)")
        else:
            print(f"API key requirement disabled, proceeding without authentication")
        
        try:
            print(f"Fetching data from API: {api_url}")
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            data = response.json()
            print(f"Successfully fetched data from API")
            return data
        except requests.RequestException as e:
            print(f"Error fetching data from API: {str(e)}")
            # If API fails and we have a data file, fall back to it
            if os.path.exists(CONFIG["data_source"]["file_path"]):
                print(f"Falling back to local data file due to API error")
                CONFIG["data_source"]["type"] = "file"
                return fetch_data()
            raise

def process_data(data):
    """
    Process the raw data, converting any Markdown to HTML and adding any computed fields.
    
    Args:
        data (dict): The raw AI research data
        
    Returns:
        dict: The processed data ready for template rendering
    """
    processed_data = {}
    
    # Expected sections based on requirements
    expected_sections = [
        "AI Model Updates", 
        "Hardware Advancements",
        "Robotics",
        "Enterprise AI",
        "Regulatory News",
        "Research",
        "Future Trends"
    ]
    
    # Initialize any missing sections to avoid template errors
    for section in expected_sections:
        if section not in data:
            data[section] = []
    
    # Process each section
    for section in expected_sections:
        processed_data[section] = []
        
        if section not in data:
            continue
            
        for item in data[section]:
            # Clone the item to avoid modifying the original
            processed_item = dict(item)
            
            # Convert Markdown to HTML if present
            if 'description_md' in processed_item:
                processed_item['description_html'] = markdown(processed_item['description_md'])
            
            # Format date if present
            if 'date' in processed_item:
                try:
                    # Assuming ISO format date string
                    date_obj = datetime.datetime.fromisoformat(processed_item['date'])
                    processed_item['formatted_date'] = date_obj.strftime('%b %d, %Y')
                except (ValueError, TypeError):
                    # If date parsing fails, keep the original
                    processed_item['formatted_date'] = processed_item['date']
            
            processed_data[section].append(processed_item)
    
    return processed_data

def render_html(data):
    """
    Render the HTML using the Jinja2 template engine.
    
    Args:
        data (dict): The processed research data
        
    Returns:
        str: The rendered HTML content
    """
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(CONFIG["template"]["dir"]))
    template = env.get_template(CONFIG["template"]["file"])
    
    # Prepare the context with all the data needed by the template
    context = {
        "data": data,
        "generated_date": datetime.date.today().strftime('%B %d, %Y'),
        "canonical_url": CONFIG["output"]["canonical_url"],
        "last_updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Render the template with the data
    return template.render(**context)

def save_html(html_content):
    """
    Save the HTML content to the output file, ensuring the directory exists.
    
    Args:
        html_content (str): The HTML content to save
    """
    output_path = CONFIG["output"]["html_path"]
    output_dir = os.path.dirname(output_path)
    
    # Create the output directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Create a temporary file first, then rename to ensure atomic file write
    temp_path = f"{output_path}.tmp"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Rename temp file to target (atomic on most file systems)
        os.replace(temp_path, output_path)
        print(f"Successfully saved HTML to {output_path}")
    except IOError as e:
        print(f"Error saving HTML file: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)  # Clean up temp file if it exists
        raise

def main():
    """Main function to run the pipeline."""
    try:
        print(f"AI Research Index Generator started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Fetch the data
        raw_data = fetch_data()
        
        # Step 2: Process the data
        processed_data = process_data(raw_data)
        
        # Step 3: Render the HTML
        html_content = render_html(processed_data)
        
        # Step 4: Save the HTML
        save_html(html_content)
        
        print(f"AI Research index page generated successfully at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}!")
        return 0
    except Exception as e:
        print(f"Error generating research page: {str(e)}")
        # In a production environment, we might want to send an alert or notification here
        return 1

if __name__ == "__main__":
    exit(main()) 