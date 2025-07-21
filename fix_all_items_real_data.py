#!/usr/bin/env python3
"""
Fix All Items with Real Data
Updates all item files with accurate data from the website
"""

import requests
import json
import re
import os
import time
from bs4 import BeautifulSoup
from pathlib import Path
from real_time_item_scraper import RealTimeItemScraper

class ItemDataFixer:
    def __init__(self):
        self.scraper = RealTimeItemScraper()
        self.items_dir = Path("items")
        self.items_dir.mkdir(exist_ok=True)
    
    def fix_all_items(self):
        """Fix all items with real data from the website"""
        print("Fixing all items with real data...")
        
        # Get list of all item files
        item_files = list(self.items_dir.glob("*.json"))
        print(f"Found {len(item_files)} item files to fix")
        
        fixed_count = 0
        failed_count = 0
        
        for item_file in item_files:
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                
                item_name = item_data.get('name', '')
                if not item_name:
                    print(f"No item name found in {item_file}")
                    failed_count += 1
                    continue
                
                print(f"\nFixing {item_name}...")
                
                # Scrape real-time data
                real_data = self.scraper.scrape_specific_item(item_name)
                
                if not real_data:
                    print(f"Could not get real data for {item_name}")
                    failed_count += 1
                    continue
                
                # Update with real data
                updated_data = item_data.copy()
                
                # Update key fields
                if 'cost' in real_data:
                    updated_data['cost'] = real_data['cost']
                
                if 'stats' in real_data and real_data['stats']:
                    updated_data['stats'] = real_data['stats']
                
                if 'passive' in real_data and real_data['passive']:
                    updated_data['passive'] = real_data['passive']
                
                if 'active' in real_data and real_data['active']:
                    updated_data['active'] = real_data['active']
                
                if 'description' in real_data and real_data['description']:
                    updated_data['description'] = real_data['description']
                
                if 'tips' in real_data and real_data['tips']:
                    updated_data['tips'] = real_data['tips']
                
                # Save updated data
                with open(item_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Fixed {item_name}")
                fixed_count += 1
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fixing {item_file}: {e}")
                failed_count += 1
        
        print(f"\nCompleted! Fixed {fixed_count}/{len(item_files)} items")
        print(f"Failed: {failed_count}")
        
        return fixed_count, failed_count
    
    def fix_specific_items(self, item_names):
        """Fix specific items with real data"""
        print(f"Fixing {len(item_names)} specific items...")
        
        fixed_count = 0
        failed_count = 0
        
        for item_name in item_names:
            print(f"\nFixing {item_name}...")
            
            # Generate filename
            filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
            item_path = self.items_dir / filename
            
            # Check if file exists
            if item_path.exists():
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        item_data = json.load(f)
                except Exception as e:
                    print(f"Error reading {item_path}: {e}")
                    failed_count += 1
                    continue
            else:
                item_data = {"name": item_name}
            
            # Scrape real-time data
            real_data = self.scraper.scrape_specific_item(item_name)
            
            if not real_data:
                print(f"Could not get real data for {item_name}")
                failed_count += 1
                continue
            
            # Update with real data
            updated_data = item_data.copy()
            
            # Update key fields
            if 'cost' in real_data:
                updated_data['cost'] = real_data['cost']
            
            if 'stats' in real_data and real_data['stats']:
                updated_data['stats'] = real_data['stats']
            
            if 'passive' in real_data and real_data['passive']:
                updated_data['passive'] = real_data['passive']
            
            if 'active' in real_data and real_data['active']:
                updated_data['active'] = real_data['active']
            
            if 'description' in real_data and real_data['description']:
                updated_data['description'] = real_data['description']
            
            if 'tips' in real_data and real_data['tips']:
                updated_data['tips'] = real_data['tips']
            
            # Save updated data
            with open(item_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Fixed {item_name}")
            fixed_count += 1
            
            # Rate limiting
            time.sleep(1)
        
        print(f"\nCompleted! Fixed {fixed_count}/{len(item_names)} items")
        print(f"Failed: {failed_count}")
        
        return fixed_count, failed_count
    
    def fix_critical_items(self):
        """Fix critical items that are commonly used"""
        critical_items = [
            "Rabadon's Deathcap",
            "Infinity Edge",
            "Trinity Force",
            "Guardian Angel",
            "Duskblade of Draktharr",
            "Frozen Heart",
            "Edge of Night",
            "Warmog's Armor",
            "Crystalline Reflector",
            "Harmonic Echo"
        ]
        
        print(f"Fixing {len(critical_items)} critical items...")
        return self.fix_specific_items(critical_items)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix all items with real data from the website')
    parser.add_argument('--all', action='store_true', help='Fix all items')
    parser.add_argument('--critical', action='store_true', help='Fix critical items only')
    parser.add_argument('--item', type=str, help='Fix a specific item by name')
    
    args = parser.parse_args()
    
    fixer = ItemDataFixer()
    
    if args.all:
        fixer.fix_all_items()
    elif args.critical:
        fixer.fix_critical_items()
    elif args.item:
        fixer.fix_specific_items([args.item])
    else:
        print("Please specify an action: --all, --critical, or --item NAME")
        # Default to critical items
        fixer.fix_critical_items()

if __name__ == "__main__":
    main()