#!/usr/bin/env python3
"""
Lane-Specific Builds Extractor for WR-META.com
Specialized tool for extracting different builds per lane from champion pages.
"""

import re
import json
from bs4 import BeautifulSoup
from enhanced_scrape_champion import WRMetaScraper

class LaneSpecificBuildsExtractor(WRMetaScraper):
    def __init__(self):
        super().__init__()
        self.lane_patterns = {
            'Solo Baron': [
                r'Solo Baron.*Build',
                r'Baron Lane.*Build',
                r'Top Lane.*Build'
            ],
            'Mid Lane': [
                r'Mid.*Build',
                r'Middle Lane.*Build'
            ],
            'Jungle': [
                r'Jungle.*Build',
                r'JG.*Build'
            ],
            'Dragon Lane': [
                r'Dragon Lane.*Build',
                r'Bot Lane.*Build',
                r'ADC.*Build'
            ],
            'Support': [
                r'Support.*Build',
                r'Supp.*Build'
            ]
        }
    
    def extract_lane_builds_from_html(self, html_content):
        """Extract lane-specific builds from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        lane_builds = {}
        detected_lanes = self.detect_available_lanes(soup)
        
        print(f"Detected lanes from HTML: {detected_lanes}")
        
        for lane in detected_lanes:
            build_data = self.extract_build_for_specific_lane(soup, lane)
            if build_data and any(build_data.values()):
                lane_builds[lane] = build_data
                print(f"Extracted build for {lane}: {len(build_data.get('core_items', []))} core items")
        
        return lane_builds
    
    def detect_available_lanes(self, soup):
        """Detect which lanes are available for this champion"""
        detected_lanes = []
        
        # Method 1: Look for lane-specific icons
        lane_icons = {
            'Solo Baron': soup.find_all('i', class_='demo-icon solo-lineicon-'),
            'Mid Lane': soup.find_all('i', class_='demo-icon mid-lineicon-'),
            'Jungle': soup.find_all('i', class_='demo-icon jungle-lineicon-'),
            'Dragon Lane': soup.find_all('i', class_='demo-icon dragon-lineicon-'),
            'Support': soup.find_all('i', class_='demo-icon support-lineicon-')
        }
        
        for lane, icons in lane_icons.items():
            if icons:
                detected_lanes.append(lane)
        
        # Method 2: Look for lane-specific headings
        if not detected_lanes:
            for lane, patterns in self.lane_patterns.items():
                for pattern in patterns:
                    if soup.find(['h1', 'h2', 'h3'], string=re.compile(pattern, re.I)):
                        if lane not in detected_lanes:
                            detected_lanes.append(lane)
        
        # Method 3: Look for tab selectors
        if not detected_lanes:
            tab_selectors = soup.find_all('div', class_='tabs-fg-sel')
            for selector in tab_selectors:
                spans = selector.find_all('span')
                if len(spans) >= 2:  # Multiple tabs suggest multiple lanes
                    # Default to common lanes for multi-role champions
                    detected_lanes = ['Solo Baron', 'Mid Lane']
                    break
        
        return detected_lanes if detected_lanes else ['Solo Baron']  # Default fallback
    
    def extract_build_for_specific_lane(self, soup, lane_name):
        """Extract build data for a specific lane"""
        build_data = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'example_build': [],
            'enchants': []
        }
        
        # Find the section for this lane
        lane_section = self.find_lane_section(soup, lane_name)
        
        if lane_section:
            # Extract items from the lane section
            build_data = self.extract_items_from_lane_section(lane_section)
        else:
            # Fallback: try to extract from general sections
            build_data = self.extract_general_build_data(soup)
        
        return build_data
    
    def find_lane_section(self, soup, lane_name):
        """Find the HTML section corresponding to a specific lane"""
        # Look for headings that match the lane
        patterns = self.lane_patterns.get(lane_name, [])
        
        for pattern in patterns:
            heading = soup.find(['h1', 'h2', 'h3'], string=re.compile(pattern, re.I))
            if heading:
                # Find the parent container
                container = heading.find_parent(['div', 'section'])
                if container:
                    return container
        
        # Alternative: look for sections with lane-specific classes
        lane_class_map = {
            'Solo Baron': 'solo',
            'Mid Lane': 'mid',
            'Jungle': 'jungle',
            'Dragon Lane': 'dragon',
            'Support': 'support'
        }
        
        lane_class = lane_class_map.get(lane_name, '').lower()
        if lane_class:
            section = soup.find('div', class_=re.compile(lane_class, re.I))
            if section:
                return section
        
        return None
    
    def extract_items_from_lane_section(self, section):
        """Extract items from a lane-specific section"""
        build_data = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'example_build': [],
            'enchants': []
        }
        
        # Define section keywords for each category
        section_keywords = {
            'starting_items': ['start', 'starting', 'early'],
            'core_items': ['core', 'main', 'essential'],
            'boots': ['boots', 'footwear'],
            'situational_items': ['situational', 'optional', 'counter'],
            'example_build': ['example', 'full build', 'complete']
        }
        
        # Extract items for each category
        for category, keywords in section_keywords.items():
            items = self.extract_items_by_keywords(section, keywords)
            build_data[category] = items
        
        # Separate enchants from boots
        all_boot_items = build_data['boots'][:]
        boots = []
        enchants = []
        
        for item in all_boot_items:
            if 'enchant' in item.lower():
                enchants.append(item)
            else:
                boots.append(item)
        
        build_data['boots'] = boots
        build_data['enchants'] = enchants
        
        return build_data
    
    def extract_items_by_keywords(self, section, keywords):
        """Extract items from section based on keywords"""
        items = []
        
        for keyword in keywords:
            # Find subsections with the keyword
            subsections = section.find_all(['div', 'h3', 'h4'], 
                                         string=re.compile(keyword, re.IGNORECASE))
            
            for subsection in subsections:
                # Find parent container
                parent = subsection.find_parent(['div', 'section'])
                if parent:
                    # Extract item images
                    item_imgs = parent.find_all('img', alt=True)
                    
                    for img in item_imgs:
                        alt_text = img.get('alt', '').strip()
                        if self._is_item_image(img, alt_text):
                            item_name = self._clean_item_name(alt_text)
                            if item_name and item_name not in items:
                                items.append(item_name)
        
        return items[:8]  # Limit to 8 items per category
    
    def extract_general_build_data(self, soup):
        """Fallback method to extract general build data"""
        return self._extract_structured_build(soup)
    
    def compare_lane_builds(self, lane_builds):
        """Compare builds across lanes to identify differences"""
        if len(lane_builds) < 2:
            return {"identical": True, "differences": []}
        
        lanes = list(lane_builds.keys())
        differences = []
        
        # Compare each category across lanes
        categories = ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build']
        
        for category in categories:
            lane_items = {}
            for lane in lanes:
                items = lane_builds[lane].get(category, [])
                lane_items[lane] = set(items)
            
            # Check if all lanes have the same items
            all_items = list(lane_items.values())
            if len(set(frozenset(items) for items in all_items)) > 1:
                differences.append({
                    'category': category,
                    'lane_differences': {lane: list(items) for lane, items in lane_items.items()}
                })
        
        return {
            "identical": len(differences) == 0,
            "differences": differences
        }
    
    def generate_lane_build_summary(self, lane_builds):
        """Generate a summary of lane-specific builds"""
        if not lane_builds:
            return "No lane-specific builds found."
        
        summary = []
        summary.append(f"Found builds for {len(lane_builds)} lanes:")
        
        for lane, build in lane_builds.items():
            core_count = len(build.get('core_items', []))
            situational_count = len(build.get('situational_items', []))
            summary.append(f"  • {lane}: {core_count} core items, {situational_count} situational items")
        
        # Check for differences
        comparison = self.compare_lane_builds(lane_builds)
        if comparison['identical']:
            summary.append("\nNote: All lane builds are identical.")
        else:
            summary.append(f"\nFound {len(comparison['differences'])} categories with lane differences:")
            for diff in comparison['differences']:
                summary.append(f"  • {diff['category']}: varies by lane")
        
        return "\n".join(summary)

def main():
    """Test the lane-specific builds extractor"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python lane_specific_builds_extractor.py <champion-url>")
        sys.exit(1)
    
    champion_url = sys.argv[1]
    
    # Create extractor
    extractor = LaneSpecificBuildsExtractor()
    
    # Get HTML content
    response = extractor.session.get(champion_url)
    html_content = response.text
    
    # Extract lane builds
    lane_builds = extractor.extract_lane_builds_from_html(html_content)
    
    # Generate summary
    summary = extractor.generate_lane_build_summary(lane_builds)
    print(summary)
    
    # Save results
    if lane_builds:
        champion_name = champion_url.split('/')[-1].replace('.html', '')
        filename = f"{champion_name}_lane_builds.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lane_builds, f, indent=2, ensure_ascii=False)
        
        print(f"\nLane builds saved to: {filename}")

if __name__ == "__main__":
    main()
