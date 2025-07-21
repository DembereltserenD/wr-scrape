#!/usr/bin/env python3
"""
Test Final Data for Wild Rift
Verifies that our data is accurate and complete
"""

import json
import os
from pathlib import Path

class DataTester:
    def __init__(self):
        self.items_dir = Path("items")
        self.runes_dir = Path("runes")
        self.champions_dir = Path("champions_clean")
        self.scraped_champions_dir = Path("scraped_champions")
    
    def test_item_data(self, item_name):
        """Test a specific item's data"""
        print(f"Testing {item_name}...")
        
        # Generate filename
        filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
        item_path = self.items_dir / filename
        
        if not item_path.exists():
            print(f"Item file not found: {item_path}")
            return False
        
        try:
            with open(item_path, 'r', encoding='utf-8') as f:
                item_data = json.load(f)
            
            # Check required fields
            required_fields = ['name', 'stats', 'cost', 'description']
            missing_fields = [field for field in required_fields if field not in item_data or not item_data[field]]
            
            if missing_fields:
                print(f"Missing required fields: {', '.join(missing_fields)}")
                return False
            
            # Check stats structure
            if 'stats' in item_data and item_data['stats']:
                for stat_name, stat_value in item_data['stats'].items():
                    if not isinstance(stat_value, dict) or 'value' not in stat_value:
                        print(f"Invalid stat structure for {stat_name}")
                        return False
            
            print(f"✅ {item_name} data is valid!")
            print(f"Cost: {item_data['cost']}")
            print(f"Stats: {', '.join(f'{k}: {v['value']}' for k, v in item_data['stats'].items())}")
            if 'passive' in item_data and item_data['passive']:
                print(f"Passive: {item_data['passive']}")
            
            return True
            
        except Exception as e:
            print(f"Error testing {item_name}: {e}")
            return False
    
    def test_critical_items(self):
        """Test critical items that are commonly used"""
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
        
        print(f"Testing {len(critical_items)} critical items...")
        
        valid_count = 0
        invalid_count = 0
        
        for item_name in critical_items:
            if self.test_item_data(item_name):
                valid_count += 1
            else:
                invalid_count += 1
            print()  # Add a blank line between items
        
        print(f"\nTesting complete: {valid_count} valid, {invalid_count} invalid")
        return valid_count, invalid_count
    
    def test_all_items(self):
        """Test all items in the items directory"""
        print("Testing all items...")
        
        if not self.items_dir.exists():
            print("Items directory not found!")
            return 0, 0
        
        item_files = list(self.items_dir.glob("*.json"))
        print(f"Found {len(item_files)} item files to test")
        
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
                
                if self.test_item_data(item_name):
                    valid_count += 1
                else:
                    invalid_count += 1
                
                print()  # Add a blank line between items
                
            except Exception as e:
                print(f"Error processing {item_file}: {e}")
                invalid_count += 1
        
        print(f"\nTesting complete: {valid_count} valid, {invalid_count} invalid")
        return valid_count, invalid_count
    
    def test_champion_data(self, champion_name):
        """Test a specific champion's data"""
        print(f"Testing {champion_name}...")
        
        # Generate filename
        filename = champion_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + "_data.json"
        champion_path = self.scraped_champions_dir / filename
        
        if not champion_path.exists():
            print(f"Champion file not found: {champion_path}")
            return False
        
        try:
            with open(champion_path, 'r', encoding='utf-8') as f:
                champion_data = json.load(f)
            
            # Check required sections
            required_sections = ['champion', 'stats', 'abilities', 'builds']
            missing_sections = [section for section in required_sections if section not in champion_data]
            
            if missing_sections:
                print(f"Missing required sections: {', '.join(missing_sections)}")
                return False
            
            # Check builds structure
            if 'builds' in champion_data:
                builds = champion_data['builds']
                
                # Check item categories
                for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                    if category not in builds or not builds[category]:
                        print(f"Missing or empty {category} in builds")
                
                # Check if items exist in our database
                for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                    if category in builds and builds[category]:
                        for item_name in builds[category]:
                            item_filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
                            item_path = self.items_dir / item_filename
                            
                            if not item_path.exists():
                                print(f"Item {item_name} not found in database")
            
            print(f"✅ {champion_name} data is valid!")
            return True
            
        except Exception as e:
            print(f"Error testing {champion_name}: {e}")
            return False
    
    def test_sample_champions(self):
        """Test a sample of champions"""
        sample_champions = [
            "Aatrox",
            "Ahri",
            "Leona",
            "Kennen",
            "Malphite"
        ]
        
        print(f"Testing {len(sample_champions)} sample champions...")
        
        valid_count = 0
        invalid_count = 0
        
        for champion_name in sample_champions:
            if self.test_champion_data(champion_name):
                valid_count += 1
            else:
                invalid_count += 1
            print()  # Add a blank line between champions
        
        print(f"\nTesting complete: {valid_count} valid, {invalid_count} invalid")
        return valid_count, invalid_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test final data for Wild Rift')
    parser.add_argument('--item', type=str, help='Test a specific item by name')
    parser.add_argument('--all-items', action='store_true', help='Test all items')
    parser.add_argument('--critical-items', action='store_true', help='Test critical items')
    parser.add_argument('--champion', type=str, help='Test a specific champion by name')
    parser.add_argument('--sample-champions', action='store_true', help='Test sample champions')
    
    args = parser.parse_args()
    
    tester = DataTester()
    
    if args.item:
        tester.test_item_data(args.item)
    elif args.all_items:
        tester.test_all_items()
    elif args.critical_items:
        tester.test_critical_items()
    elif args.champion:
        tester.test_champion_data(args.champion)
    elif args.sample_champions:
        tester.test_sample_champions()
    else:
        print("Please specify an action: --item NAME, --all-items, --critical-items, --champion NAME, or --sample-champions")
        # Default to critical items
        tester.test_critical_items()

if __name__ == "__main__":
    main()