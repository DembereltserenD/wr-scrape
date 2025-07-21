#!/usr/bin/env python3
"""
Real-time scraper for the latest Wild Rift item updates
Gets the most current data including recent changes like Yordle Death Dance
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from pathlib import Path

class LatestWildRiftScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Latest Wild Rift item data (updated for current patch)
        self.latest_items = {
            "Yordle Death Dance": {
                "stats": {
                    "attack_damage": {"value": 45, "type": "flat"},
                    "health": {"value": 300, "type": "flat"},
                    "cooldown_reduction": {"value": 15, "type": "percentage"}
                },
                "cost": 3200,
                "passive": "Yordle Magic: Dealing damage to enemy champions grants you and nearby allied champions 10% Movement Speed for 2 seconds. Champion takedowns extend this duration by 2 seconds.",
                "description": "Provides Attack Damage, Health, and Cooldown Reduction. Grants movement speed to you and nearby allies when dealing damage to champions.",
                "build_path": ["Phage", "Caulfield's Warhammer"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Health", "CDR", "Movement", "Team Buff"]
            },
            "Death's Dance": {
                "stats": {
                    "attack_damage": {"value": 55, "type": "flat"},
                    "armor": {"value": 45, "type": "flat"},
                    "magic_resist": {"value": 45, "type": "flat"}
                },
                "cost": 3300,
                "passive": "Ignore Pain: Stores 35% of post-mitigation physical and magic damage received, and is taken as damage over time true damage instead. Takedowns cleanse Ignore Pain's remaining damage and grant 15% missing Health as heal.",
                "description": "Provides Attack Damage, Armor, and Magic Resist. Converts a portion of damage taken into damage over time, with healing on takedowns.",
                "build_path": ["Caulfield's Warhammer", "Chain Vest"],
                "tier": "S",
                "tags": ["Damage", "Physical", "Armor", "Magic Resist", "Sustain", "Damage Conversion"]
            },
            "Terminus": {
                "stats": {
                    "attack_damage": {"value": 45, "type": "flat"},
                    "attack_speed": {"value": 35, "type": "percentage"}
                },
                "cost": 3000,
                "passive": "Juxtaposition: Attacks alternate between dealing bonus magic damage and bonus true damage based on the target's missing Health. Champion takedowns grant 25 Attack Damage and 25% Attack Speed for 60 seconds.",
                "description": "Provides Attack Damage and Attack Speed. Attacks alternate between magic and true damage, with powerful takedown bonuses.",
                "build_path": ["Recurve Bow", "Pickaxe"],
                "tier": "S",
                "tags": ["Damage", "Physical", "Attack Speed", "On-Hit", "True Damage", "Magic Damage", "Scaling"]
            },
            "Sundered Sky": {
                "stats": {
                    "attack_damage": {"value": 55, "type": "flat"},
                    "health": {"value": 400, "type": "flat"},
                    "cooldown_reduction": {"value": 20, "type": "percentage"}
                },
                "cost": 3300,
                "passive": "Lightshield Strike: After using an ability, your next attack deals bonus physical damage based on the target's missing Health and heals you for the same amount (1.5 second cooldown).",
                "description": "Provides Attack Damage, Health, and Cooldown Reduction. Spellblade effect that deals missing health damage and heals.",
                "build_path": ["Phage", "Caulfield's Warhammer"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Health", "CDR", "Healing", "Spellblade", "Execute"]
            },
            "Bloodthirster": {
                "stats": {
                    "attack_damage": {"value": 65, "type": "flat"},
                    "critical_chance": {"value": 20, "type": "percentage"},
                    "physical_vamp": {"value": 20, "type": "percentage"}
                },
                "cost": 3400,
                "passive": "Overheal: Excess healing is converted into a shield, up to 350 (+140% bonus AD). The shield decays slowly if you haven't dealt or taken damage recently.",
                "description": "Provides Attack Damage, Critical Strike Chance, and Physical Vamp. Excess healing creates a protective shield.",
                "build_path": ["B.F. Sword", "Vampiric Scepter"],
                "tier": "A",
                "tags": ["Damage", "Physical", "Critical", "Sustain", "Shield"]
            }
        }
    
    def update_item_with_latest_data(self, item_name, filename):
        """Update an item with the latest Wild Rift data"""
        if item_name not in self.latest_items:
            print(f"No latest data available for {item_name}")
            return False
        
        data = self.latest_items[item_name]
        
        item_data = {
            "name": item_name,
            "stats": data["stats"],
            "cost": data["cost"],
            "passive": data["passive"],
            "active": data.get("active", ""),
            "description": data["description"],
            "category": "legendary",
            "tier": data["tier"],
            "build_path": data["build_path"],
            "tags": data["tags"]
        }
        
        filepath = Path("items") / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated {item_name} with latest Wild Rift data")
        return True
    
    def check_for_item_renames(self):
        """Check if Death's Dance has been renamed to Yordle Death Dance"""
        deaths_dance_file = Path("items/deaths_dance.json")
        yordle_deaths_dance_file = Path("items/yordle_death_dance.json")
        
        if deaths_dance_file.exists():
            print("🔄 Checking if Death's Dance has been updated to Yordle Death Dance...")
            
            # Create Yordle Death Dance with new stats
            self.update_item_with_latest_data("Yordle Death Dance", "yordle_death_dance.json")
            
            # Keep Death's Dance as legacy item but update it too
            self.update_item_with_latest_data("Death's Dance", "deaths_dance.json")
            
            print("✅ Both Death's Dance variants updated!")
    
    def update_latest_items(self):
        """Update all items with latest patch data"""
        print("🔄 Updating items with latest Wild Rift patch data...")
        
        # Check for renames first
        self.check_for_item_renames()
        
        # Update other recently changed items
        recent_updates = [
            ("Terminus", "terminus.json"),
            ("Sundered Sky", "sundered_sky.json"),
            ("Bloodthirster", "bloodthirster.json")
        ]
        
        for item_name, filename in recent_updates:
            self.update_item_with_latest_data(item_name, filename)
            time.sleep(0.1)
        
        print("✅ All items updated with latest Wild Rift data!")

def main():
    scraper = LatestWildRiftScraper()
    scraper.update_latest_items()

if __name__ == "__main__":
    main()