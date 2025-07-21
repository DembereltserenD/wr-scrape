#!/usr/bin/env python3
"""
Simple debug to understand header matching
"""

import requests
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper
import re

def debug_simple():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scraper = WRMetaScraper()
    
    # Test Start section specifically
    print("\n=== DEBUGGING START SECTION ===")
    
    # Find headers manually
    headers = []
    pat = re.compile('Start', re.IGNORECASE)
    
    for tag in soup.find_all(['h2','h3','h4','h5', 'div']):
        if pat.search(tag.get_text(strip=True) or ''):
            headers.append(tag)
    
    print(f"Found {len(headers)} headers matching 'Start':")
    
    for i, header in enumerate(headers):
        print(f"\nHeader {i+1}: '{header.get_text().strip()[:50]}...'")
        print(f"  Tag: {header.name}, Classes: {header.get('class', [])}")
        
        # Look at next sibling
        next_sib = header.find_next_sibling()
        if next_sib:
            print(f"  Next sibling: {next_sib.name}, Classes: {next_sib.get('class', [])}")
            
            # Look for ico-holder3
            containers = next_sib.find_all('div', class_='ico-holder3')
            print(f"  Found {len(containers)} ico-holder3 containers")
            
            for j, container in enumerate(containers):
                span = container.find('span')
                if span:
                    print(f"    Container {j+1}: '{span.get_text().strip()}'")
            
            # Look for regular images
            imgs = next_sib.find_all('img')
            item_imgs = []
            for img in imgs:
                alt = img.get('alt', '').strip()
                if scraper._is_item_image(img, alt):
                    item_imgs.append(alt)
            print(f"  Found {len(item_imgs)} item images: {item_imgs}")
        
        # Test the method on just this header
        items = []
        if next_sib:
            # Simulate what _collect_items_under_headers does
            for container in next_sib.find_all('div', class_='ico-holder3'):
                span_elem = container.find('span')
                if span_elem:
                    item_name = span_elem.get_text().strip()
                    if item_name:
                        clean = scraper._clean_item_name(item_name)
                        if clean and clean not in items:
                            items.append(clean)
            
            for img in next_sib.find_all('img'):
                alt = img.get('alt', '').strip()
                if scraper._is_item_image(img, alt):
                    clean = scraper._clean_item_name(alt, img)
                    if clean and clean not in items:
                        items.append(clean)
        
        print(f"  Items extracted from this header: {items}")

if __name__ == "__main__":
    debug_simple()
