#!/usr/bin/env python3
"""
Add missing details (tips, complete descriptions) to all items
"""

import json
import os

def add_missing_details():
    """Add missing tips and complete descriptions to all items"""
    
    # Comprehensive item details database
    item_details = {
        "Hullbreaker": {
            "description": "Split-push focused item that provides Attack Damage, Health, and Ability Haste. When isolated from allies, grants bonus resistances and structure damage while empowering nearby minions. Perfect for split-pushers who want to pressure side lanes and take towers quickly while being harder to kill when caught alone.",
            "tips": [
                "Best used by champions who can split-push effectively like Fiora, Jax, or Tryndamere",
                "The isolation bonus makes you tankier when caught alone - great for 1v1 duels",
                "Empowered minions help take towers faster and draw enemy attention",
                "Great for drawing enemy attention to side lanes while your team groups",
                "The 20 bonus resistances when isolated can be the difference in close fights"
            ]
        },
        "Trinity Force": {
            "description": "Versatile bruiser item that enhances ability-based champions. Provides a mix of offensive and defensive stats with strong synergy for spell-weaving fighters. The Spellblade passive rewards frequent ability usage with enhanced basic attacks, while Threefold Strike provides increasing mobility.",
            "tips": [
                "Perfect for champions who weave abilities between auto attacks like Jax, Irelia, or Camille",
                "The movement speed stacks help with kiting and chasing enemies",
                "Spellblade proc scales with base AD, not bonus AD - great early-mid game",
                "Great on bruisers who need both damage and survivability",
                "Use abilities frequently to maximize the Spellblade damage"
            ]
        },
        "Infinity Edge": {
            "description": "Critical strike item providing massive Attack Damage and Critical Strike Chance. The Perfection passive significantly amplifies critical strike damage when you reach the 60% threshold, making it essential for crit-based marksmen and the cornerstone of most ADC builds.",
            "tips": [
                "Build other crit items first to reach 60% crit chance for maximum effectiveness",
                "The passive bonus is huge - prioritize reaching the 60% threshold",
                "Core item for most ADC champions like Jinx, Caitlyn, and Ashe",
                "Pairs well with other crit items like Phantom Dancer and Runaan's Hurricane",
                "The 35% crit damage bonus applies to all critical strikes, not just from this item"
            ]
        },
        "Rabadon's Deathcap": {
            "description": "High-tier AP item providing massive Ability Power. The Magical Opus passive amplifies all your AP by 40%, making it the ultimate damage multiplier for mages. Best built when you already have some AP items to maximize the percentage bonus.",
            "tips": [
                "Build after other AP items to maximize the 40% bonus effect",
                "The passive applies to ALL ability power, including from other items and runes",
                "Essential for burst mages and late-game scaling champions",
                "Expensive but provides the highest AP scaling in the game",
                "Great on champions like Orianna, Syndra, and Brand who scale well with AP"
            ]
        },
        "Guardian Angel": {
            "description": "Defensive item that provides Attack Damage and Armor with a powerful revival passive. The Rebirth effect gives you a second chance in team fights, making it invaluable for carries who need to stay alive to deal damage.",
            "tips": [
                "Great for ADCs and assassins who are high-priority targets",
                "The revival gives your team time to help you or disengage",
                "Long cooldown means positioning is still crucial",
                "Can bait enemies into overcommitting when they see the passive is up",
                "Consider building when you're ahead and want to maintain your lead"
            ]
        },
        "Frozen Heart": {
            "description": "Tank item providing Armor, Mana, and Ability Haste with attack speed reduction auras. Excellent against auto-attack heavy compositions, reducing both your damage taken and nearby enemies' attack speed.",
            "tips": [
                "Perfect against teams with multiple auto-attack champions",
                "The aura affects all nearby enemies, great for team fights",
                "Provides mana for ability-hungry tanks like Malphite or Maokai",
                "The attack speed reduction stacks with the passive slow effect",
                "Great on champions who want to stay in the middle of fights"
            ]
        },
        "Edge of Night": {
            "description": "Lethality item that provides Attack Damage, Health, and a spell shield. The Annul passive blocks one enemy ability, making it great for assassins who need to avoid key crowd control or damage abilities.",
            "tips": [
                "Great for assassins who need to avoid key CC abilities",
                "The spell shield has a moderate cooldown - use it wisely",
                "Provides some health for survivability unlike other lethality items",
                "Perfect against teams with crucial single-target abilities",
                "Can block ultimates and other high-impact abilities"
            ]
        },
        "Yordle Death's Dance": {
            "description": "Defensive damage item that provides Attack Damage and resistances with damage mitigation. The Ignore Pain passive spreads damage over time, while takedowns provide healing and cleanse remaining damage.",
            "tips": [
                "Excellent for sustained fights and team battles",
                "The damage delay can save you from burst combos",
                "Takedowns cleanse remaining damage - great for multi-kills",
                "Provides both armor and magic resist for mixed damage",
                "Perfect for bruisers and fighters who stay in extended fights"
            ]
        },
        "Crystalline Reflector": {
            "description": "AP item that provides Ability Power and Armor with a damage reflection passive. Great for AP champions who need armor against AD threats while still dealing damage.",
            "tips": [
                "Perfect for AP champions facing heavy AD compositions",
                "The reflection damage scales with AP",
                "Great on champions like Malphite or Rammus who can build AP",
                "Provides both offense and defense in one item",
                "The reflection triggers on basic attacks, not abilities"
            ]
        },
        "Duskblade of Draktharr": {
            "description": "Lethality item providing Attack Damage with stealth and bonus damage. The Nightstalker passive grants invisibility after takedowns and enhances your next attack, perfect for assassins looking to chain kills.",
            "tips": [
                "Perfect for assassins who want to chain kills in team fights",
                "The invisibility helps you reposition or escape after kills",
                "Bonus damage scales with your AD - great for snowballing",
                "Long cooldown means you need to make the stealth count",
                "Great on champions like Zed, Talon, and Kha'Zix"
            ]
        },
        "Harmonic Echo": {
            "description": "AP item that provides Ability Power with echo damage on abilities. Great for poke champions and those who can proc the echo effect frequently in team fights.",
            "tips": [
                "Great for champions with low-cooldown abilities",
                "The echo effect has a per-target cooldown",
                "Perfect for poke compositions and siege scenarios",
                "Works well with AOE abilities that hit multiple targets",
                "Good on champions like Ziggs, Xerath, and Lux"
            ]
        }
    }
    
    items_dir = 'items'
    if not os.path.exists(items_dir):
        print("Items directory not found!")
        return
    
    enhanced_count = 0
    
    for filename in os.listdir(items_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(items_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                item_data = json.load(f)
            
            item_name = item_data.get('name', '')
            if not item_name:
                continue
            
            # Add missing details if available
            if item_name in item_details:
                details = item_details[item_name]
                
                # Update description if it's incomplete
                if 'description' in details:
                    current_desc = item_data.get('description', '')
                    if not current_desc or '...' in current_desc or len(current_desc) < 100:
                        item_data['description'] = details['description']
                
                # Add tips if missing
                if 'tips' in details and not item_data.get('tips'):
                    item_data['tips'] = details['tips']
                
                # Save updated data
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(item_data, f, indent=2, ensure_ascii=False)
                
                print(f"Enhanced {item_name}")
                enhanced_count += 1
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\nCompleted! Enhanced {enhanced_count} items with missing details.")

if __name__ == "__main__":
    add_missing_details()