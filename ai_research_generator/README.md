# AI Research Index Page Generator

This tool automatically generates an HTML index page with the latest AI research updates across multiple categories. It's designed to fetch data from either a local JSON file or an API endpoint, process it, and generate a static HTML page that can be served on your website.

## Features

- Fetches AI research data from either a local JSON file or an API
- Processes data including Markdown to HTML conversion
- Generates a responsive, SEO-optimized HTML page using Jinja2 templates
- Organizes research updates into structured categories
- Creates visually appealing research cards with tags, dates, and images
- Includes proper metadata for social sharing and SEO
- Can be automated via cron or other schedulers

## Requirements

- Python 3.7+
- Required Python packages:
  - `requests`
  - `jinja2`
  - `markdown`

## Installation

1. Clone this repository or download the files to your project directory.

2. Install the required dependencies:

```bash
pip install requests jinja2 markdown
```

3. Configure the settings in `generate_research_page.py` to match your environment.

## Configuration

The main configuration is in the `CONFIG` dictionary at the top of `generate_research_page.py`:

```python
CONFIG = {
    "data_source": {
        "type": "file",  # "file" or "api"
        "file_path": "ai_research_generator/data/research_data.json",
        "api_url": "https://api.example.com/ai_research_updates",
        "api_key_env": "AI_RESEARCH_API_KEY"  # Name of env var holding API key
    },
    "output": {
        "html_path": "blog/ai-research-index.html",
        "canonical_url": "https://www.michaelditter.com/blog/ai-research-index.html"
    },
    "template": {
        "dir": "ai_research_generator/templates",
        "file": "research_index.html"
    }
}
```

- **data_source**: Configure where to get the AI research data
  - `type`: Set to "file" to read from a local JSON file or "api" to fetch from an API
  - `file_path`: Path to the local JSON data file (used when type is "file")
  - `api_url`: URL of the API endpoint (used when type is "api")
  - `api_key_env`: Name of the environment variable that contains your API key

- **output**: Configure where to save the generated HTML
  - `html_path`: Path where the generated HTML file will be saved
  - `canonical_url`: The full URL where the page will be accessible online (for metadata)

- **template**: Configure the Jinja2 template
  - `dir`: Directory containing the template files
  - `file`: Name of the template file to use

## Data Format

The data should be a JSON object with section names as keys, and arrays of item objects as values:

```json
{
  "AI Model Updates": [
    {
      "title": "Model Name Released",
      "summary": "Short summary of the update",
      "description_md": "Optional Markdown content with **formatting**",
      "link": "https://example.com/article",
      "date": "2025-03-19",
      "image_url": "https://example.com/image.jpg",
      "tags": ["Tag1", "Tag2"]
    },
    ...
  ],
  "Hardware Advancements": [
    ...
  ],
  ...
}
```

Required sections (which will be displayed in this order):
- AI Model Updates
- Hardware Advancements
- Robotics
- Enterprise AI
- Regulatory News
- Research
- Future Trends

## Usage

Run the script to generate the HTML page:

```bash
python ai_research_generator/generate_research_page.py
```

## Automation

To automatically update the page regularly, set up a cron job. For example, to update daily at midnight:

```
0 0 * * * cd /path/to/project && python ai_research_generator/generate_research_page.py >> /path/to/logs/ai_research_generator.log 2>&1
```

### Important Note on API Keys

If you're using an API that requires authentication:

1. Set your API key as an environment variable:
```bash
export AI_RESEARCH_API_KEY="your-api-key-here"
```

2. Or add it to your .env file (and ensure it's in .gitignore):
```
AI_RESEARCH_API_KEY=your-api-key-here
```

3. For cron jobs, include the environment variable in the command:
```
0 0 * * * cd /path/to/project && AI_RESEARCH_API_KEY="your-api-key-here" python ai_research_generator/generate_research_page.py
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

# AI Content Generator System

This directory contains scripts for automatically generating and updating content for:
- AI Research Newsletter
- Bitcoin Market Report

## Setup

1. Ensure you have Python 3.6+ installed
2. Install required packages:
   ```
   pip install markdown jinja2 requests python-dotenv
   ```
3. Create a `.env` file in this directory with the following settings:
   ```
   DATA_SOURCE_TYPE=file
   API_URL=https://ai-research-api.michaelditter.com/api/research-data
   AI_RESEARCH_API_KEY=your_api_key_here
   ```

## Manual Content Generation

### AI Newsletter

To manually generate the AI newsletter:

```bash
./update_newsletter.sh
```

This will:
1. Validate all links in the research data
2. Generate the HTML content
3. Create a dated newsletter at `/blog/ai-newsletter-YYYY-MM-DD/`
4. Update links on the homepage

### Bitcoin Market Report

To manually generate the Bitcoin market report:

```bash
./update_bitcoin_report.sh
```

This will:
1. Fetch the latest Bitcoin price data
2. Generate an updated report HTML
3. Create a dated report at `/blog/bitcoin-market-report-YYYY-MM-DD/`
4. Update links on the homepage

## Automated Updates with Cron

For automatic updates, add the following to your crontab (`crontab -e`):

```
# Update AI Newsletter every Wednesday at 2:00 AM
0 2 * * 3 /full/path/to/ai_research_generator/update_newsletter.sh

# Update Bitcoin Market Report every Wednesday at 3:00 AM
0 3 * * 3 /full/path/to/ai_research_generator/update_bitcoin_report.sh
```

Make sure to use the full path to the scripts in your crontab entries.

## Customizing Content

### AI Newsletter Content

Update the research data file at `ai_research_generator/data/research_data.json` with new items in these categories:
- AI Model Updates
- Hardware Advancements
- Robotics
- Enterprise AI
- Regulatory News
- Research
- Future Trends

Each item should include:
- `title`: The headline
- `summary`: A brief overview
- `link`: URL to the original source
- `date`: Publication date (YYYY-MM-DD)
- `tags`: Array of related tags
- Optional `image_url`: Image to display with the item
- Optional `description_md`: Detailed content in Markdown format

### Bitcoin Market Report

For a more advanced implementation, create a data file similar to the AI research data, but with Bitcoin-specific categories and fetch real-time data using the CoinGecko API or similar services.

## Troubleshooting

- Check the log files in this directory for error messages:
  - `newsletter_update.log`
  - `bitcoin_report_update.log`

- If images are missing, they will be created as placeholder files. Replace them with actual images in the `/img/ai-research/` directory.

- Make sure your Python environment has all required packages and permissions to write to the blog directory.

## Security Notes

- The API key in your `.env` file should be kept secure
- When deploying, ensure cron tasks run with appropriate permissions
- Consider adding IP restrictions to your API endpoints 