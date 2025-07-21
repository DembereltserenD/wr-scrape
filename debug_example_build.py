#!/usr/bin/env python3
"""
Debug script to test example build extraction
"""

import requests
import re
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

def debug_example_build():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scraper = WRMetaScraper()
    
    print("\n=== LOOKING FOR EXAMPLE BUILD HEADERS ===")
    
    # Look for bildtitle2 headers
    bildtitle2_headers = soup.find_all('div', class_='bildtitle2')
    print(f"Found {len(bildtitle2_headers)} bildtitle2 headers:")
    for i, header in enumerate(bildtitle2_headers):
        text = header.get_text().strip()
        print(f"  {i+1}. '{text}'")
        
        if 'example build' in text.lower():
            print(f"    -> This is the Example build header!")
            
            # Check next sibling
            next_sibling = header.find_next_sibling()
            if next_sibling:
                print(f"    -> Next sibling: {next_sibling.name} with class {next_sibling.get('class', [])}")
                
                # Look for ico-holder3 containers
                item_containers = next_sibling.find_all('div', class_='ico-holder3')
                print(f"    -> Found {len(item_containers)} ico-holder3 containers")
                
                for j, container in enumerate(item_containers):
                    span_elem = container.find('span')
                    img_elem = container.find('img', class_='itemimage')
                    
                    span_text = span_elem.get_text().strip() if span_elem else "No span"
                    img_alt = img_elem.get('alt', '').strip() if img_elem else "No img"
                    
                    print(f"      Container {j+1}: span='{span_text}', img_alt='{img_alt}'")
    
    print("\n=== TESTING ALTERNATIVE EXTRACTION ===")
    example_items = scraper._extract_example_build_alternative(soup)
    print(f"Alternative method found {len(example_items)} items:")
    for item in example_items:
        print(f"  - {item}")
    
    print("\n=== TESTING REGULAR HEADER EXTRACTION ===")
    regular_items = scraper._collect_items_under_headers(soup, ['Example build'])
    print(f"Regular method found {len(regular_items)} items:")
    for item in regular_items:
        print(f"  - {item}")
    
    print("\n=== VALIDATION ===")
    if set(example_items) == set(regular_items):
        print("SUCCESS: Both methods return the same items!")
    else:
        print("MISMATCH: Methods return different items")
        print(f"Alternative only: {set(example_items) - set(regular_items)}")
        print(f"Regular only: {set(regular_items) - set(example_items)}")
    
    print("\n=== TESTING FULL BUILD EXTRACTION ===")
    full_build = scraper._extract_structured_build(soup)
    print(f"Full structured build extraction:")
    for category, items in full_build.items():
        if items:
            print(f"  {category}: {items}")

if __name__ == "__main__":
    debug_example_build()
