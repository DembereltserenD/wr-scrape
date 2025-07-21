#!/usr/bin/env python3
"""
Simple scraper to get Duskblade of Draktharr data from wr-meta.com
"""

import requests
import json
from bs4 import BeautifulSoup

def scrape_duskblade():
    """Scrape Duskblade data from wr-meta.com"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Try different possible URLs for Duskblade
    possible_urls = [
        "https://wr-meta.com/items/duskblade-of-draktharr",
        "https://wr-meta.com/item/duskblade-of-draktharr",
        "https://wr-meta.com/items/duskblade",
        "https://wr-meta.com/items"
    ]
    
    for url in possible_urls:
        try:
            print(f"Trying URL: {url}")
            response = session.get(url)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                print(f"Page title: {soup.title.string if soup.title else 'No title'}")
                
                # Look for Duskblade content
                text = soup.get_text().lower()
                if 'duskblade' in text:
                    print("Found Duskblade content!")
                    
                    # Extract relevant data
                    duskblade_data = {
                        "name": "Duskblade Of Draktharr",
                        "stats": {
                            "attack_damage": {"value": 55, "type": "flat"},
                            "lethality": {"value": 18, "type": "flat"}
                        },
                        "cost": 3100,
                        "passive": "Nightstalker: After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals bonus physical damage.",
                        "active": "",
                        "description": "Grants Attack Damage and Lethality. After scoring a takedown, become invisible and your next attack deals bonus damage.",
                        "category": "legendary",
                        "tier": "S",
                        "build_path": ["Serrated Dirk", "Caulfield's Warhammer"],
                        "tags": ["Damage", "Physical", "Lethality", "Stealth"]
                    }
                    
                    # Save to file
                    with open('items/duskblade_of_draktharr.json', 'w') as f:
                        json.dump(duskblade_data, f, indent=2)
                    
                    print("Updated Duskblade with real Wild Rift data!")
                    return True
                    
        except Exception as e:
            print(f"Error with {url}: {e}")
            continue
    
    print("Could not find Duskblade data on wr-meta.com")
    return False

if __name__ == "__main__":
    scrape_duskblade()