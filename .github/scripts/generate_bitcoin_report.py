#!/usr/bin/env python3
import os
import sys
import json
import yaml
import requests
import datetime
from pathlib import Path
import openai

# Configure OpenAI API
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Constants
BLOG_POST_DIR = "blog"
CURRENT_DATE = datetime.datetime.now()
POST_DATE = CURRENT_DATE.strftime("%Y-%m-%d")
TIMESTAMP = CURRENT_DATE.strftime("%Y-%m-%dT%H:%M:%S+00:00")
FORMATTED_DATE = CURRENT_DATE.strftime("%B %d, %Y")

def generate_post_slug():
    """Generate a URL-friendly slug for the Bitcoin report"""
    # Create a slug that includes the date to make it unique each week
    slug = f"bitcoin-market-report-{POST_DATE}"
    return slug

def fetch_bitcoin_data():
    """Fetch current Bitcoin data for analysis"""
    try:
        # Get Bitcoin price data
        price_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true", timeout=10)
        price_data = price_response.json()
        
        # Get Bitcoin market data
        market_response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&community_data=false&developer_data=false", timeout=10)
        market_data = market_response.json()
        
        # Extract relevant data
        current_price = price_data["bitcoin"]["usd"]
        price_change_24h = price_data["bitcoin"]["usd_24h_change"]
        market_cap = market_data["market_data"]["market_cap"]["usd"]
        total_volume = market_data["market_data"]["total_volume"]["usd"]
        high_24h = market_data["market_data"]["high_24h"]["usd"]
        low_24h = market_data["market_data"]["low_24h"]["usd"]
        ath = market_data["market_data"]["ath"]["usd"]
        ath_change_percentage = market_data["market_data"]["ath_change_percentage"]["usd"]
        
        data = {
            "current_price": current_price,
            "price_change_24h": price_change_24h,
            "market_cap": market_cap,
            "total_volume": total_volume,
            "high_24h": high_24h,
            "low_24h": low_24h,
            "ath": ath,
            "ath_change_percentage": ath_change_percentage,
            "timestamp": TIMESTAMP
        }
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to price API: {str(e)}")
        # Return fallback data if API fails
        return get_fallback_bitcoin_data()
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing Bitcoin data: {str(e)}")
        return get_fallback_bitcoin_data()
    except Exception as e:
        print(f"Unexpected error fetching Bitcoin data: {str(e)}")
        return get_fallback_bitcoin_data()

def get_fallback_bitcoin_data():
    """Provide fallback data when API calls fail"""
    print("Using fallback Bitcoin data")
    return {
        "current_price": 85000.00,
        "price_change_24h": 3.5,
        "market_cap": 1650000000000,
        "total_volume": 32000000000,
        "high_24h": 86000.00,
        "low_24h": 83000.00,
        "ath": 90000.00,
        "ath_change_percentage": -5.5,
        "timestamp": TIMESTAMP
    }

def clean_social_content(content):
    """Clean social content before saving to remove any potential issues."""
    # Strip any leading/trailing whitespace
    content = content.strip()
    
    # Remove any lines with error messages
    lines = content.split('\n')
    cleaned_lines = [line for line in lines if not line.startswith('Error:')]
    
    # Rejoin the lines
    content = '\n'.join(cleaned_lines)
    
    # Ensure it's under Twitter's character limit
    if len(content) > 280:
        print(f"Warning: Social content exceeds Twitter's 280 character limit ({len(content)} chars). Truncating...")
        content = content[:277] + "..."
    
    return content

def generate_content():
    """Generate Bitcoin report content using OpenAI"""
    
    # Get current Bitcoin data
    bitcoin_data = fetch_bitcoin_data()
    
    # Create the report slug
    slug = generate_post_slug()
    
    # Generate the title 
    title_prompt = f"""
    Generate a compelling, specific title for this week's Bitcoin market report dated {FORMATTED_DATE}.
    The title should be informative, include specific details about the current Bitcoin market situation, and be 50-70 characters long.
    Do not include quotation marks.
    
    Current Bitcoin price: ${bitcoin_data['current_price']:,.2f}
    24-hour change: {bitcoin_data['price_change_24h']:.2f}%
    """
    
    try:
        title_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cryptocurrency analyst who creates compelling titles for Bitcoin market reports."},
                {"role": "user", "content": title_prompt}
            ]
        )
        title = title_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating title: {str(e)}")
        title = f"Bitcoin Market Analysis: ${bitcoin_data['current_price']:,.2f} on {FORMATTED_DATE}"
    
    # Generate the main report content with improved formatting instructions
    content_prompt = f"""
    Create a comprehensive weekly Bitcoin market analysis report for {FORMATTED_DATE}. The report should monitor key triggers that could lead to Bitcoin price movements.

    IMPORTANT: Format the content with proper spacing, clear headings, and well-organized sections. Use HTML formatting for proper display on the web.

    Follow this structure:

    <h2>Executive Summary</h2>
    <p>
    Begin with a concise summary of the current Bitcoin market situation.
    - Current price: ${bitcoin_data['current_price']}
    - 24-hour change: {bitcoin_data['price_change_24h']:.2f}%
    - Key takeaways from this week's developments
    </p>

    <h2>1. Regulatory Moves</h2>
    <p>
    Analyze recent or pending regulatory developments (ETF updates, legislation, etc.)
    </p>
    <h3>Key Regulatory Developments:</h3>
    <ul>
    <li>First important regulatory development</li>
    <li>Second important regulatory development</li>
    <li>Third important regulatory development</li>
    </ul>
    <p>
    Provide analysis of how these regulations might impact Bitcoin's price and which countries or agencies to watch in the coming week.
    </p>

    <h2>2. Macroeconomic Factors</h2>
    <p>
    Analyze recent Federal Reserve decisions, inflation data, and global economic conditions affecting Bitcoin.
    </p>
    <h3>Key Macroeconomic Indicators:</h3>
    <ul>
    <li>Recent Federal Reserve decisions or statements</li>
    <li>Latest inflation data and trends</li>
    <li>Global economic conditions affecting Bitcoin</li>
    </ul>
    <p>
    Detailed analysis of how these macro factors are influencing Bitcoin prices.
    </p>

    <h2>3. Institutional Adoption</h2>
    <p>
    Analyze recent investments by corporations or funds and institutional products or services.
    </p>
    <h3>Notable Institutional Developments:</h3>
    <ul>
    <li>Recent investments by major corporations or funds</li>
    <li>New institutional products or services</li>
    <li>Statements from financial leaders</li>
    </ul>
    <p>
    Analysis of changing institutional sentiment toward Bitcoin.
    </p>

    <h2>4. Market Sentiment Analysis</h2>
    <p>
    Analyze current Fear & Greed Index, whale activity, and market psychology.
    </p>
    <h3>Key Sentiment Indicators:</h3>
    <ul>
    <li>Current Fear & Greed Index reading and what it suggests</li>
    <li>Whale accumulation or distribution patterns</li>
    <li>Social media and search trends related to Bitcoin</li>
    </ul>
    <p>
    Analysis of overall market psychology and what it suggests for price movement.
    </p>

    <h2>5. Technical Indicators</h2>
    <p>
    Analyze key price levels, technical indicators, and chart patterns.
    </p>
    <h3>Key Technical Signals:</h3>
    <ul>
    <li>Analysis of key price levels (e.g., $100K, $80K)</li>
    <li>RSI, moving averages, and other relevant indicators</li>
    <li>Volume analysis and what it signals</li>
    </ul>
    <p>
    Analysis of potential breakout/breakdown points and price targets.
    </p>

    <h2>Forward-Looking Analysis</h2>
    <p>
    Conclude with analysis of key events to watch, potential price targets, and overall market thesis.
    </p>
    <ul>
    <li>Key events to watch in the coming week</li>
    <li>Potential price targets and support/resistance levels</li>
    <li>Overall market thesis for the near term</li>
    </ul>
    <p>
    <em>Not investment advice. Bitcoin investments carry financial risk. Please conduct thorough research or consult a professional before making financial decisions.</em>
    </p>

    Use a professional but accessible tone. Include specific data points and references where possible. Avoid making definitive price predictions, instead focusing on analysis of key factors and potential scenarios.

    The total length should be approximately 1500-2000 words. Remember to maintain proper HTML formatting with appropriate paragraph tags, heading tags, unordered lists, and occasional emphasis.
    """
    
    content_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional cryptocurrency analyst with expertise in Bitcoin markets. You create detailed, data-driven market analysis reports with clear, well-structured HTML formatting."},
            {"role": "user", "content": content_prompt}
        ]
    )
    post_content = content_response.choices[0].message.content.strip()
    
    # Generate a shorter X/Twitter post version
    social_prompt = f"""
    Create a concise X (Twitter) post summarizing the most important points from this week's Bitcoin market analysis. 
    
    Include:
    1. Current price and 24h change
    2. 1-2 key developments/triggers from this week
    3. A brief outlook
    
    Keep under 280 characters and include relevant hashtags (#Bitcoin #BTC #Crypto).
    
    For reference, here's the full report: {post_content}
    """
    
    try:
        social_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cryptocurrency analyst who creates concise, informative social media posts about Bitcoin."},
                {"role": "user", "content": social_prompt}
            ]
        )
        social_content = social_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating social content: {str(e)}")
        # Fallback social content if API fails
        social_content = f"#Bitcoin Update: Price: ${bitcoin_data['current_price']:,.2f} ({bitcoin_data['price_change_24h']:.2f}%). Monitor key catalysts: institutional adoption, regulatory news. Overall market sentiment: {('bearish' if bitcoin_data['price_change_24h'] < 0 else 'bullish')}. #BTC #Crypto"
    
    # Clean the social content
    social_content = clean_social_content(social_content)
    
    # Save social content to a file for easier handling in GitHub Actions
    social_content_file = Path(".github") / "tmp" / "social_content.txt"
    social_content_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(social_content_file, 'w') as f:
        f.write(social_content)
    
    # Generate meta description for SEO
    description_prompt = f"Write a compelling meta description for a blog post with the title '{title}'. The description should summarize the key points of this week's Bitcoin market analysis, be 150-160 characters, and encourage readers to click."
    description_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an SEO specialist who writes compelling meta descriptions."},
            {"role": "user", "content": description_prompt}
        ]
    )
    meta_description = description_response.choices[0].message.content.strip()
    
    # Create post directory
    post_dir = Path(BLOG_POST_DIR) / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Create post data with front matter
    post_data = {
        "title": title,
        "date": TIMESTAMP,
        "description": meta_description,
        "category": "Bitcoin",
        "tags": ["Bitcoin", "Cryptocurrency", "Market Analysis", "Trading"],
        "author": "Michael J Ditter",
        "featured": True,
        "image": f"/img/blog/{slug}.jpg",  # Placeholder for image
        "slug": slug
    }
    
    # Create the HTML file
    post_file = post_dir / "index.html"
    
    # Template for HTML
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>{title} | Michael J Ditter</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="Bitcoin, Cryptocurrency, Market Analysis, Trading, Michael J Ditter">
    <meta name="author" content="Michael J Ditter">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://www.michaelditter.com/blog/{slug}/">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.michaelditter.com/blog/{slug}/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="https://www.michaelditter.com/img/blog/{slug}.jpg">
    <meta property="article:published_time" content="{TIMESTAMP}">
    <meta property="article:author" content="https://www.michaelditter.com/#person">
    <meta property="article:section" content="Bitcoin">
    <meta property="article:tag" content="Bitcoin">
    <meta property="article:tag" content="Cryptocurrency">
    <meta property="article:tag" content="Market Analysis">
    <meta property="article:tag" content="Trading">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://www.michaelditter.com/blog/{slug}/">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{meta_description}">
    <meta property="twitter:image" content="https://www.michaelditter.com/img/blog/{slug}.jpg">
    <meta property="twitter:creator" content="@michaeljditter">
    
    <!-- Favicons -->
    <link rel="apple-touch-icon" sizes="180x180" href="/img/favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon/favicon-16x16.png">
    <link rel="manifest" href="/img/favicon/site.webmanifest">
    
    <!-- CSS and Fonts -->
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="/css/blog.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    
    <!-- Schema.org structured data for Article -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{meta_description}",
        "image": "https://www.michaelditter.com/img/blog/{slug}.jpg",
        "datePublished": "{TIMESTAMP}",
        "dateModified": "{TIMESTAMP}",
        "author": {{
            "@type": "Person",
            "@id": "https://www.michaelditter.com/#person",
            "name": "Michael J Ditter",
            "url": "https://www.michaelditter.com"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Michael J Ditter",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://www.michaelditter.com/img/logo.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://www.michaelditter.com/blog/{slug}/"
        }},
        "keywords": "Bitcoin, Cryptocurrency, Market Analysis, Trading, Michael J Ditter",
        "articleSection": "Bitcoin"
    }}
    </script>
    
    <!-- Schema.org structured data for BreadcrumbList -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://www.michaelditter.com/"
            }},
            {{
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://www.michaelditter.com/blog/"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "{title}",
                "item": "https://www.michaelditter.com/blog/{slug}/"
            }}
        ]
    }}
    </script>
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-MP9VXW8V');</script>
    <!-- End Google Tag Manager -->
</head>
<body class="blog-post">
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MP9VXW8V"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    
    <!-- Header with Navigation -->
    <header class="site-header">
        <div class="container">
            <nav class="main-nav">
                <a href="/" class="logo">Michael J Ditter</a>
                <ul class="nav-links">
                    <li><a href="/#about">About</a></li>
                    <li><a href="/#expertise">Expertise</a></li>
                    <li><a href="/#services">Services</a></li>
                    <li><a href="/blog/" class="active">Insights</a></li>
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

    <!-- Blog Header -->
    <section class="blog-header">
        <div class="container">
            <div class="blog-breadcrumb">
                <a href="/">Home</a> / <a href="/blog/">Blog</a> / <span>Bitcoin Report</span>
            </div>
            <h1>{title}</h1>
            <div class="blog-meta">
                <div class="blog-author">
                    <img src="/img/profile/michael-ditter-headshot.jpg" alt="Michael J Ditter" width="50" height="50">
                    <span>By <a href="/#about">Michael J Ditter</a></span>
                </div>
                <div class="blog-details">
                    <span class="blog-date">{FORMATTED_DATE}</span>
                    <span class="blog-category">Bitcoin</span>
                    <span class="blog-read-time">10 min read</span>
                </div>
            </div>
            <div class="blog-featured-image">
                <img src="/img/blog/{slug}.jpg" alt="{title}" width="800" height="450">
            </div>
        </div>
    </section>

    <!-- Blog Content -->
    <article class="blog-content">
        <div class="container container-narrow">
            <!-- Bitcoin Data Summary -->
            <div class="bitcoin-summary">
                <div class="bitcoin-price-card">
                    <div class="price-header">
                        <h3>Bitcoin Price</h3>
                        <span class="update-time">Updated: {FORMATTED_DATE}</span>
                    </div>
                    <div class="price-main">
                        <span class="current-price">${bitcoin_data['current_price']}</span>
                        <span class="price-change {'' if bitcoin_data['price_change_24h'] < 0 else 'positive'}">{bitcoin_data['price_change_24h']:.2f}% (24h)</span>
                    </div>
                    <div class="price-details">
                        <div class="detail-item">
                            <span class="detail-label">Market Cap</span>
                            <span class="detail-value">${bitcoin_data['market_cap']:,}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">24h High</span>
                            <span class="detail-value">${bitcoin_data['high_24h']}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">24h Low</span>
                            <span class="detail-value">${bitcoin_data['low_24h']}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">All-Time High</span>
                            <span class="detail-value">${bitcoin_data['ath']} ({bitcoin_data['ath_change_percentage']:.2f}%)</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Main content with improved formatting -->
            <div class="blog-sections">
                {post_content}
            </div>
            
            <!-- Social Share -->
            <div class="social-share">
                <h3>Share This Report</h3>
                <p>Found this analysis helpful? Share it with your network:</p>
                <div class="share-buttons">
                    <a href="https://twitter.com/intent/tweet?text={social_content.replace(' ', '%20')}&url=https://www.michaelditter.com/blog/{slug}/" target="_blank" rel="noopener" class="share-button twitter">
                        <img src="/img/icons/twitter.svg" alt="Share on Twitter" width="24" height="24">
                        Share on X (Twitter)
                    </a>
                    <a href="https://www.linkedin.com/shareArticle?mini=true&url=https://www.michaelditter.com/blog/{slug}/&title={title.replace(' ', '%20')}" target="_blank" rel="noopener" class="share-button linkedin">
                        <img src="/img/icons/linkedin.svg" alt="Share on LinkedIn" width="24" height="24">
                        Share on LinkedIn
                    </a>
                </div>
            </div>
            
            <!-- Author Bio -->
            <div class="author-bio">
                <img src="/img/profile/michael-ditter-headshot.jpg" alt="Michael J Ditter" width="100" height="100">
                <div class="author-info">
                    <h3>About the Author</h3>
                    <p>
                        Michael J Ditter is the Director of AI Strategy and Emerging Technology at Diageo with extensive experience in AI implementation, immersive technologies, and digital innovation. He specializes in developing strategic approaches to AI adoption, AR/VR experiences, and emerging technology integration for global brands.
                    </p>
                    <div class="author-social">
                        <a href="https://www.linkedin.com/in/michaeljditter/" target="_blank" rel="noopener">LinkedIn</a>
                        <a href="https://twitter.com/michaeljditter" target="_blank" rel="noopener">Twitter</a>
                    </div>
                </div>
            </div>
            
            <!-- Related Posts -->
            <div class="related-posts">
                <h2>Related Articles</h2>
                <div class="related-posts-grid">
                    <div class="related-post">
                        <a href="/blog/ai-optimization-techniques">
                            <img src="/img/blog/ai-optimization.jpg" alt="AI Optimization Techniques" width="300" height="200">
                            <h3>10 Advanced AI Optimization Techniques to Improve Model Performance</h3>
                        </a>
                    </div>
                    <div class="related-post">
                        <a href="/blog/ethical-ai-frameworks">
                            <img src="/img/blog/ethical-ai.jpg" alt="Ethical AI Frameworks" width="300" height="200">
                            <h3>Building Ethical AI Frameworks: A Comprehensive Guide</h3>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </article>

    <!-- Newsletter Signup -->
    <section class="newsletter-section">
        <div class="container">
            <div class="newsletter-content">
                <h2>Get Weekly Bitcoin Analysis</h2>
                <p>Subscribe to my newsletter for weekly insights on Bitcoin, AI, and emerging technologies.</p>
                <form class="newsletter-form" action="/api/subscribe" method="POST">
                    <input type="email" name="email" placeholder="Your email address" required>
                    <button type="submit" class="btn-primary">Subscribe</button>
                </form>
                <p class="form-privacy">I respect your privacy. Unsubscribe at any time.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-main">
                <div class="footer-brand">
                    <a href="/" class="footer-logo">Michael J Ditter</a>
                    <p>Director of AI Strategy and Emerging Technology at Diageo, specializing in AI implementation, immersive technologies, and digital innovation.</p>
                    <div class="social-links">
                        <a href="https://www.linkedin.com/in/michaeljditter/" aria-label="LinkedIn Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/linkedin.svg" alt="LinkedIn" width="24" height="24">
                        </a>
                        <a href="https://twitter.com/michaeljditter" aria-label="Twitter Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/twitter.svg" alt="Twitter" width="24" height="24">
                        </a>
                        <a href="https://github.com/michaeljditter" aria-label="GitHub Profile" target="_blank" rel="noopener">
                            <img src="/img/icons/github.svg" alt="GitHub" width="24" height="24">
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
                            <li><a href="/blog/category/machine-learning">Machine Learning</a></li>
                            <li><a href="/blog/category/ai-ethics">AI Ethics</a></li>
                            <li><a href="/blog/category/bitcoin">Bitcoin</a></li>
                            <li><a href="/resources/white-papers">White Papers</a></li>
                            <li><a href="/resources/webinars">Webinars</a></li>
                        </ul>
                    </div>
                    <div class="footer-legal">
                        <h3>Legal</h3>
                        <ul>
                            <li><a href="/terms">Terms of Service</a></li>
                            <li><a href="/privacy">Privacy Policy</a></li>
                            <li><a href="/cookie-policy">Cookie Policy</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2023</span> Michael J Ditter. All rights reserved.</p>
                <p>Built with <span class="heart">♥</span> for optimal performance, accessibility, and SEO.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="/js/main.js"></script>
</body>
</html>'''
    
    # Save the HTML file
    with open(post_file, 'w') as f:
        f.write(html_template)
    
    # Create a JSON file with newsletter data for Buttondown
    newsletter_data = {
        "title": title,
        "content": post_content,
        "social_content": social_content,
        "description": meta_description,
        "tags": ["Bitcoin", "Cryptocurrency", "Market Analysis", "Trading"],
        "slug": slug,
        "url": f"https://www.michaelditter.com/blog/{slug}/",
        "bitcoin_data": bitcoin_data
    }
    
    newsletter_file = Path(".github") / "tmp" / f"{slug}-newsletter-data.json"
    newsletter_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(newsletter_file, 'w') as f:
        json.dump(newsletter_data, f, indent=2)
    
    # Create placeholder directories if they don't exist
    placeholder_dir = Path("img") / "blog"
    placeholder_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generated Bitcoin report: \"{title}\"")
    print(f"Report saved to: {post_file}")
    print(f"Newsletter data saved to: {newsletter_file}")
    print(f"Social media content: {social_content}")
    
    # Export the slug for use in other workflow steps
    try:
        if "GITHUB_ENV" in os.environ:
            github_env = os.environ["GITHUB_ENV"]
            with open(github_env, "a") as env_file:
                env_file.write(f"POST_SLUG={slug}\n")
                env_file.write(f"POST_TITLE={title}\n")
                
                # Use multi-line syntax for social content to avoid issues with special characters
                env_file.write("SOCIAL_CONTENT<<EOF\n")
                env_file.write(f"{social_content}\n")
                env_file.write("EOF\n")
            print("Successfully set workflow environment variables")
        else:
            print("GITHUB_ENV not found, skipping setting environment variables")
    except Exception as e:
        print(f"Warning: Failed to set GitHub environment variables: {str(e)}")
        print("This won't affect report generation but might impact subsequent workflow steps")
    
    return True

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        sys.exit(1)
    
    generate_content() 