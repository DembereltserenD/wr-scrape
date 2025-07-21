#!/usr/bin/env python3
"""
Fix all remaining items by adding tips and complete descriptions
"""

import json
import os
import re
import random

class ItemEnhancer:
    def __init__(self):
        self.items_dir = 'items'
        
        # Template tips for different item types
        self.tip_templates = {
            # Damage items
            "damage": [
                "Great for champions who want to maximize their damage output",
                "Synergizes well with other damage items for burst potential",
                "Consider building this when ahead to snowball your advantage",
                "Effective against squishy targets with low resistances",
                "Pairs well with champions who have high AD/AP ratios"
            ],
            # Tank items
            "tank": [
                "Excellent for frontline champions who need to absorb damage",
                "Build this when facing heavy {damage_type} damage compositions",
                "The resistances help you survive longer in team fights",
                "Great for engaging champions who need to withstand initial burst",
                "Consider building this when your team needs a durable frontline"
            ],
            # Support items
            "support": [
                "Perfect for enhancing your team's capabilities",
                "Helps protect and empower your carries",
                "The active/passive effect can turn the tide of team fights",
                "Position properly to maximize the benefit to your team",
                "Great for champions who focus on utility over damage"
            ],
            # Boots
            "boots": [
                "The movement speed helps with map rotations and positioning",
                "Consider these boots when facing teams with heavy {damage_type}",
                "The unique effect complements {champion_type} champions",
                "Great for both engaging and disengaging from fights",
                "Can be upgraded with enchantments for additional effects"
            ],
            # Ability-focused items
            "ability": [
                "Perfect for champions who rely heavily on abilities",
                "The cooldown reduction/ability haste maximizes spell uptime",
                "Synergizes well with champions who have low cooldowns",
                "Great for ability-spamming champions",
                "Consider building this when you need to cast abilities frequently"
            ],
            # Attack speed items
            "attack_speed": [
                "Excellent for champions who rely on basic attacks",
                "Helps with last hitting and taking objectives faster",
                "Synergizes well with on-hit effects",
                "Great for sustained damage output in extended fights",
                "Consider building this on champions with attack resets or steroids"
            ],
            # Mana items
            "mana": [
                "Perfect for champions with high mana consumption",
                "Helps sustain your presence in lane without frequent recalls",
                "The mana pool allows for extended ability usage in fights",
                "Great for champions who need to spam abilities",
                "Consider building this when you find yourself frequently out of mana"
            ],
            # Lethality/penetration items
            "penetration": [
                "Excellent against targets building resistances",
                "The penetration helps maintain damage relevance as the game progresses",
                "Great for assassins looking to eliminate priority targets",
                "Synergizes well with other penetration items for maximum effect",
                "Consider building this when enemies start stacking armor/magic resist"
            ],
            # Healing/sustain items
            "sustain": [
                "Provides excellent sustain in lane and during fights",
                "The healing/lifesteal helps you stay in fights longer",
                "Great for champions who take extended trades",
                "Consider building this when you need to survive poke or DOT damage",
                "Synergizes well with champions who deal consistent damage"
            ],
            # Movement items
            "movement": [
                "The movement speed helps with roaming and map presence",
                "Great for champions who need to reposition frequently in fights",
                "Helps with both engaging and disengaging from unfavorable situations",
                "Consider building this when you need to kite or chase effectively",
                "Synergizes well with champions who rely on positioning"
            ],
            # Utility items
            "utility": [
                "Provides unique utility that can change fight dynamics",
                "The active/passive effect creates opportunities for your team",
                "Great for creating picks or saving teammates",
                "Consider building this when your team needs additional utility",
                "Effective when used at the right moment in team fights"
            ]
        }
        
        # Specific tips for common items
        self.specific_item_tips = {
            "Black Cleaver": [
                "Great against teams with multiple tanks or bruisers",
                "The armor shred benefits your entire team's physical damage",
                "Stack the effect quickly with multi-hit abilities",
                "Perfect for bruisers who deal sustained physical damage",
                "Synergizes well with other armor penetration items"
            ],
            "Bloodthirster": [
                "The shield from Overheal provides extra survivability",
                "Great for ADCs who need sustain and damage",
                "Build this when you need to survive burst damage",
                "The lifesteal allows you to heal from minions between fights",
                "Consider building this against poke compositions"
            ],
            "Luden's Echo": [
                "Great for mages who want to burst and poke",
                "The movement speed helps with kiting and positioning",
                "The echo effect helps with waveclear and AOE damage",
                "Perfect for champions with long-range abilities",
                "Consider building this as a first item on burst mages"
            ],
            "Sunfire Aegis": [
                "Perfect for tanks who want to deal consistent AOE damage",
                "The immolate effect helps with waveclear and jungle clear",
                "Stack the effect in extended fights for maximum damage",
                "Great for champions who can stay in the middle of fights",
                "Consider building this when you need to apply constant pressure"
            ],
            "Void Staff": [
                "Essential against teams building magic resistance",
                "The percentage penetration scales well into late game",
                "Great for maintaining damage relevance as MR increases",
                "Consider building this as a second or third item on mages",
                "Particularly effective when enemies have over 100 MR"
            ],
            "Morellonomicon": [
                "Essential against teams with healing or lifesteal",
                "Applies Grievous Wounds to reduce enemy healing",
                "Great for dealing with champions like Soraka, Dr. Mundo, or Vladimir",
                "The health provides some survivability for mages",
                "Consider building this when facing multiple healing sources"
            ],
            "Thornmail": [
                "Perfect against auto-attack heavy compositions",
                "Applies Grievous Wounds to attackers automatically",
                "Great for tanks who get focused by ADCs",
                "The reflected damage adds up in extended fights",
                "Consider building this against champions like Yasuo, Tryndamere, or Jinx"
            ],
            "Zeke's Convergence": [
                "Bind to your strongest carry for maximum effect",
                "Use your ultimate at the start of team fights to activate the effect",
                "Great for supports who want to amplify their ADC's damage",
                "The stats provide a good mix of offense and defense",
                "Consider building this when your team has a fed carry"
            ],
            "Nashor's Tooth": [
                "Perfect for AP champions who auto-attack frequently",
                "Great on champions like Diana, Kayle, or Teemo",
                "The on-hit damage scales with your AP",
                "Helps with taking objectives and split pushing",
                "Consider building this on hybrid damage champions"
            ],
            "Sterak's Gage": [
                "The shield scales with your bonus health - build health items",
                "Great for surviving burst damage in team fights",
                "Perfect for bruisers and juggernauts",
                "The AD scales with your base AD, benefiting Trinity Force users",
                "Consider building this when you need to frontline for your team"
            ]
        }
    
    def categorize_item(self, item_data):
        """Categorize item based on stats and description"""
        name = item_data.get('name', '')
        stats = item_data.get('stats', {})
        description = item_data.get('description', '').lower()
        tags = item_data.get('tags', [])
        passive = item_data.get('passive', '').lower()
        
        categories = []
        
        # Check for boots
        if 'boots' in name.lower() or 'greaves' in name.lower() or 'treads' in name.lower():
            categories.append('boots')
        
        # Check for damage items
        if 'attack_damage' in stats or 'ability_power' in stats:
            if 'attack_damage' in stats:
                categories.append('damage')
            if 'ability_power' in stats:
                categories.append('ability')
        
        # Check for tank items
        if 'health' in stats or 'armor' in stats or 'magic_resist' in stats:
            categories.append('tank')
        
        # Check for attack speed items
        if 'attack_speed' in stats:
            categories.append('attack_speed')
        
        # Check for mana items
        if 'mana' in stats:
            categories.append('mana')
        
        # Check for penetration items
        if any(x in description for x in ['penetration', 'lethality', 'ignore']):
            categories.append('penetration')
        
        # Check for sustain items
        if any(x in description for x in ['heal', 'lifesteal', 'vamp', 'regen']):
            categories.append('sustain')
        
        # Check for movement items
        if 'movement_speed' in stats or any(x in description for x in ['movement speed', 'mobility']):
            categories.append('movement')
        
        # Check for support items
        if any(x in description for x in ['ally', 'allies', 'shield', 'protect', 'support']):
            categories.append('support')
        
        # Check for utility items
        if any(x in description for x in ['active', 'slow', 'stun', 'immobilize', 'shield']):
            categories.append('utility')
        
        # Check tags
        for tag in tags:
            tag = tag.lower()
            if 'damage' in tag or 'physical' in tag or 'critical' in tag:
                categories.append('damage')
            elif 'magic' in tag or 'ap' in tag:
                categories.append('ability')
            elif 'tank' in tag or 'health' in tag or 'armor' in tag or 'resist' in tag:
                categories.append('tank')
            elif 'support' in tag or 'heal' in tag or 'shield' in tag:
                categories.append('support')
            elif 'movement' in tag or 'speed' in tag:
                categories.append('movement')
            elif 'sustain' in tag or 'lifesteal' in tag or 'vamp' in tag:
                categories.append('sustain')
        
        # Remove duplicates
        categories = list(set(categories))
        
        # Default to utility if no categories found
        if not categories:
            categories.append('utility')
        
        return categories
    
    def generate_tips(self, item_data):
        """Generate tips for an item based on its properties"""
        name = item_data.get('name', '')
        
        # Check if we have specific tips for this item
        if name in self.specific_item_tips:
            return self.specific_item_tips[name]
        
        # Categorize the item
        categories = self.categorize_item(item_data)
        
        # Generate tips based on categories
        tips = []
        for category in categories[:2]:  # Use up to 2 categories
            if category in self.tip_templates:
                # Get template tips for this category
                category_tips = self.tip_templates[category].copy()
                
                # Fill in placeholders
                filled_tips = []
                for tip in category_tips:
                    if '{damage_type}' in tip:
                        if 'magic_resist' in item_data.get('stats', {}):
                            tip = tip.replace('{damage_type}', 'magic')
                        elif 'armor' in item_data.get('stats', {}):
                            tip = tip.replace('{damage_type}', 'physical')
                        else:
                            tip = tip.replace('{damage_type}', 'mixed')
                    
                    if '{champion_type}' in tip:
                        if 'attack_damage' in item_data.get('stats', {}):
                            tip = tip.replace('{champion_type}', 'AD')
                        elif 'ability_power' in item_data.get('stats', {}):
                            tip = tip.replace('{champion_type}', 'AP')
                        else:
                            tip = tip.replace('{champion_type}', 'tank')
                    
                    filled_tips.append(tip)
                
                # Add tips from this category
                tips.extend(filled_tips[:3])  # Add up to 3 tips from each category
        
        # Add a generic tip if we don't have enough
        if len(tips) < 3:
            tips.append("Consider the item's cost efficiency when deciding your build order")
            tips.append("This item works well in both early and late game situations")
        
        # Ensure we have at least 3 tips but no more than 5
        return tips[:5]
    
    def enhance_item_description(self, item_data):
        """Enhance item description if it's incomplete"""
        description = item_data.get('description', '')
        
        # Check if description is incomplete
        if not description or '...' in description or len(description) < 50:
            name = item_data.get('name', '')
            stats = item_data.get('stats', {})
            passive = item_data.get('passive', '')
            active = item_data.get('active', '')
            
            # Build a more complete description
            stat_descriptions = []
            for stat, value in stats.items():
                if stat == 'attack_damage':
                    stat_descriptions.append(f"Attack Damage")
                elif stat == 'ability_power':
                    stat_descriptions.append(f"Ability Power")
                elif stat == 'health':
                    stat_descriptions.append(f"Health")
                elif stat == 'armor':
                    stat_descriptions.append(f"Armor")
                elif stat == 'magic_resist':
                    stat_descriptions.append(f"Magic Resist")
                elif stat == 'attack_speed':
                    stat_descriptions.append(f"Attack Speed")
                elif stat == 'cooldown_reduction' or stat == 'ability_haste':
                    stat_descriptions.append(f"Ability Haste")
                elif stat == 'movement_speed':
                    stat_descriptions.append(f"Movement Speed")
            
            stat_text = ", ".join(stat_descriptions)
            
            # Create description based on item type
            if 'boots' in name.lower() or 'greaves' in name.lower() or 'treads' in name.lower():
                new_desc = f"Boots that provide {stat_text}. "
            else:
                new_desc = f"Item that provides {stat_text}. "
            
            # Add passive/active info
            if passive:
                passive_clean = re.sub(r'^[^:]+:', '', passive).strip()
                new_desc += f"Passive effect: {passive_clean}. "
            
            if active:
                active_clean = re.sub(r'^[^:]+:', '', active).strip()
                new_desc += f"Active effect: {active_clean}. "
            
            # Add usage hint
            categories = self.categorize_item(item_data)
            if 'damage' in categories:
                new_desc += "Great for champions looking to maximize their damage output."
            elif 'tank' in categories:
                new_desc += "Perfect for frontline champions who need to absorb damage."
            elif 'support' in categories:
                new_desc += "Excellent for supporting allies and enhancing team capabilities."
            elif 'boots' in categories:
                new_desc += "Provides essential mobility for map rotations and positioning."
            else:
                new_desc += "A versatile item that can benefit many champion types."
            
            return new_desc
        
        return description
    
    def enhance_all_items(self):
        """Enhance all items with tips and complete descriptions"""
        if not os.path.exists(self.items_dir):
            print("Items directory not found!")
            return
        
        item_files = [f for f in os.listdir(self.items_dir) if f.endswith('.json')]
        print(f"Found {len(item_files)} item files to enhance")
        
        enhanced_count = 0
        for item_file in item_files:
            item_path = os.path.join(self.items_dir, item_file)
            
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                
                item_name = item_data.get('name', '')
                if not item_name:
                    continue
                
                # Check if tips are missing
                tips = item_data.get('tips', [])
                if not tips:
                    # Generate tips
                    item_data['tips'] = self.generate_tips(item_data)
                    
                    # Enhance description if needed
                    current_desc = item_data.get('description', '')
                    if not current_desc or '...' in current_desc or len(current_desc) < 50:
                        item_data['description'] = self.enhance_item_description(item_data)
                    
                    # Save enhanced data
                    with open(item_path, 'w', encoding='utf-8') as f:
                        json.dump(item_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Enhanced {item_name}")
                    enhanced_count += 1
                
            except Exception as e:
                print(f"Error processing {item_file}: {e}")
        
        print(f"\nCompleted! Enhanced {enhanced_count} items with missing details.")

def main():
    enhancer = ItemEnhancer()
    enhancer.enhance_all_items()

if __name__ == "__main__":
    main()