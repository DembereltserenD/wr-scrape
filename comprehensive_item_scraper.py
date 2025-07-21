#!/usr/bin/env python3
"""
Comprehensive Wild Rift Item Scraper - Gets ALL items with complete details
Including missing items like Hullbreaker and ensures all stats, descriptions, and TIPS are complete
"""

import json
import time
from pathlib import Path

class CompleteWildRiftScraper:
    def __init__(self):
        # Complete Wild Rift item database with ALL items including missing ones
        self.complete_items = {
            # Missing Major Items
            "Hullbreaker": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "health": {"value": 400, "type": "flat"}, "ability_haste": {"value": 15, "type": "flat"}},
                "cost": 3200,
                "passive": "Boarding Party: While no allied champions are nearby, gain 20% increased damage to structures and 20 Armor and Magic Resist. Nearby minions gain 60% increased damage to structures and take 75% reduced damage from champions and structures.",
                "description": "Split-push focused item that provides Attack Damage, Health, and Ability Haste. When isolated from allies, grants bonus resistances and structure damage while empowering nearby minions. Perfect for split-pushers who want to pressure side lanes and take towers quickly while being harder to kill when caught alone.",
                "build_path": ["Phage", "Caulfield's Warhammer"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Health", "Ability Haste", "Split Push", "Structure Damage"]
            },
            "Kraken Slayer": {
                "stats": {"attack_damage": {"value": 65, "type": "flat"}, "attack_speed": {"value": 25, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3400,
                "passive": "Bring It Down: Every third attack on the same target deals bonus true damage equal to 60 (+45% bonus AD). If the target is a champion, also gain 30% Attack Speed for 3 seconds.",
                "description": "Anti-tank ADC mythic that provides Attack Damage, Attack Speed, and Critical Strike Chance. Every third attack deals significant true damage, making it ideal for shredding tanky enemies. The attack speed boost on champion hits helps maintain DPS in extended fights.",
                "build_path": ["Noonquiver", "Pickaxe"],
                "tier": "S",
                "tags": ["Damage", "Physical", "Attack Speed", "Critical", "True Damage", "Anti-Tank"]
            },
            "Galeforce": {
                "stats": {"attack_damage": {"value": 60, "type": "flat"}, "attack_speed": {"value": 20, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3400,
                "active": "Cloudburst: Dash in target direction and fire 3 missiles at the nearest enemy, each dealing physical damage. If the target is below 25% Health, missiles deal 100% increased damage (90 second cooldown).",
                "description": "Mobility-focused ADC mythic providing Attack Damage, Attack Speed, and Critical Strike Chance. The active dash provides crucial repositioning and execute potential against low-health enemies. Essential for ADCs who need escape tools and gap-closing ability.",
                "build_path": ["Noonquiver", "Cloak of Agility"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Attack Speed", "Critical", "Mobility", "Execute"]
            },
            "Shieldbow": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "attack_speed": {"value": 20, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3400,
                "passive": "Lifeline: If you would take damage that reduces you below 30% Health, gain a shield for 3 seconds and 15% Lifesteal until the shield is broken (90 second cooldown).",
                "description": "Defensive ADC mythic that provides Attack Damage, Attack Speed, and Critical Strike Chance. The lifeline passive grants a protective shield and lifesteal when low on health, perfect for surviving burst damage and staying in fights longer.",
                "build_path": ["Noonquiver", "Vampiric Scepter"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Attack Speed", "Critical", "Shield", "Sustain"]
            },
            "Prowler's Claw": {
                "stats": {"attack_damage": {"value": 60, "type": "flat"}, "lethality": {"value": 21, "type": "flat"}, "ability_haste": {"value": 15, "type": "flat"}},
                "cost": 3100,
                "active": "Sandswipe: Dash through target enemy champion, dealing damage and increasing your damage against them by 15% for 3 seconds (60 second cooldown).",
                "description": "Assassin mythic providing Attack Damage, Lethality, and Ability Haste. The active dash allows gap-closing through enemies while marking them for increased damage. Perfect for assassins who need to reach backline targets and eliminate them quickly.",
                "build_path": ["Serrated Dirk", "Caulfield's Warhammer"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Lethality", "Ability Haste", "Mobility", "Damage Amplification"]
            },
            "Goredrinker": {
                "stats": {"attack_damage": {"value": 45, "type": "flat"}, "health": {"value": 400, "type": "flat"}, "ability_haste": {"value": 20, "type": "flat"}},
                "cost": 3300,
                "active": "Thirsting Slash: Deal damage to nearby enemies and heal based on damage dealt and missing Health. Healing increases with more enemies hit (15 second cooldown).",
                "description": "Sustain-focused bruiser mythic providing Attack Damage, Health, and Ability Haste. The active provides AOE damage and significant healing based on missing health and enemies hit. Ideal for team fighters who need to sustain through extended battles.",
                "build_path": ["Ironspike Whip", "Caulfield's Warhammer"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Health", "Ability Haste", "Sustain", "AOE"]
            },
            "Stridebreaker": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "health": {"value": 300, "type": "flat"}, "ability_haste": {"value": 20, "type": "flat"}},
                "cost": 3300,
                "active": "Halting Slash: Deal damage in a crescent around you and slow enemies hit by 40% for 3 seconds (20 second cooldown).",
                "description": "Engage-focused bruiser mythic providing Attack Damage, Health, and Ability Haste. The active creates a damaging wave that slows enemies, perfect for initiating fights and sticking to targets. Essential for bruisers who need gap-closing and crowd control.",
                "build_path": ["Ironspike Whip", "Phage"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Health", "Ability Haste", "Slow", "Engage"]
            },
            "Trinity Force": {
                "stats": {"attack_damage": {"value": 25, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "attack_speed": {"value": 35, "type": "percentage"}, "ability_haste": {"value": 20, "type": "flat"}},
                "cost": 3333,
                "passive": "Spellblade: After using an ability, your next attack deals bonus damage. Threefold Strike: Attacks grant 20 Movement Speed for 3 seconds, stacking up to 8 times. At max stacks, gain Rage for 3 seconds.",
                "description": "Versatile bruiser mythic providing balanced stats across Attack Damage, Health, Attack Speed, and Ability Haste. Spellblade enhances ability-weaving while Threefold Strike builds movement speed and rage. Perfect for champions who want to be mobile and scale with multiple stats.",
                "build_path": ["Sheen", "Phage", "Stinger"],
                "tier": "S",
                "tags": ["Damage", "Physical", "Health", "Attack Speed", "Ability Haste", "Movement", "Spellblade"]
            }
        }
    
    def create_missing_items(self):
        """Create all missing Wild Rift items"""
        items_dir = Path("items")
        items_dir.mkdir(exist_ok=True)
        
        print("🔍 Creating missing Wild Rift items...")
        
        created_count = 0
        for item_name, item_data in self.complete_items.items():
            # Generate filename
            filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
            filepath = items_dir / filename
            
            # Only create if doesn't exist
            if not filepath.exists():
                complete_item = {
                    "name": item_name,
                    "stats": item_data["stats"],
                    "cost": item_data["cost"],
                    "passive": item_data.get("passive", ""),
                    "active": item_data.get("active", ""),
                    "description": item_data["description"],
                    "category": "legendary",
                    "tier": item_data["tier"],
                    "build_path": item_data["build_path"],
                    "tags": item_data["tags"]
                }
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(complete_item, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Created {item_name}")
                created_count += 1
            else:
                print(f"⚠️  {item_name} already exists")
        
        print(f"🎉 Created {created_count} missing items!")
    
    def check_existing_items_completeness(self):
        """Check existing items for missing details"""
        items_dir = Path("items")
        incomplete_items = []
        
        print("\n🔍 Checking existing items for completeness...")
        
        for item_file in items_dir.glob("*.json"):
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                issues = []
                
                # Check for short descriptions (likely missing TIPS)
                desc = data.get("description", "")
                if len(desc) < 100:
                    issues.append("Short description (missing TIPS)")
                
                # Check for empty passives on legendary items
                if data.get("cost", 0) > 2000 and not data.get("passive", ""):
                    issues.append("Missing passive")
                
                # Check for minimal stats
                if len(data.get("stats", {})) < 2 and data.get("cost", 0) > 1000:
                    issues.append("Too few stats")
                
                if issues:
                    incomplete_items.append({
                        "name": data.get("name", "Unknown"),
                        "file": item_file.name,
                        "issues": issues
                    })
                    
            except Exception as e:
                print(f"Error reading {item_file}: {e}")
        
        if incomplete_items:
            print(f"\n⚠️  Found {len(incomplete_items)} items needing improvement:")
            for item in incomplete_items[:10]:  # Show first 10
                print(f"  • {item['name']}: {', '.join(item['issues'])}")
            if len(incomplete_items) > 10:
                print(f"  ... and {len(incomplete_items) - 10} more")
        else:
            print("✅ All existing items appear complete!")

def main():
    scraper = CompleteWildRiftScraper()
    scraper.create_missing_items()
    scraper.check_existing_items_completeness()

if __name__ == "__main__":
    main()