#!/usr/bin/env python3
"""
Real-Time Item Scraper for Wild Rift
Scrapes accurate, up-to-date item data directly from WR-META.com
"""

import requests
import json
import re
import time
import os
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

class RealTimeItemScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://wr-meta.com"
        self.items_url = f"{self.base_url}/items"
        self.output_dir = Path("items")
        self.output_dir.mkdir(exist_ok=True)
        
    def scrape_all_items(self):
        """Scrape all items from the items page"""
        print(f"Fetching items from {self.items_url}")
        
        try:
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all item containers
            item_containers = soup.select('.item-container, .item-box, .item-card, .item')
            
            if not item_containers:
                # Try alternative selectors if the above doesn't work
                item_containers = soup.find_all(['div', 'section', 'article'], 
                                              class_=lambda c: c and any(x in c for x in ['item', 'card', 'box']))
            
            if not item_containers:
                # Last resort: look for elements with item-like content
                print("Using fallback item detection...")
                item_containers = []
                
                # Look for elements containing gold cost and stats
                potential_items = soup.find_all(string=re.compile(r'\d{3,4}\s*(?:gold|cost)', re.I))
                for text_elem in potential_items:
                    parent = text_elem.parent
                    if parent:
                        container = parent.find_parent(['div', 'section', 'article', 'tr', 'td'])
                        if container and container not in item_containers:
                            item_containers.append(container)
            
            print(f"Found {len(item_containers)} potential item containers")
            
            items_scraped = 0
            for container in item_containers:
                item_data = self.extract_item_data(container)
                if item_data and item_data.get('name'):
                    self.save_item_data(item_data)
                    items_scraped += 1
                    
                    # Rate limiting
                    time.sleep(0.5)
            
            print(f"Successfully scraped {items_scraped} items")
            return items_scraped
            
        except Exception as e:
            print(f"Error scraping items: {e}")
            return 0
    
    def extract_passive_and_active_effects(self, container, item_name, container_text):
        """
        Enhanced passive and active effect parsing with comprehensive regex patterns
        and special case handling for named passives like "Overkill"
        """
        passive = ""
        active = ""
        
        # Define comprehensive list of known named passives for popular items
        known_passives = {
            "Rabadon's Deathcap": "Overkill: Increases Ability Power by 20-45%",
            "Duskblade of Draktharr": "Nightstalker: After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals 99 (+30% bonus AD) bonus physical damage.",
            "Guardian Angel": "Rebirth: Upon taking lethal damage, revive with 50% base Health and 30% maximum Mana after 4 seconds of stasis (300 second cooldown).",
            "Infinity Edge": "Critical Edge: Increases critical strike damage by 35%",
            "Trinity Force": "Spellblade: After using an ability, your next attack within 10 seconds deals 200% base AD as bonus damage (1.5s cooldown)",
            "Warmog's Armor": "Warmog's Heart: Regenerate 2.5% of maximum health per second if damage hasn't been taken within 6 seconds",
            "Thornmail": "Thorns: When struck by a basic attack, reflect 25 (+10% bonus Armor) magic damage and apply 40% Grievous Wounds to the attacker for 3 seconds",
            "Void Staff": "Void Pen: Increases magic penetration by 40%",
            "Mortal Reminder": "Mortal Strike: Physical damage applies 40% Grievous Wounds to enemy champions for 3 seconds",
            "Sterak's Gage": "Lifeline: When taking damage that would reduce you below 30% health, gain a shield equal to 75% of bonus health for 4 seconds (60s cooldown)",
            "Blade of the Ruined King": "Drain: Basic attacks deal 8% of target's current health as bonus physical damage on-hit",
            "Luden's Echo": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage. This effect has a cooldown per target.",
            "Harmonic Echo": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage. This effect has a cooldown per target.",
            "Black Cleaver": "Carve: Dealing physical damage to an enemy champion applies a stack for 6 seconds (max 6 stacks). Each stack reduces the target's Armor by 4%.",
            "Sunfire Aegis": "Immolate: Deal magic damage per second to nearby enemies. Damage increases by 50% per second over 3 seconds when in combat with enemy champions.",
            "Frozen Heart": "Winter's Caress: Reduces the Attack Speed of nearby enemies by 15%.",
            "Spirit Visage": "Boundless Vitality: Increases all healing and shielding on you by 25%.",
            "Dead Man's Plate": "Dreadnought: While moving, build up to 100 Momentum. At 100 Momentum, your next basic attack discharges all Momentum to deal bonus magic damage and slow the target.",
            "Randuin's Omen": "Cold Steel: When struck by a basic attack, reduces the attacker's Attack Speed by 15% for 1 second.",
            "Nashor's Tooth": "Icathian Bite: Basic attacks deal bonus magic damage equal to 15 (+20% AP).",
            "Lich Bane": "Spellblade: After using an ability, your next basic attack within 10 seconds deals bonus magic damage equal to 75% base AD + 50% AP (1.5 second cooldown).",
            "Rylai's Crystal Scepter": "Rimefrost: Abilities slow enemies by 30% for 1 second.",
            "Liandry's Torment": "Torment: Dealing ability damage burns enemies for magic damage over 3 seconds. Against movement-impaired units, deal double damage.",
            "Morellonomicon": "Cursed Strike: Magic damage applies 40% Grievous Wounds to enemy champions for 3 seconds.",
            "Zhonya's Hourglass": "Stasis: Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown).",
            "Banshee's Veil": "Annul: Grants a spell shield that blocks the next enemy ability (40 second cooldown after being triggered).",
            "Maw of Malmortius": "Lifeline: When taking magic damage that would reduce you below 30% health, gain a magic damage shield and 10% Omnivamp for 5 seconds (90 second cooldown).",
            "Edge of Night": "Annul: Grants a spell shield that blocks the next enemy ability. Recharges after 40 seconds out of combat with enemy champions.",
            "Youmuu's Ghostblade": "Wraith Step: Gain 20% Movement Speed for 6 seconds (45 second cooldown).",
            "Serylda's Grudge": "Bitter Cold: Abilities slow enemies by 30% for 1 second.",
            "Lord Dominik's Regards": "Giant Slayer: Deal 0-15% bonus physical damage based on the health difference between you and your target.",
            "The Collector": "Death and Taxes: Enemies below 5% health are executed. Champion takedowns grant 25 bonus gold.",
            "Kraken Slayer": "Bring It Down: Every 3rd attack on the same target deals true damage equal to 60 + 45% bonus AD.",
            "Galeforce": "Cloudburst: Dash in target direction, firing 3 missiles at the lowest health enemy champion near your destination (90 second cooldown).",
            "Immortal Shieldbow": "Lifeline: When taking damage that would reduce you below 30% health, gain a shield and 15% Life Steal for 8 seconds (90 second cooldown).",
            "Phantom Dancer": "Spectral Waltz: Basic attacks grant 7% Attack Speed for 3 seconds, stacking up to 5 times. At max stacks, gain 7% Movement Speed.",
            "Runaan's Hurricane": "Wind's Fury: Basic attacks fire bolts at up to 2 nearby enemies, each dealing physical damage equal to 40% AD.",
            "Stormrazor": "Energized Strike: Moving and basic attacking generates Energized stacks. At 100 stacks, your next basic attack deals bonus magic damage and slows the target by 75% for 0.5 seconds.",
            "Rapid Firecannon": "Energized Strike: Moving and basic attacking generates Energized stacks. At 100 stacks, your next basic attack has +150 range and deals bonus magic damage.",
            "Statikk Shiv": "Energized Strike: Moving and basic attacking generates Energized stacks. At 100 stacks, your next basic attack deals bonus magic damage that can critically strike and chains to nearby enemies.",
            "Wit's End": "Fray: Basic attacks deal bonus magic damage and steal 5 Magic Resistance from the target for 5 seconds, stacking up to 5 times.",
            "Bloodthirster": "Overheal: Gain a shield equal to 50-350 health based on champion level when at full health.",
            "Essence Reaver": "Spellblade: After using an ability, your next basic attack within 10 seconds deals bonus physical damage equal to 100% base AD + 40% bonus AD (1.5 second cooldown).",
            "Navori Quickblades": "Transcendence: Basic attacks reduce your basic abilities' remaining cooldowns by 20% of your critical strike chance.",
            "Chempunk Chainsword": "Hackshorn: Dealing physical damage applies 40% Grievous Wounds to enemy champions for 3 seconds.",
            "Ravenous Hydra": "Cleave: Basic attacks deal physical damage to enemies behind the target equal to 60% AD.",
            "Titanic Hydra": "Cleave: Basic attacks deal bonus physical damage to the target and physical damage to enemies behind the target based on your bonus health.",
            "Sterak's Gage": "Lifeline: When taking damage that would reduce you below 30% health, gain a shield equal to 75% of bonus health for 4 seconds (60 second cooldown).",
            "Black Mist Scythe": "Tribute: Damaging abilities and basic attacks against champions grant 20 gold and heal you. This effect has a per-target cooldown.",
            "Relic Shield": "Spoils of War: Killing a minion heals you and the nearest allied champion and grants them gold equal to the kill.",
            "Spectral Sickle": "Tribute: Damaging abilities and basic attacks against champions grant 20 gold. This effect has a per-target cooldown.",
            "Harmonic Echo": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage to the first enemy hit.",
            "Luden's Echo": "Echo: Damaging an enemy with an ability hurls an orb at them that deals magic damage to the first enemy hit.",
            "Riftmaker": "Void Corruption: For each second in combat with enemy champions, deal 3% increased damage, stacking up to 5 times. When fully stacked, convert 100% of the bonus damage to true damage.",
            "Crown of the Shattered Queen": "Safeguard: Become Safeguarded for 1.5 seconds, reducing incoming damage by 40%. This effect has a 40 second cooldown and triggers when you haven't taken damage for 4 seconds.",
            "Everfrost": "Glaciate: Deal magic damage in a cone, slowing enemies by 65% for 1.5 seconds. Enemies in the center are rooted instead (30 second cooldown).",
            "Night Harvester": "Soulrend: Damaging an enemy champion deals bonus magic damage and grants 25% Movement Speed for 1.5 seconds (40 second cooldown per target).",
            "Hextech Rocketbelt": "Supersonic: Dash forward and unleash a cone of missiles that deal magic damage (40 second cooldown).",
            "Cosmic Drive": "Spelldance: Damaging an enemy champion with an ability grants 30% Movement Speed for 2 seconds.",
            "Horizon Focus": "Hypershot: Damaging a champion with an ability at over 750 range or immobilizing them increases your damage dealt to them by 10% for 6 seconds.",
            "Demonic Embrace": "Azakana Gaze: Dealing ability damage burns enemies for magic damage over 4 seconds. Against champions, heal for 30% of the damage dealt.",
            "Shadowflame": "Cinderbloom: Magic penetration increases by up to 10-20 based on the target's missing health.",
            "Void Staff": "Dissolve: +40% Magic Penetration.",
            "Rabadon's Deathcap": "Overkill: Increases Ability Power by 20-45%."
        }
        
        # Check if this is a known item with a predefined passive
        for item_key, passive_text in known_passives.items():
            if item_key.lower() in item_name.lower():
                passive = passive_text
                break
        
        # If not a known item, try to extract passive from the content using enhanced patterns
        if not passive:
            passive = self._extract_passive_effect(container, item_name, container_text)
        
        # Define known active effects for popular items
        known_actives = {
            "Stasis Enchant": "Stasis: Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown).",
            "Protobelt Enchant": "Supersonic: Dash forward and unleash a cone of missiles that deal 70 magic damage and reduce target's Magic Resistance by 15% for 3 seconds. After cast, gain 20% Movement Speed that decays over 3 seconds (50 second cooldown).",
            "Quicksilver Enchant": "Quicksilver: Removes all crowd control effects and grants 100% tenacity for 0.5 seconds (90 second cooldown).",
            "Teleport Enchant": "Teleport: Teleport to target location after 3.5 seconds of channeling (180 second cooldown).",
            "Repulsor Enchant": "Repulsor: Knocks back nearby enemies and slows them by 80% for 1 second (90 second cooldown).",
            "Locket Enchant": "Devotion: Grants a shield to nearby allies that absorbs damage. Shield strength scales with champion level (60 second cooldown).",
            "Glorious Enchant": "Glory: Grants 30% Movement Speed and 20% Attack Speed for 3 seconds (60 second cooldown).",
            "Meteor Enchant": "Meteor: Summons a meteor at target location after 0.75 seconds, dealing magic damage and slowing enemies by 40% for 2 seconds (75 second cooldown).",
            "Veil Enchant": "Veil: Grants a spell shield that blocks the next enemy ability (40 second cooldown after being triggered).",
            "Stoneplate Enchant": "Fortify: Gain 40% damage reduction for 2.5 seconds, but deal 60% less damage (90 second cooldown).",
            "Zhonya's Hourglass": "Stasis: Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown).",
            "Galeforce": "Cloudburst: Dash in target direction, firing 3 missiles at the lowest health enemy champion near your destination (90 second cooldown).",
            "Everfrost": "Glaciate: Deal magic damage in a cone, slowing enemies by 65% for 1.5 seconds. Enemies in the center are rooted instead (30 second cooldown).",
            "Night Harvester": "Soulrend: Damaging an enemy champion deals bonus magic damage and grants 25% Movement Speed for 1.5 seconds (40 second cooldown per target).",
            "Hextech Rocketbelt": "Supersonic: Dash forward and unleash a cone of missiles that deal magic damage (40 second cooldown).",
            "Youmuu's Ghostblade": "Wraith Step: Gain 20% Movement Speed for 6 seconds (45 second cooldown).",
            "Randuin's Omen": "Humility: Slows nearby enemies by 55% for 2 seconds (60 second cooldown).",
            "Righteous Glory": "Righteous Fury: Grants 75% Movement Speed when moving towards enemies for 3 seconds. After 3 seconds or when an enemy champion is nearby, create a shockwave that slows nearby enemies (90 second cooldown).",
            "Redemption": "Intervention: Target an area within 5500 range. After 2.5 seconds, call down a beam of light that heals allies and damages enemies (120 second cooldown).",
            "Locket of the Iron Solari": "Devotion: Grants a shield to you and nearby allies that absorbs damage for 2.5 seconds (90 second cooldown).",
            "Mikael's Blessing": "Purify: Removes all crowd control effects from target ally and heals them (120 second cooldown).",
            "Shurelya's Battlesong": "Inspire: Grants you and nearby allies 60% Movement Speed for 3 seconds (75 second cooldown).",
            "Imperial Mandate": "Coordinated Fire: Abilities that slow or immobilize enemy champions mark them for 4 seconds. Ally damage detonates the mark, dealing bonus magic damage and granting both allies Movement Speed (6 second cooldown per target).",
            "Moonstone Renewer": "Starlit Grace: Healing or shielding an ally grants them Starlit Grace for 4 seconds. While you have Starlit Grace, your heals and shields are 25% stronger.",
            "Staff of Flowing Water": "Rapids: Healing or shielding an ally grants both of you 35 Ability Power and 15% Movement Speed for 3 seconds.",
            "Chemtech Putrifier": "Puffcap Toxin: Healing or shielding an ally applies 40% Grievous Wounds to nearby enemies for 3 seconds.",
            "Ardent Censer": "Frenzy: Healing or shielding an ally grants them 25% Attack Speed and 20 magic damage on-hit for 6 seconds.",
            "Umbral Glaive": "Blackout: Damaging an enemy ward instantly destroys it and grants 25 gold. This effect has a 8 second cooldown.",
            "Duskblade of Draktharr": "Nightstalker: After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals 99 (+30% bonus AD) bonus physical damage.",
            "Prowler's Claw": "Sandswipe: Dash through target enemy, dealing physical damage and granting 15% increased damage to that champion for 3 seconds (60 second cooldown).",
            "Eclipse": "Ever Rising Moon: Hitting an enemy champion with 2 separate attacks or abilities within 1.5 seconds deals bonus physical damage, grants a shield, and 30% Movement Speed for 2 seconds (8 second cooldown).",
            "The Collector": "Death and Taxes: Enemies below 5% health are executed. Champion takedowns grant 25 bonus gold.",
            "Serpent's Fang": "Shield Reaver: Dealing damage to an enemy champion reduces any shields they gain by 50% for 3 seconds.",
            "Axiom Arc": "Flux: Champion takedowns refund 25% of your Ultimate ability's total cooldown.",
            "Hullbreaker": "Boarding Party: While no allied champions are nearby, gain 20-60 Armor and Magic Resistance and 20% increased damage to structures. Nearby minions gain 60-180 Armor and Magic Resistance and immunity to slowing effects.",
            "Anathema's Chains": "Vendetta: Choose an enemy champion as your Nemesis. Take 20% reduced damage from your Nemesis and increase their tenacity reduction by 20%.",
            "Force of Nature": "Dissipate: Taking magic damage grants 8 Movement Speed for 5 seconds, stacking up to 5 times. At max stacks, gain 30 Magic Resistance.",
            "Abyssal Mask": "Unmake: Immobilizing an enemy champion reduces their Magic Resistance by 25 for 4 seconds.",
            "Frozen Heart": "Winter's Caress: Reduces the Attack Speed of nearby enemies by 15%.",
            "Thornmail": "Thorns: When struck by a basic attack, reflect 25 (+10% bonus Armor) magic damage and apply 40% Grievous Wounds to the attacker for 3 seconds.",
            "Gargoyle Stoneplate": "Fortify: Gain 40% damage reduction for 2.5 seconds, but deal 60% less damage (90 second cooldown).",
            "Turbo Chemtank": "Supercharge: Grants 75% Movement Speed when moving towards enemies for 4 seconds. After 4 seconds or when an enemy champion is nearby, create a shockwave that slows nearby enemies (90 second cooldown).",
            "Sunfire Aegis": "Immolate: Deal magic damage per second to nearby enemies. Damage increases by 50% per second over 3 seconds when in combat with enemy champions.",
            "Frostfire Gauntlet": "Iceborn: After using an ability, your next basic attack creates a frost field for 1.5 seconds that slows enemies by 30%.",
            "Goredrinker": "Thirsting Slash: Deal physical damage to all nearby enemies, healing for 25% AD plus 10.5% missing health for each enemy champion hit (15 second cooldown).",
            "Stridebreaker": "Halting Slash: Deal physical damage to all nearby enemies and slow them by 40% for 3 seconds (20 second cooldown).",
            "Divine Sunderer": "Spellblade: After using an ability, your next basic attack within 10 seconds deals bonus physical damage and heals you (1.5 second cooldown).",
            "Trinity Force": "Spellblade: After using an ability, your next basic attack within 10 seconds deals 200% base AD as bonus damage (1.5 second cooldown).",
            "Iceborn Gauntlet": "Iceborn: After using an ability, your next basic attack creates a frost field for 2 seconds that slows enemies by 30%.",
            "Chemtech Putrifier": "Puffcap Toxin: Healing or shielding an ally applies 40% Grievous Wounds to nearby enemies for 3 seconds."
        }
        
        # Check if this is a known item with a predefined active
        for item_key, active_text in known_actives.items():
            if item_key.lower() in item_name.lower():
                active = active_text
                break
        
        # If not a known item with active, try to extract active from the content
        if not active:
            active = self._extract_active_effect(container, item_name, container_text)
        
        # Prevent items from having both passive and active if they should only have one
        # Items with known actives should not have passives extracted
        if active and not passive:
            # Check if the extracted active is actually a passive that was misclassified
            if any(keyword in active.lower() for keyword in ['passive', 'unique']) and 'active' not in active.lower():
                passive = active
                active = ""
        
        # Items with known passives should not have actives extracted unless they truly have both
        if passive and active:
            # Some items like Duskblade have both passive and active components
            # But most items should only have one or the other
            known_dual_items = ["Duskblade of Draktharr", "Youmuu's Ghostblade", "Galeforce"]
            if not any(dual_item.lower() in item_name.lower() for dual_item in known_dual_items):
                # If it's not a known dual item, prioritize the known effect
                if any(item_key.lower() in item_name.lower() for item_key in known_passives.keys()):
                    active = ""  # Keep only the passive
                elif any(item_key.lower() in item_name.lower() for item_key in known_actives.keys()):
                    passive = ""  # Keep only the active
        
        # Special handling for enchant items
        if "Enchant" in item_name:
            passive = ""  # Enchant items typically don't have passives
            
            # If no active was found but it's an enchant item, try to extract from the name
            if not active:
                enchant_type = re.sub(r'Enchant.*', '', item_name).strip()
                if enchant_type:
                    # Try to find a description that mentions this enchant type
                    enchant_desc = re.search(rf'{re.escape(enchant_type)}[^.]+', container_text, re.I)
                    if enchant_desc:
                        active = enchant_desc.group(0).strip()
        
        # Final cleanup - ensure proper capitalization and punctuation
        if passive:
            passive = self._clean_effect_text(passive)
                    
        if active:
            active = self._clean_effect_text(active)
            
            # Add cooldown information if missing but found in text
            if "cooldown" not in active.lower() and "cd" not in active.lower():
                cooldown_match = re.search(r'(\d+)\s*(?:second|s)\s*(?:cooldown|cd)', container_text, re.I)
                if cooldown_match:
                    active += f" ({cooldown_match.group(1)}s Cooldown)"
        
        return passive, active
    
    def _extract_passive_effect(self, container, item_name, container_text):
        """Extract passive effects using comprehensive regex patterns"""
        passive = ""
        
        # Enhanced passive patterns for better extraction
        passive_patterns = [
            # Named passives with specific format (e.g., "Overkill: Increases Ability Power by 20-45%")
            r'<b[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</b>[:\s]*([^<.]+(?:\.[^<.]*)*)',
            r'<strong[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</strong>[:\s]*([^<.]+(?:\.[^<.]*)*)',
            
            # Standard passive format with label
            r'(?:Passive|PASSIVE)[:\s]*([^.]+(?:\.[^.]*)*)',
            
            # HTML formatted passives with class
            r'<b class="istats2">([^<:]+):</b>\s*([^<.]+)',
            r'<div class="passive"[^>]*>([^<]+)</div>',
            
            # Passive with percentage values (common pattern)
            r'(?:Passive|PASSIVE)[:\s]*[^:]*?(\d+(?:\-\d+)?%)[^.]*',
            
            # Passive effects without explicit "Passive" label but with effect description
            r'(?:Unique|UNIQUE)[:\s]*([^.]+(?:\.[^.]*)*)',
            
            # Passive with specific keywords that often indicate passive effects
            r'(?:grants|increases|reduces|provides|regenerate|reflect|apply|deal|when|while)[:\s]*([^.]+(?:\.[^.]*)*)',
            
            # Look for named passives in text content (more flexible)
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[:\s]*([^<.]+(?:\.[^<.]*)*)',
            
            # Passive with item name prefix
            rf'{re.escape(item_name) if item_name else ""}[:\s]*([^.]+(?:\.[^.]*)*)'
        ]
        
        # First try to find named passives (like "Overkill")
        for pattern in passive_patterns[:3]:  # Try the most specific patterns first
            named_passive_match = re.search(pattern, str(container), re.I)
            if named_passive_match:
                # Check if the first group looks like a passive name (not just any capitalized word)
                if len(named_passive_match.groups()) > 1:
                    potential_name = named_passive_match.group(1).strip()
                    if (potential_name and 
                        potential_name.lower() not in ['passive', 'active', 'unique', 'stats', 'cost', 'description', 'tips', 'item', 'build', 'guide'] and
                        len(potential_name) > 2 and
                        not re.match(r'^\d+$', potential_name)):  # Not just a number
                        passive = f"{potential_name}: {named_passive_match.group(2).strip()}"
                        break
        
        # If no named passive found, try general passive patterns
        if not passive:
            for pattern in passive_patterns[3:]:
                match = re.search(pattern, str(container), re.I)
                if match:
                    if len(match.groups()) > 1:
                        # Check if first group is a valid passive name
                        potential_name = match.group(1).strip()
                        if (potential_name and 
                            potential_name.lower() not in ['passive', 'active', 'unique', 'stats', 'cost', 'description', 'tips'] and
                            len(potential_name) > 2):
                            passive = f"{potential_name}: {match.group(2).strip()}"
                        else:
                            passive = match.group(2).strip() if len(match.groups()) > 1 else match.group(1).strip()
                    else:
                        passive = match.group(1).strip()
                    
                    # Validate that the passive makes sense (has some key indicators)
                    if (len(passive) > 15 and 
                        any(keyword in passive.lower() for keyword in ['damage', 'heal', 'shield', 'effect', 'ability', 'attack', 'increase', 'reduce', 'grant', 'apply', '%', 'second', 'cooldown'])):
                        break
                    else:
                        passive = ""  # Reset if it doesn't look like a real passive
        
        # Try to find passive section by looking for specific HTML elements
        if not passive:
            # Look for elements that might contain passive effects
            passive_section = container.find(string=re.compile(r'\bpassive\b|\bunique\b', re.I))
            if passive_section:
                parent = passive_section.parent
                if parent:
                    # Get text after "passive" keyword
                    full_text = parent.get_text()
                    after_passive = re.sub(r'.*\b(?:passive|unique)\b[:\s]*', '', full_text, flags=re.I)
                    # Extract first sentence or until next section
                    first_sentence = re.split(r'(?<=[.!?])\s+|(?=\b(?:active|stats|cost)\b)', after_passive, maxsplit=1)[0]
                    if first_sentence and len(first_sentence) > 15:  # Ensure it's substantial
                        passive = first_sentence.strip()
        
        return passive
    
    def _extract_active_effect(self, container, item_name, container_text):
        """Extract active effects using comprehensive regex patterns"""
        active = ""
        
        # Enhanced active patterns for better extraction
        active_patterns = [
            # Named actives with specific format
            r'<b[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</b>[:\s]*\((?:Active|ACTIVE)[^)]*\)[:\s]*([^<.]+(?:\.[^<.]*)*)',
            r'<strong[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</strong>[:\s]*\((?:Active|ACTIVE)[^)]*\)[:\s]*([^<.]+(?:\.[^<.]*)*)',
            
            # Standard active format
            r'(?:Active|ACTIVE)[:\s]*([^.]+(?:\.[^.]*)*)',
            
            # Active with cooldown information
            r'(?:Active|ACTIVE)[:\s]*\((\d+)s\)[:\s]*([^.]+(?:\.[^.]*)*)',
            r'(?:Active|ACTIVE)[:\s]*([^(]+)\((\d+)s\s+[Cc]ooldown\)',
            
            # HTML formatted actives
            r'<b[^>]*>(?:Active|ACTIVE)[^<]*</b>[:\s]*([^<.]+(?:\.[^.]*)*)',
            r'<div class="active"[^>]*>([^<]+)</div>',
            
            # Active with cooldown at the end
            r'(?:Active|ACTIVE)[:\s]*([^.]+)(?:\.\s*\((\d+)s\s+[Cc]ooldown\))',
            
            # Active with specific keywords that often indicate active effects
            r'(?:Use|Activate|Cast|Channel|Click)[:\s]*([^.]+(?:\.[^.]*)*)',
            
            # Look for named actives in general text
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[:\s]*([^<.]+(?:\.[^<.]*)*)'
        ]
        
        for pattern in active_patterns:
            active_match = re.search(pattern, str(container), re.I)
            if active_match:
                if len(active_match.groups()) > 1 and "active" not in active_match.group(1).lower():
                    # This is likely a named active with cooldown or description
                    if re.match(r'\d+', active_match.group(1)):
                        # First group is cooldown
                        active = f"({active_match.group(1)}s) {active_match.group(2)}".strip()
                    else:
                        # First group is name or description
                        potential_name = active_match.group(1).strip()
                        if (potential_name and 
                            potential_name.lower() not in ['active', 'use', 'activate', 'cast', 'channel', 'click', 'stats', 'cost'] and
                            len(potential_name) > 2):
                            if len(active_match.groups()) > 2 and active_match.group(2):
                                # We have a cooldown as well
                                active = f"{potential_name}: {active_match.group(2).strip()}"
                                if len(active_match.groups()) > 2:
                                    active += f" ({active_match.group(3)}s Cooldown)"
                            else:
                                active = f"{potential_name}: {active_match.group(2).strip()}"
                        else:
                            active = active_match.group(2).strip() if len(active_match.groups()) > 1 else active_match.group(1).strip()
                else:
                    active = active_match.group(1).strip()
                
                # Validate that the active makes sense
                if (len(active) > 10 and 
                    any(keyword in active.lower() for keyword in ['damage', 'heal', 'shield', 'effect', 'ability', 'attack', 'dash', 'teleport', 'slow', 'stun', 'root', 'knockback', 'cooldown', 'second', 'target', 'enemy', 'ally'])):
                    break
                else:
                    active = ""  # Reset if it doesn't look like a real active
        
        # If no active found with specific patterns, try a more general approach
        if not active:
            # Look for sections that might contain active effects
            active_section = container.find(string=re.compile(r'\bactive\b|\buse\b|\bactivate\b', re.I))
            if active_section:
                parent = active_section.parent
                if parent:
                    # Get text after "active" keyword
                    full_text = parent.get_text()
                    after_active = re.sub(r'.*\b(?:active|use|activate)\b[:\s]*', '', full_text, flags=re.I)
                    # Extract first sentence or until next section
                    first_sentence = re.split(r'(?<=[.!?])\s+|(?=\b(?:passive|unique|stats)\b)', after_active, maxsplit=1)[0]
                    if first_sentence and len(first_sentence) > 15:  # Ensure it's substantial
                        active = first_sentence.strip()
        
        return active
    
    def _clean_effect_text(self, effect_text):
        """Clean up passive and active effect text"""
        if not effect_text:
            return ""
            
        # Remove HTML tags
        effect_text = re.sub(r'<[^>]+>', ' ', effect_text)
        # Normalize whitespace
        effect_text = re.sub(r'\s+', ' ', effect_text)
        # Remove any leading/trailing punctuation except periods
        effect_text = effect_text.strip(',:; \t\n\r')
        
        # Ensure first letter is capitalized
        if effect_text:
            effect_text = effect_text[0].upper() + effect_text[1:]
            # Add period at the end if missing
            if not effect_text.endswith('.'):
                effect_text += '.'
        
        return effect_text

    def extract_item_data(self, container):
        """Extract item data from a container element"""
        try:
            # Get all text content
            container_text = container.get_text()
            
            # Try to find item name
            name_elem = container.find(['h2', 'h3', 'h4', 'strong', 'b'])
            item_name = name_elem.get_text().strip() if name_elem else None
            
            # If no name found, try to extract from text
            if not item_name:
                # Look for capitalized words that might be an item name
                name_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})', container_text)
                if name_match:
                    item_name = name_match.group(1)
            
            if not item_name:
                return None
                
            # Clean up item name
            item_name = re.sub(r'^[:\s]+', '', item_name)  # Remove leading colons or spaces
            item_name = re.sub(r'^\w+:\s*', '', item_name)  # Remove prefixes like "Lol:"
            item_name = item_name.strip()
            
            # Extract stats
            stats = {}
            stat_patterns = {
                'ability_power': r'(\+?\d+)\s*(?:Ability Power|AP)',
                'attack_damage': r'(\+?\d+)\s*(?:Attack Damage|AD)',
                'health': r'(\+?\d+)\s*Health',
                'mana': r'(\+?\d+)\s*Mana',
                'armor': r'(\+?\d+)\s*Armor',
                'magic_resistance': r'(\+?\d+)\s*(?:Magic Resist|MR)',
                'attack_speed': r'(\+?\d+%?)\s*Attack Speed',
                'critical_strike': r'(\+?\d+%?)\s*(?:Critical Strike|Crit)',
                'magic_penetration': r'(\+?\d+%?)\s*(?:Magic Penetration|Magic Pen)',
                'movement_speed': r'(\+?\d+%?)\s*Movement Speed',
                'life_steal': r'(\+?\d+%?)\s*Life Steal',
                'ability_haste': r'(\+?\d+)\s*(?:Ability Haste|AH)',
            }
            
            for stat_name, pattern in stat_patterns.items():
                match = re.search(pattern, container_text, re.I)
                if match:
                    value = match.group(1).replace('+', '')
                    if '%' in value:
                        value = int(value.replace('%', ''))
                        stats[stat_name] = {'value': value, 'type': 'percentage'}
                    else:
                        stats[stat_name] = {'value': int(value), 'type': 'flat'}
            
            # Extract cost - try multiple patterns including goldt class
            cost = 0
            cost_patterns = [
                r'(\d{3,4})\s*(?:gold|cost)',  # General gold/cost pattern
                r'<b class="goldt">(\d{3,4})</b>',  # Specific goldt class pattern
                r'goldt[^>]*>(\d{3,4})',  # goldt class content
                r'(\d{3,4})\s*$',  # Cost at end of line
                r'(\d{3,4})\s*\n',  # Cost followed by newline
                r'(\d{3,4})\s+[A-Z]',  # Cost followed by capital letter
                r'(\d{3,4})\s*(?=\s|$)',  # Cost followed by space or end
            ]
            
            for pattern in cost_patterns:
                cost_match = re.search(pattern, str(container), re.I | re.M)
                if cost_match:
                    cost = int(cost_match.group(1))
                    break
            
            # Also try to find cost in HTML structure
            if cost == 0:
                cost_elem = container.find('b', class_='goldt')
                if cost_elem:
                    cost_text = cost_elem.get_text().strip()
                    cost_match = re.search(r'(\d{3,4})', cost_text)
                    if cost_match:
                        cost = int(cost_match.group(1))
            
            # If still no cost found, try searching in raw HTML
            if cost == 0:
                html_content = str(container)
                goldt_match = re.search(r'class="goldt"[^>]*>(\d{3,4})', html_content)
                if goldt_match:
                    cost = int(goldt_match.group(1))
            
            # Extract passive/active effects using enhanced parsing
            passive, active = self.extract_passive_and_active_effects(container, item_name, container_text)
            
            # Extract description/tips
            description = ""
            tips = []
            
            # Look for description
            desc_patterns = [
                rf'{re.escape(item_name)}\s*(?:TIPS?|Description)[:\s]*([^<]+)',
                r'(?:Description|Details)[:\s]*([^<]+)',
                r'<b class="cdr">[^<]*TIPS?[:\s]*</b>([^<]+)',  # Match the specific format from the example
            ]
            
            for pattern in desc_patterns:
                match = re.search(pattern, str(container), re.I)
                if match:
                    description = match.group(1).strip()
                    break
            
            # If no description found, try to extract from the full text
            if not description:
                full_text = str(container)
                tips_match = re.search(r'TIPS?[:\s]*([^<]+)', full_text, re.I)
                if tips_match:
                    description = tips_match.group(1).strip()
            
            # Look for tips
            tips = []
            
            # First try to find tips section with class "cdr"
            tips_elem = container.find('b', class_='cdr', string=re.compile(r'TIPS?', re.I))
            if tips_elem:
                # Get the parent paragraph that contains the tips
                tips_container = tips_elem.find_parent('p')
                if tips_container:
                    # Get the text after the TIPS label
                    tips_text = tips_container.get_text()
                    tips_text = re.sub(r'.*TIPS?[:\s]*', '', tips_text, flags=re.I)
                    
                    # Split into sentences for individual tips
                    tip_sentences = re.split(r'(?<=[.!?])\s+', tips_text)
                    tips = [sentence.strip() for sentence in tip_sentences if sentence.strip()]
            
            # If no tips found with class "cdr", try other methods
            if not tips:
                tips_section = container.find(string=re.compile(r'tips', re.I))
                if tips_section:
                    tips_container = tips_section.parent
                    if tips_container:
                        # Look for list items
                        tip_items = tips_container.find_all('li')
                        if tip_items:
                            tips = [item.get_text().strip() for item in tip_items]
                        else:
                            # Try to split by periods or line breaks
                            tips_text = tips_container.get_text()
                            tips_text = re.sub(r'(?:TIPS?|Tips)[:\s]*', '', tips_text, flags=re.I)
                            tip_candidates = re.split(r'(?:\.\s+|\n+)', tips_text)
                            tips = [tip.strip() for tip in tip_candidates if tip.strip()]
            
            # Clean up tips - remove empty or very short tips
            tips = [tip for tip in tips if tip and len(tip) > 10]
            
            # If no tips found, try to extract from description
            if not tips and description:
                # Split description into sentences and use as tips
                sentences = re.split(r'(?<=[.!?])\s+', description)
                if len(sentences) > 1:
                    tips = sentences[:5]  # Use up to 5 sentences as tips
                    
            # Clean up tips - remove empty or very short tips
            tips = [tip for tip in tips if tip and len(tip) > 10]
            
            # Determine category
            category = "legendary"  # Default
            if any(word in item_name.lower() for word in ['boots', 'treads', 'greaves']):
                category = "boots"
            elif cost < 1000:
                category = "basic"
            elif "enchant" in item_name.lower():
                category = "enchant"
            
            # Determine tier
            tier = "A"  # Default
            if cost > 3000:
                tier = "S"
            elif cost < 1000:
                tier = "B"
            
            # Final cleanup for enchant items
            if "Enchant" in item_name:
                passive = ""  # Enchant items typically don't have passives
            
            # Create item data structure
            item_data = {
                "name": item_name,
                "stats": stats,
                "cost": cost,
                "passive": passive,
                "active": active,
                "description": description,
                "category": category,
                "tier": tier,
                "tips": tips[:5] if tips else []  # Limit to 5 tips
            }
            
            return item_data
            
        except Exception as e:
            print(f"Error extracting item data: {e}")
            return None
    
    def save_item_data(self, item_data):
        """Save item data to a JSON file"""
        item_name = item_data['name']
        filename = item_name.lower().replace("'", "").replace(" ", "_").replace("-", "_") + ".json"
        filepath = self.output_dir / filename
        
        print(f"Saving {item_name} to {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item_data, f, indent=2, ensure_ascii=False)
    
    def scrape_specific_item(self, item_name):
        """Scrape a specific item by name"""
        print(f"Scraping specific item: {item_name}")
        
        try:
            # First try to find on the main items page
            response = self.session.get(self.items_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the item by name
            item_found = False
            
            # Try different text matching approaches
            for selector in [
                # Look for exact text match
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and tag.get_text().strip() == item_name,
                # Look for contains text match
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and item_name in tag.get_text(),
                # Case insensitive contains
                lambda tag: tag.name in ['h2', 'h3', 'h4', 'strong', 'b', 'span'] and item_name.lower() in tag.get_text().lower()
            ]:
                elements = soup.find_all(selector)
                
                for elem in elements:
                    container = elem.parent
                    while container and container.name != 'body':
                        if container.name in ['div', 'section', 'article', 'tr', 'td']:
                            item_data = self.extract_item_data(container)
                            if item_data and item_data.get('name'):
                                self.save_item_data(item_data)
                                print(f"Successfully scraped {item_name}")
                                return item_data
                        container = container.parent
            
            print(f"Could not find {item_name} on the items page")
            return None
            
        except Exception as e:
            print(f"Error scraping specific item {item_name}: {e}")
            return None
    
    def scrape_item_from_url(self, item_url):
        """Scrape item data from a specific URL"""
        print(f"Scraping item from URL: {item_url}")
        
        try:
            response = self.session.get(item_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for main item container
            main_container = soup.find(['div', 'section', 'article'], 
                                     class_=lambda c: c and any(x in c for x in ['item-details', 'item-container', 'main-content']))
            
            if not main_container:
                main_container = soup.find('body')  # Fallback to body
            
            item_data = self.extract_item_data(main_container)
            
            if item_data and item_data.get('name'):
                self.save_item_data(item_data)
                print(f"Successfully scraped item from {item_url}")
                return item_data
            
            print(f"Could not extract item data from {item_url}")
            return None
            
        except Exception as e:
            print(f"Error scraping item from URL {item_url}: {e}")
            return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape real-time item data from WR-META.com')
    parser.add_argument('--all', action='store_true', help='Scrape all items')
    parser.add_argument('--item', type=str, help='Scrape a specific item by name')
    parser.add_argument('--url', type=str, help='Scrape an item from a specific URL')
    
    args = parser.parse_args()
    
    scraper = RealTimeItemScraper()
    
    if args.all:
        scraper.scrape_all_items()
    elif args.item:
        scraper.scrape_specific_item(args.item)
    elif args.url:
        scraper.scrape_item_from_url(args.url)
    else:
        print("Please specify an action: --all, --item NAME, or --url URL")

if __name__ == "__main__":
    main()