import feedparser
import csv
import re
from datetime import datetime

##########################################################################################
# Things it needs to do
#
# need to have blank fields for the rest that arent in the RSS feed
# slug, year, month, actor, actor_type, organization, industry_code, industry, 
# motive, event_type, event_subtype, source_url, country, actor_country
# 
# need to only grab cyber attacks and not the rest of the stuff
# for each write in the with open need to add a ai thing for it to look at the summary and put into categories
#
# from the categories there needs also to be a few categories made 
#
# For the full thing it needs to run after x amount of days
#
# Needs to send an update with the amount added and that the process was completed 
#
##########################################################################################

# Function to clean the summary 
def clean_summary(summary):
    summary = re.sub(r'<[^>]+>', '', summary)
    summary = re.sub(r'\s+', ' ', summary).strip()
    return summary

# Function to fetch, filter, and deduplicate RSS data
def fetch_rss_data(url, unique_rows):
    feed = feedparser.parse(url)
    print("Feed Title:", feed.feed.title)
    for entry in feed.entries:
        # Check if the summary contains relevant keywords
        if any(keyword in entry.summary.lower() for keyword in ["cyber attack", "hacker", "hacker group", "data breach"]):
            if entry.link not in unique_rows:
                try:
                    # Parse the published date into year and month
                    published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")  # Format: "Fri, 04 Apr 2025 13:26:38 -0400"
                    year = published_date.year
                    month = published_date.month
                except Exception:
                    year = None
                    month = None

                # Clean the summary field
                cleaned_summary = clean_summary(entry.summary)

                # Add only the expected fields to unique_rows
                unique_rows[entry.link] = {
                    'title': entry.title,
                    'link': entry.link,
                    'year': year,
                    'month': month,
                    'summary': cleaned_summary
                }


rss_feed_urls = [
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.securityweek.com/feed",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.wired.com/feed/category/security/latest/rss"
]


unique_rows = {}


for url in rss_feed_urls:
    fetch_rss_data(url, unique_rows)

# Write everything INSIDE the 'with open' block
with open('testpilot.csv', mode='a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'link', 'year', 'month', 'summary']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in unique_rows.values():
        writer.writerow(row)
