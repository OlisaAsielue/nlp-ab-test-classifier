import csv
import time
from detail_scraper import scrape_case_study

# --- CONFIGURATION ---
# The input file containing one URL per line
URL_FILE = 'vwo_urls.txt'
# The output file for our final dataset
OUTPUT_FILE = 'vwo_corpus.csv'

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    print("Starting Stage 3: Orchestrator")

    # Read all the target URLs from our text file
    with open(URL_FILE, 'r') as f:
        # .read().splitlines() is a quick way to get a list of all lines
        target_urls = f.read().splitlines()

    # An empty list to hold all the dictionaries of scraped data
    full_dataset = []
    total_urls = len(target_urls)
    
    print(f"Found {total_urls} URLs to scrape.")
    
    # Loop through every URL in the list
    for i, url in enumerate(target_urls):
        # The enumerate function gives us both the index (i) and the value (url)
        print(f"Scraping URL {i+1} of {total_urls}: {url}")
        
        # Call our robust scraping function from the other file
        scraped_data = scrape_case_study(url)
        
        # Only add the data to our dataset if the scrape was successful
        if scraped_data:
            full_dataset.append(scraped_data)
        
        # A polite pause to avoid overwhelming the server
        time.sleep(1)

    print(f"\n--- SCRAPING PHASE COMPLETE ---")
    print(f"Successfully scraped {len(full_dataset)} out of {total_urls} pages.")

    # --- SAVING THE DATA ---
    if full_dataset:
        # Open the output file in write mode
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            # Get the headers from the keys of the first dictionary in our list
            headers = full_dataset[0].keys()
            
            # Create a DictWriter object, which can write dictionaries to a CSV
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write the header row to the CSV file
            writer.writeheader()
            
            # Write all the dictionary rows to the CSV file
            writer.writerows(full_dataset)
            
        print(f"Data has been saved to '{OUTPUT_FILE}'")
    else:
        print("No data was collected, so no output file was created.")