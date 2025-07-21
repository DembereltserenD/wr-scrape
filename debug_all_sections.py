#!/usr/bin/env python3
"""
Debug script to test all build section extractions
"""

import requests
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

def debug_all_sections():
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
        
        # Also test what the first header with this name actually contains
        headers = soup.find_all(['h2','h3','h4','h5', 'div'])
        for header in headers:
            if any(keyword.lower() in header.get_text().strip().lower() for keyword in keywords):
                print(f"   First {section_name} header found: '{header.get_text().strip()}'")
                next_sib = header.find_next_sibling()
                if next_sib:
                    containers = next_sib.find_all('div', class_='ico-holder3')
                    print(f"   Next sibling has {len(containers)} ico-holder3 containers")
                    for i, container in enumerate(containers):
                        span = container.find('span')
                        if span:
                            print(f"     Container {i+1}: {span.get_text().strip()}")
                break
    
    print("\n=== LOOKING AT ALL BILDTITLE2 HEADERS AND THEIR CONTENT ===")
    bildtitle2_headers = soup.find_all('div', class_='bildtitle2')
    
    for i, header in enumerate(bildtitle2_headers):
        header_text = header.get_text().strip()
        print(f"\n{i+1}. Header: '{header_text}'")
        
        # Look at the next sibling content
        next_sibling = header.find_next_sibling()
        if next_sibling:
            print(f"   Next sibling: {next_sibling.name} with classes {next_sibling.get('class', [])}")
            
            # Look for ico-holder3 containers
            containers = next_sibling.find_all('div', class_='ico-holder3')
            print(f"   Found {len(containers)} ico-holder3 containers:")
            
            for j, container in enumerate(containers):
                span_elem = container.find('span')
                img_elem = container.find('img')
                
                span_text = span_elem.get_text().strip() if span_elem else "No span"
                img_alt = img_elem.get('alt', '').strip() if img_elem else "No img"
                img_src = img_elem.get('src', '') if img_elem else "No src"
                
                print(f"     Container {j+1}: span='{span_text}', img_alt='{img_alt}'")
                if 'itemimage' in img_elem.get('class', []) if img_elem else False:
                    print(f"       -> This is an item image")
                
            # Also look for regular img tags
            regular_imgs = next_sibling.find_all('img')
            item_imgs = [img for img in regular_imgs if scraper._is_item_image(img, img.get('alt', ''))]
            if item_imgs:
                print(f"   Found {len(item_imgs)} regular item images:")
                for img in item_imgs:
                    print(f"     - {img.get('alt', 'No alt')}")

if __name__ == "__main__":
    debug_all_sections()
