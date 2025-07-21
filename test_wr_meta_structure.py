#!/usr/bin/env python3
"""
Test script to understand wr-meta.com structure for items
"""

import requests
from bs4 import BeautifulSoup
import json

def test_item_page_structure():
    """Test the structure of wr-meta.com item pages"""
    
    # Test with hullbreaker
    test_urls = [
        "https://wr-meta.com/items/hullbreaker",
        "https://wr-meta.com/item/hullbreaker",
        "https://wr-meta.com/items/",
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for url in test_urls:
        print(f"\n=== Testing URL: {url} ===")
        try:
            response = session.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Print page title
                title = soup.find('title')
                if title:
                    print(f"Page Title: {title.get_text()}")
                
                # Look for common item-related elements
                print("\n--- Looking for item elements ---")
                
                # Check for item name/title
                item_titles = soup.find_all(['h1', 'h2', 'h3'], class_=lambda x: x and ('item' in x.lower() or 'title' in x.lower()))
                if item_titles:
                    print("Item titles found:")
                    for title in item_titles[:3]:
                        print(f"  - {title.get_text(strip=True)}")
                
                # Check for stats sections
                stats_sections = soup.find_all(['div', 'section'], class_=lambda x: x and 'stat' in x.lower())
                if stats_sections:
                    print("Stats sections found:")
                    for section in stats_sections[:3]:
                        print(f"  - Class: {section.get('class')}")
                        print(f"    Text: {section.get_text(strip=True)[:100]}...")
                
                # Check for description/passive sections
                desc_sections = soup.find_all(['div', 'p'], class_=lambda x: x and ('desc' in x.lower() or 'passive' in x.lower()))
                if desc_sections:
                    print("Description/Passive sections found:")
                    for section in desc_sections[:3]:
                        print(f"  - Class: {section.get('class')}")
                        print(f"    Text: {section.get_text(strip=True)[:100]}...")
                
                # Look for any divs with item-related classes
                item_divs = soup.find_all('div', class_=lambda x: x and any(keyword in x.lower() for keyword in ['item', 'build', 'recipe', 'component']))
                if item_divs:
                    print("Item-related divs found:")
                    for div in item_divs[:5]:
                        print(f"  - Class: {div.get('class')}")
                
                # Print first few div classes to understand structure
                print("\n--- First 10 div classes ---")
                divs = soup.find_all('div', class_=True)[:10]
                for div in divs:
                    classes = div.get('class', [])
                    if classes:
                        print(f"  - {' '.join(classes)}")
                
                break  # If we get a successful response, stop testing other URLs
                
        except Exception as e:
            print(f"Error accessing {url}: {e}")
    
    # Also test the main items page to see the structure
    print(f"\n=== Testing main items page ===")
    try:
        response = session.get("https://wr-meta.com/items", timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for item links
            item_links = soup.find_all('a', href=lambda x: x and 'item' in x.lower())
            if item_links:
                print("Item links found:")
                for link in item_links[:10]:
                    href = link.get('href')
                    text = link.get_text(strip=True)
                    print(f"  - {text}: {href}")
    except Exception as e:
        print(f"Error accessing items page: {e}")

if __name__ == "__main__":
    test_item_page_structure()