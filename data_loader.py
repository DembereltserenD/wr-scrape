#!/usr/bin/env python3
"""
Data Loader - Smart utility to load champion, item, and rune data
Usage: 
    loader = DataLoader()
    champion = loader.get_champion("blitzcrank")
    item = loader.get_item("Rabadon's Deathcap")
    rune = loader.get_rune("Guardian")
"""

import json
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.base_dir = Path(".")
        self.items_dir = self.base_dir / "items"
        self.runes_dir = self.base_dir / "runes"
        self.champions_dir = self.base_dir / "champions_clean"
        
        # Load indexes
        self.items_index = self._load_index(self.items_dir / "index.json")
        self.runes_index = self._load_index(self.runes_dir / "index.json")

    def _load_index(self, index_path):
        """Load index file"""
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_champion(self, champion_name):
        """Get champion data"""
        champion_file = self.champions_dir / f"{champion_name.lower()}.json"
        try:
            with open(champion_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def get_item(self, item_name):
        """Get detailed item data"""
        if item_name not in self.items_index.get('items', {}):
            return None
        
        item_info = self.items_index['items'][item_name]
        item_file = self.items_dir / item_info['file']
        
        try:
            with open(item_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def get_rune(self, rune_name):
        """Get detailed rune data"""
        if rune_name not in self.runes_index.get('runes', {}):
            return None
        
        rune_info = self.runes_index['runes'][rune_name]
        rune_file = self.runes_dir / rune_info['file']
        
        try:
            with open(rune_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def get_champion_with_details(self, champion_name):
        """Get champion data with full item and rune details"""
        champion = self.get_champion(champion_name)
        if not champion:
            return None
        
        # Add detailed items to builds
        if 'builds' in champion:
            builds = champion['builds']
            
            # Add details for each item category
            for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build']:
                if category in builds and builds[category]:
                    detailed_items = []
                    for item_name in builds[category]:
                        item_details = self.get_item(item_name)
                        if item_details:
                            detailed_items.append(item_details)
                        else:
                            # Fallback to basic structure
                            detailed_items.append({"name": item_name, "error": "Details not found"})
                    builds[f"{category}_detailed"] = detailed_items
        
        # Add detailed runes
        if 'runes' in champion:
            runes = champion['runes']
            
            # Primary runes
            if 'primary' in runes:
                primary = runes['primary']
                if 'keystone' in primary:
                    primary['keystone_detailed'] = self.get_rune(primary['keystone'])
                if 'runes' in primary:
                    primary['runes_detailed'] = [self.get_rune(rune) for rune in primary['runes']]
            
            # Secondary runes
            if 'secondary' in runes and 'runes' in runes['secondary']:
                runes['secondary']['runes_detailed'] = [
                    self.get_rune(rune) for rune in runes['secondary']['runes']
                ]
        
        return champion

    def list_items(self, category=None):
        """List all items, optionally filtered by category"""
        items = self.items_index.get('items', {})
        if category:
            return {name: info for name, info in items.items() if info.get('category') == category}
        return items

    def list_runes(self, tree=None):
        """List all runes, optionally filtered by tree"""
        runes = self.runes_index.get('runes', {})
        if tree:
            return {name: info for name, info in runes.items() if info.get('tree') == tree}
        return runes

    def search_items(self, query):
        """Search items by name"""
        items = self.items_index.get('items', {})
        query_lower = query.lower()
        return {name: info for name, info in items.items() if query_lower in name.lower()}

# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    
    # Get champion with full details
    blitz = loader.get_champion_with_details("blitzcrank")
    if blitz:
        print(f"Champion: {blitz['champion']['name']}")
        
        # Show item details
        if 'builds' in blitz and 'starting_items_detailed' in blitz['builds']:
            for item in blitz['builds']['starting_items_detailed']:
                print(f"Item: {item['name']} - Cost: {item.get('cost', 'Unknown')}")
    
    # Get specific item
    rabadon = loader.get_item("Rabadon's Deathcap")
    if rabadon:
        print(f"\nRabadon's Deathcap:")
        print(f"Cost: {rabadon.get('cost', 'Unknown')}")
        print(f"Description: {rabadon.get('description', 'No description')}")
