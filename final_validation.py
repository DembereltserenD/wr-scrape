#!/usr/bin/env python3
"""
Final comprehensive validation to ensure ALL items have real Wild Rift data and descriptions
"""

import json
import os
from pathlib import Path

def final_validation():
    """Comprehensive validation of all item data"""
    items_dir = Path("items")
    
    if not items_dir.exists():
        print("Items directory not found!")
        return
    
    # All possible placeholder indicators
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
        "Boot enhancement that provides additional active o",
        "Tank item that provides defensive stats and utilit",
        "Wild Rift item with real stats and effects from wr-meta.com"
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
            
            # Check for empty or minimal data
            stats = data.get("stats", {})
            cost = data.get("cost", 0)
            name = data.get("name", "Unknown")
            
            # Additional checks for real data
            has_real_description = len(description) > 20 and not has_placeholder
            has_meaningful_stats = len(stats) > 0 and cost > 0
            
            if has_placeholder or not has_real_description or not has_meaningful_stats:
                placeholder_items.append({
                    "file": item_file.name,
                    "name": name,
                    "cost": cost,
                    "stats_count": len(stats),
                    "description": data.get("description", "")[:80] + "..." if len(data.get("description", "")) > 80 else data.get("description", ""),
                    "passive": data.get("passive", "")[:50] + "..." if len(data.get("passive", "")) > 50 else data.get("passive", "")
                })
            else:
                valid_items.append({
                    "file": item_file.name,
                    "name": name,
                    "cost": cost,
                    "stats_count": len(stats),
                    "tier": data.get("tier", "Unknown")
                })
                
        except Exception as e:
            print(f"Error reading {item_file}: {e}")
    
    print(f"📊 FINAL VALIDATION RESULTS:")
    print(f"✅ Valid items with real Wild Rift data: {len(valid_items)}")
    print(f"❌ Items with placeholder/incomplete data: {len(placeholder_items)}")
    print()
    
    if valid_items:
        print("✅ ITEMS WITH COMPLETE REAL WILD RIFT DATA:")
        for item in sorted(valid_items, key=lambda x: x['name']):
            print(f"  • {item['name']} - {item['cost']}g, {item['stats_count']} stats, Tier {item['tier']}")
    
    if placeholder_items:
        print(f"\n❌ ITEMS STILL NEEDING REAL DATA ({len(placeholder_items)}):")
        for item in placeholder_items:
            print(f"  • {item['name']} - {item['cost']}g, {item['stats_count']} stats")
            print(f"    Description: {item['description']}")
            if item['passive']:
                print(f"    Passive: {item['passive']}")
            print()
    
    # Summary
    total_items = len(valid_items) + len(placeholder_items)
    completion_rate = (len(valid_items) / total_items * 100) if total_items > 0 else 0
    
    print(f"📈 COMPLETION RATE: {completion_rate:.1f}% ({len(valid_items)}/{total_items})")
    
    if len(placeholder_items) == 0:
        print("\n🎉 PERFECT! ALL ITEMS HAVE REAL WILD RIFT DATA!")
        print("🚀 Database is 100% complete with authentic Wild Rift information!")
    else:
        print(f"\n⚠️  {len(placeholder_items)} items still need real data updates.")
    
    return len(placeholder_items) == 0

if __name__ == "__main__":
    final_validation()