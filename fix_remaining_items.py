#!/usr/bin/env python3
"""
Fix the remaining problematic items
"""

import json
import os
from pathlib import Path

def fix_remaining_items():
    """Fix the last few problematic items"""
    
    # Fix Serylda's Grudge with real data
    seryldas_data = {
        "name": "Serylda's Grudge",
        "stats": {
            "attack_damage": {"value": 45, "type": "flat"},
            "armor_penetration": {"value": 30, "type": "percentage"},
            "cooldown_reduction": {"value": 20, "type": "percentage"}
        },
        "cost": 3200,
        "passive": "Bitter Cold: Damaging an enemy champion with an Ability slows them by 30% for 1 second.",
        "active": "",
        "description": "Wild Rift item with real stats and effects from wr-meta.com",
        "category": "legendary",
        "tier": "A",
        "build_path": ["Last Whisper", "Caulfield's Warhammer"],
        "tags": ["Damage", "Physical", "Armor Penetration", "CDR", "Slow"]
    }
    
    # Try to find and fix the Serylda file
    items_dir = Path("items")
    for item_file in items_dir.glob("*serylda*"):
        print(f"Found Serylda file: {item_file}")
        with open(item_file, 'w', encoding='utf-8') as f:
            json.dump(seryldas_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Fixed {item_file}")
    
    # Remove unknown.json if it exists
    unknown_file = items_dir / "unknown.json"
    if unknown_file.exists():
        unknown_file.unlink()
        print("✅ Removed unknown.json")
    
    # Check for index.json and remove if it's not a real item
    index_file = items_dir / "index.json"
    if index_file.exists():
        try:
            with open(index_file, 'r') as f:
                data = json.load(f)
            if data.get("name") == "Unknown" or not data.get("stats"):
                index_file.unlink()
                print("✅ Removed invalid index.json")
        except:
            index_file.unlink()
            print("✅ Removed corrupted index.json")

if __name__ == "__main__":
    fix_remaining_items()
    print("🎉 All remaining items fixed!")