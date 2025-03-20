#!/usr/bin/env python3
"""
AI Commentary Generator for Newsletter

This module handles the integration with AI services (like OpenAI or Anthropic)
to generate expert commentary for each section of the AI Research newsletter.
"""

import os
import json
import requests
from typing import List, Dict, Any

# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("python-dotenv not installed, skipping .env loading")

# API keys for different AI services
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def generate_commentary_with_openai(category: str, articles: List[Dict[str, Any]]) -> str:
    """
    Generate commentary for a category using OpenAI's API.
    
    Args:
        category: The category name (e.g., "AI Model Updates")
        articles: List of article data for that category
    
    Returns:
        str: The generated commentary
    """
    if not OPENAI_API_KEY:
        print("OpenAI API key not found. Returning default commentary.")
        return f"Here's the latest news in {category}."
    
    # Prepare article summaries for the prompt
    article_summaries = "\n".join([
        f"- {article.get('title', 'Untitled')}: {article.get('summary', 'No summary available')}"
        for article in articles[:5]  # Limit to first 5 articles to keep prompt size reasonable
    ])
    
    # Construct the prompt
    prompt = f"""As an AI research expert, provide a brief insightful commentary (2-3 paragraphs) on recent developments in {category}. 
These are the latest news items:

{article_summaries}

Your commentary should:
1. Summarize the key trends or developments shown in these news items
2. Provide context on why these developments matter
3. Offer a thoughtful perspective on what this means for the field
4. Be written in a professional but accessible tone

Commentary:"""

    try:
        # Call OpenAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        data = {
            "model": "gpt-4o",  # Use GPT-4 for high-quality commentary
            "messages": [
                {"role": "system", "content": "You are an AI research expert providing insights for a weekly AI newsletter."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            commentary = result["choices"][0]["message"]["content"].strip()
            return commentary
        else:
            print(f"Error from OpenAI API: {response.status_code}")
            print(response.text)
            return f"Recent developments in {category} show promising advances in the field."
            
    except Exception as e:
        print(f"Error generating commentary with OpenAI: {str(e)}")
        return f"Recent developments in {category} show promising advances in the field."

def generate_commentary_with_anthropic(category: str, articles: List[Dict[str, Any]]) -> str:
    """
    Generate commentary for a category using Anthropic's Claude API.
    
    Args:
        category: The category name (e.g., "AI Model Updates")
        articles: List of article data for that category
    
    Returns:
        str: The generated commentary
    """
    if not ANTHROPIC_API_KEY:
        print("Anthropic API key not found. Returning default commentary.")
        return f"Here's the latest news in {category}."
    
    # Prepare article summaries for the prompt
    article_summaries = "\n".join([
        f"- {article.get('title', 'Untitled')}: {article.get('summary', 'No summary available')}"
        for article in articles[:5]  # Limit to first 5 articles
    ])
    
    # Construct the prompt
    prompt = f"""As an AI research expert, provide a brief insightful commentary (2-3 paragraphs) on recent developments in {category}. 
These are the latest news items:

{article_summaries}

Your commentary should:
1. Summarize the key trends or developments shown in these news items
2. Provide context on why these developments matter
3. Offer a thoughtful perspective on what this means for the field
4. Be written in a professional but accessible tone

Commentary:"""

    try:
        # Call Anthropic API
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 500,
            "temperature": 0.7,
            "system": "You are an AI research expert providing insights for a weekly AI newsletter.",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            commentary = result["content"][0]["text"]
            return commentary
        else:
            print(f"Error from Anthropic API: {response.status_code}")
            print(response.text)
            return f"Recent developments in {category} show promising advances in the field."
            
    except Exception as e:
        print(f"Error generating commentary with Anthropic: {str(e)}")
        return f"Recent developments in {category} show promising advances in the field."

def generate_commentary(category: str, articles: List[Dict[str, Any]]) -> str:
    """
    Generate AI commentary for a category of articles.
    
    This function tries multiple AI services in order of preference.
    
    Args:
        category: The category name (e.g., "AI Model Updates")
        articles: List of article data for that category
    
    Returns:
        str: The generated commentary
    """
    # Skip if there are no articles
    if not articles:
        return ""
    
    # Determine which AI service to use
    preferred_service = os.environ.get("PREFERRED_AI_SERVICE", "openai").lower()
    
    if preferred_service == "anthropic" and ANTHROPIC_API_KEY:
        return generate_commentary_with_anthropic(category, articles)
    elif preferred_service == "openai" and OPENAI_API_KEY:
        return generate_commentary_with_openai(category, articles)
    elif OPENAI_API_KEY:
        return generate_commentary_with_openai(category, articles)
    elif ANTHROPIC_API_KEY:
        return generate_commentary_with_anthropic(category, articles)
    else:
        print("No AI service API keys found. Returning default commentary.")
        return f"Recent developments in {category} show promising advances in the field."

# For testing
if __name__ == "__main__":
    # Test with a sample article
    test_category = "AI Model Updates"
    test_articles = [
        {
            "title": "OpenAI Releases GPT-5 with Enhanced Reasoning Capabilities",
            "summary": "The new model shows significant improvements in mathematical reasoning and code generation."
        },
        {
            "title": "Google DeepMind Announces Breakthrough in Protein Folding",
            "summary": "New algorithm can predict protein structures with unprecedented accuracy."
        }
    ]
    
    commentary = generate_commentary(test_category, test_articles)
    print(f"Commentary for {test_category}:")
    print(commentary) 