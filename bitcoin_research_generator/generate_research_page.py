#!/usr/bin/env python3
"""
Bitcoin Research Index Page Generator

This script fetches the latest Bitcoin research data from either an API or local JSON file,
processes it, and generates a static HTML page that presents Bitcoin research updates across
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
        "file_path": get_env_var("DATA_FILE_PATH", "bitcoin_research_generator/data/research_data.json"),
        "api_url": get_env_var("API_URL", "https://bitcoin-research-api.vercel.app/api/bitcoin-data"),
        "api_key_env": get_env_var("API_KEY_ENV", "BITCOIN_RESEARCH_API_KEY")  # Name of env var holding API key
    },
    "output": {
        "html_path": get_env_var("OUTPUT_HTML_PATH", "blog/bitcoin-research-index.html"),
        "canonical_url": get_env_var("CANONICAL_URL", "https://www.michaelditter.com/blog/bitcoin-research-index.html")
    },
    "template": {
        "dir": get_env_var("TEMPLATE_DIR", "bitcoin_research_generator/templates"),
        "file": get_env_var("TEMPLATE_FILE", "research_index.html")
    }
}

def fetch_data():
    """
    Fetch Bitcoin research data from either a local JSON file or an API.
    
    Returns:
        dict: The structured Bitcoin research data
    """
    print(f"Fetching Bitcoin research data...")
    
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
        api_key = os.environ.get(CONFIG["data_source"]["api_key_env"])
        
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            print(f"Using API key from environment variable {CONFIG['data_source']['api_key_env']}")
        else:
            print(f"Warning: No API key found in environment variable {CONFIG['data_source']['api_key_env']}")
        
        try:
            print(f"Fetching data from API: {api_url}")
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            data = response.json()
            print(f"Successfully fetched data from API")
            
            # Process the API response into the expected format for the template
            formatted_data = format_api_data(data)
            return formatted_data
        except requests.RequestException as e:
            print(f"Error fetching data from API: {str(e)}")
            # If API fails and we have a data file, fall back to it
            if os.path.exists(CONFIG["data_source"]["file_path"]):
                print(f"Falling back to local data file due to API error")
                CONFIG["data_source"]["type"] = "file"
                return fetch_data()
            raise

def format_api_data(api_data):
    """
    Format the API response data into the structure expected by the template.
    The Bitcoin API has a different format than what our template expects.
    
    Args:
        api_data (dict): The raw API response data
        
    Returns:
        dict: The formatted data, structured for the template
    """
    # Create the expected structure for the template
    formatted_data = {
        "Bitcoin Market Trends": [],
        "Price Analysis": [],
        "Institutional Developments": [],
        "Regulatory Updates": [],
        "Technology Advancements": [],
        "Research Insights": [],
        "Outlook & Forecasts": []
    }
    
    # Extract the report date and bitcoin price data
    report_date = api_data.get("reportDate", datetime.date.today().isoformat())
    
    # Market summary data
    if "bitcoinPrice" in api_data and "marketSummary" in api_data:
        price_data = api_data["bitcoinPrice"]
        market_data = api_data["marketSummary"]
        
        formatted_data["Bitcoin Market Trends"].append({
            "title": f"Bitcoin at {price_data.get('current', '$0')} with {price_data.get('weeklyChange', '0%')} Weekly Change",
            "summary": f"Current market cap is {market_data.get('marketCap', '$0')} with 24-hour volume of {market_data.get('volume24h', '$0')}. Bitcoin dominance is at {market_data.get('dominance', '0%')}.",
            "date": report_date,
            "tags": ["Price", "Market Cap", "Trading Volume"],
            "trend": price_data.get('weeklyTrend', 'neutral')
        })
    
    # Technical analysis data
    if "technicalAnalysis" in api_data:
        tech_analysis = api_data["technicalAnalysis"]
        indicators = tech_analysis.get("indicators", {})
        
        formatted_data["Price Analysis"].append({
            "title": f"Technical Analysis: RSI at {indicators.get('rsi', 'N/A')} with {indicators.get('macd', 'Neutral')} MACD",
            "summary": f"Support levels at {', '.join(tech_analysis.get('supportLevels', ['N/A']))}. Resistance at {', '.join(tech_analysis.get('resistanceLevels', ['N/A']))}. {indicators.get('movingAverages', 'Moving averages show neutral trend.')}",
            "date": report_date,
            "tags": ["Technical Analysis", "RSI", "MACD", "Support/Resistance"]
        })
    
    # Key insights data
    if "keyInsights" in api_data:
        for insight in api_data["keyInsights"]:
            formatted_data["Institutional Developments"].append({
                "title": insight.get("title", "Institutional Update"),
                "summary": insight.get("content", ""),
                "date": insight.get("date", report_date),
                "link": insight.get("link", ""),
                "source": insight.get("source", ""),
                "tags": ["Institutional", "Adoption"]
            })
    
    # Regulatory updates
    if "regulatoryUpdates" in api_data:
        for update in api_data["regulatoryUpdates"]:
            formatted_data["Regulatory Updates"].append({
                "title": f"{update.get('region', 'Global')}: {update.get('development', 'Regulatory Update')}",
                "summary": f"Impact: {update.get('impact', 'Unknown')}",
                "date": update.get("date", report_date),
                "tags": ["Regulation", update.get('region', 'Global')]
            })
    
    # Lightning Network & technology updates (placeholder until API provides this)
    formatted_data["Technology Advancements"].append({
        "title": "Bitcoin Technology Developments",
        "summary": "Latest updates on Bitcoin technology, including Lightning Network, Taproot usage, and core protocol development.",
        "date": report_date,
        "tags": ["Lightning Network", "Protocol Development", "Taproot"]
    })
    
    # Research insights (from various fields in the API)
    if "outlook" in api_data:
        outlook = api_data["outlook"]
        
        formatted_data["Research Insights"].append({
            "title": "Current Bitcoin Research Insights",
            "summary": f"Short-term outlook: {outlook.get('shortTerm', 'Mixed')}. Mid-term projections: {outlook.get('midTerm', 'Uncertain')}.",
            "description_md": "## Key Risks\n\n" + "\n".join([f"- {risk}" for risk in outlook.get('keyRisks', ['Market volatility'])]),
            "date": report_date,
            "tags": ["Research", "Risk Analysis", "Projections"]
        })
    
    # Upcoming events
    if "upcomingEvents" in api_data:
        events_md = "## Upcoming Bitcoin Events\n\n"
        
        for event in api_data["upcomingEvents"]:
            events_md += f"### {event.get('name', 'Event')}\n"
            events_md += f"**Date:** {event.get('date', 'TBD')}\n\n"
            events_md += f"{event.get('significance', 'Important industry event')}\n\n"
        
        formatted_data["Outlook & Forecasts"].append({
            "title": "Bitcoin Calendar: Upcoming Events & Projections",
            "summary": f"Key upcoming events that may impact Bitcoin price and adoption.",
            "description_md": events_md,
            "date": report_date,
            "tags": ["Events", "Calendar", "Projections"]
        })
    
    return formatted_data

def process_data(data):
    """
    Process the raw data, converting any Markdown to HTML and adding any computed fields.
    
    Args:
        data (dict): The raw Bitcoin research data
        
    Returns:
        dict: The processed data ready for template rendering
    """
    processed_data = {}
    
    # Expected sections based on requirements
    expected_sections = [
        "Bitcoin Market Trends", 
        "Price Analysis",
        "Institutional Developments",
        "Regulatory Updates",
        "Technology Advancements",
        "Research Insights",
        "Outlook & Forecasts"
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
        "title": "Bitcoin Research Index",
        "description": "Weekly analysis of Bitcoin markets, technology developments, regulatory updates, and research insights.",
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
        print(f"Bitcoin Research Index Generator started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Fetch the data
        raw_data = fetch_data()
        
        # Step 2: Process the data
        processed_data = process_data(raw_data)
        
        # Step 3: Render the HTML
        html_content = render_html(processed_data)
        
        # Step 4: Save the HTML
        save_html(html_content)
        
        print(f"Bitcoin Research index page generated successfully at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}!")
        return 0
    except Exception as e:
        print(f"Error generating research page: {str(e)}")
        # In a production environment, we might want to send an alert or notification here
        return 1

if __name__ == "__main__":
    exit(main()) 