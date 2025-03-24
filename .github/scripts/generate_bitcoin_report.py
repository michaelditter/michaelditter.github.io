#!/usr/bin/env python3
"""
Generate a formatted Bitcoin market report using data from fetch_bitcoin_data.py
"""

import os
import json
import sys
import logging
from pathlib import Path
from datetime import datetime
import re
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('bitcoin_report_generator')

# Check for debug mode
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
if DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    logger.debug("Running in DEBUG mode")

# Try to load formatting configuration
CONFIG_PATH = Path(".github/config/report_format.json")
try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
    logger.info(f"Loaded configuration from {CONFIG_PATH}")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.warning(f"Could not load configuration: {e}")
    # Default configuration if file not found or invalid
    CONFIG = {
        "emojis": {
            "price": "📈",
            "key_points": "🔑",
            "analysis": "📊",
            "outlook": "🔮",
            "bullish": "🚀",
            "bearish": "📉",
            "neutral": "⏺️",
            "point1": "1️⃣",
            "point2": "2️⃣",
            "point3": "3️⃣"
        },
        "styling": {
            "use_color_coding": True,
            "positive_color": "#28a745",
            "negative_color": "#dc3545",
            "neutral_color": "#6c757d"
        }
    }

# Report template with emojis and proper formatting - Updated with new structure
REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>Bitcoin Market Report - {date} | Michael J Ditter</title>
    <meta name="description" content="Bitcoin price analysis and market insights for {date} by Michael J Ditter. Price: {price} {price_change_24h}.">
    <meta name="keywords" content="Bitcoin, Cryptocurrency, Market Analysis, Crypto Report, Bitcoin Price, {date}">
    <meta name="author" content="Michael J Ditter">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://www.michaelditter.com/blog/{post_slug}/">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.michaelditter.com/blog/{post_slug}/">
    <meta property="og:title" content="Bitcoin Market Report - {date}">
    <meta property="og:description" content="Bitcoin price analysis and market insights. Price: {price} {price_change_24h}.">
    <meta property="og:image" content="https://www.michaelditter.com/img/blog/{post_slug}.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://www.michaelditter.com/blog/{post_slug}/">
    <meta property="twitter:title" content="Bitcoin Market Report - {date}">
    <meta property="twitter:description" content="Bitcoin price analysis and market insights. Price: {price} {price_change_24h}.">
    <meta property="twitter:image" content="https://www.michaelditter.com/img/blog/{post_slug}.jpg">
    
    <!-- CSS and Fonts -->
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/custom-overrides.css">
    
    <style>
        .bitcoin-report {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 0;
        }
        
        .bitcoin-report h1 {
            color: {header_color};
            margin-bottom: 1.5rem;
            font-size: 2.5rem;
        }
        
        .price-section {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .price-label {
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        .price-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin-right: 0.5rem;
        }
        
        .price-change {
            font-size: 1.2rem;
            font-weight: 600;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }
        
        .positive {
            color: {positive_color};
            background-color: rgba(40, 167, 69, 0.1);
        }
        
        .negative {
            color: {negative_color};
            background-color: rgba(220, 53, 69, 0.1);
        }
        
        .neutral {
            color: {neutral_color};
            background-color: rgba(108, 117, 125, 0.1);
        }

        .report-section {
            margin-bottom: 2.5rem;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .section-header {
            background-color: #f0f7ff;
            padding: 1rem 1.5rem;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border-left: 4px solid #0066cc;
        }
        
        .section-header h2 {
            margin: 0;
            color: #0066cc;
            font-size: 1.5rem;
        }
        
        .section-content {
            padding: 1.5rem;
            background-color: #f8f9fa;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            border-left: 4px solid #f0f7ff;
        }
        
        .section-subtitle {
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: #333;
        }
        
        .key-points {
            margin-bottom: 1.5rem;
        }
        
        .key-points li {
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        
        .analysis-section p {
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        
        .outlook {
            font-size: 1.2rem;
            font-weight: 500;
            padding: 1rem;
            border-radius: 8px;
            background-color: #f8f9fa;
            margin-bottom: 2rem;
            border-left: 4px solid #0066cc;
        }
        
        .timestamp {
            font-size: 0.9rem;
            color: #6c757d;
            text-align: right;
            border-top: 1px solid #e9ecef;
            padding-top: 1rem;
        }
        
        .data-source {
            display: inline-block;
            background-color: #f1f3f5;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            font-size: 0.85rem;
        }
        
        .archive-link {
            margin-left: 1rem;
            color: {header_color};
            text-decoration: none;
        }
        
        .archive-link:hover {
            text-decoration: underline;
        }

        .indicator-item {
            display: flex;
            margin-bottom: 1rem;
            padding: 0.75rem;
            background-color: #fff;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .indicator-label {
            font-weight: 600;
            margin-right: 0.5rem;
            min-width: 120px;
        }
        
        .indicator-value {
            font-weight: 500;
        }
        
        .technical-levels {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .level-item {
            background-color: #fff;
            padding: 0.75rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .level-label {
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #555;
        }
        
        .level-value {
            font-size: 1.2rem;
            font-weight: 700;
        }
        
        .support {
            border-left: 3px solid #28a745;
        }
        
        .resistance {
            border-left: 3px solid #dc3545;
        }
        
        @media (max-width: 768px) {
            .technical-levels {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Header with Navigation -->
    <header class="site-header">
        <div class="container">
            <nav class="main-nav">
                <a href="/" class="logo">Michael J Ditter</a>
                <ul class="nav-links">
                    <li><a href="/#about">About</a></li>
                    <li><a href="/#expertise">Expertise</a></li>
                    <li><a href="/#services">Services</a></li>
                    <li><a href="/blog/">Insights</a></li>
                    <li><a href="/#speaking">Speaking</a></li>
                    <li><a href="/#contact" class="btn-primary">Contact</a></li>
                </ul>
                <button class="mobile-menu-toggle" aria-label="Toggle Navigation Menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </nav>
        </div>
    </header>

    <!-- Report Content -->
    <section class="blog-content-section">
        <div class="container">
            <div class="bitcoin-report">
                <h1>{emoji_price} Bitcoin Market Report - {date}</h1>
                
                <!-- Executive Summary -->
                <div class="price-section">
                    <span class="price-label">Current Price:</span>
                    <span class="price-value">{price}</span>
                    <span class="price-change {change_class}">{price_change_24h}</span>
                </div>
                
                <div class="executive-summary">
                    <p>Weekly Bitcoin market analysis with key insights on regulatory developments, macroeconomic factors, institutional adoption, market sentiment, and technical indicators.</p>
                </div>
                
                <!-- Key Developments Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>{emoji_key_points} Key Developments</h2>
                    </div>
                    <div class="section-content">
                        <ul class="key-points">
                            {key_points_html}
                        </ul>
                    </div>
                </div>
                
                <!-- Regulatory Moves Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>🏛️ Regulatory Developments</h2>
                    </div>
                    <div class="section-content">
                        <div class="section-subtitle">Key Regulatory Moves:</div>
                        <div class="analysis-section">
                            {regulatory_html}
                        </div>
                    </div>
                </div>
                
                <!-- Macroeconomic Factors Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>🌐 Macroeconomic Factors</h2>
                    </div>
                    <div class="section-content">
                        <div class="section-subtitle">Economic Indicators:</div>
                        <div class="analysis-section">
                            {macroeconomic_html}
                        </div>
                    </div>
                </div>
                
                <!-- Institutional Adoption Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>🏢 Institutional Adoption</h2>
                    </div>
                    <div class="section-content">
                        <div class="section-subtitle">Notable Developments:</div>
                        <div class="analysis-section">
                            {institutional_html}
                        </div>
                    </div>
                </div>
                
                <!-- Market Sentiment Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>🧠 Market Sentiment</h2>
                    </div>
                    <div class="section-content">
                        <div class="section-subtitle">Sentiment Indicators:</div>
                        <div class="analysis-section">
                            {sentiment_html}
                        </div>
                    </div>
                </div>
                
                <!-- Technical Analysis Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>{emoji_analysis} Technical Analysis</h2>
                    </div>
                    <div class="section-content">
                        <div class="analysis-section">
                            {technical_html}
                        </div>
                        
                        <div class="technical-levels">
                            <div class="level-item support">
                                <div class="level-label">Support 1</div>
                                <div class="level-value">{support_1}</div>
                            </div>
                            <div class="level-item resistance">
                                <div class="level-label">Resistance 1</div>
                                <div class="level-value">{resistance_1}</div>
                            </div>
                            <div class="level-item support">
                                <div class="level-label">Support 2</div>
                                <div class="level-value">{support_2}</div>
                            </div>
                            <div class="level-item resistance">
                                <div class="level-label">Resistance 2</div>
                                <div class="level-value">{resistance_2}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Forward-Looking Analysis Section -->
                <div class="report-section">
                    <div class="section-header">
                        <h2>{emoji_outlook} Forward-Looking Analysis</h2>
                    </div>
                    <div class="section-content">
                        <p class="outlook">{outlook_emoji} {outlook}</p>
                        <p><strong>Disclaimer:</strong> This analysis is for informational purposes only and does not constitute investment advice. Cryptocurrency investments involve risk, and past performance does not guarantee future results. Always conduct your own research before making investment decisions.</p>
                    </div>
                </div>
                
                <div class="timestamp">
                    <p>{emoji_date} Report generated on {timestamp} 
                    <span class="data-source">{emoji_source} Data source: {data_source}</span></p>
                    <p><a href="/blog/bitcoin-report-archive/" class="archive-link">View Historical Reports</a></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-main">
                <div class="footer-brand">
                    <a href="/" class="footer-logo">Michael J Ditter</a>
                    <p>AI Specialist & Technology Consultant helping organizations navigate the complex world of artificial intelligence and emerging technologies.</p>
                    <div class="social-links">
                        <a href="https://www.linkedin.com/in/michaeljditter" aria-label="LinkedIn Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/linkedin.svg" alt="LinkedIn" width="24" height="24">
                        </a>
                        <a href="https://twitter.com/michaeljditter" aria-label="Twitter Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/twitter.svg" alt="Twitter" width="24" height="24">
                        </a>
                        <a href="https://github.com/michaeljditter" aria-label="GitHub Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/github.svg" alt="GitHub" width="24" height="24">
                        </a>
                        <a href="https://www.instagram.com/drinkpartay" aria-label="Instagram Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/instagram.svg" alt="Instagram" width="24" height="24">
                        </a>
                    </div>
                </div>
                <div class="footer-links">
                    <div class="footer-nav">
                        <h3>Navigation</h3>
                        <ul>
                            <li><a href="/">Home</a></li>
                            <li><a href="/#about">About</a></li>
                            <li><a href="/#expertise">Expertise</a></li>
                            <li><a href="/#services">Services</a></li>
                            <li><a href="/blog/">Insights</a></li>
                            <li><a href="/#speaking">Speaking</a></li>
                            <li><a href="/#contact">Contact</a></li>
                        </ul>
                    </div>
                    <div class="footer-resources">
                        <h3>Resources</h3>
                        <ul>
                            <li><a href="/blog/category/ai-strategy">AI Strategy</a></li>
                            <li><a href="/resources/machine-learning">Machine Learning</a></li>
                            <li><a href="/resources/ai-ethics">AI Ethics</a></li>
                            <li><a href="/resources/ai-regulatory-frameworks">AI Regulations</a></li>
                            <li><a href="/resources/case-studies">Case Studies</a></li>
                            <li><a href="/resources/white-papers">White Papers</a></li>
                            <li><a href="/resources/webinars">Webinars</a></li>
                        </ul>
                    </div>
                    <div class="footer-legal">
                        <h3>Legal</h3>
                        <ul>
                            <li><a href="/terms.html">Terms of Service</a></li>
                            <li><a href="/privacy.html">Privacy Policy</a></li>
                            <li><a href="/cookie-policy.html">Cookie Policy</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2025</span> Michael J Ditter. All rights reserved.</p>
                <p>Built with <span class="heart">♥</span> for optimal performance, accessibility, and SEO.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

def load_report_data(data_file=None):
    """Load Bitcoin report data from a JSON file."""
    # If no file is specified, check environment variable
    if not data_file:
        data_file = os.environ.get("NEWSLETTER_DATA_FILE")
    
    if not data_file or not os.path.exists(data_file):
        logger.error(f"Data file not found: {data_file}")
        sys.exit(1)
    
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
            logger.info(f"Loaded report data from {data_file}")
            if DEBUG_MODE:
                logger.debug(f"Data: {json.dumps(data, indent=2)}")
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading report data: {e}")
        sys.exit(1)

def format_date(date_str=None):
    """Format date for display in the report."""
    if date_str:
        # Try to parse date string
        try:
            date_formats = ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"]
            for date_format in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, date_format)
                    return date_obj.strftime("%B %d, %Y")
                except ValueError:
                    continue
            
            # If no format matched, return as is
            return date_str
        except Exception as e:
            logger.warning(f"Could not parse date {date_str}: {e}")
            return date_str
    else:
        # Use current date
        return datetime.now().strftime("%B %d, %Y")

def get_change_class(price_change):
    """Determine the CSS class for price change."""
    if not price_change:
        return "neutral"
    
    # Extract numeric value from formatted price change string
    # E.g., "(+3.60%)" -> "+3.60" -> 3.60
    change_str = re.search(r'([+-]?\d+\.?\d*)', price_change)
    if not change_str:
        return "neutral"
    
    change = float(change_str.group(1))
    if change > 0:
        return "positive"
    elif change < 0:
        return "negative"
    else:
        return "neutral"

def get_emoji_for_sentiment(sentiment):
    """Get appropriate emoji based on sentiment."""
    sentiment = sentiment.lower() if sentiment else "neutral"
    
    # Check if the sentiment is in the config
    if sentiment in CONFIG["emojis"]:
        return CONFIG["emojis"][sentiment]
    
    # Fallbacks
    if "very" in sentiment:
        if "bull" in sentiment:
            return CONFIG["emojis"].get("very_bullish", CONFIG["emojis"]["bullish"])
        elif "bear" in sentiment:
            return CONFIG["emojis"].get("very_bearish", CONFIG["emojis"]["bearish"])
    
    if "bull" in sentiment:
        return CONFIG["emojis"]["bullish"]
    elif "bear" in sentiment:
        return CONFIG["emojis"]["bearish"]
    else:
        return CONFIG["emojis"]["neutral"]

def format_key_points(key_points):
    """Format key points for HTML display."""
    if not key_points:
        return "<li>No key points available</li>"
    
    html = ""
    for i, point in enumerate(key_points):
        point_emoji = CONFIG["emojis"].get(f"point{i+1}", "•")
        html += f"<li>{point_emoji} {point}</li>\n"
    
    return html

def format_analysis(analysis):
    """Format analysis paragraphs for HTML display."""
    if not analysis:
        return "<p>No analysis available</p>"
    
    html = ""
    for paragraph in analysis:
        html += f"<p>{paragraph}</p>\n"
    
    return html

def format_regulatory_analysis(data):
    """Format regulatory analysis for HTML display."""
    regulatory_insights = data.get("regulatory_insights", [
        "Recent regulatory developments have shown increased clarity in certain jurisdictions, while others continue to refine their stance on cryptocurrencies.",
        "The SEC continues to evaluate Bitcoin ETF applications, which remains a significant factor for institutional adoption.",
        "Global regulatory frameworks are gradually evolving, with a trend toward more defined but varied approaches across different regions."
    ])
    
    return format_analysis(regulatory_insights)

def format_macroeconomic_analysis(data):
    """Format macroeconomic analysis for HTML display."""
    macro_insights = data.get("macroeconomic_insights", [
        "Inflation metrics and central bank policies continue to influence Bitcoin's positioning as a potential hedge asset.",
        "Global economic uncertainty has contributed to increased interest in alternative assets, including cryptocurrencies.",
        "Market liquidity conditions and interest rate environments remain significant factors in Bitcoin's price movements."
    ])
    
    return format_analysis(macro_insights)

def format_institutional_analysis(data):
    """Format institutional adoption analysis for HTML display."""
    institutional_insights = data.get("institutional_insights", [
        "Institutional interest in Bitcoin continues to grow, with several major financial entities expanding their cryptocurrency offerings.",
        "Corporate treasury adoption remains selective but shows signs of gradual expansion in certain sectors.",
        "Bitcoin ETFs and other investment vehicles are evolving, providing more avenues for institutional exposure to the asset class."
    ])
    
    return format_analysis(institutional_insights)

def format_sentiment_analysis(data):
    """Format market sentiment analysis for HTML display."""
    sentiment_insights = data.get("sentiment_insights", [
        f"The current market sentiment appears to be {data.get('sentiment', 'neutral')}, with social media activity showing corresponding patterns.",
        "On-chain metrics indicate wallet accumulation patterns that align with longer-term market cycles.",
        "The Fear & Greed Index has shown notable shifts over the past week, reflecting changing market psychology."
    ])
    
    return format_analysis(sentiment_insights)

def format_technical_analysis(data):
    """Format technical analysis for HTML display."""
    technical_insights = data.get("technical_insights", [
        "Bitcoin's price action shows significant resistance at higher levels, with key support zones being tested in recent trading sessions.",
        "Volume patterns indicate changing market dynamics, with institutional-sized transactions showing particular patterns of interest.",
        "Moving averages and momentum indicators suggest the current trend direction remains intact, though with potential volatility ahead."
    ])
    
    return format_analysis(technical_insights)

def generate_support_resistance_levels(price):
    """Generate support and resistance levels based on current price."""
    if isinstance(price, str):
        # Try to extract numeric value from price string
        # E.g., "$84,570" -> 84570
        price_str = re.search(r'[\$£€]?([0-9,]+\.?[0-9]*)', price)
        if price_str:
            # Remove commas and convert to float
            price_num = float(price_str.group(1).replace(',', ''))
        else:
            # Fallback
            price_num = 50000
    else:
        price_num = float(price)
    
    # Generate support and resistance levels as percentages of current price
    return {
        "support_1": f"${int(price_num * 0.95):,}",
        "support_2": f"${int(price_num * 0.90):,}",
        "resistance_1": f"${int(price_num * 1.05):,}",
        "resistance_2": f"${int(price_num * 1.10):,}"
    }

def generate_report_html(data, post_slug):
    """Generate complete HTML for Bitcoin report."""
    logger.info("Generating Bitcoin report HTML")
    
    # Extract relevant data
    price = data.get("price", "$0.00")
    price_change_24h = data.get("price_change_24h", "(0.00%)")
    key_points = data.get("key_points", [])
    analysis = data.get("analysis", [])
    outlook = data.get("outlook", "Market outlook unavailable")
    data_source = data.get("data_source", "Unknown")
    sentiment = data.get("sentiment", "neutral")
    date = format_date(data.get("date"))
    
    # Generate support and resistance levels
    levels = generate_support_resistance_levels(price)
    
    # Format report timestamp
    timestamp = data.get("timestamp")
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_timestamp = dt.strftime("%B %d, %Y at %I:%M %p")
        except (ValueError, TypeError):
            formatted_timestamp = timestamp
    else:
        formatted_timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Get styling values
    styling = CONFIG.get("styling", {})
    positive_color = styling.get("positive_color", "#28a745")
    negative_color = styling.get("negative_color", "#dc3545")
    neutral_color = styling.get("neutral_color", "#6c757d")
    header_color = styling.get("header_color", "#0066cc")
    
    # Get appropriate CSS class for price change
    change_class = get_change_class(price_change_24h)
    
    # Get emojis
    emojis = CONFIG.get("emojis", {})
    emoji_price = emojis.get("price", "📈")
    emoji_key_points = emojis.get("key_points", "🔑")
    emoji_analysis = emojis.get("analysis", "📊")
    emoji_outlook = emojis.get("outlook", "🔮")
    emoji_date = emojis.get("date", "📅")
    emoji_source = emojis.get("source", "🔎")
    
    # Get sentiment-specific emoji for outlook
    outlook_emoji = get_emoji_for_sentiment(sentiment)
    
    # Format content sections for HTML
    key_points_html = format_key_points(key_points)
    regulatory_html = format_regulatory_analysis(data)
    macroeconomic_html = format_macroeconomic_analysis(data)
    institutional_html = format_institutional_analysis(data)
    sentiment_html = format_sentiment_analysis(data)
    technical_html = format_technical_analysis(data)
    
    # Generate complete HTML
    html = REPORT_TEMPLATE.format(
        post_slug=post_slug,
        date=date,
        price=price,
        price_change_24h=price_change_24h,
        key_points_html=key_points_html,
        regulatory_html=regulatory_html,
        macroeconomic_html=macroeconomic_html,
        institutional_html=institutional_html,
        sentiment_html=sentiment_html,
        technical_html=technical_html,
        outlook=outlook,
        timestamp=formatted_timestamp,
        data_source=data_source,
        change_class=change_class,
        positive_color=positive_color,
        negative_color=negative_color,
        neutral_color=neutral_color,
        header_color=header_color,
        emoji_price=emoji_price,
        emoji_key_points=emoji_key_points,
        emoji_analysis=emoji_analysis,
        emoji_outlook=emoji_outlook,
        outlook_emoji=outlook_emoji,
        emoji_date=emoji_date,
        emoji_source=emoji_source,
        support_1=levels["support_1"],
        support_2=levels["support_2"],
        resistance_1=levels["resistance_1"],
        resistance_2=levels["resistance_2"]
    )
    
    logger.info("Bitcoin report HTML generated successfully")
    return html

def save_report(html, post_slug):
    """Save the report HTML to a file."""
    # Create the blog post directory
    blog_dir = Path(f"blog/{post_slug}")
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the HTML to index.html
    file_path = blog_dir / "index.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    logger.info(f"Bitcoin report saved to {file_path}")
    return file_path

def generate_placeholder_image(post_slug):
    """Generate a placeholder image for the report."""
    try:
        # This is handled in the GitHub workflow now, so just checking if needed
        img_dir = Path("img/blog")
        img_path = img_dir / f"{post_slug}.jpg"
        
        if img_path.exists():
            logger.info(f"Image already exists: {img_path}")
            return img_path
        
        # Ensure directory exists
        img_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to use PIL to generate a simple placeholder
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple colored rectangle
            img = Image.new('RGB', (1200, 630), color=(247, 147, 26))  # Bitcoin orange
            draw = ImageDraw.Draw(img)
            
            # Add text - basic version
            text = f"Bitcoin Report - {datetime.now().strftime('%B %d, %Y')}"
            font_path = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
            try:
                font = ImageFont.truetype(font_path, size=60)
            except (OSError, IOError):
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Try to center the text
            try:
                text_width = draw.textlength(text, font=font)
            except (AttributeError, TypeError):
                # For older PIL versions
                text_width = font.getsize(text)[0]
            
            position = ((1200 - text_width) // 2, 300)
            draw.text(position, text, fill=(255, 255, 255), font=font)
            
            # Save the image
            img.save(img_path)
            logger.info(f"Generated placeholder image: {img_path}")
            
        except ImportError as e:
            logger.warning(f"PIL not available to generate image: {e}")
            # Just create an empty file as placeholder
            with open(img_path, 'wb') as f:
                f.write(b'')
            logger.warning(f"Created empty placeholder file: {img_path}")
        
        return img_path
        
    except Exception as e:
        logger.error(f"Error generating placeholder image: {e}")
        return None

def validate_data(data):
    """Validate the report data for required fields."""
    required_fields = ['price', 'price_change_24h', 'key_points', 'analysis', 'outlook']
    missing = [field for field in required_fields if field not in data]
    
    if missing:
        logger.error(f"Missing required fields in report data: {', '.join(missing)}")
        return False
    
    # Check if key points and analysis are non-empty lists
    if not data.get('key_points', []):
        logger.error("Key points list is empty")
        return False
    
    if not data.get('analysis', []):
        logger.error("Analysis list is empty")
        return False
    
    return True

def main():
    """Main function to generate Bitcoin report."""
    parser = argparse.ArgumentParser(description='Generate Bitcoin Market Report')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--data-file', type=str, help='Path to JSON data file')
    args = parser.parse_args()
    
    # Set debug mode if requested
    if args.debug or DEBUG_MODE:
        global DEBUG_MODE
        DEBUG_MODE = True
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        # Load report data
        data = load_report_data(args.data_file)
        
        # Validate data
        if not validate_data(data):
            logger.error("Data validation failed")
            sys.exit(1)
        
        # Get or generate post slug
        today = datetime.now().strftime("%Y-%m-%d")
        post_slug = os.environ.get("POST_SLUG")
        if not post_slug:
            post_slug = f"bitcoin-market-report-{today}"
            logger.info(f"Generated post slug: {post_slug}")
        
        # Generate report HTML
        html = generate_report_html(data, post_slug)
        
        # Save report to file
        report_path = save_report(html, post_slug)
        
        # Generate placeholder image if needed
        img_path = generate_placeholder_image(post_slug)
        
        logger.info("Bitcoin report generation completed successfully")
        logger.info(f"Report saved to: {report_path}")
        if img_path:
            logger.info(f"Image saved to: {img_path}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error generating Bitcoin report: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 