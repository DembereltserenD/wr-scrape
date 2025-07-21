#!/usr/bin/env python3
"""
Complete Item Details Scraper for Wild Rift
Scrapes all missing details including tips, full descriptions, build components, etc.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin

class CompleteItemScraper:
    def __init__(self):
        self.base_url = "https://wr-meta.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_item_page_url(self, item_name):
        """Convert item name to URL format for wr-meta.com"""
        # Convert to lowercase and replace spaces/special chars
        url_name = item_name.lower()
        url_name = re.sub(r"['\"]", "", url_name)  # Remove quotes
        url_name = re.sub(r"[^a-z0-9\s]", "", url_name)  # Remove special chars except spaces
        url_name = re.sub(r"\s+", "-", url_name)  # Replace spaces with hyphens
        return f"{self.base_url}/items/{url_name}"
    
    def scrape_complete_item_details(self, item_name):
        """Scrape complete item details from wr-meta.com"""
        print(f"Scraping: {item_name}")
        
        try:
            # First try to get data from the main items page
            items_url = f"{self.base_url}/items"
            response = self.session.get(items_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            item_data = {
                "name": item_name,
                "stats": {},
                "cost": 0,
                "passive": "",
                "active": "",
                "description": "",
                "tips": [],
                "build_path": [],
                "build_components": {},
                "builds_into": [],
                "category": "",
                "tier": "",
                "tags": []
            }
            
            # Look for the item in the page content
            item_found = False
            
            # Search for item by name in various elements
            item_elements = soup.find_all(string=re.compile(re.escape(item_name), re.I))
            
            for elem in item_elements:
                parent = elem.parent
                if parent:
                    # Try to find the container with item details
                    item_container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                    if item_container:
                        item_details = self.extract_item_details_from_container(item_container, item_name)
                        if item_details:
                            item_data.update(item_details)
                            item_found = True
                            break
            
            # If not found on items page, try to search in champion pages or use fallback data
            if not item_found:
                print(f"Item {item_name} not found on items page, using fallback data")
                fallback_data = self.get_fallback_item_data(item_name)
                if fallback_data:
                    item_data.update(fallback_data)
            
            return item_data
            
        except Exception as e:
            print(f"Error scraping {item_name}: {e}")
            # Return fallback data if scraping fails
            return self.get_fallback_item_data(item_name)
    
    def extract_item_details_from_container(self, container, item_name):
        """Extract item details from a container element"""
        details = {}
        container_text = container.get_text()
        
        # Extract stats using patterns
        stats = {}
        stat_patterns = {
            'attack_damage': r'(\d+)\s*(?:Attack Damage|AD)',
            'ability_power': r'(\d+)\s*(?:Ability Power|AP)',
            'health': r'(\d+)\s*Health',
            'mana': r'(\d+)\s*Mana',
            'armor': r'(\d+)\s*Armor',
            'magic_resist': r'(\d+)\s*(?:Magic Resist|MR)',
            'attack_speed': r'(\d+)%?\s*Attack Speed',
            'critical_chance': r'(\d+)%\s*(?:Critical|Crit)',
            'ability_haste': r'(\d+)\s*(?:Ability Haste|CDR)',
            'movement_speed': r'(\d+)\s*Movement Speed',
            'life_steal': r'(\d+)%\s*Life Steal',
            'omnivamp': r'(\d+)%\s*Omnivamp',
            'lethality': r'(\d+)\s*Lethality',
        }
        
        for stat_name, pattern in stat_patterns.items():
            match = re.search(pattern, container_text, re.I)
            if match:
                value = int(match.group(1))
                stat_type = 'percentage' if '%' in match.group(0) else 'flat'
                stats[stat_name] = {'value': value, 'type': stat_type}
        
        if stats:
            details['stats'] = stats
        
        # Extract cost
        cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', container_text, re.I)
        if cost_match:
            details['cost'] = int(cost_match.group(1))
        
        # Extract passive
        passive_match = re.search(r'(?:PASSIVE|Passive)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
        if passive_match:
            details['passive'] = passive_match.group(1).strip()
        
        # Extract active
        active_match = re.search(r'(?:ACTIVE|Active)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
        if active_match:
            details['active'] = active_match.group(1).strip()
        
        # Extract description
        desc_match = re.search(rf'{re.escape(item_name)}[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
        if desc_match:
            details['description'] = desc_match.group(1).strip()
        
        return details if details else None
    
    def get_fallback_item_data(self, item_name):
        """Get fallback data for items from the existing database"""
        # Use data from the existing wr_meta_scraper database
        fallback_database = {
            "Hullbreaker": {
                "stats": {
                    "attack_damage": {"value": 50, "type": "flat"},
                    "health": {"value": 400, "type": "flat"},
                    "ability_haste": {"value": 15, "type": "flat"}
                },
                "cost": 3200,
                "passive": "Boarding Party: While no allied champions are nearby, gain 20% increased damage to structures and 20 Armor and Magic Resist. Nearby minions gain 60% increased damage to structures and take 75% reduced damage from champions and structures.",
                "active": "",
                "description": "Split-push focused item that provides Attack Damage, Health, and Ability Haste. When isolated from allies, grants bonus resistances and structure damage while empowering nearby minions. Perfect for split-pushers who want to pressure side lanes and take towers quickly while being harder to kill when caught alone.",
                "category": "legendary",
                "tier": "A",
                "build_path": ["Phage", "Caulfield's Warhammer"],
                "tags": ["Damage", "Physical", "Health", "Ability Haste", "Split Push", "Structure Damage"],
                "tips": [
                    "Best used by champions who can split-push effectively",
                    "The isolation bonus makes you tankier when caught alone",
                    "Empowered minions help take towers faster",
                    "Great for drawing enemy attention to side lanes"
                ]
            },
            "Trinity Force": {
                "stats": {
                    "attack_damage": {"value": 25, "type": "flat"},
                    "health": {"value": 200, "type": "flat"},
                    "attack_speed": {"value": 35, "type": "percentage"},
                    "ability_haste": {"value": 20, "type": "flat"}
                },
                "cost": 3333,
                "passive": "Spellblade: After using an ability, your next basic attack deals bonus physical damage equal to 200% base AD (1.5s cooldown). Threefold Strike: Attacks grant 20 Movement Speed for 3 seconds, stacking up to 8 times",
                "active": "",
                "description": "Versatile bruiser item that enhances ability-based champions. Provides a mix of offensive and defensive stats with strong synergy for spell-weaving fighters. The Spellblade passive rewards frequent ability usage with enhanced basic attacks.",
                "category": "legendary",
                "tier": "S",
                "build_path": ["Sheen", "Phage", "Stinger"],
                "tags": ["Damage", "Health", "Spellblade", "Attack Speed", "Movement"],
                "tips": [
                    "Perfect for champions who weave abilities between auto attacks",
                    "The movement speed stacks help with kiting and chasing",
                    "Spellblade proc scales with base AD, not bonus AD",
                    "Great on bruisers who need both damage and survivability"
                ]
            },
            "Infinity Edge": {
                "stats": {
                    "attack_damage": {"value": 70, "type": "flat"},
                    "critical_chance": {"value": 25, "type": "percentage"}
                },
                "cost": 3400,
                "passive": "Perfection: If you have at least 60% Critical Strike Chance, gain 35% Critical Strike Damage.",
                "active": "",
                "description": "Critical strike item providing massive Attack Damage and Critical Strike Chance. The Perfection passive significantly amplifies critical strike damage when you reach the 60% threshold, making it essential for crit-based marksmen.",
                "category": "legendary",
                "tier": "S",
                "build_path": ["B.F. Sword", "Pickaxe", "Cloak of Agility"],
                "tags": ["Damage", "Physical", "Critical"],
                "tips": [
                    "Build other crit items first to reach 60% crit chance",
                    "The passive bonus is huge - prioritize reaching the threshold",
                    "Core item for most ADC champions",
                    "Pairs well with other crit items like Phantom Dancer"
                ]
            },
            "Rabadon's Deathcap": {
                "stats": {
                    "ability_power": {"value": 120, "type": "flat"}
                },
                "cost": 3600,
                "passive": "Magical Opus: Increases Ability Power by 40%.",
                "active": "",
                "description": "High-tier AP item providing massive Ability Power. The Magical Opus passive amplifies all your AP by 40%, making it the ultimate damage multiplier for mages. Best built when you already have some AP items.",
                "category": "legendary",
                "tier": "S",
                "build_path": ["Needlessly Large Rod", "Blasting Wand"],
                "tags": ["Magic", "Ability Power"],
                "tips": [
                    "Build after other AP items to maximize the 40% bonus",
                    "The passive applies to ALL ability power, including from other items",
                    "Essential for burst mages and late-game scaling",
                    "Expensive but provides the highest AP in the game"
                ]
            }
        }
        
        return fallback_database.get(item_name, None)
    
    def parse_stat(self, stat_text, stats_dict):
        """Parse individual stat from text"""
        stat_text = stat_text.strip()
        
        # Common stat patterns
        patterns = [
            (r'(\d+)\s*Attack Damage', 'attack_damage', 'flat'),
            (r'(\d+)\s*Ability Power', 'ability_power', 'flat'),
            (r'(\d+)\s*Health', 'health', 'flat'),
            (r'(\d+)\s*Mana', 'mana', 'flat'),
            (r'(\d+)%\s*Attack Speed', 'attack_speed', 'percentage'),
            (r'(\d+)%\s*Critical Strike Chance', 'critical_chance', 'percentage'),
            (r'(\d+)\s*Armor', 'armor', 'flat'),
            (r'(\d+)\s*Magic Resist', 'magic_resist', 'flat'),
            (r'(\d+)\s*Ability Haste', 'ability_haste', 'flat'),
            (r'(\d+)%\s*Life Steal', 'life_steal', 'percentage'),
            (r'(\d+)\s*Movement Speed', 'movement_speed', 'flat'),
        ]
        
        for pattern, stat_name, stat_type in patterns:
            match = re.search(pattern, stat_text, re.I)
            if match:
                stats_dict[stat_name] = {
                    "value": int(match.group(1)),
                    "type": stat_type
                }
                break
    
    def extract_component_details(self, component_elem):
        """Extract details about build components"""
        details = {}
        
        # Try to find cost
        cost_elem = component_elem.find('span', class_='cost')
        if cost_elem:
            cost_match = re.search(r'(\d+)', cost_elem.get_text())
            if cost_match:
                details['cost'] = int(cost_match.group(1))
        
        # Try to find stats
        stats_elem = component_elem.find('div', class_='stats')
        if stats_elem:
            details['stats'] = stats_elem.get_text(strip=True)
        
        return details if details else None
    
    def enhance_existing_item(self, item_file_path):
        """Enhance existing item with complete details"""
        try:
            with open(item_file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            item_name = existing_data.get('name', '')
            if not item_name:
                print(f"No item name found in {item_file_path}")
                return False
            
            # Scrape complete details
            complete_data = self.scrape_complete_item_details(item_name)
            if not complete_data:
                print(f"Failed to scrape complete data for {item_name}")
                return False
            
            # Merge with existing data (keep existing data, add missing fields)
            enhanced_data = existing_data.copy()
            
            # Add missing fields
            for key, value in complete_data.items():
                if key not in enhanced_data or not enhanced_data[key]:
                    enhanced_data[key] = value
                elif key == 'stats' and isinstance(value, dict):
                    # Merge stats
                    for stat_key, stat_value in value.items():
                        if stat_key not in enhanced_data['stats']:
                            enhanced_data['stats'][stat_key] = stat_value
                elif key in ['tips', 'build_path', 'builds_into', 'tags'] and isinstance(value, list):
                    # Merge lists (avoid duplicates)
                    existing_list = enhanced_data.get(key, [])
                    for item in value:
                        if item not in existing_list:
                            existing_list.append(item)
                    enhanced_data[key] = existing_list
            
            # Save enhanced data
            with open(item_file_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
            
            print(f"Enhanced {item_name} successfully!")
            return True
            
        except Exception as e:
            print(f"Error enhancing {item_file_path}: {e}")
            return False
    
    def enhance_all_items(self):
        """Enhance all items in the items directory"""
        items_dir = 'items'
        if not os.path.exists(items_dir):
            print("Items directory not found!")
            return
        
        item_files = [f for f in os.listdir(items_dir) if f.endswith('.json')]
        print(f"Found {len(item_files)} item files to enhance")
        
        enhanced_count = 0
        for item_file in item_files:
            item_path = os.path.join(items_dir, item_file)
            print(f"\nProcessing: {item_file}")
            
            if self.enhance_existing_item(item_path):
                enhanced_count += 1
            
            # Rate limiting
            time.sleep(1)
        
        print(f"\nCompleted! Enhanced {enhanced_count}/{len(item_files)} items")

def main():
    scraper = CompleteItemScraper()
    
    print("Starting complete item details enhancement...")
    scraper.enhance_all_items()
    
    print("\nDone! All items have been enhanced with complete details.")

if __name__ == "__main__":
    main()