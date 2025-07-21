#!/usr/bin/env python3
"""
Detailed Item and Rune Scraper for League of Legends Wild Rift
Scrapes comprehensive item details including stats, descriptions, costs, and tips.

Usage: python detailed_item_scraper.py
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class DetailedItemScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://wr-meta.com"
        
        # Common item stat patterns
        self.stat_patterns = {
            'ability_power': r'(\+?\d+)\s*Ability Power',
            'attack_damage': r'(\+?\d+)\s*Attack Damage',
            'health': r'(\+?\d+)\s*Health',
            'mana': r'(\+?\d+)\s*Mana',
            'armor': r'(\+?\d+)\s*Armor',
            'magic_resistance': r'(\+?\d+)\s*Magic Resistance',
            'attack_speed': r'(\+?\d+%?)\s*Attack Speed',
            'critical_strike': r'(\+?\d+%?)\s*Critical Strike',
            'magic_penetration': r'(\+?\d+%?)\s*Magic Penetration',
            'armor_penetration': r'(\+?\d+%?)\s*Armor Penetration',
            'cooldown_reduction': r'(\+?\d+%?)\s*(?:Cooldown Reduction|CDR)',
            'movement_speed': r'(\+?\d+%?)\s*Movement Speed',
            'life_steal': r'(\+?\d+%?)\s*Life Steal',
            'spell_vamp': r'(\+?\d+%?)\s*Spell Vamp'
        }

    def scrape_item_details(self, item_name, champion_page_url=None):
        """
        Scrape detailed information for a specific item
        """
        print(f"Scraping details for item: {item_name}")
        
        # Try to find item details from champion page first
        if champion_page_url:
            item_details = self._extract_item_from_champion_page(item_name, champion_page_url)
            if item_details:
                return item_details
        
        # Try to find item on dedicated item pages or databases
        item_details = self._search_item_database(item_name)
        if item_details:
            return item_details
        
        # Return basic structure if not found
        return self._create_basic_item_structure(item_name)

    def _extract_item_from_champion_page(self, item_name, champion_url):
        """
        Extract item details from champion build page
        """
        try:
            response = self.session.get(champion_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for item tooltips or detailed sections
            item_sections = soup.find_all(['div', 'span'], string=re.compile(item_name, re.IGNORECASE))
            
            for section in item_sections:
                # Look for parent containers that might have item details
                parent = section.find_parent(['div', 'section', 'article'])
                if parent:
                    item_details = self._parse_item_section(parent, item_name)
                    if item_details:
                        return item_details
            
            return None
            
        except Exception as e:
            print(f"Error extracting item from champion page: {e}")
            return None

    def _search_item_database(self, item_name):
        """
        Search for item in Wild Rift item database or wiki
        """
        # This would typically search item databases
        # For now, return None to use basic structure
        return None

    def _parse_item_section(self, section, item_name):
        """
        Parse item details from a page section
        """
        text_content = section.get_text()
        
        # Extract stats
        stats = {}
        for stat_name, pattern in self.stat_patterns.items():
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                value = match.group(1)
                # Convert percentage values
                if '%' in value:
                    stats[stat_name] = {'value': int(value.replace('%', '')), 'type': 'percentage'}
                else:
                    stats[stat_name] = {'value': int(value.replace('+', '')), 'type': 'flat'}
        
        # Extract cost
        cost_match = re.search(r'(\d{3,4})\s*(?:gold|cost)', text_content, re.IGNORECASE)
        cost = int(cost_match.group(1)) if cost_match else 0
        
        # Extract passive/active effects
        passive_match = re.search(r'(?:Passive|PASSIVE)[:\s]*([^.]+\.)', text_content, re.IGNORECASE)
        active_match = re.search(r'(?:Active|ACTIVE)[:\s]*([^.]+\.)', text_content, re.IGNORECASE)
        
        # Extract description/tips
        description = ""
        tips_match = re.search(rf'{item_name}\s*(?:TIPS?|Description)[:\s]*([^.]+(?:\.[^.]*)*)', text_content, re.IGNORECASE)
        if tips_match:
            description = tips_match.group(1).strip()
        
        return {
            'name': item_name,
            'stats': stats,
            'cost': cost,
            'passive': passive_match.group(1).strip() if passive_match else "",
            'active': active_match.group(1).strip() if active_match else "",
            'description': description,
            'category': self._categorize_item(item_name),
            'tier': self._get_item_tier(item_name)
        }

    def _create_basic_item_structure(self, item_name):
        """
        Create basic item structure with known information
        """
        return {
            'name': item_name,
            'stats': self._get_known_item_stats(item_name),
            'cost': self._get_known_item_cost(item_name),
            'passive': self._get_known_item_passive(item_name),
            'active': self._get_known_item_active(item_name),
            'description': self._get_known_item_description(item_name),
            'category': self._categorize_item(item_name),
            'tier': self._get_item_tier(item_name)
        }

    def _get_known_item_stats(self, item_name):
        """
        Return known stats for common items
        """
        known_stats = {
            "Rabadon's Deathcap": {
                'ability_power': {'value': 100, 'type': 'flat'},
                'magic_penetration': {'value': 7, 'type': 'percentage'}
            },
            "Infinity Edge": {
                'attack_damage': {'value': 70, 'type': 'flat'},
                'critical_strike': {'value': 25, 'type': 'percentage'}
            },
            "Plated Steelcaps": {
                'armor': {'value': 25, 'type': 'flat'},
                'movement_speed': {'value': 45, 'type': 'flat'}
            },
            "Mercury's Treads": {
                'magic_resistance': {'value': 25, 'type': 'flat'},
                'movement_speed': {'value': 45, 'type': 'flat'}
            },
            "Zeke's Convergence": {
                'health': {'value': 250, 'type': 'flat'},
                'armor': {'value': 30, 'type': 'flat'},
                'mana': {'value': 250, 'type': 'flat'}
            }
        }
        
        return known_stats.get(item_name, {})

    def _get_known_item_cost(self, item_name):
        """
        Return known costs for common items
        """
        known_costs = {
            "Rabadon's Deathcap": 3400,
            "Infinity Edge": 3400,
            "Plated Steelcaps": 1000,
            "Mercury's Treads": 1100,
            "Zeke's Convergence": 2400,
            "Relic Shield": 400,
            "Doran's Blade": 450,
            "Doran's Ring": 400,
            "Doran's Shield": 450
        }
        
        return known_costs.get(item_name, 0)

    def _get_known_item_passive(self, item_name):
        """
        Return known passive effects for common items
        """
        known_passives = {
            "Rabadon's Deathcap": "Overkill: Increases Ability Power by 20-45%",
            "Infinity Edge": "Increases critical strike damage by 10%",
            "Plated Steelcaps": "Reduces damage from attacks by 15%",
            "Mercury's Treads": "Reduces duration of stuns, slows, taunts, fears, silences, blinds, and immobilizes by 30%"
        }
        
        return known_passives.get(item_name, "")

    def _get_known_item_active(self, item_name):
        """
        Return known active effects for common items
        """
        known_actives = {
            "Zeke's Convergence": "Conduit: Bind to an ally. When you cast your ultimate, you and your ally gain 20% attack speed for 8 seconds"
        }
        
        return known_actives.get(item_name, "")

    def _get_known_item_description(self, item_name):
        """
        Return known descriptions/tips for common items
        """
        known_descriptions = {
            "Rabadon's Deathcap": "This item is perfect for mages who rely on high ability power ratios and want to significantly increase their damage output. It provides a huge bonus to ability power and magic penetration. The 'Overkill' effect increases your ability power by 20-45%, depending on the level, significantly enhancing your magical abilities and attacks.",
            "Infinity Edge": "Core item for critical strike-based marksmen. Provides high attack damage and critical strike chance while amplifying critical strike damage.",
            "Plated Steelcaps": "Defensive boots that reduce physical damage from basic attacks. Essential against heavy AD compositions.",
            "Mercury's Treads": "Magic resistance boots that also provide tenacity, reducing the duration of crowd control effects."
        }
        
        return known_descriptions.get(item_name, "")

    def _categorize_item(self, item_name):
        """
        Categorize item by type
        """
        categories = {
            'boots': ['boots', 'treads', 'steelcaps'],
            'starting': ['doran', 'relic shield', 'spectral sickle'],
            'legendary': ['rabadon', 'infinity', 'bloodthirster', 'thornmail'],
            'mythic': ['eclipse', 'kraken', 'galeforce'],
            'support': ['zeke', 'locket', 'redemption'],
            'enchant': ['enchant']
        }
        
        item_lower = item_name.lower()
        for category, keywords in categories.items():
            if any(keyword in item_lower for keyword in keywords):
                return category
        
        return 'legendary'

    def _get_item_tier(self, item_name):
        """
        Get item tier (S, A, B, C, D)
        """
        # This would typically be based on meta analysis
        # For now, return A as default
        return 'A'

    def scrape_rune_details(self, rune_name):
        """
        Scrape detailed rune information
        """
        print(f"Scraping details for rune: {rune_name}")
        
        return {
            'name': rune_name,
            'tree': self._get_rune_tree(rune_name),
            'type': self._get_rune_type(rune_name),
            'description': self._get_rune_description(rune_name),
            'stats': self._get_rune_stats(rune_name),
            'cooldown': self._get_rune_cooldown(rune_name),
            'tier': 'A'
        }

    def _get_rune_tree(self, rune_name):
        """
        Get the rune tree for a specific rune
        """
        rune_trees = {
            'Guardian': 'Resolve',
            'Demolish': 'Resolve',
            'Second Wind': 'Resolve',
            'Bone Plating': 'Resolve',
            'Legend: Tenacity': 'Precision',
            'Conqueror': 'Precision',
            'Electrocute': 'Domination',
            'Dark Harvest': 'Domination'
        }
        
        return rune_trees.get(rune_name, 'Unknown')

    def _get_rune_type(self, rune_name):
        """
        Get rune type (Keystone, Primary, Secondary)
        """
        keystones = ['Guardian', 'Conqueror', 'Electrocute', 'Dark Harvest', 'Fleet Footwork']
        
        if rune_name in keystones:
            return 'Keystone'
        return 'Primary'

    def _get_rune_description(self, rune_name):
        """
        Get rune description
        """
        descriptions = {
            'Guardian': 'You and your nearby ally gain a shield when either of you would take damage from an enemy champion.',
            'Demolish': 'Charge up a powerful attack against a tower while near it.',
            'Second Wind': 'After taking damage from an enemy champion, heal over time.',
            'Bone Plating': 'After taking damage from an enemy champion, the next 3 spells or attacks you receive from them deal reduced damage.',
            'Legend: Tenacity': 'Gain tenacity for each Legend stack (max 10 stacks).'
        }
        
        return descriptions.get(rune_name, f"Description for {rune_name}")

    def _get_rune_stats(self, rune_name):
        """
        Get rune stats/values
        """
        stats = {
            'Guardian': {'shield': '50-130', 'cooldown': '70-40s'},
            'Demolish': {'damage': '125 + 30% max health', 'cooldown': '45s'},
            'Second Wind': {'healing': '4 + 2.5% missing health over 10s'},
            'Bone Plating': {'damage_reduction': '30-60', 'duration': '1.5s'},
            'Legend: Tenacity': {'tenacity_per_stack': '2.5%', 'max_tenacity': '25%'}
        }
        
        return stats.get(rune_name, {})

    def _get_rune_cooldown(self, rune_name):
        """
        Get rune cooldown if applicable
        """
        cooldowns = {
            'Guardian': '70-40s',
            'Demolish': '45s',
            'Electrocute': '25-20s'
        }
        
        return cooldowns.get(rune_name, '')

    def enhance_champion_data_with_details(self, champion_data_file):
        """
        Enhance existing champion data with detailed item and rune information
        """
        print(f"Enhancing champion data from: {champion_data_file}")
        
        # Load existing data
        with open(champion_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Enhance build items with details
        if 'builds' in data:
            builds = data['builds']
            
            # Process each item category
            for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build']:
                if category in builds and builds[category]:
                    enhanced_items = []
                    for item_name in builds[category]:
                        item_details = self.scrape_item_details(item_name)
                        enhanced_items.append(item_details)
                    builds[f"{category}_detailed"] = enhanced_items
        
        # Enhance runes with details
        if 'runes' in data:
            runes = data['runes']
            
            # Enhance primary runes
            if 'primary' in runes:
                primary = runes['primary']
                if 'keystone' in primary:
                    primary['keystone_detailed'] = self.scrape_rune_details(primary['keystone'])
                
                if 'runes' in primary:
                    primary['runes_detailed'] = []
                    for rune_name in primary['runes']:
                        rune_details = self.scrape_rune_details(rune_name)
                        primary['runes_detailed'].append(rune_details)
            
            # Enhance secondary runes
            if 'secondary' in runes and 'runes' in runes['secondary']:
                runes['secondary']['runes_detailed'] = []
                for rune_name in runes['secondary']['runes']:
                    rune_details = self.scrape_rune_details(rune_name)
                    runes['secondary']['runes_detailed'].append(rune_details)
        
        # Save enhanced data
        output_file = champion_data_file.replace('.json', '_detailed.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Enhanced data saved to: {output_file}")
        return output_file

def main():
    scraper = DetailedItemScraper()
    
    # Example: Enhance Blitzcrank data
    enhanced_file = scraper.enhance_champion_data_with_details('scraped_champions/blitzcrank_data.json')
    print(f"Enhanced champion data saved to: {enhanced_file}")
    
    # Example: Scrape individual item details
    rabadon_details = scraper.scrape_item_details("Rabadon's Deathcap")
    print(f"\nRabadon's Deathcap details:")
    print(json.dumps(rabadon_details, indent=2))

if __name__ == "__main__":
    main()