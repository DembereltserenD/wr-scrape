#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re

def test_lane_differences(url):
    """Test if different sections actually have different content"""
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f"Testing lane differences: {url}")
    print("=" * 60)
    
    # Find all core sections
    core_sections = soup.find_all(['div', 'h3'], string=re.compile(r'core', re.I))
    
    print(f"Found {len(core_sections)} core sections")
    
    section_contents = []
    
    for i, section in enumerate(core_sections):
        print(f"\nCore Section {i+1}:")
        
        # Find parent container
        parent = section.find_parent(['div', 'section'])
        if parent:
            # Get all item images
            items = parent.find_all('img', alt=True)
            item_names = []
            
            for img in items:
                alt_text = img.get('alt', '').strip()
                if alt_text and len(alt_text) > 3:
                    # Skip non-item images
                    if not any(skip in alt_text.lower() for skip in ['ability', 'skill', 'passive', 'ultimate', 'champion', 'rune']):
                        item_names.append(alt_text)
            
            print(f"  Items: {item_names}")
            section_contents.append(item_names)
        else:
            print("  No parent container found")
            section_contents.append([])
    
    # Compare sections
    if len(section_contents) > 1:
        print(f"\nComparison:")
        all_same = True
        for i in range(1, len(section_contents)):
            same = section_contents[0] == section_contents[i]
            print(f"  Section 1 vs Section {i+1}: {'SAME' if same else 'DIFFERENT'}")
            if not same:
                all_same = False
                # Show differences
                diff1 = set(section_contents[0]) - set(section_contents[i])
                diff2 = set(section_contents[i]) - set(section_contents[0])
                if diff1:
                    print(f"    Only in Section 1: {list(diff1)}")
                if diff2:
                    print(f"    Only in Section {i+1}: {list(diff2)}")
        
        print(f"\nOverall: {'All sections are IDENTICAL' if all_same else 'Sections have DIFFERENCES'}")
    
    # Also check if there are any lane-specific indicators near the sections
    print(f"\nLooking for lane indicators:")
    lane_keywords = ['baron', 'mid', 'jungle', 'dragon', 'support', 'adc', 'top', 'bot']
    
    for i, section in enumerate(core_sections):
        print(f"\nSection {i+1} context:")
        
        # Look for lane indicators in nearby text
        parent = section.find_parent(['div', 'section'])
        if parent:
            parent_text = parent.get_text().lower()
            found_lanes = [keyword for keyword in lane_keywords if keyword in parent_text]
            if found_lanes:
                print(f"  Lane indicators found: {found_lanes}")
            else:
                print(f"  No lane indicators found")
        
        # Look for lane indicators in siblings or nearby elements
        siblings = section.find_next_siblings()[:5]  # Check next 5 siblings
        for sibling in siblings:
            sibling_text = sibling.get_text().lower()
            found_lanes = [keyword for keyword in lane_keywords if keyword in sibling_text]
            if found_lanes:
                print(f"  Lane indicators in siblings: {found_lanes}")
                break

if __name__ == "__main__":
    # Test with champions that should have different lane builds
    test_urls = [
        "https://wr-meta.com/58-kennen.html",
        "https://wr-meta.com/332-aatrox.html",
        "https://wr-meta.com/1-ahri.html"
    ]
    
    for url in test_urls:
        test_lane_differences(url)
        print("\n" + "="*80 + "\n")
