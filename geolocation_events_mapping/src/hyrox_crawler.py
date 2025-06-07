import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import logging
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HyroxCrawler:
    def __init__(self):
        self.base_url = "https://hyrox.com/find-my-race/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    def fetch_page(self, url):
        """Fetch the webpage content with retry mechanism."""
        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("Max retries reached. Could not fetch the page.")
                    return None

    def debug_html_structure(self, html_content):
        """Debug function to print the HTML structure of event cards."""
        if not html_content:
            return

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try different possible selectors
        selectors = [
            'a.event-card',
            'div.event-card',
            'div[class*="event"]',
            'div[class*="race"]',
            'div[class*="competition"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                logger.info(f"\nFound {len(elements)} elements with selector: {selector}")
                for i, element in enumerate(elements[:1]):  # Print only first element as example
                    logger.info(f"\nExample element {i+1}:")
                    logger.info(element.prettify())
                break
        else:
            logger.info("No elements found with any of the selectors. Printing page structure:")
            logger.info(soup.prettify()[:1000])  # Print first 1000 chars of the page

    def parse_events(self, html_content):
        """Parse the HTML content to extract event information."""
        if not html_content:
            return []

        # First, debug the HTML structure
        self.debug_html_structure(html_content)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        events = []

        # Find all event cards - using the correct selector
        event_cards = soup.find_all('div', class_='w-grid-item-h')

        for card in event_cards:
            try:
                # Extract event details using the correct selectors
                title_element = card.select_one('.w-post-elm.post_title a')
                date_element = card.select_one('.w-post-elm-value')
                location_element = card.select_one('.w-post-elm.post_custom_field')
                url_element = card.select_one('.w-post-elm.post_title a')
                
                if title_element and date_element:
                    event = {
                        'title': title_element.text.strip(),
                        'date': date_element.text.strip(),
                        'location': location_element.text.strip() if location_element else '',
                        'url': url_element['href'] if url_element and 'href' in url_element.attrs else '',
                        'continent': self._extract_continent(card),
                        'status': 'Active'  # Default status
                    }
                    
                    # Clean and validate the data
                    event = {k: v.strip() if isinstance(v, str) else v for k, v in event.items()}
                    
                    # Only add events that have at least a title and date
                    if event['title'] and event['date']:
                        events.append(event)
                    else:
                        logger.warning(f"Skipping event due to missing required fields: {event}")
                    
            except Exception as e:
                logger.error(f"Error parsing event card: {e}")

        return events

    def _extract_continent(self, element):
        """Helper method to extract continent from the element's classes."""
        try:
            classes = element.get('class', [])
            for class_name in classes:
                if class_name.startswith('continent-'):
                    return class_name.replace('continent-', '').replace('-', ' ').title()
            return ''
        except Exception as e:
            logger.error(f"Error extracting continent: {e}")
            return ''

    def save_to_csv(self, events, filename='output/data/hyrox_events.csv'):
        """Save events to a CSV file."""
        try:
            df = pd.DataFrame(events)
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Events saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

    def save_to_json(self, events, filename='output/data/hyrox_events.json'):
        """Save events to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
            logger.info(f"Events saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

def main():
    crawler = HyroxCrawler()
    
    # Fetch the page
    logger.info("Fetching HYROX events page...")
    html_content = crawler.fetch_page(crawler.base_url)
    
    if html_content:
        # Parse events
        logger.info("Parsing events...")
        events = crawler.parse_events(html_content)
        
        if events:
            # Save results
            crawler.save_to_csv(events)
            crawler.save_to_json(events)
            logger.info(f"Successfully extracted {len(events)} events")
        else:
            logger.warning("No events found")
    else:
        logger.error("Failed to fetch page content")

if __name__ == "__main__":
    main() 