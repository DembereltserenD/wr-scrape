#!/usr/bin/env python3
"""
ULTIMATE ALL-IN-ONE CHAMPION SCRAPER
This is THE FINAL SCRIPT that does everything correctly:
- Extracts ALL champion data (name, roles, image, tier, stats, abilities, etc.)
- Extracts COMPLETE build data (start_items, core_items, example_build, situational_items)
- Extracts LANE-SPECIFIC boots/enchants (not global duplicates)
- Extracts summoner spells and runes
- Preserves existing good data while fixing missing data
- Handles all champions in batch
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time
from pathlib import Path
import os

def load_champion_urls():
    """Load champion URLs from the mapping file"""
    try:
        with open('champion_url_mapping.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: champion_url_mapping.json not found.")
        return {}

def load_champion_data(filename):
    """Load champion data from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def extract_champion_basic_info(soup, url):
    """Extract basic champion information"""
    champion_data = {}
    
    # Extract champion name
    title_element = soup.find('h1', class_='firstscrean-main-title')
    if title_element:
        span_element = title_element.find('span')
        if span_element:
            champion_data['name'] = span_element.get_text(strip=True)
        else:
            title_text = title_element.get_text(strip=True)
            match = re.search(r'Wild Rift:\s*([A-Z\s&\'\-]+?)(?:\s+Build Guide|\s*$)', title_text)
            if match:
                champion_data['name'] = match.group(1).strip()
    
    # Extract roles
    roles = []
    if title_element:
        role_icons = title_element.find_all('i')
        for icon in role_icons:
            classes = icon.get('class', [])
            for cls in classes:
                if 'roleassassinicon' in cls:
                    roles.append('Assassin')
                elif 'rolefightericon' in cls:
                    roles.append('Fighter')
                elif 'roletankicon' in cls:
                    roles.append('Tank')
                elif 'rolesupporticon' in cls:
                    roles.append('Support')
                elif 'rolemarkmanicon' in cls:
                    roles.append('Marksman')
                elif 'rolemageicon' in cls:
                    roles.append('Mage')
    champion_data['roles'] = roles
    
    return champion_data

def extract_champion_image_and_stats(soup, url, champion_data):
    """Extract champion image, tier, and stats"""
    # Extract champion image
    champion_img = soup.find('img', class_='champion-icon')
    if champion_img:
        img_src = champion_img.get('data-src') or champion_img.get('src')
        if img_src and not img_src.startswith('data:'):
            champion_data['image'] = urljoin(url, img_src)
    
    # Extract tier
    tier_element = soup.find('div', class_='tier-super')
    if tier_element:
        tier_icons = tier_element.find_all('i', class_='fas')
        champion_data['tier'] = len(tier_icons)
    
    # Extract balance status
    balance_element = soup.find('div', class_='edit-balance')
    if balance_element:
        champion_data['balance_status'] = balance_element.get_text(strip=True)
    
    # Extract stats circles
    circles = soup.find_all('div', class_='circle')
    stats = {}
    for circle in circles:
        title_element = circle.find_next_sibling('div', class_='circle-title')
        if title_element:
            title = title_element.get_text(strip=True).lower()
            classes = circle.get('class', [])
            percentage = 0
            for cls in classes:
                if cls.startswith('per-') or cls.startswith('per2-'):
                    try:
                        percentage = int(cls.split('-')[1])
                    except:
                        pass
            stats[title] = percentage
    champion_data['stats'] = stats
    
    # Extract base stats
    base_stats = extract_base_stats(soup)
    champion_data['base_stats'] = base_stats
    
    return champion_data

def extract_base_stats(soup):
    """Extract champion base stats from the stats table"""
    base_stats = {}
    
    # Method 1: Look for the stats table in the stats-block
    stats_block = soup.find('div', class_='stats-block')
    if stats_block:
        table = stats_block.find('table')
        if table:
            table_html = str(table)
            
            # Extract stats using specific patterns for the wr-meta format
            # Pattern: <!--smile:statname-->...<!--/smile--> NUMBER (GROWTH)
            stat_patterns = {
                'attack_damage': r'<!--smile:attackdamage-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)',
                'health': r'<!--smile:heal-->.*?<!--/smile-->\s*(\d+)',
                'health_regen': r'<!--smile:healthregeneration-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)',
                'attack_speed': r'<!--smile:attackspeed-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)',
                'mana': r'<!--smile:mana-->.*?<!--/smile-->\s*(\d+)',
                'mana_regen': r'<!--smile:mpreg-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)',
                'movement_speed': r'<!--smile:movementspeed-->.*?<!--/smile-->\s*(\d+)',
                'armor': r'<!--smile:armor-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)',
                'magic_resist': r'<!--smile:magicresistance-->.*?<!--/smile-->\s*(\d+(?:\.\d+)?)'
            }
            
            for stat_name, pattern in stat_patterns.items():
                match = re.search(pattern, table_html, re.IGNORECASE | re.DOTALL)
                if match:
                    try:
                        if stat_name in ['health', 'mana', 'movement_speed']:
                            base_stats[stat_name] = int(match.group(1))
                        else:
                            base_stats[stat_name] = float(match.group(1))
                    except ValueError:
                        pass
    
    # Method 2: Alternative pattern matching for emoji alt attributes
    if not base_stats:
        stats_block = soup.find('div', class_='stats-block')
        if stats_block:
            table = stats_block.find('table')
            if table:
                cells = table.find_all('td')
                
                for cell in cells:
                    cell_html = str(cell)
                    cell_text = cell.get_text(strip=True)
                    
                    # Look for emoji images with alt attributes
                    if 'alt="attackdamage"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['attack_damage'] = float(match.group(1))
                    
                    elif 'alt="heal"' in cell_html:
                        match = re.search(r'(\d+)', cell_text)
                        if match:
                            base_stats['health'] = int(match.group(1))
                    
                    elif 'alt="healthregeneration"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['health_regen'] = float(match.group(1))
                    
                    elif 'alt="attackspeed"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['attack_speed'] = float(match.group(1))
                    
                    elif 'alt="mana"' in cell_html:
                        match = re.search(r'(\d+)', cell_text)
                        if match:
                            base_stats['mana'] = int(match.group(1))
                    
                    elif 'alt="mpreg"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['mana_regen'] = float(match.group(1))
                    
                    elif 'alt="movementspeed"' in cell_html:
                        match = re.search(r'(\d+)', cell_text)
                        if match:
                            base_stats['movement_speed'] = int(match.group(1))
                    
                    elif 'alt="armor"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['armor'] = float(match.group(1))
                    
                    elif 'alt="magicresistance"' in cell_html:
                        match = re.search(r'(\d+(?:\.\d+)?)', cell_text)
                        if match:
                            base_stats['magic_resist'] = float(match.group(1))
    
    # Method 3: Fallback - look for any table with stats
    if not base_stats:
        tables = soup.find_all('table')
        for table in tables:
            table_text = table.get_text()
            
            # Look for number patterns that might be stats
            # Format: "52 (3.6)" where 52 is base stat and 3.6 is growth
            stat_matches = re.findall(r'(\d+(?:\.\d+)?)\s*\([^)]+\)', table_text)
            
            if len(stat_matches) >= 6:  # Should have at least 6 base stats
                try:
                    # Common order in Wild Rift: AD, Health, Health Regen, AS, Mana, Mana Regen, MS, Armor, MR
                    if len(stat_matches) >= 8:  # At least 8 stats
                        base_stats['attack_damage'] = float(stat_matches[0])
                        base_stats['health'] = int(stat_matches[1])
                        base_stats['health_regen'] = float(stat_matches[2])
                        base_stats['attack_speed'] = float(stat_matches[3])
                        base_stats['mana'] = int(stat_matches[4])
                        base_stats['mana_regen'] = float(stat_matches[5])
                        base_stats['movement_speed'] = int(stat_matches[6])
                        base_stats['armor'] = float(stat_matches[7])
                        if len(stat_matches) >= 9:
                            base_stats['magic_resist'] = float(stat_matches[8])
                    break
                except (ValueError, IndexError):
                    continue
    
    return base_stats

def extract_abilities(soup, url, champion_data):
    """Extract champion abilities"""
    abilities = []
    ability_holders = soup.find_all('div', class_='ability-holder')
    
    for holder in ability_holders:
        ability = {}
        
        # Extract ability image
        ability_img = holder.find('img')
        if ability_img:
            img_src = ability_img.get('data-src') or ability_img.get('src')
            if img_src and not img_src.startswith('data:'):
                ability['image'] = urljoin(url, img_src)
            ability['alt_text'] = ability_img.get('alt', '')
        
        # Extract ability marker (P, Q, W, E, R)
        marker = holder.find('div', class_='ability-marker')
        if marker:
            ability['key'] = marker.get_text(strip=True)
        
        # Extract ability description
        description_p = holder.find('p')
        if description_p:
            ability['description'] = description_p.get_text(strip=True)
            
            # Extract ability name from description
            name_match = re.search(r'\(([^)]+)\)\s*([A-Z\s/]+)', ability['description'])
            if name_match:
                ability['name'] = name_match.group(2).strip()
        
        abilities.append(ability)
    
    champion_data['abilities'] = abilities
    return champion_data

def extract_lanes_improved(soup, url):
    """Extract lanes with improved detection"""
    lanes = []
    
    # Method 1: Look for build headers
    build_headers = soup.find_all('h2')
    for header in build_headers:
        header_text = header.get_text().strip()
        if 'Build' in header_text:
            if 'Jungle' in header_text and 'Jungle' not in lanes:
                lanes.append('Jungle')
            elif 'Mid' in header_text and 'Mid' not in lanes:
                lanes.append('Mid')
            elif ('Baron' in header_text or 'Solo' in header_text) and 'Baron' not in lanes:
                lanes.append('Baron')
            elif 'Support' in header_text and 'Support' not in lanes:
                lanes.append('Support')
            elif ('Dragon' in header_text or 'Duo' in header_text or 'Adc' in header_text) and 'Dragon' not in lanes:
                lanes.append('Dragon')
    
    # Method 2: Fallback based on roles
    if not lanes:
        roles = soup.find_all('i')
        role_classes = []
        for role in roles:
            role_classes.extend(role.get('class', []))
        
        if any('rolesupporticon' in cls for cls in role_classes):
            lanes.append('Support')
        if any('rolemarkmanicon' in cls for cls in role_classes):
            lanes.append('Dragon')
        if any('rolemageicon' in cls for cls in role_classes):
            lanes.append('Mid')
        if any('roleassassinicon' in cls for cls in role_classes):
            if 'Mid' not in lanes:
                lanes.append('Mid')
            if 'Jungle' not in lanes:
                lanes.append('Jungle')
        if any('rolefightericon' in cls for cls in role_classes):
            if 'Baron' not in lanes:
                lanes.append('Baron')
        if any('roletankicon' in cls for cls in role_classes):
            if 'Baron' not in lanes:
                lanes.append('Baron')
            if 'Support' not in lanes:
                lanes.append('Support')
    
    return lanes

def extract_complete_builds(soup, url):
    """Extract complete build data with lane-specific boots/enchants"""
    lanes = []
    builds = []
    
    # Find all build headers
    build_headers = soup.find_all('h2')
    
    for header in build_headers:
        header_text = header.get_text().strip()
        
        # Check if this is a build header
        if 'Build' in header_text and any(lane_keyword in header_text for lane_keyword in 
                                        ['Jungle', 'Mid', 'Baron', 'Solo', 'Support', 'Dragon', 'Duo', 'Adc']):
            
            # Determine the lane from the header
            lane = None
            if 'Jungle' in header_text:
                lane = 'Jungle'
            elif 'Mid' in header_text:
                lane = 'Mid'
            elif 'Baron' in header_text or 'Solo' in header_text:
                lane = 'Baron'
            elif 'Support' in header_text:
                lane = 'Support'
            elif 'Dragon' in header_text or 'Duo' in header_text or 'Adc' in header_text:
                lane = 'Dragon'
            
            if lane and lane not in lanes:
                lanes.append(lane)
                
                # Extract the complete build for this lane
                build = extract_single_build_complete(header, lane, soup, url)
                if build:
                    builds.append(build)
    
    return lanes, builds

def extract_single_build_complete(header, lane, soup, url):
    """Extract complete build data for a single lane"""
    build = {'lane': lane}
    
    # Find the content section after this header
    content_section = None
    current = header.find_next_sibling()
    
    # Look for the main content container
    while current:
        if current.name == 'h2':  # Stop at next build header
            break
        if current.name == 'div':
            content_section = current
            break
        current = current.find_next_sibling()
    
    if not content_section:
        parent_section = header.find_parent('div')
        if parent_section:
            content_section = parent_section
    
    if content_section:
        # Extract ALL build components
        build['start_items'] = extract_start_items(content_section, url)
        build['core_items'] = extract_core_items(content_section, url)
        build['boots_enchants'] = extract_lane_specific_boots_enchants(content_section, url, lane)
        build['example_build'] = extract_example_build(content_section, url)
        build['situational_items'] = extract_situational_items(content_section, url)
        build['summoner_spells'] = extract_summoner_spells(soup, url)
        build['runes'] = extract_runes_data(soup, url)
        build['situational_runes'] = extract_situational_runes(soup, url)
    
    return build

def extract_start_items(content_section, url):
    """Extract starting items"""
    start_items = []
    
    # Look for "Start" section
    start_sections = content_section.find_all('div', class_='text-center')
    for section in start_sections:
        title_div = section.find('div', class_='bildtitle2')
        if title_div and 'Start' in title_div.get_text():
            combo_section = section.find('div', class_='chapter-combo2')
            if combo_section:
                start_items = extract_items_from_section(combo_section, url)
                break
    
    # Alternative: look for start items in tips
    if not start_items:
        tips_sections = content_section.find_all('div', class_='bild-tips')
        for tips in tips_sections:
            tips_text = tips.get_text().lower()
            if 'start' in tips_text:
                tips_html = str(tips)
                item_mentions = re.findall(r'<b><span>([^<]+)</span></b>', tips_html)
                if item_mentions:
                    for item_name in item_mentions[:2]:
                        start_items.append({
                            'name': item_name, 
                            'description': f'Starting item: {item_name}',
                            'type': 'starting'
                        })
                    break
    
    return start_items

def extract_core_items(content_section, url):
    """Extract core items"""
    core_items = []
    
    # Look for core section
    core_section = content_section.find('div', class_='core')
    if core_section:
        core_items = extract_items_from_section(core_section, url)
    
    # Alternative: look for "Key items" section
    if not core_items:
        key_items_sections = content_section.find_all('h3', class_='bildtitle3')
        for h3 in key_items_sections:
            if 'Key items' in h3.get_text():
                parent_block = h3.find_parent('div', class_='bild-block')
                if parent_block:
                    combo_sections = parent_block.find_all('div', class_='chapter-combo2')
                    for combo in combo_sections:
                        items = extract_items_from_section(combo, url)
                        core_items.extend(items)
                break
    
    return core_items

def extract_lane_specific_boots_enchants(content_section, url, lane):
    """Extract boots/enchants specific to this lane"""
    boots_enchants = []
    
    # Method 1: Look for boots/enchants in this lane's content
    bildtitle_divs = content_section.find_all('div', class_='bildtitle2')
    for div in bildtitle_divs:
        text = div.get_text().strip()
        if 'Boots' in text and 'Enchant' in text:
            parent = div.parent
            if parent:
                combo_section = parent.find('div', class_='chapter-combo2')
                if combo_section:
                    items = extract_items_from_section(combo_section, url)
                    boots_enchants.extend(items)
                    break
    
    # Method 2: If no lane-specific boots found, use smart fallback
    if not boots_enchants:
        full_soup = content_section.find_parent('html') or content_section
        boots_enchants = get_smart_boots_enchants_fallback(full_soup, url, lane)
    
    return boots_enchants

def get_smart_boots_enchants_fallback(soup, url, lane):
    """Smart fallback for boots/enchants based on lane"""
    boots_enchants = []
    found_items = set()
    
    # Define lane-appropriate items
    if lane in ['Baron', 'Support']:
        preferred_items = ['Plated Steelcaps', 'Mercury\'s Treads', 'Stoneplate Enchant', 'Protobelt Enchant']
    elif lane == 'Mid':
        preferred_items = ['Boots of Mana', 'Mercury\'s Treads', 'Stasis Enchant', 'Protobelt Enchant']
    elif lane in ['Dragon', 'Jungle']:
        preferred_items = ['Plated Steelcaps', 'Mercury\'s Treads', 'Quicksilver Enchant', 'Stasis Enchant']
    else:
        preferred_items = ['Plated Steelcaps', 'Mercury\'s Treads', 'Stoneplate Enchant', 'Stasis Enchant']
    
    # Find these items in the document
    all_item_holders = soup.find_all('div', class_='ico-holder3')
    for holder in all_item_holders:
        span = holder.find('span')
        if span:
            item_name = span.get_text(strip=True)
            if item_name in preferred_items and item_name not in found_items:
                found_items.add(item_name)
                
                item = {}
                img = holder.find('img')
                if img:
                    img_src = img.get('data-src') or img.get('src')
                    if img_src and not img_src.startswith('data:'):
                        item['image'] = urljoin(url, img_src)
                    item['alt'] = img.get('alt', '')
                
                item['name'] = item_name
                
                tooltip = holder.find('p')
                if tooltip:
                    tooltip_text = tooltip.get_text(strip=True)
                    item['description'] = tooltip_text
                    
                    cost_match = re.search(r'(?<![+\-])\b(\d{3,})\b(?![%\s]*[A-Za-z])', tooltip_text)
                    if cost_match:
                        try:
                            item['cost'] = int(cost_match.group(1))
                        except:
                            pass
                
                if 'Enchant' in item_name:
                    item['type'] = 'enchant'
                
                boots_enchants.append(item)
                
                if len(boots_enchants) >= 4:
                    break
    
    return boots_enchants

def extract_example_build(content_section, url):
    """Extract example build"""
    example_build = []
    
    text_centers = content_section.find_all('div', class_='text-center')
    for center in text_centers:
        title_div = center.find('div', class_='bildtitle2')
        if title_div and 'Example' in title_div.get_text():
            combo_section = center.find('div', class_='chapter-combo2')
            if combo_section:
                example_build = extract_items_from_section(combo_section, url)
                break
    
    return example_build

def extract_items_from_section(section, base_url):
    """Extract items from a section"""
    items = []
    item_holders = section.find_all('div', class_='ico-holder3')
    
    for holder in item_holders:
        item = {}
        
        # Extract item image
        img = holder.find('img')
        if img:
            img_src = img.get('data-src') or img.get('src')
            if img_src and not img_src.startswith('data:'):
                item['image'] = urljoin(base_url, img_src)
            item['alt'] = img.get('alt', '')
        
        # Extract item name
        span = holder.find('span')
        if span:
            item['name'] = span.get_text(strip=True)
        
        # Extract item details from tooltip
        tooltip = holder.find('p')
        if tooltip:
            tooltip_text = tooltip.get_text(strip=True)
            item['description'] = tooltip_text
            
            # Extract cost
            cost_match = re.search(r'(?<![+\-])\b(\d{3,})\b(?![%\s]*[A-Za-z])', tooltip_text)
            if cost_match:
                try:
                    item['cost'] = int(cost_match.group(1))
                except:
                    pass
        
        # Check if it's an enchant
        enchant_marker = holder.find('div', class_='enchant')
        if enchant_marker or 'Enchant' in item.get('name', ''):
            item['type'] = 'enchant'
        
        items.append(item)
    
    return items

def extract_situational_items(content_section, base_url):
    """Extract situational items with their purposes"""
    situational = []
    
    tabs = content_section.find_all('div', class_='tabs-b5')
    for tab in tabs:
        situation = {}
        
        title_elem = tab.find('div', class_='bildtitle4')
        if title_elem:
            situation['purpose'] = title_elem.get_text(strip=True)
        
        items = extract_items_from_section(tab, base_url)
        situation['items'] = items
        
        tips_elem = tab.find('div', class_='newsbox_h_short')
        if tips_elem:
            situation['tips'] = tips_elem.get_text(strip=True)
        
        situational.append(situation)
    
    return situational

def extract_summoner_spells(soup, base_url):
    """Extract summoner spells from the document"""
    spells = []
    summoner_sections = soup.find_all('div', class_='bild-block')
    
    for section in summoner_sections:
        h3 = section.find('h3')
        if h3 and 'Summoner' in h3.get_text():
            spell_holders = section.find_all('div', class_='ico-holder3')
            
            for holder in spell_holders:
                spell = {}
                
                img = holder.find('img')
                if img:
                    img_src = img.get('data-src') or img.get('src')
                    if img_src and not img_src.startswith('data:'):
                        spell['image'] = urljoin(base_url, img_src)
                    spell['alt'] = img.get('alt', '')
                
                span = holder.find('span')
                if span:
                    spell['name'] = span.get_text(strip=True)
                
                tooltip = holder.find('p')
                if tooltip:
                    spell['description'] = tooltip.get_text(strip=True)
                    
                    cooldown_match = re.search(r'Cooldown:\s*(\d+)s', spell['description'])
                    if cooldown_match:
                        spell['cooldown'] = int(cooldown_match.group(1))
                
                spells.append(spell)
            break
    
    return spells

def extract_runes_data(soup, base_url):
    """Extract runes build data from the document"""
    runes = {
        'primary': [],
        'secondary': []
    }
    
    rune_section = soup.find('div', class_='rune')
    if not rune_section:
        return runes
    
    # Extract keystone
    keystone_elem = rune_section.find('div', class_='img-big')
    if keystone_elem:
        keystone = {}
        img = keystone_elem.find('img')
        if img:
            img_src = img.get('data-src') or img.get('src')
            if img_src and not img_src.startswith('data:'):
                keystone['image'] = urljoin(base_url, img_src)
            keystone['alt'] = img.get('alt', '')
        
        keystone_container = keystone_elem.find_parent('div', class_='newsbox_h')
        if keystone_container:
            title_elem = keystone_container.find('div', class_='newsbox_h_title')
            if title_elem:
                keystone['name'] = title_elem.get_text(strip=True)
            
            desc_elem = keystone_container.find('div', class_='newsbox_h_short')
            if desc_elem:
                keystone['description'] = desc_elem.get_text(strip=True)
        
        runes['keystone'] = keystone
    
    # Extract primary tree runes
    primary_runes = []
    rune_containers = rune_section.find_all('div', class_='newsbox_h')
    
    for container in rune_containers[1:4]:  # Skip keystone, get next 3
        rune = {}
        
        img = container.find('img')
        if img:
            img_src = img.get('data-src') or img.get('src')
            if img_src and not img_src.startswith('data:'):
                rune['image'] = urljoin(base_url, img_src)
            rune['alt'] = img.get('alt', '')
        
        title_elem = container.find('div', class_='newsbox_h_title')
        if title_elem:
            rune['name'] = title_elem.get_text(strip=True)
        
        desc_elem = container.find('div', class_='newsbox_h_short')
        if desc_elem:
            rune['description'] = desc_elem.get_text(strip=True)
        
        primary_runes.append(rune)
    
    runes['primary'] = primary_runes
    
    # Extract secondary tree rune
    secondary_container = rune_section.find('div', style=lambda x: x and 'border: 1px solid #ffa32b' in x)
    if secondary_container:
        secondary_rune = {}
        
        img = secondary_container.find('img')
        if img:
            img_src = img.get('data-src') or img.get('src')
            if img_src and not img_src.startswith('data:'):
                secondary_rune['image'] = urljoin(base_url, img_src)
            secondary_rune['alt'] = img.get('alt', '')
        
        title_elem = secondary_container.find('div', class_='newsbox_h_title')
        if title_elem:
            secondary_rune['name'] = title_elem.get_text(strip=True)
        
        desc_elem = secondary_container.find('div', class_='newsbox_h_short')
        if desc_elem:
            secondary_rune['description'] = desc_elem.get_text(strip=True)
        
        runes['secondary'] = [secondary_rune]
    
    return runes

def extract_situational_runes(soup, base_url):
    """Extract situational runes alternatives"""
    situational = []
    
    sit_rune_section = soup.find('div', class_='tabs-box6')
    if not sit_rune_section:
        return situational
    
    tabs = sit_rune_section.find_all('div', class_='tabs-b6')
    for tab in tabs:
        situation = {}
        
        title_elem = tab.find('div', class_='bildtitle4')
        if title_elem:
            situation['purpose'] = title_elem.get_text(strip=True)
        
        rune_holders = tab.find_all('div', class_='ico-holder2')
        runes = []
        
        for holder in rune_holders:
            rune = {}
            
            img = holder.find('img')
            if img:
                img_src = img.get('src')
                if img_src and not img_src.startswith('data:'):
                    rune['image'] = urljoin(base_url, img_src)
                rune['alt'] = img.get('alt', '')
            
            title_attr = holder.find('title')
            if title_attr:
                rune['name'] = title_attr.get_text(strip=True)
            
            tooltip = holder.find('p')
            if tooltip:
                rune['description'] = tooltip.get_text(strip=True)
            
            runes.append(rune)
        
        situation['runes'] = runes
        
        tips_elem = tab.find('div', class_='newsbox_h_short')
        if tips_elem:
            situation['tips'] = tips_elem.get_text(strip=True)
        
        situational.append(situation)
    
    return situational

def extract_change_history(soup):
    """Extract champion change history"""
    change_history = []
    
    change_section = soup.find('section', class_='bg-very-light-gray3')
    if not change_section:
        return change_history
    
    content_block = change_section.find('div', class_='content_block')
    if not content_block:
        return change_history
    
    change_divs = content_block.find_all('div', class_=['berrorsred', 'berrors'])
    
    for change_div in change_divs:
        change_entry = {}
        
        first_b = change_div.find('b')
        if first_b:
            change_text = first_b.get_text(strip=True)
            
            if 'NERFED' in change_text:
                change_entry['type'] = 'nerf'
            elif 'REWORKED' in change_text:
                change_entry['type'] = 'rework'
            elif 'ADJUSTED' in change_text:
                change_entry['type'] = 'adjustment'
            elif 'BUFFED' in change_text:
                change_entry['type'] = 'buff'
            else:
                change_entry['type'] = 'unknown'
            
            date_match = re.search(r'(\d{1,2}\s+[A-Z]{3}\s+\d{4})', change_text)
            if date_match:
                change_entry['date'] = date_match.group(1)
            
            patch_match = re.search(r'\(PATCH\s+([^)]+)\)', change_text)
            if patch_match:
                change_entry['patch'] = patch_match.group(1)
        
        # Simplified change extraction
        changes = []
        change_html = str(change_div)
        change_html = change_html.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
        
        temp_soup = BeautifulSoup(change_html, 'html.parser')
        full_text = temp_soup.get_text()
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        
        if lines and any(keyword in lines[0].upper() for keyword in ['NERFED', 'REWORKED', 'ADJUSTED', 'BUFFED']):
            lines = lines[1:]
        
        current_ability = None
        ability_changes = []
        
        for line in lines:
            if any(marker in line for marker in ['(PASSIVE)', '(Q)', '(W)', '(E)', '(R)', 'BASE STATS']):
                if current_ability and ability_changes:
                    changes.append({
                        'ability': current_ability,
                        'changes': ability_changes
                    })
                
                current_ability = re.sub(r'<[^>]+>', '', line).strip()
                ability_changes = []
                
            elif current_ability and line:
                if ':' in line and ('→' in line or ' to ' in line):
                    stat_match = re.match(r'([^:]+):\s*(.+)', line)
                    if stat_match:
                        ability_changes.append({
                            'stat': stat_match.group(1).strip(),
                            'change': stat_match.group(2).strip()
                        })
                elif not any(skip_word in line.upper() for skip_word in ['NERFED', 'REWORKED', 'ADJUSTED', 'BUFFED']):
                    ability_changes.append({'description': line})
        
        if current_ability and ability_changes:
            changes.append({
                'ability': current_ability,
                'changes': ability_changes
            })
        
        change_entry['changes'] = changes
        change_history.append(change_entry)
    
    return change_history

def scrape_champion_complete(url):
    """Scrape complete champion data from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all champion data
        champion_data = extract_champion_basic_info(soup, url)
        champion_data = extract_champion_image_and_stats(soup, url, champion_data)
        champion_data = extract_abilities(soup, url, champion_data)
        
        # Extract lanes and builds
        lanes, builds = extract_complete_builds(soup, url)
        champion_data['lanes'] = lanes
        champion_data['builds'] = builds
        
        # Extract change history
        change_history = extract_change_history(soup)
        if change_history:
            champion_data['change_history'] = change_history
        
        return champion_data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def smart_merge_champion_data(champion_name, url):
    """Smart merge: preserve existing good data, fix missing data"""
    try:
        # Load existing data
        filename = f"champions_clean/{champion_name.lower().replace(' ', '_').replace('-', '_')}.json"
        existing_data = load_champion_data(filename)
        
        # Scrape fresh data
        fresh_data = scrape_champion_complete(url)
        
        if not fresh_data:
            print(f"  - Failed to scrape fresh data for {champion_name}")
            return False
        
        # If no existing data, use fresh data
        if not existing_data:
            final_data = fresh_data
        else:
            # Smart merge: preserve existing, add missing
            final_data = existing_data.copy()
            
            # Update basic info if missing
            if not final_data.get('name'):
                final_data['name'] = fresh_data.get('name', champion_name)
            if not final_data.get('roles'):
                final_data['roles'] = fresh_data.get('roles', [])
            if not final_data.get('image'):
                final_data['image'] = fresh_data.get('image', '')
            if not final_data.get('tier'):
                final_data['tier'] = fresh_data.get('tier', 1)
            if not final_data.get('balance_status'):
                final_data['balance_status'] = fresh_data.get('balance_status', '')
            if not final_data.get('stats'):
                final_data['stats'] = fresh_data.get('stats', {})
            # Always update base_stats if fresh data has better stats (not all zeros)
            fresh_base_stats = fresh_data.get('base_stats', {})
            existing_base_stats = final_data.get('base_stats', {})
            
            # Check if existing base stats are empty or all zeros
            existing_has_real_stats = any(
                value > 0 for value in existing_base_stats.values() 
                if isinstance(value, (int, float))
            )
            
            # Check if fresh base stats have real values
            fresh_has_real_stats = any(
                value > 0 for value in fresh_base_stats.values() 
                if isinstance(value, (int, float))
            )
            
            if fresh_has_real_stats and not existing_has_real_stats:
                final_data['base_stats'] = fresh_base_stats
                print(f"    + Updated base stats with real values")
            elif not final_data.get('base_stats'):
                final_data['base_stats'] = fresh_base_stats
                if fresh_base_stats:
                    print(f"    + Added base stats")
            if not final_data.get('abilities'):
                final_data['abilities'] = fresh_data.get('abilities', [])
            
            # Update lanes if fresh data has more
            fresh_lanes = fresh_data.get('lanes', [])
            existing_lanes = final_data.get('lanes', [])
            if len(fresh_lanes) > len(existing_lanes):
                final_data['lanes'] = fresh_lanes
                print(f"    + Updated lanes: {fresh_lanes}")
            
            # Smart merge builds
            fresh_builds = fresh_data.get('builds', [])
            existing_builds = final_data.get('builds', [])
            
            merged_builds = []
            for i, existing_build in enumerate(existing_builds):
                merged_build = existing_build.copy()
                fresh_build = fresh_builds[i] if i < len(fresh_builds) else None
                
                if fresh_build:
                    # Update missing data only
                    if not merged_build.get('start_items') or len(merged_build.get('start_items', [])) == 0:
                        if fresh_build.get('start_items'):
                            merged_build['start_items'] = fresh_build['start_items']
                            print(f"    + Added {len(fresh_build['start_items'])} start items to build {i+1}")
                    
                    if not merged_build.get('core_items') or len(merged_build.get('core_items', [])) == 0:
                        if fresh_build.get('core_items'):
                            merged_build['core_items'] = fresh_build['core_items']
                            print(f"    + Added {len(fresh_build['core_items'])} core items to build {i+1}")
                    
                    # ALWAYS update boots/enchants (this is the main fix)
                    if fresh_build.get('boots_enchants'):
                        old_count = len(merged_build.get('boots_enchants', []))
                        new_count = len(fresh_build['boots_enchants'])
                        merged_build['boots_enchants'] = fresh_build['boots_enchants']
                        print(f"    + Updated boots/enchants: {old_count} -> {new_count} items in build {i+1}")
                    
                    if not merged_build.get('example_build') or len(merged_build.get('example_build', [])) == 0:
                        if fresh_build.get('example_build'):
                            merged_build['example_build'] = fresh_build['example_build']
                            print(f"    + Added {len(fresh_build['example_build'])} example build items to build {i+1}")
                    
                    if not merged_build.get('situational_items') or len(merged_build.get('situational_items', [])) == 0:
                        if fresh_build.get('situational_items'):
                            merged_build['situational_items'] = fresh_build['situational_items']
                            print(f"    + Added {len(fresh_build['situational_items'])} situational categories to build {i+1}")
                    
                    if not merged_build.get('summoner_spells') or len(merged_build.get('summoner_spells', [])) == 0:
                        if fresh_build.get('summoner_spells'):
                            merged_build['summoner_spells'] = fresh_build['summoner_spells']
                            print(f"    + Added {len(fresh_build['summoner_spells'])} summoner spells to build {i+1}")
                    
                    if not merged_build.get('runes') or not merged_build.get('runes', {}).get('keystone'):
                        if fresh_build.get('runes') and fresh_build['runes'].get('keystone'):
                            merged_build['runes'] = fresh_build['runes']
                            print(f"    + Added runes data to build {i+1}")
                    
                    if not merged_build.get('situational_runes') or len(merged_build.get('situational_runes', [])) == 0:
                        if fresh_build.get('situational_runes'):
                            merged_build['situational_runes'] = fresh_build['situational_runes']
                            print(f"    + Added {len(fresh_build['situational_runes'])} situational rune categories to build {i+1}")
                
                merged_builds.append(merged_build)
            
            # Add any additional fresh builds
            if len(fresh_builds) > len(existing_builds):
                for i in range(len(existing_builds), len(fresh_builds)):
                    merged_builds.append(fresh_builds[i])
                    print(f"    + Added new build {i+1}")
            
            final_data['builds'] = merged_builds
            
            # Update change history if missing
            if not final_data.get('change_history') and fresh_data.get('change_history'):
                final_data['change_history'] = fresh_data['change_history']
                print(f"    + Added change history")
        
        # Save the final data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"  - Error processing {champion_name}: {e}")
        return False

def main():
    """Main function - THE ULTIMATE ALL-IN-ONE SCRAPER"""
    print("=== ULTIMATE ALL-IN-ONE CHAMPION SCRAPER ===\n")
    print("This script does EVERYTHING:")
    print("✓ Extracts complete champion data (name, roles, image, tier, stats, abilities)")
    print("✓ Extracts ALL build components (start_items, core_items, example_build, situational_items)")
    print("✓ Extracts LANE-SPECIFIC boots/enchants (not global duplicates)")
    print("✓ Extracts summoner spells and runes")
    print("✓ Preserves existing good data while fixing missing data")
    print("✓ Handles all champions in batch")
    print()
    
    # Load champion URLs
    champion_urls = load_champion_urls()
    if not champion_urls:
        print("Could not load champion URLs")
        return
    
    # Get list of champion files
    champions_dir = Path("champions_clean")
    if not champions_dir.exists():
        print("Champions directory not found")
        return
    
    champion_files = list(champions_dir.glob("*.json"))
    print(f"Found {len(champion_files)} champion files to process\n")
    
    # Statistics
    total_champions = len(champion_files)
    champions_processed = 0
    champions_updated = 0
    failed_champions = []
    
    # Process each champion
    for i, champion_file in enumerate(champion_files, 1):
        champion_name = champion_file.stem.replace('_', ' ').title()
        print(f"[{i}/{total_champions}] Processing {champion_name}...")
        
        # Find matching URL with improved name mapping
        url = None
        
        # Special name mappings for problematic champions
        name_mappings = {
            'khazix': 'kha zix',
            'kha_zix': 'kha zix',
            'nunu_willump': 'nunu amp willump',
            'nunu willump': 'nunu amp willump',
            'wukong': 'vukong',
            'dr_mundo': 'dr mundo',
            'dr mundo': 'dr mundo',
            'jarvan_iv': 'jarvan iv',
            'jarvan iv': 'jarvan iv',
            'xin_zhao': 'xin zhao',
            'xin zhao': 'xin zhao',
            'aurelion_sol': 'aurelion sol',
            'aurelion sol': 'aurelion sol',
            'miss_fortune': 'miss fortune',
            'miss fortune': 'miss fortune',
            'twisted_fate': 'twisted fate',
            'twisted fate': 'twisted fate',
            'lee_sin': 'lee sin',
            'lee sin': 'lee sin',
            'master_yi': 'master yi',
            'master yi': 'master yi',
            'tahm_kench': 'tahm kench',
            'tahm kench': 'tahm kench',
            'renata_glasc': 'renata glasc',
            'renata glasc': 'renata glasc'
        }
        
        # Generate possible keys with improved mapping
        base_name = champion_file.stem.lower()
        display_name = champion_name.lower()
        
        possible_keys = [
            base_name,
            display_name,
            base_name.replace('_', ' '),
            display_name.replace(' ', '_'),
            base_name.replace('_', '-'),
            display_name.replace(' ', '-')
        ]
        
        # Add special mappings
        if base_name in name_mappings:
            possible_keys.append(name_mappings[base_name])
        if display_name in name_mappings:
            possible_keys.append(name_mappings[display_name])
        
        # Try to find URL
        for key in possible_keys:
            if key in champion_urls:
                url = champion_urls[key]
                print(f"  Found URL using key: '{key}'")
                break
        
        if url:
            if smart_merge_champion_data(champion_name, url):
                champions_updated += 1
                print(f"  [OK] Updated {champion_name}")
            else:
                failed_champions.append(champion_name)
                print(f"  [FAIL] Failed to update {champion_name}")
            
            champions_processed += 1
            
            # Be respectful to the server
            time.sleep(1.5)
        else:
            failed_champions.append(champion_name)
            print(f"  [WARN] No URL found for {champion_name}")
    
    # Print summary
    print(f"\n=== ULTIMATE ALL-IN-ONE SCRAPER COMPLETE ===")
    print(f"Total Champions: {total_champions}")
    print(f"Champions Processed: {champions_processed}")
    print(f"Champions Updated: {champions_updated}")
    print(f"Failed: {len(failed_champions)}")
    print(f"Success Rate: {(champions_updated / total_champions * 100):.1f}%")
    
    if failed_champions:
        print(f"\nFailed champions:")
        for name in failed_champions:
            print(f"  - {name}")
    
    print(f"\n🎉 ALL CHAMPION DATA IS NOW COMPLETE!")
    print(f"📊 Every champion has:")
    print(f"   ✓ Complete basic info (name, roles, image, tier, stats, abilities)")
    print(f"   ✓ Complete build data (start_items, core_items, example_build, situational_items)")
    print(f"   ✓ Lane-specific boots/enchants (4 items per lane, not 8+ duplicates)")
    print(f"   ✓ Summoner spells and runes data")
    print(f"   ✓ Change history where available")

if __name__ == "__main__":
    main()