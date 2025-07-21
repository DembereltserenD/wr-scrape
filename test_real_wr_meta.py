#!/usr/bin/env python3
"""
Test real wr-meta.com structure to understand how to scrape items properly
"""

import requests
from bs4 import BeautifulSoup
import json
import re

def test_wr_meta_items():
    """Test different ways to access item data on wr-meta.com"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Test different URL patterns
    test_urls = [
        "https://wr-meta.com/items",
        "https://wr-meta.com/items/",
        "https://wr-meta.com/item/hullbreaker",
        "https://wr-meta.com/items/hullbreaker",
        "https://wr-meta.com/equipment",
        "https://wr-meta.com/builds",
    ]
    
    for url in test_urls:
        print(f"\n=== Testing: {url} ===")
        try:
            response = session.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f"Title: {title.get_text()}")
                
                # Look for item-related content
                item_elements = soup.find_all(text=re.compile(r'hullbreaker|infinity|rabadon', re.I))
                if item_elements:
                    print(f"Found {len(item_elements)} item references")
                    for elem in item_elements[:3]:
                        print(f"  - {elem.strip()[:100]}")
                
                # Look for any JSON data
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and ('item' in script.string.lower() or 'hullbreaker' in script.string.lower()):
                        print("Found potential item data in script:")
                        print(script.string[:200] + "...")
                        break
                
                break  # Stop after first successful response
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Test a champion page to see if items are listed there
    print(f"\n=== Testing Champion Page ===")
    try:
        champion_url = "https://wr-meta.com/58-kennen.html"
        response = session.get(champion_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for item names in the page
            item_names = ['hullbreaker', 'infinity edge', 'rabadon', 'trinity force', 'boots']
            found_items = []
            
            for item in item_names:
                if soup.find(text=re.compile(item, re.I)):
                    found_items.append(item)
            
            print(f"Found items on champion page: {found_items}")
            
            # Look for build sections
            build_sections = soup.find_all(['div', 'section'], class_=lambda x: x and 'build' in x.lower())
            print(f"Found {len(build_sections)} build sections")
            
            # Look for item images or links
            item_imgs = soup.find_all('img', src=lambda x: x and 'item' in x.lower())
            print(f"Found {len(item_imgs)} item images")
            
    except Exception as e:
        print(f"Error testing champion page: {e}")

if __name__ == "__main__":
    test_wr_meta_items()