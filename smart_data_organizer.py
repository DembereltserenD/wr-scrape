#!/usr/bin/env python3
"""
Smart Data Organizer - Separates champion data from item/rune details
Creates clean architecture with separate folders for different data types.

Usage: python smart_data_organizer.py
"""

import os
import json
import glob
from pathlib import Path

class SmartDataOrganizer:
    def __init__(self):
        self.base_dir = Path(".")
        self.items_dir = Path("items")
        self.runes_dir = Path("runes")
        self.champions_dir = Path("champions_clean")
        
        # Create directories
        self.items_dir.mkdir(exist_ok=True)
        self.runes_dir.mkdir(exist_ok=True)
        self.champions_dir.mkdir(exist_ok=True)
        
        # Storage for unique items and runes
        self.items_database = {}
        self.runes_database = {}

    def extract_and_organize_data(self):
        """
        Extract item and rune data from enhanced champion files
        and organize into separate folders
        """
        print("🚀 Starting smart data organization...")
        
        # Find all enhanced champion files
        enhanced_files = glob.glob('scraped_champions/*_enhanced.json')
        enhanced_files.extend(glob.glob('*_enhanced.json'))
        
        print(f"Found {len(enhanced_files)} enhanced files to process")
        
        processed_champions = 0
        
        for file_path in enhanced_files:
            try:
                print(f"Processing: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract items and runes, clean champion data
                clean_champion_data = self._process_champion_file(data)
                
                # Save clean champion data
                champion_name = self._get_champion_name_from_file(file_path)
                clean_file_path = self.champions_dir / f"{champion_name}.json"
                
                with open(clean_file_path, 'w', encoding='utf-8') as f:
                    json.dump(clean_champion_data, f, indent=2, ensure_ascii=False)
                
                processed_champions += 1
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Save item and rune databases
        self._save_items_database()
        self._save_runes_database()
        
        print(f"\n✅ Successfully processed {processed_champions} champions")
        print(f"📦 Created {len(self.items_database)} unique items")
        print(f"🔮 Created {len(self.runes_database)} unique runes")
        
        return processed_champions

    def _process_champion_file(self, data):
        """
        Process champion file: extract items/runes, return clean champion data
        """
        clean_data = data.copy()
        
        # Process builds
        if 'builds' in clean_data:
            clean_data['builds'] = self._clean_builds_section(clean_data['builds'])
        
        # Process runes
        if 'runes' in clean_data:
            clean_data['runes'] = self._clean_runes_section(clean_data['runes'])
        
        return clean_data

    def _clean_builds_section(self, builds):
        """
        Clean builds section: extract detailed items, keep only references
        """
        clean_builds = builds.copy()
        
        # Categories that have detailed versions
        detailed_categories = [
            'starting_items_detailed',
            'boots_detailed', 
            'situational_items_detailed',
            'example_build_detailed'
        ]
        
        for category in detailed_categories:
            if category in builds and builds[category]:
                # Extract items to database
                for item_data in builds[category]:
                    if isinstance(item_data, dict) and 'name' in item_data:
                        item_name = item_data['name']
                        if item_name and item_name.strip():  # Skip empty names
                            self.items_database[item_name] = item_data
                
                # Remove detailed version from champion data
                del clean_builds[category]
        
        return clean_builds

    def _clean_runes_section(self, runes):
        """
        Clean runes section: extract detailed runes, keep only references
        """
        clean_runes = runes.copy()
        
        # Process primary runes
        if 'primary' in runes:
            primary = runes['primary'].copy()
            
            # Extract keystone details
            if 'keystone_detailed' in primary:
                keystone_data = primary['keystone_detailed']
                if isinstance(keystone_data, dict) and 'name' in keystone_data:
                    rune_name = keystone_data['name']
                    if rune_name and rune_name.strip():
                        self.runes_database[rune_name] = keystone_data
                del primary['keystone_detailed']
            
            # Extract primary runes details
            if 'runes_detailed' in primary:
                for rune_data in primary['runes_detailed']:
                    if isinstance(rune_data, dict) and 'name' in rune_data:
                        rune_name = rune_data['name']
                        if rune_name and rune_name.strip():
                            self.runes_database[rune_name] = rune_data
                del primary['runes_detailed']
            
            clean_runes['primary'] = primary
        
        # Process secondary runes
        if 'secondary' in runes and 'runes_detailed' in runes['secondary']:
            for rune_data in runes['secondary']['runes_detailed']:
                if isinstance(rune_data, dict) and 'name' in rune_data:
                    rune_name = rune_data['name']
                    if rune_name and rune_name.strip():
                        self.runes_database[rune_name] = rune_data
            del clean_runes['secondary']['runes_detailed']
        
        return clean_runes

    def _save_items_database(self):
        """
        Save individual item files and create index
        """
        print(f"💾 Saving {len(self.items_database)} items...")
        
        # Save individual item files
        for item_name, item_data in self.items_database.items():
            # Create safe filename
            safe_name = self._create_safe_filename(item_name)
            item_file = self.items_dir / f"{safe_name}.json"
            
            with open(item_file, 'w', encoding='utf-8') as f:
                json.dump(item_data, f, indent=2, ensure_ascii=False)
        
        # Create items index
        items_index = {
            "total_items": len(self.items_database),
            "items": {
                name: {
                    "file": f"{self._create_safe_filename(name)}.json",
                    "category": data.get('category', 'unknown'),
                    "cost": data.get('cost', 0),
                    "tier": data.get('tier', 'A')
                }
                for name, data in self.items_database.items()
            }
        }
        
        with open(self.items_dir / "index.json", 'w', encoding='utf-8') as f:
            json.dump(items_index, f, indent=2, ensure_ascii=False)

    def _save_runes_database(self):
        """
        Save individual rune files and create index
        """
        print(f"🔮 Saving {len(self.runes_database)} runes...")
        
        # Save individual rune files
        for rune_name, rune_data in self.runes_database.items():
            if not rune_name or not rune_name.strip():  # Skip empty names
                continue
                
            # Create safe filename
            safe_name = self._create_safe_filename(rune_name)
            rune_file = self.runes_dir / f"{safe_name}.json"
            
            with open(rune_file, 'w', encoding='utf-8') as f:
                json.dump(rune_data, f, indent=2, ensure_ascii=False)
        
        # Create runes index
        valid_runes = {name: data for name, data in self.runes_database.items() 
                      if name and name.strip()}
        
        runes_index = {
            "total_runes": len(valid_runes),
            "runes": {
                name: {
                    "file": f"{self._create_safe_filename(name)}.json",
                    "tree": data.get('tree', 'Unknown'),
                    "type": data.get('type', 'Primary'),
                    "tier": data.get('tier', 'A')
                }
                for name, data in valid_runes.items()
            }
        }
        
        with open(self.runes_dir / "index.json", 'w', encoding='utf-8') as f:
            json.dump(runes_index, f, indent=2, ensure_ascii=False)

    def _create_safe_filename(self, name):
        """
        Create safe filename from item/rune name
        """
        # Replace problematic characters
        safe_name = name.replace("'", "").replace(":", "").replace("/", "_")
        safe_name = safe_name.replace(" ", "_").replace("-", "_")
        safe_name = safe_name.replace("(", "").replace(")", "")
        safe_name = safe_name.lower()
        
        # Remove multiple underscores
        while "__" in safe_name:
            safe_name = safe_name.replace("__", "_")
        
        return safe_name.strip("_")

    def _get_champion_name_from_file(self, file_path):
        """
        Extract champion name from file path
        """
        filename = os.path.basename(file_path)
        # Remove _enhanced.json or _data_enhanced.json
        name = filename.replace('_enhanced.json', '')
        name = name.replace('_data_enhanced.json', '')
        name = name.replace('_complete_data_enhanced.json', '')
        return name

    def create_data_loader(self):
        """
        Create a data loader utility for accessing items and runes
        """
        loader_code = '''#!/usr/bin/env python3
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
        print(f"\\nRabadon's Deathcap:")
        print(f"Cost: {rabadon.get('cost', 'Unknown')}")
        print(f"Description: {rabadon.get('description', 'No description')}")
'''
        
        with open('data_loader.py', 'w', encoding='utf-8') as f:
            f.write(loader_code)
        
        print("📚 Created data_loader.py utility")

def main():
    organizer = SmartDataOrganizer()
    
    # Organize data
    processed = organizer.extract_and_organize_data()
    
    # Create data loader utility
    organizer.create_data_loader()
    
    print("\n" + "="*50)
    print("🎉 SMART ORGANIZATION COMPLETE!")
    print("="*50)
    print(f"📁 Structure created:")
    print(f"  ├── champions_clean/     - Clean champion data")
    print(f"  ├── items/              - Individual item files + index")
    print(f"  ├── runes/              - Individual rune files + index")
    print(f"  └── data_loader.py      - Smart data access utility")
    print(f"\n🔧 Usage:")
    print(f"  from data_loader import DataLoader")
    print(f"  loader = DataLoader()")
    print(f"  item = loader.get_item('Rabadon\\'s Deathcap')")
    print(f"  champion = loader.get_champion_with_details('blitzcrank')")

if __name__ == "__main__":
    main()