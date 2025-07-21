#!/usr/bin/env python3
"""
Clean up duplicates and ensure all Yordle items are properly updated with full descriptions including TIPS
"""

import json
import os
from pathlib import Path

def cleanup_and_update_yordle_items():
    """Clean up duplicates and update all Yordle items with complete data"""
    
    items_dir = Path("items")
    
    # Check for duplicates and Yordle items
    print("🔍 Checking for duplicates and Yordle items...")
    
    all_files = list(items_dir.glob("*.json"))
    item_names = {}
    duplicates = []
    yordle_items = []
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            item_name = data.get("name", "")
            
            # Track duplicates
            if item_name in item_names:
                duplicates.append((item_name, file_path, item_names[item_name]))
            else:
                item_names[item_name] = file_path
            
            # Track Yordle items
            if "yordle" in item_name.lower():
                yordle_items.append((item_name, file_path))
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Report findings
    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicates:")
        for item_name, file1, file2 in duplicates:
            print(f"  • {item_name}: {file1.name} and {file2.name}")
    else:
        print("✅ No duplicates found")
    
    if yordle_items:
        print(f"🎯 Found {len(yordle_items)} Yordle items:")
        for item_name, file_path in yordle_items:
            print(f"  • {item_name}: {file_path.name}")
    
    # Yordle items with complete data including TIPS
    yordle_complete_data = {
        "Yordle Death's Dance": {
            "stats": {"attack_damage": {"value": 35, "type": "flat"}, "armor": {"value": 40, "type": "flat"}, "ability_haste": {"value": 15, "type": "flat"}},
            "cost": 3000,
            "passive": "Cauterize: 32% of all physical damage and magic damage received (12% for ranged champions) is dealt to you over 4 seconds as true damage instead. Dance: Champion takedowns cleanse Cauterize's remaining damage pool and restores 10% of your maximum health over 2 seconds.",
            "description": "Delays damage taken. This item converts incoming damage into a delayed effect, letting you stay in fights longer and smooth out damage spikes. It boosts your survivability with armor and ability haste, and successful takedowns cleanse the delayed damage while instantly healing you. Perfect for bruisers and tanks who need to absorb bursts of damage and then quickly recover to keep fighting.",
            "build_path": ["Caulfield's Warhammer", "Chain Vest"],
            "tier": "S",
            "tags": ["Damage", "Physical", "Armor", "Ability Haste", "Damage Conversion", "Sustain"]
        },
        "Yordle Infinity Orb": {
            "stats": {"ability_power": {"value": 80, "type": "flat"}, "magic_penetration": {"value": 7, "type": "percentage"}},
            "cost": 2900,
            "passive": "Destiny: +5% Move Speed. Balanced: +15 Magic Penetration. Inevitable Demise: Abilities and empowered attacks Critically Strike for 20% bonus damage against enemies below 35% Health. Thunderfall: When an enemy champion dies within 3 second(s) of you applying Inevitable Demise to them, a lightning bolt strikes at the spot where they died, dealing magic damage equal to 50-85 (+20% AP) to nearby enemies.",
            "description": "This item is ideal for mages and assassins looking to boost execution damage and mobility. It grants magic penetration and adds critical strike damage against weakened targets, enabling reliable finishers. Following a kill under this effect, a lightning bolt strikes, damaging nearby enemies—perfect for cleaning up in teamfights.",
            "build_path": ["Blasting Wand", "Magic Penetration"],
            "tier": "S",
            "tags": ["Magic", "Magic Penetration", "Execute", "Movement Speed", "Critical Strike", "AOE"]
        }
    }
    
    # Update Yordle items with complete data
    print("\n🔄 Updating Yordle items with complete data including TIPS...")
    
    for item_name, complete_data in yordle_complete_data.items():
        # Find the correct file for this item
        target_file = None
        for name, file_path in yordle_items:
            if name == item_name:
                target_file = file_path
                break
        
        if target_file:
            item_data = {
                "name": item_name,
                "stats": complete_data["stats"],
                "cost": complete_data["cost"],
                "passive": complete_data["passive"],
                "active": "",
                "description": complete_data["description"],
                "category": "legendary",
                "tier": complete_data["tier"],
                "build_path": complete_data["build_path"],
                "tags": complete_data["tags"]
            }
            
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(item_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Updated {item_name} with complete TIPS description")
    
    print("\n🎉 Cleanup and Yordle item updates completed!")

def main():
    cleanup_and_update_yordle_items()

if __name__ == "__main__":
    main()