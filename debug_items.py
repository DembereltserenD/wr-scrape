#!/usr/bin/env python3
"""
Debug script to check what items are found under specific headers
"""

import requests
import re
from bs4 import BeautifulSoup

def debug_items():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find "Key items" header
    print("\n=== LOOKING FOR 'Key items' HEADER ===")
    key_items_headers = []
    for tag in soup.find_all(['h2','h3','h4','h5']):
        text = tag.get_text(strip=True)
        if 'key items' in text.lower():
            key_items_headers.append(tag)
            print(f"Found: {tag.name} - '{text}'")
    
    if key_items_headers:
        print(f"\n=== EXAMINING FIRST 'Key items' SECTION ===")
        header = key_items_headers[0]
        print(f"Header: {header}")
        
        print("\n--- Next siblings ---")
        for i, sib in enumerate(header.find_next_siblings()):
            if sib.name in ('h2','h3','h4','h5'):
                print(f"Sibling {i}: HEADER {sib.name} - '{sib.get_text(strip=True)}' - STOPPING")
                break
            
            print(f"Sibling {i}: {sib.name}")
            
            # Look for images in this sibling
            images = sib.find_all('img', alt=True) if hasattr(sib, 'find_all') else []
            if images:
                print(f"  Found {len(images)} images:")
                for img in images[:5]:  # Show first 5
                    alt = img.get('alt', '').strip()
                    print(f"    - '{alt}'")
            
            if i >= 10:  # Limit to first 10 siblings
                print("  ... (stopping after 10 siblings)")
                break
    
    # Also check "Situational items"
    print("\n=== LOOKING FOR 'Situational items' HEADER ===")
    sit_headers = []
    for tag in soup.find_all(['h2','h3','h4','h5']):
        text = tag.get_text(strip=True)
        if text == 'Situational items':
            sit_headers.append(tag)
            print(f"Found: {tag.name} - '{text}'")
    
    if sit_headers:
        print(f"\n=== EXAMINING FIRST 'Situational items' SECTION ===")
        header = sit_headers[0]
        
        print("\n--- Next siblings ---")
        for i, sib in enumerate(header.find_next_siblings()):
            if sib.name in ('h2','h3','h4','h5'):
                print(f"Sibling {i}: HEADER {sib.name} - '{sib.get_text(strip=True)}' - STOPPING")
                break
            
            print(f"Sibling {i}: {sib.name}")
            
            # Look for images in this sibling
            images = sib.find_all('img', alt=True) if hasattr(sib, 'find_all') else []
            if images:
                print(f"  Found {len(images)} images:")
                for img in images[:10]:  # Show first 10
                    alt = img.get('alt', '').strip()
                    print(f"    - '{alt}'")
            
            if i >= 5:  # Limit to first 5 siblings
                print("  ... (stopping after 5 siblings)")
                break

if __name__ == "__main__":
    debug_items()
