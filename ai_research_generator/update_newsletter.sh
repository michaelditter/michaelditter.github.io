#!/bin/bash
#
# AI Newsletter Update Script
#
# This script updates the AI newsletter by:
# 1. Validating and fixing links in the research data
# 2. Generating the HTML content
# 3. Updating both the research index and newsletter pages
#
# It can be scheduled via cron for automatic updates.
# Example cron entry to run weekly on Wednesday at 2am:
# 0 2 * * 3 /path/to/ai_research_generator/update_newsletter.sh

# Exit on any error
set -e

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NEWSLETTER_DATE=$(date +%Y-%m-%d)
NEWSLETTER_DIR="${BASE_DIR}/blog/ai-newsletter-${NEWSLETTER_DATE}"
LOG_FILE="${BASE_DIR}/ai_research_generator/newsletter_update.log"

# Log start
echo "$(date): Starting AI newsletter update" | tee -a "$LOG_FILE"

# Change to base directory
cd "$BASE_DIR"

# Create newsletter directory if it doesn't exist
if [ ! -d "$NEWSLETTER_DIR" ]; then
  echo "Creating newsletter directory: $NEWSLETTER_DIR" | tee -a "$LOG_FILE"
  mkdir -p "$NEWSLETTER_DIR"
fi

# Run the link validator (this also updates the research index HTML)
echo "Validating links and updating content..." | tee -a "$LOG_FILE"
python3 "${BASE_DIR}/ai_research_generator/validate_links.py" | tee -a "$LOG_FILE"

# Update the AI newsletter path in the configuration
export OUTPUT_HTML_PATH="blog/ai-research-index.html"
export CANONICAL_URL="https://www.michaelditter.com/blog/ai-research-index.html"
export DATA_SOURCE_TYPE=file

# Generate the research index page
echo "Generating research index page..." | tee -a "$LOG_FILE"
python3 "${BASE_DIR}/ai_research_generator/generate_research_page.py" | tee -a "$LOG_FILE"

# Copy to newsletter location and update canonical URL
echo "Updating newsletter page..." | tee -a "$LOG_FILE"
cp "${BASE_DIR}/blog/ai-research-index.html" "${NEWSLETTER_DIR}/index.html"
sed -i '' "s|https://www.michaelditter.com/blog/ai-research-index.html|https://www.michaelditter.com/blog/ai-newsletter-${NEWSLETTER_DATE}/|g" "${NEWSLETTER_DIR}/index.html"

# Create backup
cp "${NEWSLETTER_DIR}/index.html" "${NEWSLETTER_DIR}/index.html.bak"

# Update Twitter card URL in homepage
if grep -q "ai-newsletter" "${BASE_DIR}/index.html"; then
  echo "Updating Twitter card on homepage..." | tee -a "$LOG_FILE"
  sed -i '' "s|/blog/ai-newsletter-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/|/blog/ai-newsletter-${NEWSLETTER_DATE}/|g" "${BASE_DIR}/index.html"
fi

echo "$(date): AI newsletter update completed successfully" | tee -a "$LOG_FILE"
echo "Newsletter available at: https://www.michaelditter.com/blog/ai-newsletter-${NEWSLETTER_DATE}/" 