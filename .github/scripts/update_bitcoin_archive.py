#!/usr/bin/env python3
"""
Update the Bitcoin report archive page to include the latest report.
This script maintains an archive of all Bitcoin reports for historical reference.
"""

import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

ARCHIVE_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>Bitcoin Market Report Archive | Michael J Ditter</title>
    <meta name="description" content="Archive of daily Bitcoin market reports with analysis, trends, and insights by Michael J Ditter">
    <meta name="keywords" content="Bitcoin, Cryptocurrency, Market Analysis, Crypto Reports, Bitcoin Price">
    <meta name="author" content="Michael J Ditter">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://www.michaelditter.com/blog/bitcoin-report-archive/">
    
    <!-- CSS and Fonts -->
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/custom-overrides.css">
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

    <!-- Archive Content -->
    <section class="archive-section">
        <div class="container">
            <div class="archive-header">
                <h1>Bitcoin Market Report Archive</h1>
                <p class="archive-subtitle">A historical record of Bitcoin market analysis and insights</p>
            </div>
            
            <div class="archive-description">
                <p>This archive contains all historical Bitcoin market reports, providing a comprehensive view of Bitcoin's price movement, market trends, and key events over time. Each report includes price analysis, significant market developments, and outlook projections.</p>
            </div>

            <div class="archive-search">
                <input type="text" id="archiveSearch" placeholder="Search reports..." onkeyup="filterReports()">
            </div>
            
            <div class="archive-list" id="archiveList">
                <!-- Archive entries will be automatically added here -->
                {archive_entries}
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
                            <li><a href="/blog/bitcoin-report-archive/">Bitcoin Archive</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span id="currentYear">2025</span> Michael J Ditter. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Set current year
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        
        // Search functionality
        function filterReports() {
            var input = document.getElementById('archiveSearch');
            var filter = input.value.toUpperCase();
            var items = document.getElementsByClassName('archive-item');
            
            for (var i = 0; i < items.length; i++) {
                var txtValue = items[i].textContent || items[i].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    items[i].style.display = "";
                } else {
                    items[i].style.display = "none";
                }
            }
        }
    </script>
    
    <style>
        .archive-section {
            padding: 80px 0;
        }
        
        .archive-header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .archive-header h1 {
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 10px;
        }
        
        .archive-subtitle {
            font-size: 1.2rem;
            color: #666;
        }
        
        .archive-description {
            max-width: 800px;
            margin: 0 auto 40px;
            text-align: center;
        }
        
        .archive-search {
            margin-bottom: 30px;
            text-align: center;
        }
        
        .archive-search input {
            width: 100%;
            max-width: 500px;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
        }
        
        .archive-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .archive-item {
            padding: 20px;
            border: 1px solid #eee;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .archive-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .archive-item-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .archive-item-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            margin: 0;
        }
        
        .archive-item-date {
            font-size: 0.9rem;
            color: #888;
        }
        
        .archive-item-content {
            margin-bottom: 15px;
        }
        
        .archive-item-price {
            font-weight: 600;
            color: #0066cc;
        }
        
        .archive-item-change {
            font-weight: 500;
            margin-left: 10px;
        }
        
        .archive-item-change.positive {
            color: #28a745;
        }
        
        .archive-item-change.negative {
            color: #dc3545;
        }
        
        .archive-item-points {
            margin-top: 10px;
            padding-left: 20px;
        }
        
        .archive-item-points li {
            margin-bottom: 5px;
        }
        
        .archive-item-link {
            display: inline-block;
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
            margin-top: 10px;
        }
        
        .archive-item-link:hover {
            text-decoration: underline;
        }
    </style>
</body>
</html>
"""

ARCHIVE_ITEM_TEMPLATE = """
<div class="archive-item">
    <div class="archive-item-header">
        <h2 class="archive-item-title">Bitcoin Market Report - {date}</h2>
        <span class="archive-item-date">{date_full}</span>
    </div>
    <div class="archive-item-content">
        <span class="archive-item-price">{price}</span>
        <span class="archive-item-change {change_class}">{price_change}</span>
        <ul class="archive-item-points">
            {points}
        </ul>
    </div>
    <a href="/blog/{slug}/" class="archive-item-link">Read Full Report</a>
</div>
"""

def extract_reports_from_blog():
    """Extract existing Bitcoin reports from the blog directory."""
    reports = []
    blog_dir = Path("blog")
    
    if not blog_dir.exists():
        return reports
    
    # Pattern to match Bitcoin report folders
    pattern = re.compile(r"bitcoin-market-report-(\d{4})-(\d{2})-(\d{2})")
    
    for item in blog_dir.iterdir():
        if item.is_dir():
            match = pattern.match(item.name)
            if match:
                reports.append(item.name)
    
    return sorted(reports, reverse=True)  # Most recent first

def extract_report_data(report_slug, json_data_file=None):
    """Extract data for a specific report."""
    data = {
        "slug": report_slug,
        "price": "$84,570",
        "price_change": "(+3.60%)",
        "key_points": [
            "Positive regulatory moves & pending SEC Bitcoin ETF decision",
            "Institutional adoption with Fidelity & BlackRock"
        ],
        "date": "Mar 21, 2025"
    }
    
    # Try to get date from slug
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", report_slug)
    if date_match:
        year, month, day = date_match.groups()
        date_obj = datetime(int(year), int(month), int(day))
        data["date"] = date_obj.strftime("%b %d, %Y")
        data["date_full"] = date_obj.strftime("%B %d, %Y")
    
    # Load data from JSON if available
    if json_data_file and os.path.exists(json_data_file):
        try:
            with open(json_data_file, 'r') as f:
                json_data = json.load(f)
                data["price"] = json_data.get("price", data["price"])
                data["price_change"] = json_data.get("price_change_24h", data["price_change"])
                if "key_points" in json_data and json_data["key_points"]:
                    data["key_points"] = json_data["key_points"]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load data from {json_data_file}: {e}")
    
    # Determine change class for styling
    if data["price_change"].startswith("(+"):
        data["change_class"] = "positive"
    elif data["price_change"].startswith("(-"):
        data["change_class"] = "negative"
    else:
        data["change_class"] = ""
    
    return data

def generate_archive_page(reports, latest_data=None):
    """Generate the archive page with all reports."""
    # Ensure the blog directory exists
    archive_dir = Path("blog/bitcoin-report-archive")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate HTML for each report
    archive_entries = ""
    
    for i, report_slug in enumerate(reports):
        # Use the latest data for the most recent report
        report_data = latest_data if i == 0 and latest_data else extract_report_data(report_slug)
        
        # Format the key points as HTML list items
        points_html = "\n".join([f"<li>{point}</li>" for point in report_data["key_points"]])
        
        # Fill in the template
        entry_html = ARCHIVE_ITEM_TEMPLATE.format(
            date=report_data["date"],
            date_full=report_data.get("date_full", report_data["date"]),
            price=report_data["price"],
            price_change=report_data["price_change"],
            change_class=report_data["change_class"],
            points=points_html,
            slug=report_slug
        )
        
        archive_entries += entry_html
    
    # Create the final HTML
    archive_html = ARCHIVE_PAGE_TEMPLATE.format(archive_entries=archive_entries)
    
    # Write to file
    archive_file = archive_dir / "index.html"
    with open(archive_file, "w", encoding="utf-8") as f:
        f.write(archive_html)
    
    print(f"Successfully created Bitcoin report archive page with {len(reports)} reports")
    return True

def main():
    """Main function to update the Bitcoin report archive."""
    # Get the current report slug
    report_slug = None
    json_data_file = None
    
    # Check command line arguments
    if len(sys.argv) > 1:
        report_slug = sys.argv[1]
    
    # If not provided via command line, check environment variables
    if not report_slug:
        report_slug = os.environ.get("POST_SLUG")
    
    # If still not available, generate based on today's date
    if not report_slug:
        today = datetime.now()
        report_slug = f"bitcoin-market-report-{today.strftime('%Y-%m-%d')}"
    
    # Check for JSON data file
    if len(sys.argv) > 2:
        json_data_file = sys.argv[2]
    else:
        json_data_file = os.environ.get("NEWSLETTER_DATA_FILE")
    
    # Get all existing reports
    reports = extract_reports_from_blog()
    
    # Make sure the current report is included
    if report_slug not in reports:
        reports.insert(0, report_slug)
    
    # Extract data for the latest report
    latest_data = extract_report_data(report_slug, json_data_file)
    
    # Generate the archive page
    success = generate_archive_page(reports, latest_data)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 