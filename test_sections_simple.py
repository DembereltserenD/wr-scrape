#!/usr/bin/env python3
"""
Simple test for all sections
"""

import requests
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

def test_sections():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scraper = WRMetaScraper()
    
    # Test each section individually
    sections_to_test = {
        'Start': ['Start'],
        'Core': ['Core'],
        'Boots': ['Boots/Enchant'],
        'Situational': ['Situational'],
        'Example': ['Example build']
    }
    
    print("\n=== TESTING INDIVIDUAL SECTIONS ===")
    for section_name, keywords in sections_to_test.items():
        print(f"\n--- {section_name} Section ---")
        items = scraper._collect_items_under_headers(soup, keywords)
        print(f"Found {len(items)} items: {items}")

if __name__ == "__main__":
    test_sections()
