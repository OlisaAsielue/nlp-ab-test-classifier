import requests
from bs4 import BeautifulSoup
import json

def scrape_case_study(url):
    """
    Scrapes a single VWO case study page for its title and body text.
    Uses robust selectors to handle variations in page layout.

    Args:
        url (str): The URL of the case study page to scrape.

    Returns:
        dict: A dictionary containing the scraped data, or None on failure.
    """
    print(f"Scraping: {url}")
    headers = {'User-Agent': 'My Learning Scraper 1.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        # --- Title Scraping ---
        # We will look for the first <h1> tag on the page. This is more
        # robust than relying on a complex, auto-generated class name.
        title = None # Default to None
        try:
            title_element = soup.find('h1')
            title = title_element.get_text(strip=True)
        except AttributeError:
            # This 'except' block will catch errors if the <h1> tag is not found
            print(f"  - Warning: Could not find title for {url}")


        # --- Body Text Scraping ---
        # We use the specific class name we found for the main content container.
        body_text = None # Default to None
        try:
            content_container = soup.find('div', class_='rich-editor-content')
            paragraphs = content_container.find_all('p')
            body_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        except AttributeError:
            # This 'except' block will catch errors if the content container is not found
            print(f"  - Warning: Could not find body text for {url}")


        # --- Compile Results ---
        return {
            'url': url,
            'title': title,
            'body_text': body_text
        }

    except requests.exceptions.RequestException as e:
        print(f"  - Request failed: {e}")
        return None

# ==============================================================================
# --- TEST HARNESS ---
# ==============================================================================
if __name__ == "__main__":
    # Test your function with a few different URLs from your list
    test_urls = [
        'https://vwo.com/success-stories/ubisoft/',
        'https://vwo.com/success-stories/citycliq/', # One of the pages you inspected
        'https://vwo.com/success-stories/schuh/'
    ]
    
    results = []
    for url in test_urls:
        data = scrape_case_study(url)
        if data:
            results.append(data)
            # Print a snippet for verification
            print("  - Success: Found title '{}'".format(data.get('title')))
            print("  - Body snippet: '{}...'".format(data.get('body_text', '')[:70]))
        print("-" * 20)

    print("\n--- SCRAPING TEST COMPLETE ---")
    print(json.dumps(results, indent=2))