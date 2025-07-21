#!/usr/bin/env python3
"""
Smart Data Organizer for Wild Rift
Integrates real-time data scraping with batch processing
"""

import os
import json
import time
import subprocess
from pathlib import Path
from real_time_item_scraper import RealTimeItemScraper

class SmartDataOrganizer:
    def __init__(self):
        self.item_scraper = RealTimeItemScraper()
        self.items_dir = Path("items")
        self.runes_dir = Path("runes")
        self.champions_dir = Path("champions_clean")
        self.scraped_champions_dir = Path("scraped_champions")
        
        # Create directories if they don't exist
        self.items_dir.mkdir(exist_ok=True)
        self.runes_dir.mkdir(exist_ok=True)
        self.champions_dir.mkdir(exist_ok=True)
        self.scraped_champions_dir.mkdir(exist_ok=True)
    
    def run_batch_scrape_champions(self, max_champions=None):
        """Run the batch champion scraper with real-time data"""
        print("Starting batch champion scraping with real-time data...")
        
        cmd = ["python", "batch_scrape_all_champions.py"]
        if max_champions:
            cmd.extend(["--max", str(max_champions)])
        
        try:
            subprocess.run(cmd, check=True)
            print("Batch champion scraping completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running batch champion scraper: {e}")
            return False
    
    def update_item_data(self):
        """Update all item data with real-time information"""
        print("Updating all item data with real-time information...")
        
        # Get list of all items from champion builds
        items_to_update = set()
        
        # Scan champion files for items
        for champion_file in self.scraped_champions_dir.glob("*_data.json"):
            try:
                with open(champion_file, 'r', encoding='utf-8') as f:
                    champion_data = json.load(f)
                
                if 'builds' in champion_data:
                    builds = champion_data['builds']
                    
                    # Collect items from all categories
                    for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                        if category in builds and builds[category]:
                            for item_name in builds[category]:
                                if item_name and isinstance(item_name, str):
                                    items_to_update.add(item_name)
            except Exception as e:
                print(f"Error reading {champion_file}: {e}")
        
        print(f"Found {len(items_to_update)} unique items to update")
        
        # Update each item
        updated_count = 0
        for item_name in items_to_update:
            print(f"\nUpdating item: {item_name}")
            
            # Scrape real-time data
            item_data = self.item_scraper.scrape_specific_item(item_name)
            
            if item_data:
                updated_count += 1
            
            # Rate limiting
            time.sleep(1)
        
        print(f"Updated {updated_count}/{len(items_to_update)} items with real-time data")
        return updated_count
    
    def validate_data_consistency(self):
        """Validate data consistency across all files"""
        print("Validating data consistency...")
        
        issues = []
        
        # Check item files
        for item_file in self.items_dir.glob("*.json"):
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                
                # Check required fields
                required_fields = ['name', 'stats', 'cost']
                for field in required_fields:
                    if field not in item_data or not item_data[field]:
                        issues.append(f"Missing {field} in {item_file}")
                
                # Check stats structure
                if 'stats' in item_data and item_data['stats']:
                    for stat_name, stat_value in item_data['stats'].items():
                        if not isinstance(stat_value, dict) or 'value' not in stat_value:
                            issues.append(f"Invalid stat structure for {stat_name} in {item_file}")
                
            except Exception as e:
                issues.append(f"Error reading {item_file}: {e}")
        
        # Check champion files
        for champion_file in self.scraped_champions_dir.glob("*_data.json"):
            try:
                with open(champion_file, 'r', encoding='utf-8') as f:
                    champion_data = json.load(f)
                
                # Check required sections
                required_sections = ['champion', 'stats', 'abilities', 'builds']
                for section in required_sections:
                    if section not in champion_data:
                        issues.append(f"Missing {section} section in {champion_file}")
                
            except Exception as e:
                issues.append(f"Error reading {champion_file}: {e}")
        
        if issues:
            print(f"\nFound {len(issues)} data consistency issues:")
            for issue in issues[:10]:  # Show first 10
                print(f"  • {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
        else:
            print("No data consistency issues found!")
        
        return issues
    
    def run_full_data_update(self, max_champions=None):
        """Run a full data update process"""
        print("Starting full data update process...")
        
        # Step 1: Run batch champion scraping
        success = self.run_batch_scrape_champions(max_champions)
        if not success:
            print("Batch champion scraping failed, stopping process")
            return False
        
        # Step 2: Update item data
        self.update_item_data()
        
        # Step 3: Validate data consistency
        issues = self.validate_data_consistency()
        
        print("\nFull data update process completed!")
        if issues:
            print(f"Found {len(issues)} issues that need attention")
        else:
            print("All data is consistent and up-to-date")
        
        return len(issues) == 0

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Data Organizer for Wild Rift')
    parser.add_argument('--full-update', action='store_true', help='Run full data update process')
    parser.add_argument('--update-items', action='store_true', help='Update all item data')
    parser.add_argument('--validate', action='store_true', help='Validate data consistency')
    parser.add_argument('--max', type=int, help='Maximum number of champions to process')
    
    args = parser.parse_args()
    
    organizer = SmartDataOrganizer()
    
    if args.full_update:
        organizer.run_full_data_update(args.max)
    elif args.update_items:
        organizer.update_item_data()
    elif args.validate:
        organizer.validate_data_consistency()
    else:
        print("Please specify an action: --full-update, --update-items, or --validate")

if __name__ == "__main__":
    main()