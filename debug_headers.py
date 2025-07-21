#!/usr/bin/env python3
"""
Debug script to check what headers are found on the Ambessa page
"""

import requests
import re
from bs4 import BeautifulSoup

def debug_headers():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("\n=== ALL HEADERS (h2-h5) ===")
    for tag in soup.find_all(['h2','h3','h4','h5']):
        text = tag.get_text(strip=True)
        print(f"{tag.name}: '{text}'")
    
    print("\n=== TESTING HEADER PATTERNS ===")
    section_map = {
        'starting_items':   ['^Start', 'Early', 'Key items'],
        'core_items':       ['Core', 'Main', 'Essential'],
        'boots':            ['Boots', 'Boots/Enchant', 'Footwear'],
        'situational_items':['Situational', 'Optional', 'Counter'],
        'example_build':    ['Example build', 'Full build', 'Complete build']
    }
    
    for category, patterns in section_map.items():
        print(f"\n--- {category} ---")
        pat = re.compile('|'.join(patterns), re.IGNORECASE)
        found_headers = []
        for tag in soup.find_all(['h2','h3','h4','h5']):
            text = tag.get_text(strip=True)
            if pat.search(text):
                found_headers.append(f"{tag.name}: '{text}'")
        
        if found_headers:
            print(f"Found headers: {found_headers}")
        else:
            print("No matching headers found")
    
    print("\n=== ALL IMAGES WITH ALT TEXT ===")
    images = soup.find_all('img', alt=True)
    print(f"Total images with alt text: {len(images)}")
    
    for i, img in enumerate(images[:20]):  # Show first 20
        alt = img.get('alt', '').strip()
        print(f"{i+1}: '{alt}'")

if __name__ == "__main__":
    debug_headers()
