#!/usr/bin/env python3
"""
Test the _is_item_image method
"""

import requests
import re
from bs4 import BeautifulSoup

def test_is_item_image(img, alt_text):
    """Check if an image represents an item - copied from scraper"""
    if not alt_text or len(alt_text) < 3:
        return False
    
    # Skip ability/champion images
    skip_keywords = ['ability', 'skill', 'passive', 'ultimate', 'champion', 'rune', 'spell']
    if any(skip in alt_text.lower() for skip in skip_keywords):
        return False
    
    # Check if it looks like an item
    # This is where the method might be incomplete - let me add basic logic
    item_indicators = ['sword', 'blade', 'armor', 'boots', 'enchant', 'wild rift']
    if any(indicator in alt_text.lower() for indicator in item_indicators):
        return True
    
    # If it's a short name without obvious non-item keywords, it's probably an item
    if len(alt_text) < 30 and not any(skip in alt_text.lower() for skip in ['attackdamage', 'heal', 'mana', 'energy']):
        return True
    
    return False

def test_items():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find "Key items" header
    key_items_headers = []
    for tag in soup.find_all(['h2','h3','h4','h5']):
        text = tag.get_text(strip=True)
        if 'key items' in text.lower():
            key_items_headers.append(tag)
    
    if key_items_headers:
        print(f"\n=== TESTING ITEM DETECTION ===")
        header = key_items_headers[0]
        
        for i, sib in enumerate(header.find_next_siblings()):
            if sib.name in ('h2','h3','h4','h5'):
                break
            
            images = sib.find_all('img', alt=True) if hasattr(sib, 'find_all') else []
            if images:
                print(f"\nSibling {i} - Testing {len(images)} images:")
                for img in images[:10]:  # Test first 10
                    alt = img.get('alt', '').strip()
                    is_item = test_is_item_image(img, alt)
                    print(f"  '{alt}' -> {is_item}")
            
            if i >= 2:  # Test first 3 siblings
                break

if __name__ == "__main__":
    test_items()
