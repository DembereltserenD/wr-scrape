#!/usr/bin/env python3
"""
Validate that all items have real Wild Rift data, not placeholders
"""

import json
import os
from pathlib import Path

def validate_item_data():
    """Check all item files for placeholder data"""
    items_dir = Path("items")
    
    if not items_dir.exists():
        print("Items directory not found!")
        return
    
    placeholder_indicators = [
        "placeholder",
        "generic",
        "example",
        "Details for",
        "Attack damage item that enhances",
        "Core component for",
        "Defensive item that provides",
        "Wild Rift item that enhances your champion's combat effectiveness",
        "Wild Rift item that enhances your champion's comba",
        "Ability power item that enhances magical damage ou",
        "Boot enhancement that provides additional active o"
    ]
    
    valid_items = []
    placeholder_items = []
    
    for item_file in items_dir.glob("*.json"):
        try:
            with open(item_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for placeholder content
            has_placeholder = False
            description = data.get("description", "").lower()
            passive = data.get("passive", "").lower()
            
            for indicator in placeholder_indicators:
                if indicator.lower() in description or indicator.lower() in passive:
                    has_placeholder = True
                    break
            
            # Check for empty or minimal stats
            stats = data.get("stats", {})
            cost = data.get("cost", 0)
            
            if has_placeholder or not stats or cost < 100:
                placeholder_items.append({
                    "file": item_file.name,
                    "name": data.get("name", "Unknown"),
                    "cost": cost,
                    "stats_count": len(stats),
                    "description": data.get("description", "")[:50] + "..."
                })
            else:
                valid_items.append({
                    "file": item_file.name,
                    "name": data.get("name", "Unknown"),
                    "cost": cost,
                    "stats_count": len(stats)
                })
                
        except Exception as e:
            print(f"Error reading {item_file}: {e}")
    
    print(f"📊 VALIDATION RESULTS:")
    print(f"✅ Valid items with real data: {len(valid_items)}")
    print(f"❌ Items with placeholder data: {len(placeholder_items)}")
    print()
    
    if valid_items:
        print("✅ ITEMS WITH REAL WILD RIFT DATA:")
        for item in valid_items:
            print(f"  • {item['name']} - {item['cost']}g, {item['stats_count']} stats")
    
    if placeholder_items:
        print("\n❌ ITEMS STILL NEEDING REAL DATA:")
        for item in placeholder_items:
            print(f"  • {item['name']} - {item['cost']}g, {item['stats_count']} stats")
            print(f"    Description: {item['description']}")
    
    return len(placeholder_items) == 0

if __name__ == "__main__":
    all_valid = validate_item_data()
    if all_valid:
        print("\n🎉 ALL ITEMS HAVE REAL WILD RIFT DATA!")
    else:
        print("\n⚠️  Some items still need real data updates.")