#!/usr/bin/env python3
"""
Debug script to test exact header matching and item extraction
"""

import requests
import re
from bs4 import BeautifulSoup

def test_is_item_image(img, alt_text):
    """Test item detection"""
    if not alt_text or len(alt_text) < 3:
        return False
    
    # Skip ability/champion images and stat icons
    skip_keywords = [
        'ability', 'skill', 'passive', 'ultimate', 'champion', 'rune', 'spell',
        'attackdamage', 'heal', 'healthregeneration', 'attackspeed', 'mana', 
        'mpreg', 'movementspeed', 'armor', 'magicresistance', 'criticalstrike',
        'energy', 'cooldownreduction', 'perlevel', 'abilitypower'
    ]
    if any(skip in alt_text.lower() for skip in skip_keywords):
        return False
    
    # Skip empty alt text
    if not alt_text.strip():
        return False
    
    # Check if it looks like an item
    src = img.get('src', '')
    data_src = img.get('data-src', '')
    
    # Look for item indicators in the image path or alt text
    item_indicators = [
        'item', 'wild rift', 'wr', 'boots', 'sword', 'staff', 'armor', 'shield',
        'blade', 'enchant', 'treads', 'steelcaps', 'cleaver', 'eclipse', 'force'
    ]
    
    # If it contains obvious item indicators, it's an item
    if any(indicator in alt_text.lower() or 
           indicator in src.lower() or 
           indicator in data_src.lower() 
           for indicator in item_indicators):
        return True
    
    # If it's a reasonable length name without obvious non-item keywords, it's probably an item
    if len(alt_text) <= 50 and alt_text.strip():
        # Additional check for common non-item patterns
        non_item_patterns = ['video', 'image', 'icon', 'logo', 'banner', 'guide']
        if not any(pattern in alt_text.lower() for pattern in non_item_patterns):
            return True
    
    return False

def clean_item_name(alt_text):
    """Clean item names"""
    item_name = alt_text.strip()
    
    # Strip common vendor prefixes (Lol:, Wild Rift, WR, HD, ITEM)
    item_name = re.sub(r'^(?:lol[:\s]*|wild rift[:\s]*|wr[:\s]*|hd[:\s]*|item[:\s]*)', '', item_name, flags=re.IGNORECASE)
    item_name = re.sub(r'\b(wild\s+rift|wr|hd|item)\b', '', item_name, flags=re.IGNORECASE)
    # Remove leading colons and spaces
    item_name = re.sub(r'^[:\s]+', '', item_name)
    item_name = re.sub(r'\s*(icon|image|img)\s*', '', item_name, flags=re.IGNORECASE)
    
    return item_name.strip()

def collect_items_under_headers(soup, header_keywords, max_items=6):
    """Test the header collection method"""
    headers = []
    # compile one big regex for this category
    pat = re.compile('|'.join(header_keywords), re.IGNORECASE)
    for tag in soup.find_all(['h2','h3','h4','h5']):
        if pat.search(tag.get_text(strip=True) or ''):
            headers.append(tag)
    
    print(f"  Found {len(headers)} matching headers: {[h.get_text(strip=True) for h in headers]}")
    
    items = []
    for header in headers:
        print(f"  Processing header: {header.get_text(strip=True)}")
        for i, sib in enumerate(header.find_next_siblings()):
            # stop at next same-level or higher heading
            if sib.name in ('h2','h3','h4','h5'):
                print(f"    Sibling {i}: HEADER {sib.name} - stopping")
                break
            
            # collect any img tags inside this sib
            images = sib.find_all('img', alt=True) if hasattr(sib, 'find_all') else []
            if images:
                print(f"    Sibling {i}: Found {len(images)} images")
                for img in images[:5]:  # Show first 5
                    alt = img['alt'].strip()
                    if test_is_item_image(img, alt):
                        clean = clean_item_name(alt)
                        if clean and clean not in items:
                            items.append(clean)
                            print(f"      Added item: '{clean}' (from '{alt}')")
                            if len(items) >= max_items:
                                return items
        # if we found any items under this header, no need to try further headers
        if items:
            break
    return items

def debug_header_matching():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("\n=== TESTING HEADER PATTERNS ===")
    section_map = {
        'starting_items':   ['Start', 'Early', 'Key items'],
        'core_items':       ['Core', 'Main', 'Essential', 'Key items'],
        'boots':            ['Boots', 'Boots/Enchant', 'Footwear'],
        'situational_items':['Situational items', 'Optional', 'Counter'],
        'example_build':    ['Example build', 'Full build', 'Complete build']
    }
    
    for category, patterns in section_map.items():
        print(f"\n--- {category} ---")
        print(f"Patterns: {patterns}")
        items = collect_items_under_headers(soup, patterns)
        print(f"Final items: {items}")

if __name__ == "__main__":
    debug_header_matching()
