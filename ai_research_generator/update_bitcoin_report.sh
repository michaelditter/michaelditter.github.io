#!/bin/bash
#
# Bitcoin Market Report Update Script
#
# This script generates and updates the Bitcoin market report by:
# 1. Fetching the latest market data
# 2. Generating the HTML report
# 3. Updating the bitcoin market report page
#
# It can be scheduled via cron for automatic updates.
# Example cron entry to run weekly on Wednesday at 3am:
# 0 3 * * 3 /path/to/ai_research_generator/update_bitcoin_report.sh

# Exit on any error
set -e

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_DIR="${BASE_DIR}/blog/bitcoin-market-report-${REPORT_DATE}"
LOG_FILE="${BASE_DIR}/ai_research_generator/bitcoin_report_update.log"
BTC_PRICE_API="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"

# Log start
echo "$(date): Starting Bitcoin market report update" | tee -a "$LOG_FILE"

# Change to base directory
cd "$BASE_DIR"

# Create report directory if it doesn't exist
if [ ! -d "$REPORT_DIR" ]; then
  echo "Creating report directory: $REPORT_DIR" | tee -a "$LOG_FILE"
  mkdir -p "$REPORT_DIR"
fi

# Fetch latest Bitcoin price (for demonstration - this would be expanded in a real implementation)
if command -v curl &> /dev/null; then
  echo "Fetching latest Bitcoin price..." | tee -a "$LOG_FILE"
  BTC_DATA=$(curl -s "$BTC_PRICE_API")
  BTC_PRICE=$(echo "$BTC_DATA" | grep -o '"usd":[0-9.]*' | cut -d':' -f2)
  BTC_CHANGE=$(echo "$BTC_DATA" | grep -o '"usd_24h_change":[0-9.-]*' | cut -d':' -f2)
  
  echo "Bitcoin price: $BTC_PRICE (24h change: ${BTC_CHANGE}%)" | tee -a "$LOG_FILE"
  
  # Update the Bitcoin price in our report JSON data
  # This is a simplified example - in a real implementation, you'd update a proper data file
  # For now, we'll just copy the existing research index and modify it
else
  echo "curl not found - skipping Bitcoin price update" | tee -a "$LOG_FILE"
fi

# Copy the existing Bitcoin report as a starting point
if [ -f "${BASE_DIR}/blog/bitcoin-research-index.html" ]; then
  echo "Copying existing Bitcoin report as template..." | tee -a "$LOG_FILE"
  cp "${BASE_DIR}/blog/bitcoin-research-index.html" "${REPORT_DIR}/index.html"
  
  # Update the canonical URL and date references
  sed -i '' "s|https://www.michaelditter.com/blog/bitcoin-research-index.html|https://www.michaelditter.com/blog/bitcoin-market-report-${REPORT_DATE}/|g" "${REPORT_DIR}/index.html"
  sed -i '' "s|Bitcoin Market Report - [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}|Bitcoin Market Report - ${REPORT_DATE}|g" "${REPORT_DIR}/index.html"
  
  # Create backup
  cp "${REPORT_DIR}/index.html" "${REPORT_DIR}/index.html.bak"
  
  echo "Bitcoin report created at: ${REPORT_DIR}/index.html" | tee -a "$LOG_FILE"
else
  echo "Error: Template file blog/bitcoin-research-index.html not found" | tee -a "$LOG_FILE"
  exit 1
fi

# Update Twitter card URL in homepage
if grep -q "bitcoin-market-report" "${BASE_DIR}/index.html"; then
  echo "Updating Bitcoin report link on homepage..." | tee -a "$LOG_FILE"
  sed -i '' "s|/blog/bitcoin-market-report-[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/|/blog/bitcoin-market-report-${REPORT_DATE}/|g" "${BASE_DIR}/index.html"
fi

echo "$(date): Bitcoin market report update completed successfully" | tee -a "$LOG_FILE"
echo "Report available at: https://www.michaelditter.com/blog/bitcoin-market-report-${REPORT_DATE}/" 