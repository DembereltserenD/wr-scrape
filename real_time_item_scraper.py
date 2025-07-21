#!/usr/bin/env python3
"""
Real-Time Item Scraper for Wild Rift
Scrapes accurate, up-to-date item data directly from WR-META.com
"""

import requests
import json
import re
import time
import os
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

class RealTimeItemScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://wr-meta.com"
        self.items_url = f"{self.base_url}/items"
        self.output_dir = Path("items")
        self.output_dir.mkdir(exist_ok=True)
        
    def scrape_all_items(self):
        """Scrape all items from the items page"""
        print(f"Fetching items from {self.items_url}")
        
        try:
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all item containers
            item_containers = soup.select('.item-container, .item-box, .item-card, .item')
            
            if not item_containers:
                # Try alternative selectors if the above doesn't work
                item_containers = soup.find_all(['div', 'section', 'article'], 
                                              class_=lambda c: c and any(x in c for x in ['item', 'card', 'box']))
            
            if not item_containers:
                # Last resort: look for elements with item-like content
                print("Using fallback item detection...")
                item_containers = []
                
                # Look for elements containing gold cost and stats
                potential_items = soup.find_all(string=re.compile(r'\d{3,4}\s*(?:gold|cost)', re.I))
                for text_elem in potential_items:
                    parent = text_elem.parent
                    if parent:
                        container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                        if container and container not in item_containers:
                            item_containers.append(container)
            
            print(f"Found {len(item_containers)} potential item containers")
            
            items_scraped = 0
            for container in item_containers:
                item_data = self.extract_item_data(container)
                if item_data and item_data.get('name'):
                    self.save_item_data(item_data)
                    items_scraped += 1
                    
                    # Rate limiting
                    time.sleep(0.5)
            
            print(f"Successfully scraped {items_scraped} items")
            return items_scraped
            
        except Exception as e:
            print(f"Error scraping items: {e}")
            return 0
    
    def extract_item_data(self, container):
        """Extract item data from a container element"""
        try:
            # Get all text content
            container_text = container.get_text()
            
            # Try to find item name
            name_elem = container.find(['h2', 'h3', 'h4', 'strong', 'b'])
            item_name = name_elem.get_text().strip() if name_elem else None
            
            # If no name found, try to extract from text
            if not item_name:
                # Look for capitalized words that might be an item name
                name_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})', container_text)
                if name_match:
                    item_name = name_match.group(1)
            
            if not item_name:
                return None
                
            # Clean up item name
            item_name = re.sub(r'^[:\s]+', '', item_name)  # Remove leading colons or spaces
            item_name = re.sub(r'^\w+:\s*', '', item_name)  # Remove prefixes like "Lol:"
            item_name = item_name.strip()
            
            # Extract stats
            stats = {}
            stat_patterns = {
                'ability_power': r'(\+?\d+)\s*(?:Ability Power|AP)',
                'attack_damage': r'(\+?\d+)\s*(?:Attack Damage|AD)',
                'health': r'(\+?\d+)\s*Health',
                'mana': r'(\+?\d+)\s*Mana',
                'armor': r'(\+?\d+)\s*Armor',
                'magic_resistance': r'(\+?\d+)\s*(?:Magic Resist|MR)',
                'attack_speed': r'(\+?\d+%?)\s*Attack Speed',
                'critical_strike': r'(\+?\d+%?)\s*(?:Critical Strike|Crit)',
                'magic_penetration': r'(\+?\d+%?)\s*(?:Magic Penetration|Magic Pen)',
                'movement_speed': r'(\+?\d+%?)\s*Movement Speed',
                'life_steal': r'(\+?\d+%?)\s*Life Steal',
                'ability_haste': r'(\+?\d+)\s*(?:Ability Haste|AH)',
            }
            
            for stat_name, pattern in stat_patterns.items():
                match = re.search(pattern, container_text, re.I)
                if match:
                    value = match.group(1).replace('+', '')
                    if '%' in value:
                        value = int(value.replace('%', ''))
                        stats[stat_name] = {'value': value, 'type': 'percentage'}
                    else:
                        stats[stat_name] = {'value': int(value), 'type': 'flat'}
            
            # Extract cost
            cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', container_text, re.I)
            cost = int(cost_match.group(1)) if cost_match else 0
            
            # Extract passive/active effects
            passive = ""
            active = ""
            
            # Look for passive effect
            passive_patterns = [
                r'(?:Passive|PASSIVE)[:\s]*([^.]+(?:\.[^.]*)*)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)[:\s]*([^.]+(?:\.[^.]*)*)',  # Named passives like "Overkill: ..."
            ]
            
            for pattern in passive_patterns:
                match = re.search(pattern, container_text, re.I)
                if match:
                    if len(match.groups()) > 1:
                        passive = f"{match.group(1)}: {match.group(2)}".strip()
                    else:
                        passive = match.group(1).strip()
                    break
            
            # Look for active effect
            active_match = re.search(r'(?:Active|ACTIVE)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
            if active_match:
                active = active_match.group(1).strip()
            
            # Extract description/tips
            description = ""
            tips = []
            
            # Look for description
            desc_patterns = [
                rf'{re.escape(item_name)}\s*(?:TIPS?|Description)[:\s]*([^.]+(?:\.[^.]*)*)',
                r'(?:Description|Details)[:\s]*([^.]+(?:\.[^.]*)*)',
            ]
            
            for pattern in desc_patterns:
                match = re.search(pattern, container_text, re.I)
                if match:
                    description = match.group(1).strip()
                    break
            
            # Look for tips
            tips_section = container.find(string=re.compile(r'tips', re.I))
            if tips_section:
                tips_container = tips_section.parent
                if tips_container:
                    # Look for list items
                    tip_items = tips_container.find_all('li')
                    if tip_items:
                        tips = [item.get_text().strip() for item in tip_items]
                    else:
                        # Try to split by periods or line breaks
                        tips_text = tips_container.get_text()
                        tips_text = re.sub(r'(?:TIPS?|Tips)[:\s]*', '', tips_text, flags=re.I)
                        tip_candidates = re.split(r'(?:\.\s+|\n+)', tips_text)
                        tips = [tip.strip() for tip in tip_candidates if tip.strip()]
            
            # Determine category
            category = "legendary"  # Default
            if any(word in item_name.lower() for word in ['boots', 'treads', 'greaves']):
                category = "boots"
            elif cost < 1000:
                category = "basic"
            elif "enchant" in item_name.lower():
                category = "enchant"
            
            # Determine tier
            tier = "A"  # Default
            if cost > 3000:
                tier = "S"
            elif cost < 1000:
                tier = "B"
            
            # Create item data structure
            item_data = {
                "name": item_name,
                "stats": stats,
                "cost": cost,
                "passive": passive,
                "active": active,
                "description": description,
                "category": category,
                "tier": tier,
                "tips": tips[:5] if tips else []  # Limit to 5 tips
            }
            
            return item_data
            
        except Exception as e:
            print(f"Error extracting item data: {e}")
            return None
    
    def save_item_data(self, item_data):
        """Save item data to a JSON file"""
        item_name = item_data['name']
        filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
        filepath = self.output_dir / filename
        
        print(f"Saving {item_name} to {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item_data, f, indent=2, ensure_ascii=False)
    
    def scrape_specific_item(self, item_name):
        """Scrape a specific item by name"""
        print(f"Scraping specific item: {item_name}")
        
        try:
            # First try to find on the main items page
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the item by name
            item_found = False
            
            # Try different text matching approaches
            for selector in [
                # Look for exact text match
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and tag.get_text().strip() == item_name,
                # Look for contains text match
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and item_name in tag.get_text(),
                # Case insensitive contains
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and item_name.lower() in tag.get_text().lower()
            ]:
                elements = soup.find_all(selector)
                
                for elem in elements:
                    container = elem.parent
                    while container and container.name != 'body':
                        if container.name in ['div', 'section', 'article', 'tr', 'td']:
                            item_data = self.extract_item_data(container)
                            if item_data and item_data.get('name'):
                                self.save_item_data(item_data)
                                print(f"Successfully scraped {item_name}")
                                return item_data
                        container = container.parent
            
            print(f"Could not find {item_name} on the items page")
            return None
            
        except Exception as e:
            print(f"Error scraping specific item {item_name}: {e}")
            return None
    
    def scrape_item_from_url(self, item_url):
        """Scrape item data from a specific URL"""
        print(f"Scraping item from URL: {item_url}")
        
        try:
            response = self.session.get(item_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for main item container
            main_container = soup.find(['div', 'section', 'article'], 
                                     class_=lambda c: c and any(x in c for x in ['item-details', 'item-container', 'main-content']))
            
            if not main_container:
                main_container = soup.find('body')  # Fallback to body
            
            item_data = self.extract_item_data(main_container)
            
            if item_data and item_data.get('name'):
                self.save_item_data(item_data)
                print(f"Successfully scraped item from {item_url}")
                return item_data
            
            print(f"Could not extract item data from {item_url}")
            return None
            
        except Exception as e:
            print(f"Error scraping item from URL {item_url}: {e}")
            return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape real-time item data from WR-META.com')
    parser.add_argument('--all', action='store_true', help='Scrape all items')
    parser.add_argument('--item', type=str, help='Scrape a specific item by name')
    parser.add_argument('--url', type=str, help='Scrape an item from a specific URL')
    
    args = parser.parse_args()
    
    scraper = RealTimeItemScraper()
    
    if args.all:
        scraper.scrape_all_items()
    elif args.item:
        scraper.scrape_specific_item(args.item)
    elif args.url:
        scraper.scrape_item_from_url(args.url)
    else:
        print("Please specify an action: --all, --item NAME, or --url URL")

if __name__ == "__main__":
    main()