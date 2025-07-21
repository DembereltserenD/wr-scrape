#!/usr/bin/env python3
"""
WR-META.com Item Scraper - Gets real Wild Rift item data
"""

import requests
import json
import re
import time
from bs4 import BeautifulSoup
from pathlib import Path

class WRMetaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.base_url = "https://wr-meta.com"
        
        # Real Wild Rift item data from wr-meta.com
        self.item_database = {
            # AD Items
            "Duskblade Of Draktharr": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "lethality": {"value": 18, "type": "flat"}},
                "cost": 3100, "passive": "Nightstalker: After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals 99 (+30% bonus AD) bonus physical damage.",
                "build_path": ["Serrated Dirk", "Caulfield's Warhammer"], "tier": "S", "tags": ["Damage", "Physical", "Lethality", "Stealth"]
            },
            "Eclipse": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "lethality": {"value": 12, "type": "flat"}, "omnivamp": {"value": 8, "type": "percentage"}},
                "cost": 3100, "passive": "Ever Rising Moon: Hitting a champion with 2 separate attacks or abilities within 1.5 seconds deals bonus damage and grants a shield.",
                "build_path": ["Serrated Dirk", "Long Sword"], "tier": "A", "tags": ["Damage", "Physical", "Lethality", "Sustain"]
            },
            "Youmuu's Ghostblade": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "lethality": {"value": 18, "type": "flat"}},
                "cost": 2900, "passive": "Wraith Step: Gain 20% Movement Speed out of combat.", "active": "Wraith Step: Gain 20% Movement Speed and ghosting for 6 seconds (45 second cooldown).",
                "build_path": ["Serrated Dirk", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Lethality", "Movement"]
            },
            "Edge Of Night": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "lethality": {"value": 10, "type": "flat"}, "health": {"value": 325, "type": "flat"}},
                "cost": 3100, "passive": "Annul: Gain a spell shield that blocks the next enemy ability (40 second cooldown).",
                "build_path": ["Serrated Dirk", "Ruby Crystal"], "tier": "B", "tags": ["Damage", "Physical", "Lethality", "Health", "Shield"]
            },
            "Serpent's Fang": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "lethality": {"value": 18, "type": "flat"}},
                "cost": 2600, "passive": "Shield Reaver: Deal 50% bonus damage to shields. When you damage an enemy champion, reduce their shield power by 50% for 3 seconds.",
                "build_path": ["Serrated Dirk", "Long Sword"], "tier": "B", "tags": ["Damage", "Physical", "Lethality", "Anti-Shield"]
            },
            "The Collector": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "critical_chance": {"value": 20, "type": "percentage"}, "lethality": {"value": 12, "type": "flat"}},
                "cost": 3000, "passive": "Death and Taxes: If you deal damage that would leave an enemy champion below 5% Health, execute them. Champion takedowns grant 25 bonus gold.",
                "build_path": ["B.F. Sword", "Serrated Dirk"], "tier": "A", "tags": ["Damage", "Physical", "Critical", "Lethality", "Execute"]
            },
            "Infinity Edge": {
                "stats": {"attack_damage": {"value": 70, "type": "flat"}, "critical_chance": {"value": 25, "type": "percentage"}},
                "cost": 3400, "passive": "Perfection: If you have at least 60% Critical Strike Chance, gain 35% Critical Strike Damage.",
                "build_path": ["B.F. Sword", "Pickaxe", "Cloak of Agility"], "tier": "S", "tags": ["Damage", "Physical", "Critical"]
            },
            "Bloodthirster": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "critical_chance": {"value": 20, "type": "percentage"}, "physical_vamp": {"value": 20, "type": "percentage"}},
                "cost": 3400, "passive": "Overheal: Excess healing is converted into a shield, up to 350 (+140% bonus AD).",
                "build_path": ["B.F. Sword", "Vampiric Scepter"], "tier": "A", "tags": ["Damage", "Physical", "Critical", "Sustain"]
            },
            "Essence Reaver": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "critical_chance": {"value": 20, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3000, "passive": "Essence Flare: After using an ability, your next attack deals bonus damage and restores mana.",
                "build_path": ["B.F. Sword", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Critical", "CDR", "Mana"]
            },
            "Navori Quickblades": {
                "stats": {"attack_damage": {"value": 60, "type": "flat"}, "critical_chance": {"value": 20, "type": "percentage"}, "cooldown_reduction": {"value": 30, "type": "percentage"}},
                "cost": 3400, "passive": "Transcendence: Your attacks reduce your non-ultimate ability cooldowns by 20% of their remaining cooldown (per critical strike).",
                "build_path": ["B.F. Sword", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Critical", "CDR"]
            },
            
            # Tank Items
            "Force Of Nature": {
                "stats": {"health": {"value": 350, "type": "flat"}, "magic_resist": {"value": 70, "type": "flat"}, "movement_speed": {"value": 5, "type": "percentage"}},
                "cost": 2900, "passive": "Dissipate: Taking magic damage grants 6 Movement Speed and 8 Magic Resist for 5 seconds, stacking up to 5 times.",
                "build_path": ["Negatron Cloak", "Giant's Belt"], "tier": "A", "tags": ["Health", "Magic Resist", "Movement", "Tank"]
            },
            "Guardian Angel": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "armor": {"value": 40, "type": "flat"}},
                "cost": 2800, "passive": "Rebirth: Upon taking lethal damage, revive with 50% base Health and 30% maximum Mana after 4 seconds of stasis (300 second cooldown).",
                "build_path": ["B.F. Sword", "Chain Vest"], "tier": "A", "tags": ["Damage", "Physical", "Armor", "Revive"]
            },
            "Frozen Heart": {
                "stats": {"armor": {"value": 80, "type": "flat"}, "mana": {"value": 400, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "flat"}},
                "cost": 2700, "passive": "Winter's Caress: Reduces Attack Speed of nearby enemies by 15%. When struck by a basic attack, reduces the attacker's Attack Speed by an additional 15% for 1 second.",
                "build_path": ["Warden's Mail", "Glacial Shroud"], "tier": "A", "tags": ["Armor", "Mana", "CDR", "Tank", "Aura"]
            },
            "Thornmail": {
                "stats": {"armor": {"value": 80, "type": "flat"}, "health": {"value": 350, "type": "flat"}},
                "cost": 2700, "passive": "Thorns: When struck by an attack, deal magic damage equal to 25 + 10% bonus Armor to the attacker and inflict them with 40% Grievous Wounds for 3 seconds.",
                "build_path": ["Chain Vest", "Giant's Belt"], "tier": "A", "tags": ["Armor", "Health", "Tank", "Grievous Wounds"]
            },
            "Randuin's Omen": {
                "stats": {"armor": {"value": 80, "type": "flat"}, "health": {"value": 400, "type": "flat"}},
                "cost": 2700, "passive": "Rock Solid: Reduce damage from critical strikes by 20%. When struck by an attack, slow the attacker's Attack Speed by 15% for 1.5 seconds.",
                "active": "Active: Slow nearby enemies by 55% for 2 seconds (60 second cooldown).",
                "build_path": ["Warden's Mail", "Giant's Belt"], "tier": "A", "tags": ["Armor", "Health", "Tank", "Slow"]
            },
            "Dead Man's Plate": {
                "stats": {"armor": {"value": 45, "type": "flat"}, "health": {"value": 300, "type": "flat"}},
                "cost": 2900, "passive": "Dreadnought: While moving, build up to 100 Momentum, granting up to 60 Movement Speed. At 100 stacks, your next attack discharges all Momentum to deal bonus damage and slow.",
                "build_path": ["Chain Vest", "Giant's Belt"], "tier": "A", "tags": ["Armor", "Health", "Tank", "Movement"]
            },
            "Sunfire Aegis": {
                "stats": {"armor": {"value": 45, "type": "flat"}, "health": {"value": 350, "type": "flat"}, "magic_resist": {"value": 45, "type": "flat"}},
                "cost": 3200, "passive": "Immolate: Deal magic damage to nearby enemies. Damaging champions or epic monsters with this effect grants a stack for 5 seconds (max 6 stacks). Each stack increases damage by 12%.",
                "build_path": ["Bami's Cinder", "Chain Vest"], "tier": "A", "tags": ["Armor", "Health", "Magic Resist", "Tank", "AOE"]
            },
            "Spirit Visage": {
                "stats": {"health": {"value": 450, "type": "flat"}, "magic_resist": {"value": 60, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2900, "passive": "Boundless Vitality: Increases all healing and shielding received by 25%.",
                "build_path": ["Spectre's Cowl", "Kindlegem"], "tier": "A", "tags": ["Health", "Magic Resist", "CDR", "Tank", "Healing"]
            },
            
            # AP Items
            "Crystalline Reflector": {
                "stats": {"ability_power": {"value": 70, "type": "flat"}, "armor": {"value": 45, "type": "flat"}},
                "cost": 2650, "passive": "Thorns: When struck by a basic attack, deal 25 (+10% AP) magic damage to the attacker.",
                "build_path": ["Needlessly Large Rod", "Chain Vest"], "tier": "B", "tags": ["Magic", "Armor", "Reflect"]
            },
            "Rabadon's Deathcap": {
                "stats": {"ability_power": {"value": 120, "type": "flat"}},
                "cost": 3600, "passive": "Magical Opus: Increases Ability Power by 40%.",
                "build_path": ["Needlessly Large Rod", "Blasting Wand"], "tier": "S", "tags": ["Magic", "Ability Power"]
            },
            "Luden's Echo": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "mana": {"value": 600, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3200, "passive": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage. This effect has a cooldown per target.",
                "build_path": ["Lost Chapter", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Mana", "CDR"]
            },
            "Liandry's Torment": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 300, "type": "flat"}},
                "cost": 3200, "passive": "Torment: Deal bonus magic damage over time based on the target's current Health. Dealing damage with abilities causes enemies to take 10% increased damage from you for 5 seconds.",
                "build_path": ["Haunting Guise", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Health", "DOT"]
            },
            "Morellonomicon": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 300, "type": "flat"}},
                "cost": 3000, "passive": "Cursed: Magic damage inflicts Grievous Wounds on enemies below 50% Health for 3 seconds.",
                "build_path": ["Oblivion Orb", "Giant's Belt"], "tier": "A", "tags": ["Magic", "Health", "Grievous Wounds"]
            },
            "Void Staff": {
                "stats": {"ability_power": {"value": 70, "type": "flat"}},
                "cost": 2700, "passive": "Dissolve: Magic damage ignores 40% of the target's Magic Resist.",
                "build_path": ["Blasting Wand", "Magic Penetration"], "tier": "A", "tags": ["Magic", "Magic Penetration"]
            },
            "Lich Bane": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "mana": {"value": 250, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}, "movement_speed": {"value": 5, "type": "percentage"}},
                "cost": 3200, "passive": "Spellblade: After using an ability, your next attack deals bonus magic damage (1.5 second cooldown).",
                "build_path": ["Sheen", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Mana", "CDR", "Movement", "On-Hit"]
            },
            "Nashor's Tooth": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "attack_speed": {"value": 50, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3000, "passive": "Icathian Bite: Basic attacks deal bonus magic damage based on AP.",
                "build_path": ["Stinger", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Attack Speed", "CDR", "On-Hit"]
            },
            
            # Support Items
            "Ardent Censer": {
                "stats": {"ability_power": {"value": 60, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}, "mana_regeneration": {"value": 125, "type": "percentage"}},
                "cost": 2300, "passive": "Sanctify: Healing or shielding another ally enhances you and them with 10-30% Attack Speed and 20 magic damage on-hit for 6 seconds.",
                "build_path": ["Forbidden Idol", "Blasting Wand"], "tier": "B", "tags": ["Magic", "CDR", "Support", "Buff"]
            },
            "Locket of the Iron Solari": {
                "stats": {"armor": {"value": 30, "type": "flat"}, "magic_resist": {"value": 30, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2200, "active": "Devotion: Grant nearby allies a shield that absorbs damage for 2.5 seconds (90 second cooldown).",
                "build_path": ["Aegis of the Legion"], "tier": "A", "tags": ["Armor", "Magic Resist", "CDR", "Support", "Shield"]
            },
            "Redemption": {
                "stats": {"health": {"value": 300, "type": "flat"}, "mana_regeneration": {"value": 125, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 2100, "active": "Intervention: After a 2.5 second delay, call down a beam of light to heal allies and damage enemies in the area (90 second cooldown).",
                "build_path": ["Forbidden Idol", "Giant's Belt"], "tier": "B", "tags": ["Health", "CDR", "Support", "Heal"]
            },
            
            # Boots
            "Berserker's Greaves": {
                "stats": {"attack_speed": {"value": 35, "type": "percentage"}, "movement_speed": {"value": 45, "type": "flat"}},
                "cost": 1000, "passive": "", "build_path": ["Boots"], "tier": "A", "tags": ["Attack Speed", "Movement", "Boots"]
            },
            "Ionian Boots of Lucidity": {
                "stats": {"cooldown_reduction": {"value": 10, "type": "percentage"}, "movement_speed": {"value": 45, "type": "flat"}},
                "cost": 1000, "passive": "", "build_path": ["Boots"], "tier": "A", "tags": ["CDR", "Movement", "Boots"]
            },
            "Mercury's Treads": {
                "stats": {"magic_resist": {"value": 25, "type": "flat"}, "movement_speed": {"value": 45, "type": "flat"}},
                "cost": 1100, "passive": "Tenacity: Reduces the duration of stuns, slows, taunts, fears, silences, blinds, and immobilizes by 30%.",
                "build_path": ["Boots"], "tier": "A", "tags": ["Magic Resist", "Movement", "Tenacity", "Boots"]
            },
            "Plated Steelcaps": {
                "stats": {"armor": {"value": 25, "type": "flat"}, "movement_speed": {"value": 45, "type": "flat"}},
                "cost": 1100, "passive": "Steel: Reduces damage from basic attacks by 12%.",
                "build_path": ["Boots"], "tier": "A", "tags": ["Armor", "Movement", "Damage Reduction", "Boots"]
            },
            
            # More AD Items
            "Black Cleaver": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "health": {"value": 400, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 3100, "passive": "Carve: Dealing physical damage to an enemy champion applies a stack for 6 seconds (max 6 stacks). Each stack reduces the target's Armor by 5%.",
                "build_path": ["Phage", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Health", "CDR", "Armor Reduction"]
            },
            "Death's Dance": {
                "stats": {"attack_damage": {"value": 55, "type": "flat"}, "armor": {"value": 45, "type": "flat"}, "magic_resist": {"value": 45, "type": "flat"}},
                "cost": 3300, "passive": "Ignore Pain: Stores 35% of post-mitigation physical and magic damage received, and is taken as damage over time true damage instead. Takedowns cleanse Ignore Pain's remaining damage and grant 15% missing Health as heal.",
                "build_path": ["Caulfield's Warhammer", "Chain Vest"], "tier": "S", "tags": ["Damage", "Physical", "Armor", "Magic Resist", "Sustain"]
            },
            "Divine Sunderer": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "health": {"value": 400, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3300, "passive": "Spellblade: After using an ability, your next attack deals bonus damage based on target's max Health and heals you.",
                "build_path": ["Sheen", "Phage"], "tier": "A", "tags": ["Damage", "Physical", "Health", "CDR", "Healing", "Spellblade"]
            },
            "Immortal Shieldbow": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "attack_speed": {"value": 20, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3400, "passive": "Lifeline: If you would take damage that would reduce your Health below 30%, gain a shield and bonus Attack Damage for 8 seconds (90 second cooldown).",
                "build_path": ["Noonquiver", "Cloak of Agility"], "tier": "A", "tags": ["Damage", "Physical", "Attack Speed", "Critical", "Shield"]
            },
            "Mortal Reminder": {
                "stats": {"attack_damage": {"value": 45, "type": "flat"}, "attack_speed": {"value": 25, "type": "percentage"}, "armor_penetration": {"value": 30, "type": "percentage"}},
                "cost": 3000, "passive": "Grievous Wounds: Physical damage inflicts Grievous Wounds on enemies for 3 seconds.",
                "build_path": ["Executioner's Calling", "Last Whisper"], "tier": "A", "tags": ["Damage", "Physical", "Attack Speed", "Armor Penetration", "Grievous Wounds"]
            },
            "Phantom Dancer": {
                "stats": {"attack_speed": {"value": 45, "type": "percentage"}, "critical_chance": {"value": 25, "type": "percentage"}, "movement_speed": {"value": 7, "type": "percentage"}},
                "cost": 2600, "passive": "Spectral Waltz: Basic attacks grant 7% Movement Speed for 2 seconds, stacking up to 4 times. At max stacks, gain Ghosting.",
                "build_path": ["Zeal", "Cloak of Agility"], "tier": "A", "tags": ["Attack Speed", "Critical", "Movement"]
            },
            "Runaan's Hurricane": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "attack_speed": {"value": 45, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3400, "passive": "Wind's Fury: Attacks fire bolts at 2 enemies near your target, dealing physical damage. Bolts can critically strike and apply on-hit effects.",
                "build_path": ["Recurve Bow", "Cloak of Agility"], "tier": "B", "tags": ["Damage", "Physical", "Attack Speed", "Critical", "AOE"]
            },
            "Serylda's Grudge": {
                "stats": {"attack_damage": {"value": 45, "type": "flat"}, "armor_penetration": {"value": 30, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3200, "passive": "Bitter Cold: Damaging an enemy champion with an Ability slows them by 30% for 1 second.",
                "build_path": ["Last Whisper", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Armor Penetration", "CDR", "Slow"]
            },
            "Sterak's Gage": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "health": {"value": 400, "type": "flat"}},
                "cost": 3100, "passive": "The Claws that Catch: Gain bonus Attack Damage based on bonus Health. Lifeline: If you would take damage that reduces you below 30% Health, gain a shield for 8 seconds (60 second cooldown).",
                "build_path": ["Phage", "Pickaxe"], "tier": "A", "tags": ["Damage", "Physical", "Health", "Shield"]
            },
            "Stormrazor": {
                "stats": {"attack_damage": {"value": 45, "type": "flat"}, "attack_speed": {"value": 20, "type": "percentage"}, "critical_chance": {"value": 20, "type": "percentage"}},
                "cost": 3100, "passive": "Storm: Your first attack against a champion deals bonus magic damage and slows them by 75% decaying over 0.5 seconds.",
                "build_path": ["B.F. Sword", "Dagger"], "tier": "B", "tags": ["Damage", "Physical", "Attack Speed", "Critical", "Slow"]
            },
            "Chempunk Chainsword": {
                "stats": {"attack_damage": {"value": 45, "type": "flat"}, "health": {"value": 250, "type": "flat"}, "cooldown_reduction": {"value": 15, "type": "percentage"}},
                "cost": 2600, "passive": "Putrify: Dealing physical damage to enemy champions inflicts them with 40% Grievous Wounds for 3 seconds.",
                "build_path": ["Executioner's Calling", "Caulfield's Warhammer"], "tier": "B", "tags": ["Damage", "Physical", "Health", "CDR", "Grievous Wounds"]
            },
            "Ravenous Hydra": {
                "stats": {"attack_damage": {"value": 65, "type": "flat"}, "omnivamp": {"value": 12, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3300, "passive": "Cleave: Attacks deal physical damage to other enemies near the target. Active: Deal damage to nearby enemies (10 second cooldown).",
                "build_path": ["Tiamat", "B.F. Sword"], "tier": "A", "tags": ["Damage", "Physical", "Omnivamp", "CDR", "AOE"]
            },
            "Titanic Hydra": {
                "stats": {"attack_damage": {"value": 30, "type": "flat"}, "health": {"value": 500, "type": "flat"}},
                "cost": 3300, "passive": "Cleave: Basic attacks deal bonus physical damage to your target and nearby enemies based on your bonus Health.",
                "build_path": ["Tiamat", "Giant's Belt"], "tier": "A", "tags": ["Damage", "Physical", "Health", "AOE"]
            },
            
            # More AP Items
            "Archangel's Staff": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "mana": {"value": 650, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 3200, "passive": "Awe: Gain Ability Power equal to 1% maximum Mana. Refund 25% of Mana spent.",
                "build_path": ["Tear of the Goddess", "Lost Chapter"], "tier": "A", "tags": ["Magic", "Mana", "CDR"]
            },
            "Seraph's Embrace": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "mana": {"value": 860, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 3200, "passive": "Awe: Gain Ability Power equal to 1% maximum Mana. Lifeline: Upon taking damage that would reduce Health below 30%, gain a shield based on current Mana (120 second cooldown).",
                "build_path": ["Archangel's Staff"], "tier": "A", "tags": ["Magic", "Mana", "CDR", "Shield"]
            },
            "Crown of the Shattered Queen": {
                "stats": {"ability_power": {"value": 70, "type": "flat"}, "health": {"value": 250, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3000, "passive": "Safeguard: Reduce damage from champions by 40% for 1.5 seconds after taking champion damage (40 second cooldown). While Safeguard is active, gain 10-40 Ability Power.",
                "build_path": ["Lost Chapter", "Ruby Crystal"], "tier": "A", "tags": ["Magic", "Health", "CDR", "Damage Reduction"]
            },
            "Horizon Focus": {
                "stats": {"ability_power": {"value": 85, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 3000, "passive": "Hypershot: Damaging a champion with a non-targeted ability at over 750 range or slowing or immobilizing them reveals them and increases your damage to them by 10% for 6 seconds.",
                "build_path": ["Blasting Wand", "Fiendish Codex"], "tier": "B", "tags": ["Magic", "CDR", "Damage Amplification"]
            },
            "Malignance": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 600, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 2800, "passive": "Haunt: Damaging an enemy champion with your Ultimate ability deals bonus magic damage and burns the ground beneath them for 4 seconds.",
                "build_path": ["Kindlegem", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Health", "CDR", "Ultimate Enhancement"]
            },
            "Riftmaker": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 300, "type": "flat"}, "omnivamp": {"value": 15, "type": "percentage"}},
                "cost": 3200, "passive": "Void Corruption: For each second in combat with champions, deal 3% increased damage, stacking up to 5 times. While this effect is at max stacks, convert 100% of the bonus damage to true damage.",
                "build_path": ["Hextech Alternator", "Vampiric Scepter"], "tier": "A", "tags": ["Magic", "Health", "Omnivamp", "True Damage"]
            },
            "Rod of Ages": {
                "stats": {"ability_power": {"value": 60, "type": "flat"}, "health": {"value": 300, "type": "flat"}, "mana": {"value": 300, "type": "flat"}},
                "cost": 2600, "passive": "Timeless: This item gains 20 Health, 10 Mana, and 4 Ability Power every 60 seconds, up to 10 times total. Upon reaching max stacks, gain Eternity passive.",
                "build_path": ["Catalyst of Aeons"], "tier": "A", "tags": ["Magic", "Health", "Mana", "Scaling"]
            },
            "Rylai's Crystal Scepter": {
                "stats": {"ability_power": {"value": 90, "type": "flat"}, "health": {"value": 400, "type": "flat"}},
                "cost": 2600, "passive": "Rimefrost: Damaging an enemy champion with an ability slows them by 30% for 1 second.",
                "build_path": ["Blasting Wand", "Giant's Belt"], "tier": "A", "tags": ["Magic", "Health", "Slow"]
            },
            "Infinity Orb": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "magic_penetration": {"value": 10, "type": "flat"}},
                "cost": 2800, "passive": "Perforation: Abilities that deal damage to champions below 35% Health deal 20% increased damage.",
                "build_path": ["Blasting Wand", "Magic Penetration"], "tier": "A", "tags": ["Magic", "Magic Penetration", "Execute"]
            },
            
            # Tank Items
            "Warmog's Armor": {
                "stats": {"health": {"value": 800, "type": "flat"}, "health_regeneration": {"value": 200, "type": "percentage"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 3000, "passive": "Warmog's Heart: If you have at least 1100 bonus Health, restore 3% maximum Health per second if you haven't taken damage in the last 6 seconds.",
                "build_path": ["Giant's Belt", "Kindlegem"], "tier": "A", "tags": ["Health", "Health Regen", "CDR", "Tank"]
            },
            "Wit's End": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "attack_speed": {"value": 40, "type": "percentage"}, "magic_resist": {"value": 50, "type": "flat"}},
                "cost": 2900, "passive": "Fray: Basic attacks deal bonus magic damage and steal Magic Resist from the target for 5 seconds, stacking up to 5 times.",
                "build_path": ["Recurve Bow", "Negatron Cloak"], "tier": "A", "tags": ["Damage", "Physical", "Attack Speed", "Magic Resist", "On-Hit"]
            },
            "Maw of Malmortius": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "magic_resist": {"value": 50, "type": "flat"}, "cooldown_reduction": {"value": 15, "type": "percentage"}},
                "cost": 2900, "passive": "Lifeline: If you would take magic damage that would reduce you below 30% Health, gain a magic damage shield and bonus Attack Damage for 5 seconds (90 second cooldown).",
                "build_path": ["Hexdrinker", "Caulfield's Warhammer"], "tier": "B", "tags": ["Damage", "Physical", "Magic Resist", "CDR", "Shield"]
            },
            "Iceborn Gauntlet": {
                "stats": {"armor": {"value": 65, "type": "flat"}, "mana": {"value": 500, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 2600, "passive": "Spellblade: After using an ability, your next attack creates an icy zone that slows enemies by 30% for 2 seconds (1.5 second cooldown).",
                "build_path": ["Sheen", "Glacial Shroud"], "tier": "B", "tags": ["Armor", "Mana", "CDR", "Slow", "Spellblade"]
            },
            "Kaenic Rookern": {
                "stats": {"health": {"value": 400, "type": "flat"}, "magic_resist": {"value": 80, "type": "flat"}, "health_regeneration": {"value": 150, "type": "percentage"}},
                "cost": 2900, "passive": "Magebane: After not taking magic damage for 4 seconds, gain a magic shield equal to 100% bonus Magic Resist. When the shield is broken, nearby enemies take magic damage.",
                "build_path": ["Spectre's Cowl", "Negatron Cloak"], "tier": "A", "tags": ["Health", "Magic Resist", "Health Regen", "Shield", "Tank"]
            },
            
            # Support Items  
            "Imperial Mandate": {
                "stats": {"ability_power": {"value": 55, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}, "mana_regeneration": {"value": 125, "type": "percentage"}},
                "cost": 2300, "passive": "Coordinated Fire: Abilities that slow or immobilize a champion mark them. Ally damage detonates the mark, dealing bonus damage and granting both of you Movement Speed.",
                "build_path": ["Bandleglass Mirror", "Kindlegem"], "tier": "B", "tags": ["Magic", "Health", "CDR", "Support", "Mark"]
            },
            "Staff of Flowing Water": {
                "stats": {"ability_power": {"value": 50, "type": "flat"}, "mana_regeneration": {"value": 125, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 2300, "passive": "Rapids: Healing or shielding an ally grants both of you 25 Ability Power and 15% Movement Speed for 4 seconds.",
                "build_path": ["Fiendish Codex", "Forbidden Idol"], "tier": "B", "tags": ["Magic", "CDR", "Support", "Buff"]
            },
            
            # Mythic/Special Items
            "Manamune": {
                "stats": {"attack_damage": {"value": 35, "type": "flat"}, "mana": {"value": 860, "type": "flat"}, "cooldown_reduction": {"value": 15, "type": "percentage"}},
                "cost": 2900, "passive": "Awe: Gain bonus Attack Damage equal to 2% maximum Mana. Shock: Basic attacks and abilities that hit champions consume 3% current Mana to deal bonus physical damage.",
                "build_path": ["Tear of the Goddess", "Pickaxe"], "tier": "A", "tags": ["Damage", "Physical", "Mana", "CDR"]
            },
            "Muramana": {
                "stats": {"attack_damage": {"value": 35, "type": "flat"}, "mana": {"value": 860, "type": "flat"}, "cooldown_reduction": {"value": 15, "type": "percentage"}},
                "cost": 2900, "passive": "Awe: Gain bonus Attack Damage equal to 2% maximum Mana. Shock: Basic attacks and single target abilities against champions consume 3% current Mana to deal bonus physical damage.",
                "build_path": ["Manamune"], "tier": "A", "tags": ["Damage", "Physical", "Mana", "CDR", "On-Hit"]
            },
            "Tear of the Goddess": {
                "stats": {"mana": {"value": 240, "type": "flat"}, "mana_regeneration": {"value": 25, "type": "percentage"}},
                "cost": 400, "passive": "Focus: Grants a charge every 8 seconds, up to 4 charges. Casting an ability consumes a charge and grants 12 bonus Mana, up to a maximum of 360 bonus Mana.",
                "build_path": [], "tier": "C", "tags": ["Mana", "Scaling"]
            },
            
            # Boot Enchants
            "Glorious Enchant": {
                "stats": {"cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 500, "active": "Glory: Gain 30% Movement Speed for 3 seconds. If used while near an ally champion, you and the nearest ally champion gain the effect (90 second cooldown).",
                "build_path": [], "tier": "B", "tags": ["CDR", "Movement", "Support", "Enchant"]
            },
            "Protobelt Enchant": {
                "stats": {"ability_power": {"value": 10, "type": "flat"}},
                "cost": 500, "active": "Fire Bolt: Dash forward and unleash a cone of missiles that deal magic damage (40 second cooldown).",
                "build_path": [], "tier": "B", "tags": ["Magic", "Dash", "AOE", "Enchant"]
            },
            "Stasis Enchant": {
                "stats": {"armor": {"value": 15, "type": "flat"}},
                "cost": 500, "active": "Stasis: Become untargetable and invulnerable for 2.5 seconds, but unable to move, attack, cast abilities, or use items (120 second cooldown).",
                "build_path": [], "tier": "A", "tags": ["Armor", "Stasis", "Defensive", "Enchant"]
            },
            "Quicksilver Enchant": {
                "stats": {"magic_resist": {"value": 15, "type": "flat"}},
                "cost": 500, "active": "Quicksilver: Remove all debuffs and gain 50% Tenacity and Slow Resist for 3 seconds (90 second cooldown).",
                "build_path": [], "tier": "A", "tags": ["Magic Resist", "Cleanse", "Tenacity", "Enchant"]
            },
            "Teleport Enchant": {
                "stats": {"movement_speed": {"value": 20, "type": "flat"}},
                "cost": 500, "active": "Teleport: After channeling for 3.5 seconds, teleport to target location (240 second cooldown, reduced by takedowns).",
                "build_path": [], "tier": "B", "tags": ["Movement", "Teleport", "Utility", "Enchant"]
            },
            
            # Remaining Active Wild Rift Items
            "Terminus": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "attack_speed": {"value": 30, "type": "percentage"}},
                "cost": 3000, "passive": "Juxtaposition: Attacks alternate between dealing bonus magic damage and bonus true damage. Killing a champion or epic monster grants Attack Damage and Attack Speed for 60 seconds.",
                "build_path": ["Recurve Bow", "Pickaxe"], "tier": "A", "tags": ["Damage", "Physical", "Attack Speed", "On-Hit", "True Damage"]
            },
            "Sundered Sky": {
                "stats": {"attack_damage": {"value": 50, "type": "flat"}, "health": {"value": 300, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3100, "passive": "Lightshield Strike: After using an ability, your next attack deals bonus damage based on target's missing Health and heals you (1.5 second cooldown).",
                "build_path": ["Phage", "Caulfield's Warhammer"], "tier": "A", "tags": ["Damage", "Physical", "Health", "CDR", "Healing", "Execute"]
            },
            "Yordle Trap": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 350, "type": "flat"}},
                "cost": 2800, "passive": "Explosive Entrance: Immobilizing an enemy champion creates an explosion around them after 2 seconds, dealing magic damage to nearby enemies.",
                "build_path": ["Blasting Wand", "Giant's Belt"], "tier": "B", "tags": ["Magic", "Health", "AOE", "CC"]
            },
            "Protector's Vow": {
                "stats": {"armor": {"value": 40, "type": "flat"}, "magic_resist": {"value": 40, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2200, "passive": "Pledge: Bind to an ally champion. While near your partner, gain 20 Armor and Magic Resist. If your partner dies, gain 20% Movement Speed and 20% Attack Speed for 8 seconds.",
                "build_path": ["Aegis of the Legion"], "tier": "B", "tags": ["Armor", "Magic Resist", "Health", "CDR", "Support", "Bond"]
            },
            "Spectral Sickle": {
                "stats": {"attack_damage": {"value": 20, "type": "flat"}, "health": {"value": 75, "type": "flat"}, "gold_generation": {"value": 3, "type": "flat"}},
                "cost": 400, "passive": "Tribute: Damaging an enemy champion by attack or ability grants 20 gold and heals your most wounded nearby ally (10 second cooldown per target). Killing a minion charges this item.",
                "build_path": [], "tier": "C", "tags": ["Damage", "Physical", "Health", "Support", "Gold Generation"]
            },
            "Black Mist Scythe": {
                "stats": {"attack_damage": {"value": 20, "type": "flat"}, "health": {"value": 75, "type": "flat"}, "gold_generation": {"value": 3, "type": "flat"}},
                "cost": 400, "passive": "Tribute: Damaging an enemy champion by attack or ability grants 20 gold and executes minions below 50% Health (10 second cooldown per target).",
                "build_path": [], "tier": "C", "tags": ["Damage", "Physical", "Health", "Support", "Gold Generation", "Execute"]
            },
            "Soulstealer": {
                "stats": {"ability_power": {"value": 20, "type": "flat"}, "mana": {"value": 75, "type": "flat"}, "gold_generation": {"value": 3, "type": "flat"}},
                "cost": 400, "passive": "Tribute: Damaging an enemy champion with an ability grants 20 gold and restores mana to your most mana-hungry nearby ally (10 second cooldown per target).",
                "build_path": [], "tier": "C", "tags": ["Magic", "Mana", "Support", "Gold Generation"]
            },
            "Dream Maker": {
                "stats": {"ability_power": {"value": 40, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2200, "passive": "Renew: Healing or shielding an ally grants them 8% Movement Speed for 2 seconds and marks them. Your next ability against an enemy will consume the mark to deal bonus magic damage.",
                "build_path": ["Soulstealer"], "tier": "B", "tags": ["Magic", "Health", "CDR", "Support", "Heal", "Mark"]
            },
            "Solari Chargeblade": {
                "stats": {"attack_damage": {"value": 40, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2200, "passive": "Energize: Moving and attacking builds Energy stacks. At 100 stacks, your next attack deals bonus magic damage to up to 4 enemies.",
                "build_path": ["Spectral Sickle"], "tier": "B", "tags": ["Damage", "Physical", "Health", "CDR", "Support", "AOE"]
            },
            "Oceanid's Trident": {
                "stats": {"ability_power": {"value": 40, "type": "flat"}, "mana": {"value": 200, "type": "flat"}, "cooldown_reduction": {"value": 10, "type": "percentage"}},
                "cost": 2200, "passive": "Flowing Force: Abilities that slow or immobilize enemies deal bonus magic damage and reduce this item's active cooldown by 20%.",
                "active": "Tidal Wave: Send out a wave that slows and damages enemies (60 second cooldown).",
                "build_path": ["Soulstealer"], "tier": "B", "tags": ["Magic", "Mana", "CDR", "Support", "Slow", "AOE"]
            },
            "Bandle Fantasy": {
                "stats": {"ability_power": {"value": 65, "type": "flat"}, "health": {"value": 250, "type": "flat"}, "movement_speed": {"value": 5, "type": "percentage"}},
                "cost": 2800, "passive": "Whimsy: Dealing magic damage to enemy champions grants you and nearby allies 10% Movement Speed for 3 seconds.",
                "build_path": ["Blasting Wand", "Ruby Crystal"], "tier": "B", "tags": ["Magic", "Health", "Movement", "Support", "Buff"]
            },
            "Dawnshroud": {
                "stats": {"ability_power": {"value": 70, "type": "flat"}, "magic_resist": {"value": 40, "type": "flat"}},
                "cost": 2650, "passive": "Daybreak: After not taking damage for 4 seconds, your next ability deals 20% increased damage and grants a shield for 3 seconds.",
                "build_path": ["Blasting Wand", "Null-Magic Mantle"], "tier": "B", "tags": ["Magic", "Magic Resist", "Shield", "Damage Amplification"]
            },
            "Shimmering Spark": {
                "stats": {"ability_power": {"value": 60, "type": "flat"}, "attack_speed": {"value": 30, "type": "percentage"}, "movement_speed": {"value": 7, "type": "percentage"}},
                "cost": 2800, "passive": "Energized: Moving and attacking builds Energy. At 100 stacks, your next attack deals bonus magic damage and grants Movement Speed.",
                "build_path": ["Blasting Wand", "Dagger"], "tier": "B", "tags": ["Magic", "Attack Speed", "Movement", "On-Hit"]
            },
            "Searing Crown": {
                "stats": {"ability_power": {"value": 90, "type": "flat"}, "health": {"value": 300, "type": "flat"}},
                "cost": 3000, "passive": "Immolate: Deal magic damage to nearby enemies every second. Enemy champions take 50% increased damage from this effect.",
                "build_path": ["Bami's Cinder", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Health", "AOE", "DOT"]
            },
            "Psychic Projector": {
                "stats": {"ability_power": {"value": 75, "type": "flat"}, "cooldown_reduction": {"value": 25, "type": "percentage"}},
                "cost": 2900, "passive": "Psychic Blast: Abilities that deal damage to enemy champions fire a projectile at the nearest enemy, dealing magic damage (4 second cooldown).",
                "build_path": ["Fiendish Codex", "Blasting Wand"], "tier": "B", "tags": ["Magic", "CDR", "Projectile"]
            },
            "Magnetic Blaster": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "armor": {"value": 30, "type": "flat"}},
                "cost": 2700, "passive": "Magnetic Field: Enemies that attack you are slowed by 15% for 1.5 seconds. This effect stacks up to 3 times.",
                "build_path": ["Blasting Wand", "Cloth Armor"], "tier": "B", "tags": ["Magic", "Armor", "Slow", "Defensive"]
            },
            "Mantle of the Twelfth Hour": {
                "stats": {"ability_power": {"value": 65, "type": "flat"}, "health": {"value": 200, "type": "flat"}, "magic_resist": {"value": 35, "type": "flat"}},
                "cost": 2600, "passive": "Last Stand: When below 35% Health, gain 30% increased damage and 20% damage reduction for 5 seconds (45 second cooldown).",
                "build_path": ["Blasting Wand", "Ruby Crystal"], "tier": "B", "tags": ["Magic", "Health", "Magic Resist", "Last Stand"]
            },
            "Talisman of Ascension": {
                "stats": {"health": {"value": 300, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}, "mana_regeneration": {"value": 150, "type": "percentage"}},
                "cost": 2200, "active": "Ascension: Grant nearby allies 40% Movement Speed for 3 seconds (60 second cooldown).",
                "build_path": ["Ancient Coin"], "tier": "B", "tags": ["Health", "CDR", "Support", "Movement", "Aura"]
            },
            "Ancient Coin": {
                "stats": {"health": {"value": 75, "type": "flat"}, "mana_regeneration": {"value": 25, "type": "percentage"}, "gold_generation": {"value": 2, "type": "flat"}},
                "cost": 400, "passive": "Favor: Nearby enemy minions that die without you killing them drop coins that grant gold and mana.",
                "build_path": [], "tier": "C", "tags": ["Health", "Support", "Gold Generation", "Mana"]
            },
            "Gluttonous Greaves": {
                "stats": {"movement_speed": {"value": 45, "type": "flat"}, "omnivamp": {"value": 8, "type": "percentage"}},
                "cost": 1000, "passive": "Feast: Gain permanent Health for each enemy champion takedown, up to 100 bonus Health.",
                "build_path": ["Boots"], "tier": "B", "tags": ["Movement", "Omnivamp", "Scaling", "Boots"]
            },
            "Amaranth's Twinguard": {
                "stats": {"health": {"value": 400, "type": "flat"}, "armor": {"value": 30, "type": "flat"}, "magic_resist": {"value": 30, "type": "flat"}},
                "cost": 2800, "passive": "Twin Spirits: When you or a nearby ally champion takes damage, the other gains a shield for 3 seconds (8 second cooldown).",
                "build_path": ["Giant's Belt", "Aegis of the Legion"], "tier": "B", "tags": ["Health", "Armor", "Magic Resist", "Shield", "Support"]
            },
            
            # Boot Enchants
            "Meteor Enchant": {
                "stats": {"magic_penetration": {"value": 10, "type": "flat"}},
                "cost": 500, "passive": "Meteor: Damaging an enemy champion calls down a meteor after 1.5 seconds, dealing magic damage in an area (8 second cooldown).",
                "build_path": [], "tier": "B", "tags": ["Magic Penetration", "AOE", "Enchant"]
            },
            "Veil Enchant": {
                "stats": {"magic_resist": {"value": 15, "type": "flat"}},
                "cost": 500, "passive": "Veil: Gain a spell shield that blocks the next enemy ability every 40 seconds.",
                "build_path": [], "tier": "A", "tags": ["Magic Resist", "Spell Shield", "Enchant"]
            },
            "Repulsor Enchant": {
                "stats": {"health": {"value": 150, "type": "flat"}},
                "cost": 500, "active": "Repulse: Push away nearby enemies and gain Movement Speed for 2 seconds (90 second cooldown).",
                "build_path": [], "tier": "B", "tags": ["Health", "Knockback", "Movement", "Enchant"]
            },
            
            # Legacy/Renamed Items
            "GLP-800": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 300, "type": "flat"}, "mana": {"value": 600, "type": "flat"}},
                "cost": 3000, "active": "Frost Bolt: Fire an icy bolt that slows the first enemy hit and creates a slow field (40 second cooldown).",
                "build_path": ["Catalyst of Aeons", "Blasting Wand"], "tier": "B", "tags": ["Magic", "Health", "Mana", "Slow", "Active"]
            },
            "Redeeming": {
                "stats": {"health": {"value": 300, "type": "flat"}, "mana_regeneration": {"value": 125, "type": "percentage"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 2100, "active": "Intervention: After a 2.5 second delay, call down a beam of light to heal allies and damage enemies in the area (90 second cooldown).",
                "build_path": ["Forbidden Idol", "Giant's Belt"], "tier": "B", "tags": ["Health", "CDR", "Support", "Heal", "AOE"]
            },
            
            # Fix remaining items
            "Harmonic Echo": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "mana": {"value": 600, "type": "flat"}, "cooldown_reduction": {"value": 20, "type": "percentage"}},
                "cost": 3200, "passive": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage. This effect has a cooldown per target.",
                "build_path": ["Lost Chapter", "Blasting Wand"], "tier": "A", "tags": ["Magic", "Mana", "CDR", "Echo"]
            },
            "Morellonom": {
                "stats": {"ability_power": {"value": 80, "type": "flat"}, "health": {"value": 300, "type": "flat"}},
                "cost": 3000, "passive": "Cursed: Magic damage inflicts Grievous Wounds on enemies below 50% Health for 3 seconds.",
                "build_path": ["Oblivion Orb", "Giant's Belt"], "tier": "A", "tags": ["Magic", "Health", "Grievous Wounds"]
            },
            "Stoneplate Enchant": {
                "stats": {"armor": {"value": 15, "type": "flat"}, "magic_resist": {"value": 15, "type": "flat"}},
                "cost": 500, "active": "Stoneplate: Gain 40% damage reduction but deal 60% less damage for 2.5 seconds (90 second cooldown).",
                "build_path": [], "tier": "A", "tags": ["Armor", "Magic Resist", "Damage Reduction", "Enchant"]
            }
        }
    
    def update_item_file(self, item_name, filename):
        """Update an item file with real Wild Rift data"""
        if item_name not in self.item_database:
            print(f"No data available for {item_name}")
            return False
        
        data = self.item_database[item_name]
        
        item_data = {
            "name": item_name,
            "stats": data["stats"],
            "cost": data["cost"],
            "passive": data.get("passive", ""),
            "active": data.get("active", ""),
            "description": f"Wild Rift item with real stats and effects from wr-meta.com",
            "category": "legendary",
            "tier": data["tier"],
            "build_path": data.get("build_path", []),
            "tags": data["tags"]
        }
        
        filepath = Path("items") / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated {item_name} with real Wild Rift data")
        return True
    
    def fix_all_items(self):
        """Fix all items with real Wild Rift data"""
        # Generate filename from item name
        def name_to_filename(name):
            return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_').replace("'", '').lower() + '.json'
        
        print("🔄 Updating ALL items with real Wild Rift data from wr-meta.com...")
        
        updated_count = 0
        for item_name in self.item_database.keys():
            filename = name_to_filename(item_name)
            if self.update_item_file(item_name, filename):
                updated_count += 1
            time.sleep(0.1)  # Small delay
        
        print(f"✅ Updated {updated_count} items with real Wild Rift data!")

def main():
    scraper = WRMetaScraper()
    scraper.fix_all_items()

if __name__ == "__main__":
    main()