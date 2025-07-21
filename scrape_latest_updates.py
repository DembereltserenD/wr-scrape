#!/usr/bin/env python3
"""
Scrape Latest Updates for Wild Rift Items
Focuses on getting the most up-to-date information for specific items
"""

import requests
import json
import re
import time
from bs4 import BeautifulSoup
from pathlib import Path
from real_time_item_scraper import RealTimeItemScraper

def scrape_rabadon():
    """Scrape the latest data for Rabadon's Deathcap"""
    print("Scraping latest data for Rabadon's Deathcap...")
    
    scraper = RealTimeItemScraper()
    item_data = scraper.scrape_specific_item("Rabadon's Deathcap")
    
    if item_data:
        print("\nSuccessfully scraped Rabadon's Deathcap:")
        print(f"Name: {item_data['name']}")
        print(f"Cost: {item_data['cost']}")
        print(f"Stats: {json.dumps(item_data['stats'], indent=2)}")
        print(f"Passive: {item_data['passive']}")
        print(f"Description: {item_data['description']}")
        if item_data.get('tips'):
            print("Tips:")
            for tip in item_data['tips']:
                print(f"  • {tip}")
    else:
        print("Failed to scrape Rabadon's Deathcap")
        
        # Try direct approach with custom URL
        print("\nTrying direct approach...")
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        try:
            response = session.get("https://wr-meta.com/items", timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Rabadon's in the page content
            rabadon_elements = soup.find_all(string=re.compile(r"Rabadon", re.I))
            
            if rabadon_elements:
                print(f"Found {len(rabadon_elements)} mentions of Rabadon")
                
                for elem in rabadon_elements:
                    print(f"\nFound mention: {elem}")
                    
                    # Look at parent elements
                    parent = elem.parent
                    if parent:
                        container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                        if container:
                            print("Container text:")
                            container_text = container.get_text()
                            print(container_text[:500] + "..." if len(container_text) > 500 else container_text)
                            
                            # Extract key information
                            cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', container_text, re.I)
                            if cost_match:
                                print(f"Cost: {cost_match.group(1)}")
                            
                            ap_match = re.search(r'(\+?\d+)\s*(?:Ability Power|AP)', container_text, re.I)
                            if ap_match:
                                print(f"Ability Power: {ap_match.group(1)}")
                            
                            passive_match = re.search(r'(?:Passive|PASSIVE|Overkill)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
                            if passive_match:
                                print(f"Passive: {passive_match.group(1).strip()}")
            else:
                print("No mentions of Rabadon found on the page")
        
        except Exception as e:
            print(f"Error in direct approach: {e}")

def scrape_multiple_items():
    """Scrape multiple important items"""
    items_to_scrape = [
        "Rabadon's Deathcap",
        "Infinity Edge",
        "Trinity Force",
        "Guardian Angel",
        "Duskblade of Draktharr"
    ]
    
    scraper = RealTimeItemScraper()
    
    for item_name in items_to_scrape:
        print(f"\nScraping {item_name}...")
        item_data = scraper.scrape_specific_item(item_name)
        
        if item_data:
            print(f"Successfully scraped {item_name}")
            print(f"Cost: {item_data['cost']}")
            print(f"Stats: {', '.join(f'{k}: {v['value']}' for k, v in item_data['stats'].items())}")
        else:
            print(f"Failed to scrape {item_name}")
        
        # Rate limiting
        time.sleep(1)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape latest updates for Wild Rift items')
    parser.add_argument('--rabadon', action='store_true', help='Scrape Rabadon\'s Deathcap')
    parser.add_argument('--multiple', action='store_true', help='Scrape multiple important items')
    
    args = parser.parse_args()
    
    if args.rabadon:
        scrape_rabadon()
    elif args.multiple:
        scrape_multiple_items()
    else:
        print("Please specify an action: --rabadon or --multiple")
        # Default to Rabadon's
        scrape_rabadon()

if __name__ == "__main__":
    main()