#!/usr/bin/env python3
"""
Validate if all items have tips from wr-meta.com
"""

import json
import os
import sys

def validate_item_tips():
    """Check all items for tips and report which ones are missing"""
    
    items_dir = 'items'
    if not os.path.exists(items_dir):
        print("Items directory not found!")
        return
    
    total_items = 0
    items_with_tips = 0
    items_without_tips = []
    
    for filename in os.listdir(items_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(items_dir, filename)
        total_items += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                item_data = json.load(f)
            
            item_name = item_data.get('name', filename.replace('.json', ''))
            
            # Check if tips exist and are not empty
            tips = item_data.get('tips', [])
            if tips and len(tips) > 0:
                items_with_tips += 1
            else:
                items_without_tips.append((item_name, filename))
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Print results
    print(f"\n=== ITEM TIPS VALIDATION RESULTS ===")
    print(f"Total items: {total_items}")
    print(f"Items with tips: {items_with_tips} ({(items_with_tips/total_items)*100:.1f}%)")
    print(f"Items without tips: {len(items_without_tips)} ({(len(items_without_tips)/total_items)*100:.1f}%)")
    
    if items_without_tips:
        print("\nItems missing tips:")
        for i, (name, filename) in enumerate(sorted(items_without_tips), 1):
            print(f"{i}. {name} ({filename})")
    
    return items_without_tips

if __name__ == "__main__":
    missing_tips = validate_item_tips()
    
    # Exit with error code if any items are missing tips
    if missing_tips:
        print("\nSome items are missing tips. See above for details.")
        sys.exit(1)
    else:
        print("\nAll items have tips! Success!")
        sys.exit(0)