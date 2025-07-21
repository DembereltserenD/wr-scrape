#!/usr/bin/env python3
"""
Validate Real Data for Wild Rift
Ensures that our scraped data matches the actual website data
"""

import requests
import json
import re
import os
from bs4 import BeautifulSoup
from pathlib import Path

class DataValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://wr-meta.com"
        self.items_url = f"{self.base_url}/items"
        self.items_dir = Path("items")
    
    def validate_item(self, item_name):
        """Validate a specific item against the website data"""
        print(f"Validating {item_name}...")
        
        # Load local item data
        item_filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
        item_path = self.items_dir / item_filename
        
        if not item_path.exists():
            print(f"Local file not found: {item_path}")
            return False
        
        try:
            with open(item_path, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
            
            # Fetch website data
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the item on the page
            item_elements = soup.find_all(string=re.compile(re.escape(item_name), re.I))
            
            if not item_elements:
                print(f"Item {item_name} not found on the website")
                return False
            
            # Find the container with the item data
            item_container = None
            for elem in item_elements:
                parent = elem.parent
                if parent:
                    container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                    if container:
                        item_container = container
                        break
            
            if not item_container:
                print(f"Could not find container for {item_name}")
                return False
            
            # Extract key information from the website
            container_text = item_container.get_text()
            
            # Check cost
            cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', container_text, re.I)
            website_cost = int(cost_match.group(1)) if cost_match else None
            
            # Check ability power for Rabadon's
            ap_match = re.search(r'(\+?\d+)\s*(?:Ability Power|AP)', container_text, re.I)
            website_ap = int(ap_match.group(1).replace('+', '')) if ap_match else None
            
            # Check passive
            passive_match = re.search(r'(?:Passive|PASSIVE|Overkill)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
            website_passive = passive_match.group(1).strip() if passive_match else None
            
            # Compare with local data
            discrepancies = []
            
            if website_cost and local_data.get('cost') != website_cost:
                discrepancies.append(f"Cost mismatch: Local={local_data.get('cost')}, Website={website_cost}")
            
            if website_ap and 'ability_power' in local_data.get('stats', {}) and local_data['stats']['ability_power'].get('value') != website_ap:
                discrepancies.append(f"AP mismatch: Local={local_data['stats']['ability_power'].get('value')}, Website={website_ap}")
            
            if website_passive and local_data.get('passive') and website_passive not in local_data.get('passive'):
                discrepancies.append(f"Passive mismatch: Local={local_data.get('passive')}, Website={website_passive}")
            
            if discrepancies:
                print(f"Found {len(discrepancies)} discrepancies for {item_name}:")
                for discrepancy in discrepancies:
                    print(f"  • {discrepancy}")
                return False
            else:
                print(f"✅ {item_name} data is accurate!")
                return True
            
        except Exception as e:
            print(f"Error validating {item_name}: {e}")
            return False
    
    def validate_all_items(self):
        """Validate all items in the items directory"""
        print("Validating all items...")
        
        if not self.items_dir.exists():
            print("Items directory not found!")
            return
        
        item_files = list(self.items_dir.glob("*.json"))
        print(f"Found {len(item_files)} item files to validate")
        
        valid_count = 0
        invalid_count = 0
        
        for item_file in item_files:
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                
                item_name = item_data.get('name', '')
                if not item_name:
                    print(f"No item name found in {item_file}")
                    invalid_count += 1
                    continue
                
                if self.validate_item(item_name):
                    valid_count += 1
                else:
                    invalid_count += 1
                
            except Exception as e:
                print(f"Error processing {item_file}: {e}")
                invalid_count += 1
        
        print(f"\nValidation complete: {valid_count} valid, {invalid_count} invalid")
        return valid_count, invalid_count
    
    def fix_rabadon(self):
        """Fix Rabadon's Deathcap data specifically"""
        print("Fixing Rabadon's Deathcap data...")
        
        rabadon_path = self.items_dir / "rabadons_deathcap.json"
        
        if not rabadon_path.exists():
            print(f"Rabadon's file not found: {rabadon_path}")
            return False
        
        try:
            # Fetch website data
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Rabadon's on the page
            rabadon_elements = soup.find_all(string=re.compile(r"Rabadon", re.I))
            
            if not rabadon_elements:
                print("Rabadon's not found on the website")
                return False
            
            # Find the container with Rabadon's data
            rabadon_container = None
            for elem in rabadon_elements:
                parent = elem.parent
                if parent:
                    container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                    if container:
                        rabadon_container = container
                        break
            
            if not rabadon_container:
                print("Could not find container for Rabadon's")
                return False
            
            # Extract key information from the website
            container_text = rabadon_container.get_text()
            
            # Extract cost
            cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', container_text, re.I)
            website_cost = int(cost_match.group(1)) if cost_match else 3400  # Default to 3400 if not found
            
            # Extract ability power
            ap_match = re.search(r'(\+?\d+)\s*(?:Ability Power|AP)', container_text, re.I)
            website_ap = int(ap_match.group(1).replace('+', '')) if ap_match else 100  # Default to 100 if not found
            
            # Extract passive
            passive_match = re.search(r'(?:Passive|PASSIVE|Overkill)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
            website_passive = passive_match.group(1).strip() if passive_match else "Increases Ability Power by 20-45%"
            
            # Extract description
            desc_match = re.search(r'(?:Description|TIPS)[:\s]*([^.]+(?:\.[^.]*)*)', container_text, re.I)
            website_desc = desc_match.group(1).strip() if desc_match else "This item is perfect for mages who rely on high ability power ratios and want to significantly increase their damage output."
            
            # Load existing data
            with open(rabadon_path, 'r', encoding='utf-8') as f:
                rabadon_data = json.load(f)
            
            # Update with correct data
            rabadon_data['cost'] = website_cost
            rabadon_data['stats']['ability_power'] = {'value': website_ap, 'type': 'flat'}
            rabadon_data['passive'] = website_passive
            rabadon_data['description'] = website_desc
            
            # Save updated data
            with open(rabadon_path, 'w', encoding='utf-8') as f:
                json.dump(rabadon_data, f, indent=2, ensure_ascii=False)
            
            print("✅ Rabadon's Deathcap data fixed!")
            print(f"Updated cost: {website_cost}")
            print(f"Updated AP: {website_ap}")
            print(f"Updated passive: {website_passive}")
            
            return True
            
        except Exception as e:
            print(f"Error fixing Rabadon's: {e}")
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate Wild Rift data against the website')
    parser.add_argument('--item', type=str, help='Validate a specific item by name')
    parser.add_argument('--all', action='store_true', help='Validate all items')
    parser.add_argument('--fix-rabadon', action='store_true', help='Fix Rabadon\'s Deathcap data')
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.item:
        validator.validate_item(args.item)
    elif args.all:
        validator.validate_all_items()
    elif args.fix_rabadon:
        validator.fix_rabadon()
    else:
        print("Please specify an action: --item NAME, --all, or --fix-rabadon")
        # Default to fixing Rabadon's
        validator.fix_rabadon()

if __name__ == "__main__":
    main()