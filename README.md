# Michael Ditter - Personal Branding Website

This repository contains the code for Michael Ditter's personal branding website, optimized for both traditional search engines and AI models (GEO/LLMO - Generative Engine Optimization/Large Language Model Optimization).

## Project Structure

- `index.html`: Main landing page
- `css/`: Stylesheet directory
  - `styles.css`: Main stylesheet
- `js/`: JavaScript directory
  - `main.js`: Main JavaScript file
- `img/`: Image assets
- `blog/`: Blog articles and content
  - `ai-research-index.html`: Weekly AI research index (auto-generated)
  - `bitcoin-research-index.html`: Weekly Bitcoin research index (auto-generated)
- `ai_research_generator/`: Code for generating the AI research index
- `bitcoin_research_generator/`: Code for generating the Bitcoin research index
- `ai-research-api/`: Serverless API for AI research data
- `bitcoin-research-api/`: Serverless API for Bitcoin research data
- `.github/workflows/`: GitHub Actions for automated content generation
- `sitemap.xml`: XML sitemap for search engines
- `robots.txt`: Instructions for search engine crawlers

## Development

This website is built with modern HTML5, CSS3, and JavaScript to ensure optimal performance, accessibility, and SEO.

## Automated Research Index Generators

This project includes two automated research index generators:

1. **AI Research Index Generator**
   - Updates every Wednesday
   - Aggregates and presents the latest AI research
   - Uses a serverless API for data collection

2. **Bitcoin Research Index Generator**
   - Updates every Friday
   - Compiles the latest Bitcoin market trends, research, and analysis
   - Uses a serverless API for real-time data

### Quick Start Guide

To run the generators locally:

```bash
# For AI Research Generator
cd ai_research_generator
pip install -r requirements.txt
./run_generator.sh

# For Bitcoin Research Generator
cd bitcoin_research_generator
pip install -r requirements.txt
./run_generator.sh
```

For deployment and API setup, see:
- [Deployment Guide](DEPLOYMENT.md)
- [API Keys Guide](API_KEYS_GUIDE.md)
- [Production Checklist](PRODUCTION_CHECKLIST.md)

## SEO & AI Optimization Features

- Semantic HTML structure
- Schema.org structured data
- Clear content hierarchy with proper heading structure
- Optimized metadata for search engines
- Open Graph and Twitter Card integration
- XML sitemap and robots.txt configuration
- Mobile-first responsive design
- Optimized page load speed
- Automated content generation with GitHub Actions

## Security

All API keys and sensitive information are stored using environment variables and are never committed to the repository. See the [API Keys Guide](API_KEYS_GUIDE.md) for best practices on API key management. 