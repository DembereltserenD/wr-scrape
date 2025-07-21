#!/usr/bin/env python3
"""
Test script for the Selenium-enhanced scraper
"""

import json
import sys
from selenium_enhanced_scraper import SeleniumWRMetaScraper

def test_selenium_scraper():
    """Test the Selenium scraper with known multi-lane champions"""
    
    test_champions = [
        {
            'name': 'Kennen',
            'url': 'https://wr-meta.com/58-kennen.html',
            'expected_lanes': ['Solo Baron', 'Mid Lane']
        },
        {
            'name': 'Ahri', 
            'url': 'https://wr-meta.com/1-ahri.html',
            'expected_lanes': ['Mid Lane']
        }
    ]
    
    scraper = SeleniumWRMetaScraper(headless=True)
    
    for champion in test_champions:
        print(f"\n{'='*60}")
        print(f"Testing {champion['name']}")
        print(f"URL: {champion['url']}")
        print(f"Expected lanes: {champion['expected_lanes']}")
        print(f"{'='*60}")
        
        try:
            # Test Selenium scraping
            data = scraper.scrape_champion_data_selenium(champion['url'])
            
            print(f"✅ Successfully scraped {data['champion']['name']}")
            print(f"📍 Detected lanes: {data['champion']['lanes']}")
            
            # Check for lane-specific builds
            if 'lane_specific' in data['builds']:
                lane_builds = data['builds']['lane_specific']
                print(f"🎯 Lane-specific builds found: {list(lane_builds.keys())}")
                
                # Analyze differences between lanes
                if len(lane_builds) > 1:
                    lanes = list(lane_builds.keys())
                    first_lane = lanes[0]
                    second_lane = lanes[1]
                    
                    first_core = set(lane_builds[first_lane].get('core_items', []))
                    second_core = set(lane_builds[second_lane].get('core_items', []))
                    
                    if first_core == second_core:
                        print(f"⚠️  Core items are identical between {first_lane} and {second_lane}")
                    else:
                        print(f"✨ Different core items found:")
                        print(f"   {first_lane}: {list(first_core)[:3]}...")
                        print(f"   {second_lane}: {list(second_core)[:3]}...")
                
            else:
                print(f"📝 Single build extracted (no lane differences)")
            
            # Show core items
            core_items = data['builds'].get('core_items', [])
            print(f"🔧 Core items: {core_items[:3]}...")
            
        except Exception as e:
            print(f"❌ Error testing {champion['name']}: {e}")
    
    print(f"\n{'='*60}")
    print("Test completed!")

def test_specific_champion(champion_url):
    """Test a specific champion URL"""
    scraper = SeleniumWRMetaScraper(headless=True)
    
    try:
        data = scraper.scrape_champion_data_selenium(champion_url)
        
        print(f"Champion: {data['champion']['name']}")
        print(f"Lanes: {data['champion']['lanes']}")
        print(f"Core items: {data['builds'].get('core_items', [])}")
        
        if 'lane_specific' in data['builds']:
            print(f"Lane-specific builds: {list(data['builds']['lane_specific'].keys())}")
            
            # Save detailed results
            filename = f"test_{data['champion']['name'].lower()}_selenium.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Detailed results saved to: {filename}")
        
        return data
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific champion
        champion_url = sys.argv[1]
        test_specific_champion(champion_url)
    else:
        # Run full test suite
        test_selenium_scraper()
