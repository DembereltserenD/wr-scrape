#!/usr/bin/env python3
"""
Test script to validate example build extraction works correctly across different champions
"""

import requests
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

def test_champion_example_build(champion_url, champion_name):
    """Test example build extraction for a specific champion"""
    print(f"\n=== Testing {champion_name} ===")
    print(f"URL: {champion_url}")
    
    try:
        response = requests.get(champion_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        scraper = WRMetaScraper()
        
        # Test alternative method
        alternative_items = scraper._extract_example_build_alternative(soup)
        print(f"Alternative method found {len(alternative_items)} items:")
        for item in alternative_items:
            print(f"  - {item}")
        
        # Test regular method
        regular_items = scraper._collect_items_under_headers(soup, ['Example build'])
        print(f"Regular method found {len(regular_items)} items:")
        for item in regular_items:
            print(f"  - {item}")
        
        # Test full structured build
        structured_build = scraper._extract_structured_build(soup)
        example_build = structured_build.get('example_build', [])
        print(f"Structured build example: {example_build}")
        
        # Validation
        if alternative_items and len(alternative_items) > 0:
            print(f"SUCCESS: Found {len(alternative_items)} example build items")
            return True
        else:
            print("FAILED: No example build items found")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Test multiple champions to ensure the fix works broadly"""
    test_champions = [
        ("https://wr-meta.com/528-ambessa.html", "Ambessa"),
        ("https://wr-meta.com/332-aatrox.html", "Aatrox"),
        ("https://wr-meta.com/103-ahri.html", "Ahri"),
        ("https://wr-meta.com/84-akali.html", "Akali"),
        ("https://wr-meta.com/166-akshan.html", "Akshan")
    ]
    
    print("Testing Example Build Extraction Fix")
    print("=" * 50)
    
    success_count = 0
    total_count = len(test_champions)
    
    for url, name in test_champions:
        if test_champion_example_build(url, name):
            success_count += 1
    
    print(f"\n" + "=" * 50)
    print(f"SUMMARY: {success_count}/{total_count} champions passed")
    
    if success_count == total_count:
        print("ALL TESTS PASSED! Example build extraction is working correctly.")
    else:
        print(f"WARNING: {total_count - success_count} champions failed. May need additional fixes.")

if __name__ == "__main__":
    main()
