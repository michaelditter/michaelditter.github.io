#!/usr/bin/env python3
import os
import sys
import json
import yaml
import requests
import datetime
from pathlib import Path
import frontmatter
import openai

# Configure OpenAI API
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Get topics from workflow input or use default
topic = os.environ.get("TOPIC", "ai-strategy")

# Constants
BLOG_POST_DIR = "blog"
CURRENT_DATE = datetime.datetime.now()
POST_DATE = CURRENT_DATE.strftime("%Y-%m-%d")
TIMESTAMP = CURRENT_DATE.strftime("%Y-%m-%dT%H:%M:%S+00:00")

# Map topics to specific details
TOPIC_DETAILS = {
    "ai-strategy": {
        "category": "AI Strategy",
        "title_prefix": "AI Strategy: ",
        "prompt_prefix": "Write an informative article about AI strategy, focusing on how businesses can effectively implement AI solutions. ",
        "tags": ["AI Strategy", "Leadership", "Digital Transformation"]
    },
    "machine-learning": {
        "category": "Machine Learning",
        "title_prefix": "Machine Learning Insights: ",
        "prompt_prefix": "Create a detailed technical article about recent advancements in machine learning, focusing on practical applications. ",
        "tags": ["Machine Learning", "Neural Networks", "AI Development"]
    },
    "ai-ethics": {
        "category": "AI Ethics",
        "title_prefix": "Ethical Considerations in AI: ",
        "prompt_prefix": "Compose a thoughtful piece about ethical considerations in artificial intelligence, addressing concerns and best practices. ",
        "tags": ["AI Ethics", "Responsible AI", "Technology Ethics"]
    },
    "emerging-tech": {
        "category": "Emerging Technology",
        "title_prefix": "Emerging Technology Trends: ",
        "prompt_prefix": "Write an analysis of current emerging technology trends, focusing on AI, AR/VR, and how they're transforming industries. ",
        "tags": ["Emerging Technology", "Innovation", "Digital Trends"]
    }
}

def get_topic_details():
    """Get details for the selected topic"""
    if topic in TOPIC_DETAILS:
        return TOPIC_DETAILS[topic]
    # Default to AI Strategy if topic not found
    return TOPIC_DETAILS["ai-strategy"]

def generate_post_slug(title):
    """Generate a URL-friendly slug from the title"""
    slug = title.lower()
    # Replace special characters with spaces
    for char in "!@#$%^&*()_+{}|:\"<>?`-=[]\\;',./":
        slug = slug.replace(char, " ")
    # Replace multiple spaces with a single space
    slug = " ".join(slug.split())
    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")
    return slug

def generate_content():
    """Generate blog post content using OpenAI"""
    topic_details = get_topic_details()
    
    # First, generate a title
    title_prompt = f"Generate a compelling, specific title for a professional blog post about {topic}. The title should be informative, include specific details, and be 50-70 characters long. Do not include quotation marks."
    title_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional content strategist who creates compelling titles for technical blog posts."},
                  {"role": "user", "content": title_prompt}]
    )
    title = title_response.choices[0].message.content.strip()
    if title_details := topic_details.get("title_prefix"):
        if not title.startswith(title_details):
            title = f"{title_details}{title}"
    
    # Get slug from title
    slug = generate_post_slug(title)
    
    # Generate the full blog post content
    content_prompt = f"""{topic_details.get('prompt_prefix', '')}
The article should:
- Start with a compelling introduction that establishes why this topic matters
- Include 4-5 main sections with clear, informative headings
- Provide specific, actionable insights rather than general advice
- Include real-world examples or case studies where applicable
- End with a conclusion summarizing key points and suggesting next steps
- Be approximately 1500-2000 words, written in a professional but accessible tone
- Include markdown formatting for headers, lists, bold text for emphasis
- Be written in the voice of Michael J Ditter, Director of AI Strategy and Emerging Technology at Diageo

The content should demonstrate deep expertise without being overly academic, and should position the author as a thought leader in AI and emerging technologies.
    """
    
    content_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional technology writer with expertise in AI, machine learning, and emerging technologies."},
            {"role": "user", "content": content_prompt}
        ]
    )
    post_content = content_response.choices[0].message.content.strip()
    
    # Generate meta description for SEO
    description_prompt = f"Write a compelling meta description for a blog post with the title '{title}'. The description should be 150-160 characters, include keywords related to {topic}, and encourage readers to click. Do not use quotes in your response."
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
        "category": topic_details.get("category", "AI Strategy"),
        "tags": topic_details.get("tags", ["AI Strategy"]),
        "author": "Michael J Ditter",
        "featured": False,
        "image": f"/img/blog/{slug}.jpg",  # Placeholder for image
        "slug": slug
    }
    
    # Create the markdown file with frontmatter
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
    <meta name="keywords" content="{", ".join(topic_details.get("tags", ["AI Strategy"]))}, Michael J Ditter">
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
    <meta property="article:section" content="{topic_details.get("category", "AI Strategy")}">
    {" ".join([f'<meta property="article:tag" content="{tag}">' for tag in topic_details.get("tags", ["AI Strategy"])])}
    
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
        "keywords": "{", ".join(topic_details.get("tags", ["AI Strategy"]))}, AI, Technology, Michael J Ditter",
        "articleSection": "{topic_details.get("category", "AI Strategy")}"
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
</head>
<body class="blog-post">
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
                <a href="/">Home</a> / <a href="/blog/">Blog</a> / <span>{title}</span>
            </div>
            <h1>{title}</h1>
            <div class="blog-meta">
                <div class="blog-author">
                    <img src="/img/profile/michael-ditter-headshot.jpg" alt="Michael J Ditter" width="50" height="50">
                    <span>By <a href="/#about">Michael J Ditter</a></span>
                </div>
                <div class="blog-details">
                    <span class="blog-date">{CURRENT_DATE.strftime("%B %d, %Y")}</span>
                    <span class="blog-category">{topic_details.get("category", "AI Strategy")}</span>
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
            <!-- Convert Markdown to HTML -->
            {post_content}
            
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
                <h2>Stay Updated on AI Trends</h2>
                <p>Subscribe to my newsletter for the latest insights on AI, machine learning, and technology strategy.</p>
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
                            <li><a href="/blog/category/case-studies">Case Studies</a></li>
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
        "description": meta_description,
        "tags": topic_details.get("tags", ["AI Strategy"]),
        "slug": slug,
        "url": f"https://www.michaelditter.com/blog/{slug}/"
    }
    
    newsletter_file = Path(".github") / "tmp" / f"{slug}-newsletter-data.json"
    newsletter_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(newsletter_file, 'w') as f:
        json.dump(newsletter_data, f, indent=2)
    
    # Create a placeholder image
    placeholder_dir = Path("img") / "blog"
    placeholder_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generated blog post: {title}")
    print(f"Post saved to: {post_file}")
    print(f"Newsletter data saved to: {newsletter_file}")
    
    # Export the slug for use in other workflow steps
    with open(os.environ["GITHUB_ENV"], "a") as env_file:
        env_file.write(f"POST_SLUG={slug}\n")
        env_file.write(f"POST_TITLE={title}\n")
    
    return True

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        sys.exit(1)
    
    generate_content() 