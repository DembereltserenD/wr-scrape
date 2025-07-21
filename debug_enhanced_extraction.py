#!/usr/bin/env python3
"""
Debug script to test the enhanced item extraction
"""

import requests
import re
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

def debug_enhanced_extraction():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scraper = WRMetaScraper()
    
    print("\n=== TESTING ENHANCED _collect_items_under_headers ===")
    
    # Test Key items extraction
    print("\n--- Key items ---")
    key_items = scraper._collect_items_under_headers(soup, ['Key items'])
    print(f"Found {len(key_items)} key items:")
    for item in key_items:
        category = scraper._categorize_item(item)
        print(f"  - '{item}' -> {category}")
    
    # Test Situational items extraction
    print("\n--- Situational items ---")
    situational_items = scraper._collect_items_under_headers(soup, ['Situational items'])
    print(f"Found {len(situational_items)} situational items:")
    for item in situational_items:
        category = scraper._categorize_item(item)
        print(f"  - '{item}' -> {category}")
    
    # Test the full structured build extraction
    print("\n=== TESTING _extract_structured_build ===")
    build = scraper._extract_structured_build(soup)
    
    for category, items in build.items():
        print(f"{category}: {len(items)} items")
        for item in items:
            print(f"  - {item}")

if __name__ == "__main__":
    debug_enhanced_extraction()
