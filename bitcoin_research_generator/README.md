# Bitcoin Research Index Page Generator

This tool automatically generates an HTML index page with the latest Bitcoin research updates across multiple categories. It's designed to fetch data from either a local JSON file or an API endpoint, process it, and generate a static HTML page that can be served on your website.

## Features

- Fetches Bitcoin research data from either a local JSON file or an API
- Processes data including Markdown to HTML conversion
- Generates a responsive, SEO-optimized HTML page using Jinja2 templates
- Organizes research updates into structured categories (market trends, price analysis, etc.)
- Creates visually appealing research cards with tags, dates, and trend indicators
- Includes proper metadata for social sharing and SEO
- Can be automated via GitHub Actions or other schedulers (runs every Friday by default)

## Requirements

- Python 3.7+
- Required Python packages:
  - `requests`
  - `jinja2`
  - `markdown`
  - `python-dotenv` (optional, for .env file support)

## Installation

1. Clone this repository or download the files to your project directory.

2. Install the required dependencies:

```bash
pip install -r bitcoin_research_generator/requirements.txt
```

3. Configure the settings by setting environment variables or editing the script directly.

## Configuration

The main configuration is in the `CONFIG` dictionary at the top of `generate_research_page.py`. You can override these settings using environment variables:

- **DATA_SOURCE_TYPE**: Set to "file" to read from a local JSON file or "api" to fetch from an API (default: "api")
- **DATA_FILE_PATH**: Path to the local JSON data file (used when type is "file")
- **API_URL**: URL of the API endpoint (used when type is "api")
- **API_KEY_ENV**: Name of the environment variable that contains your API key
- **OUTPUT_HTML_PATH**: Path where the generated HTML file will be saved
- **CANONICAL_URL**: The full URL where the page will be accessible online
- **TEMPLATE_DIR**: Directory containing the template files
- **TEMPLATE_FILE**: Name of the template file to use

## API Data Format

When using the API data source, the API response is expected to have the following structure:

```json
{
  "reportDate": "2023-06-09",
  "bitcoinPrice": {
    "current": "$84,570",
    "weeklyChange": "2.5%",
    "weeklyTrend": "up"
  },
  "marketSummary": {
    "marketCap": "$1.65 trillion",
    "volume24h": "$45.2 billion",
    "dominance": "57.2%"
  },
  "keyInsights": [
    {
      "title": "Institutional Adoption Accelerates",
      "content": "Major financial institutions including Fidelity and BlackRock continue to increase their Bitcoin holdings.",
      "source": "Bloomberg Financial",
      "date": "2023-06-07"
    }
  ],
  "technicalAnalysis": {
    "supportLevels": ["$79,500", "$77,800", "$75,200"],
    "resistanceLevels": ["$86,500", "$90,000", "$100,000"],
    "indicators": {
      "rsi": "65.2",
      "macd": "Bullish crossover forming",
      "movingAverages": "Trading above all major MAs"
    }
  },
  "regulatoryUpdates": [
    {
      "region": "United States",
      "development": "Treasury Department clarifies reporting requirements for cryptocurrency transactions above $10,000.",
      "impact": "Moderate",
      "date": "2023-06-07"
    }
  ],
  "outlook": {
    "shortTerm": "Bullish, with potential volatility around ETF decisions",
    "midTerm": "Strong upward momentum expected to continue through Q3",
    "keyRisks": [
      "Regulatory uncertainty in key markets",
      "Macroeconomic headwinds affecting risk assets",
      "Technical resistance at psychological $100K level"
    ]
  },
  "upcomingEvents": [
    {
      "name": "Bitcoin Amsterdam Conference",
      "date": "2023-06-23",
      "significance": "Major industry gathering with key announcements expected"
    }
  ]
}
```

The generator will format this data into the following categories for the HTML template:

- Bitcoin Market Trends
- Price Analysis
- Institutional Developments
- Regulatory Updates
- Technology Advancements
- Research Insights
- Outlook & Forecasts

## Usage

Run the script to generate the HTML page:

```bash
python bitcoin_research_generator/generate_research_page.py
```

## GitHub Action Automation

This tool is designed to be used with GitHub Actions for automated updates. The workflow runs every Friday at midnight UTC by default.

To set up:

1. Make sure the repository has the `.github/workflows/bitcoin-research-update.yml` file
2. Set the required secrets in your GitHub repository settings:
   - `BITCOIN_RESEARCH_API_KEY` (if your API requires authentication)

The action will:
1. Fetch the latest Bitcoin research data from the API
2. Generate the HTML page
3. Commit and push any changes to the repository

## API Keys and Security

If you're using an API that requires authentication:

1. Set your API key as an environment variable:
```bash
export BITCOIN_RESEARCH_API_KEY="your-api-key-here"
```

2. Or add it to your .env file (and ensure it's in .gitignore):
```
BITCOIN_RESEARCH_API_KEY=your-api-key-here
```

3. For cron jobs or scripts, include the environment variable in the command:
```
BITCOIN_RESEARCH_API_KEY="your-api-key-here" python bitcoin_research_generator/generate_research_page.py
```

**NEVER hardcode API keys directly in your script or commit them to version control.**

## Customization

To customize the appearance of the generated page:
1. Edit the `research_index.html` template in the templates directory
2. Modify the inline CSS in the template

## License

[MIT License](LICENSE)

## Author

Michael J Ditter 