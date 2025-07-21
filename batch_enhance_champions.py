#!/usr/bin/env python3
"""
Batch Champion Enhancement Script
Enhances all scraped champion data with detailed item and rune information.

Usage: python batch_enhance_champions.py
"""

import os
import json
import glob
from advanced_item_scraper import AdvancedItemScraper

def batch_enhance_champions():
    """
    Enhance all champion data files with detailed item and rune information
    """
    scraper = AdvancedItemScraper(use_selenium=False)
    
    # Find all champion data files
    champion_files = glob.glob('scraped_champions/*_data.json')
    champion_files.extend(glob.glob('*_complete_data.json'))
    
    print(f"Found {len(champion_files)} champion data files to enhance")
    
    enhanced_files = []
    
    for champion_file in champion_files:
        try:
            print(f"\nProcessing: {champion_file}")
            
            # Extract champion name from filename for URL construction
            filename = os.path.basename(champion_file)
            champion_name = filename.replace('_complete_data.json', '').replace('_data.json', '')
            champion_url = f"https://wr-meta.com/{champion_name}.html"
            
            # Enhance the champion data
            enhanced_file = scraper.enhance_champion_builds(champion_file, champion_url)
            enhanced_files.append(enhanced_file)
            
            print(f"✓ Enhanced: {enhanced_file}")
            
        except Exception as e:
            print(f"✗ Error processing {champion_file}: {e}")
            continue
    
    print(f"\n🎉 Successfully enhanced {len(enhanced_files)} champion files!")
    print("\nEnhanced files:")
    for file in enhanced_files:
        print(f"  - {file}")
    
    return enhanced_files

def create_item_database():
    """
    Create a comprehensive item database from all enhanced champion data
    """
    print("\nCreating comprehensive item database...")
    
    item_database = {}
    rune_database = {}
    
    # Find all enhanced files
    enhanced_files = glob.glob('scraped_champions/*_enhanced.json')
    enhanced_files.extend(glob.glob('*_enhanced.json'))
    
    for file in enhanced_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract items from builds
            if 'builds' in data:
                builds = data['builds']
                
                for category in ['starting_items_detailed', 'boots_detailed', 'situational_items_detailed', 'example_build_detailed']:
                    if category in builds:
                        for item in builds[category]:
                            if 'name' in item:
                                item_name = item['name']
                                if item_name not in item_database:
                                    item_database[item_name] = item
                                else:
                                    # Merge data if more complete
                                    if len(item.get('stats', {})) > len(item_database[item_name].get('stats', {})):
                                        item_database[item_name] = item
            
            # Extract runes
            if 'runes' in data:
                runes = data['runes']
                
                # Primary runes
                if 'primary' in runes:
                    if 'keystone_detailed' in runes['primary']:
                        keystone = runes['primary']['keystone_detailed']
                        if 'name' in keystone:
                            rune_database[keystone['name']] = keystone
                    
                    if 'runes_detailed' in runes['primary']:
                        for rune in runes['primary']['runes_detailed']:
                            if 'name' in rune:
                                rune_database[rune['name']] = rune
                
                # Secondary runes
                if 'secondary' in runes and 'runes_detailed' in runes['secondary']:
                    for rune in runes['secondary']['runes_detailed']:
                        if 'name' in rune:
                            rune_database[rune['name']] = rune
                            
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    # Save databases
    with open('comprehensive_item_database.json', 'w', encoding='utf-8') as f:
        json.dump(item_database, f, indent=2, ensure_ascii=False)
    
    with open('comprehensive_rune_database.json', 'w', encoding='utf-8') as f:
        json.dump(rune_database, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Item database created with {len(item_database)} items")
    print(f"✓ Rune database created with {len(rune_database)} runes")
    
    return item_database, rune_database

def generate_item_summary():
    """
    Generate a summary of all items with their key information
    """
    try:
        with open('comprehensive_item_database.json', 'r', encoding='utf-8') as f:
            item_db = json.load(f)
        
        summary = {
            'total_items': len(item_db),
            'categories': {},
            'cost_ranges': {},
            'stat_types': set(),
            'items_by_category': {}
        }
        
        for item_name, item_data in item_db.items():
            category = item_data.get('category', 'unknown')
            cost = item_data.get('cost', 0)
            stats = item_data.get('stats', {})
            
            # Count categories
            if category not in summary['categories']:
                summary['categories'][category] = 0
            summary['categories'][category] += 1
            
            # Track items by category
            if category not in summary['items_by_category']:
                summary['items_by_category'][category] = []
            summary['items_by_category'][category].append({
                'name': item_name,
                'cost': cost,
                'tier': item_data.get('tier', 'A')
            })
            
            # Cost ranges
            if cost > 0:
                if cost < 1000:
                    cost_range = 'Low (< 1000g)'
                elif cost < 2500:
                    cost_range = 'Medium (1000-2500g)'
                else:
                    cost_range = 'High (> 2500g)'
                
                if cost_range not in summary['cost_ranges']:
                    summary['cost_ranges'][cost_range] = 0
                summary['cost_ranges'][cost_range] += 1
            
            # Stat types
            for stat_name in stats.keys():
                summary['stat_types'].add(stat_name)
        
        summary['stat_types'] = list(summary['stat_types'])
        
        with open('item_database_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Item summary generated: {summary['total_items']} items across {len(summary['categories'])} categories")
        
        return summary
        
    except Exception as e:
        print(f"Error generating item summary: {e}")
        return None

def main():
    print("🚀 Starting batch champion enhancement...")
    
    # Step 1: Enhance all champion data
    enhanced_files = batch_enhance_champions()
    
    # Step 2: Create comprehensive databases
    item_db, rune_db = create_item_database()
    
    # Step 3: Generate summary
    summary = generate_item_summary()
    
    print("\n" + "="*50)
    print("📊 ENHANCEMENT COMPLETE!")
    print("="*50)
    print(f"Enhanced {len(enhanced_files)} champion files")
    print(f"Created database with {len(item_db)} items and {len(rune_db)} runes")
    
    if summary:
        print(f"\nItem Categories:")
        for category, count in summary['categories'].items():
            print(f"  - {category.title()}: {count} items")
        
        print(f"\nCost Distribution:")
        for cost_range, count in summary['cost_ranges'].items():
            print(f"  - {cost_range}: {count} items")
    
    print("\n📁 Generated Files:")
    print("  - comprehensive_item_database.json")
    print("  - comprehensive_rune_database.json") 
    print("  - item_database_summary.json")
    for file in enhanced_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()