import csv
from bleepinScrap import fetch_rss_data
from Fontend import main_function  


rss_feed_urls = [
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.securityweek.com/feed",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.wired.com/feed/category/security/latest/rss"
]
input_file = "testpilot.csv"
output_file = "output.csv"

print("Fetching RSS data...")

# Fetch RSS data
unique_rows = {}
for url in rss_feed_urls:
    try:
        print(f"Fetching data from {url}...")
        fetch_rss_data(url, unique_rows)
    except Exception as e:
        print(f"Error fetching RSS feed from {url}: {e}")

if not unique_rows:
    print("No relevant RSS data found.")
else:
    print("Writing data to testpilot.csv...")
    try:
        # Ensure the keys in unique_rows match the fieldnames
        fieldnames = ['title', 'link', 'year', 'month', 'summary']
        filtered_rows = [
            {key: row.get(key, None) for key in fieldnames} for row in unique_rows.values()
        ]

        # Write the fetched data to the input file
        with open(input_file, mode='w', newline='', encoding='utf-8') as csvfile_in:
            writer = csv.DictWriter(csvfile_in, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print("RSS data fetched and written to testpilot.csv")
    except Exception as e:
        print(f"Error writing to {input_file}: {e}")

    # Run Fontend.py logic to predict fields and update output.csv
    print("Running Fontend.py logic to predict fields and update output.csv...")
    try:
        main_function()  # Call the main function from Fontend.py
        print("Fontend.py logic executed successfully.")
    except Exception as e:
        print(f"Error occurred while running Fontend.py logic: {e}")