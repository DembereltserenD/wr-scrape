#!/usr/bin/env python3
"""
Fix ALL existing items to have proper Wild Rift descriptions instead of generic ones
"""

import json
import os
from pathlib import Path

def generate_proper_description(item_data):
    """Generate a proper Wild Rift description based on item data"""
    name = item_data.get("name", "")
    stats = item_data.get("stats", {})
    passive = item_data.get("passive", "")
    active = item_data.get("active", "")
    cost = item_data.get("cost", 0)
    
    # Build stats description
    stat_descriptions = []
    if "attack_damage" in stats:
        stat_descriptions.append(f"{stats['attack_damage']['value']} Attack Damage")
    if "ability_power" in stats:
        stat_descriptions.append(f"{stats['ability_power']['value']} Ability Power")
    if "health" in stats:
        stat_descriptions.append(f"{stats['health']['value']} Health")
    if "armor" in stats:
        stat_descriptions.append(f"{stats['armor']['value']} Armor")
    if "magic_resist" in stats:
        stat_descriptions.append(f"{stats['magic_resist']['value']} Magic Resist")
    if "lethality" in stats:
        stat_descriptions.append(f"{stats['lethality']['value']} Lethality")
    if "critical_chance" in stats:
        stat_descriptions.append(f"{stats['critical_chance']['value']}% Critical Strike Chance")
    if "attack_speed" in stats:
        stat_descriptions.append(f"{stats['attack_speed']['value']}% Attack Speed")
    if "cooldown_reduction" in stats:
        stat_descriptions.append(f"{stats['cooldown_reduction']['value']}% Cooldown Reduction")
    if "mana" in stats:
        stat_descriptions.append(f"{stats['mana']['value']} Mana")
    if "movement_speed" in stats:
        if stats['movement_speed']['type'] == 'percentage':
            stat_descriptions.append(f"{stats['movement_speed']['value']}% Movement Speed")
        else:
            stat_descriptions.append(f"{stats['movement_speed']['value']} Movement Speed")
    if "magic_penetration" in stats:
        stat_descriptions.append(f"{stats['magic_penetration']['value']} Magic Penetration")
    if "armor_penetration" in stats:
        stat_descriptions.append(f"{stats['armor_penetration']['value']}% Armor Penetration")
    if "omnivamp" in stats:
        stat_descriptions.append(f"{stats['omnivamp']['value']}% Omnivamp")
    if "physical_vamp" in stats:
        stat_descriptions.append(f"{stats['physical_vamp']['value']}% Physical Vamp")
    
    stats_text = ", ".join(stat_descriptions) if stat_descriptions else "various stats"
    
    # Create description based on item type and effects
    if "Enchant" in name:
        if active:
            return f"Boot enchantment that provides {stats_text}. {active[:60]}..."
        else:
            return f"Boot enchantment that provides {stats_text} and additional effects."
    
    elif any(word in name.lower() for word in ["boots", "greaves", "treads"]):
        base_desc = f"Provides {stats_text} and enhanced movement."
        if passive:
            return f"{base_desc} {passive[:50]}..."
        return base_desc
    
    elif "lethality" in stats or any(word in name.lower() for word in ["duskblade", "eclipse", "youmuu", "serpent"]):
        base_desc = f"Assassin item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Enhances burst damage against squishy targets."
    
    elif "critical_chance" in stats or any(word in name.lower() for word in ["infinity", "bloodthirster", "essence"]):
        base_desc = f"Critical strike item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Core item for ADC champions."
    
    elif "ability_power" in stats:
        base_desc = f"Ability Power item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Enhances magical damage and abilities."
    
    elif "armor" in stats and stats["armor"]["value"] > 40:
        base_desc = f"Tank item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Provides defensive capabilities against physical damage."
    
    elif "magic_resist" in stats and stats["magic_resist"]["value"] > 40:
        base_desc = f"Magic resistance item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Provides defensive capabilities against magical damage."
    
    elif "health" in stats and stats["health"]["value"] > 300:
        base_desc = f"Health item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Increases survivability and tankiness."
    
    elif any(word in name.lower() for word in ["support", "sickle", "coin", "shield"]):
        base_desc = f"Support item that provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        return f"{base_desc} Designed for support champions to aid their team."
    
    else:
        base_desc = f"Provides {stats_text}."
        if passive:
            return f"{base_desc} {passive[:60]}..."
        elif active:
            return f"{base_desc} {active[:60]}..."
        return f"{base_desc} Enhances champion capabilities in Wild Rift."

def fix_all_descriptions():
    """Fix all item descriptions"""
    items_dir = Path("items")
    fixed_count = 0
    
    for item_file in items_dir.glob("*.json"):
        try:
            with open(item_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            current_desc = data.get("description", "")
            
            # Check if it has the generic description
            if "Wild Rift item with real stats and effects from wr-meta.com" in current_desc:
                # Generate proper description
                new_description = generate_proper_description(data)
                data["description"] = new_description
                
                # Write back to file
                with open(item_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Fixed description for {data.get('name', 'Unknown')}")
                fixed_count += 1
                
        except Exception as e:
            print(f"Error processing {item_file}: {e}")
    
    print(f"🎉 Fixed {fixed_count} item descriptions!")

if __name__ == "__main__":
    fix_all_descriptions()