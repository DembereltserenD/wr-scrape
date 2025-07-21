#!/usr/bin/env python3
"""
Validate if all items have complete descriptions (no truncated descriptions with "...")
"""

import json
import os
import sys

def validate_item_descriptions():
    """Check all items for complete descriptions"""
    
    items_dir = 'items'
    if not os.path.exists(items_dir):
        print("Items directory not found!")
        return
    
    total_items = 0
    items_with_complete_desc = 0
    items_with_truncated_desc = []
    
    for filename in os.listdir(items_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(items_dir, filename)
        total_items += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                item_data = json.load(f)
            
            item_name = item_data.get('name', filename.replace('.json', ''))
            
            # Check if description is complete (not truncated with "...")
            description = item_data.get('description', '')
            if description and '...' not in description:
                items_with_complete_desc += 1
            else:
                items_with_truncated_desc.append((item_name, filename))
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Print results
    print(f"\n=== ITEM DESCRIPTION VALIDATION RESULTS ===")
    print(f"Total items: {total_items}")
    print(f"Items with complete descriptions: {items_with_complete_desc} ({(items_with_complete_desc/total_items)*100:.1f}%)")
    print(f"Items with truncated descriptions: {len(items_with_truncated_desc)} ({(len(items_with_truncated_desc)/total_items)*100:.1f}%)")
    
    if items_with_truncated_desc:
        print("\nItems with truncated descriptions:")
        for i, (name, filename) in enumerate(sorted(items_with_truncated_desc), 1):
            print(f"{i}. {name} ({filename})")
    
    return items_with_truncated_desc

if __name__ == "__main__":
    truncated_descriptions = validate_item_descriptions()
    
    # Exit with error code if any items have truncated descriptions
    if truncated_descriptions:
        print("\nSome items have truncated descriptions. See above for details.")
        sys.exit(1)
    else:
        print("\nAll items have complete descriptions! Success!")
        sys.exit(0)