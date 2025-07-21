#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json

def analyze_champion_page(url):
    """Analyze the complete structure of a champion page"""
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f"Analyzing: {url}")
    print("=" * 80)
    
    # 1. Look for lane/role selectors
    print("1. LANE/ROLE SELECTORS:")
    lane_elements = soup.find_all(['button', 'div', 'span', 'a'], 
                                 class_=re.compile(r'lane|role|position', re.I))
    lane_elements.extend(soup.find_all(['button', 'div', 'span', 'a'], 
                                      string=re.compile(r'baron|mid|jungle|dragon|support|adc', re.I)))
    
    print(f"Found {len(lane_elements)} lane-related elements")
    for elem in lane_elements[:10]:
        print(f"  - Tag: {elem.name}, Class: {elem.get('class')}, Text: '{elem.get_text().strip()}'")
    
    # 2. Look for build sections
    print("\n2. BUILD SECTIONS:")
    build_sections = soup.find_all(['div', 'section'], 
                                  class_=re.compile(r'build|item|equipment', re.I))
    
    print(f"Found {len(build_sections)} build sections")
    for i, section in enumerate(build_sections[:5]):
        print(f"  Section {i+1}: Class: {section.get('class')}")
        # Look for items in this section
        items_in_section = section.find_all('img', alt=True)
        item_names = [img.get('alt') for img in items_in_section if img.get('alt') and len(img.get('alt')) > 3]
        print(f"    Items found: {len(item_names)}")
        if item_names:
            print(f"    Sample items: {item_names[:3]}")
    
    # 3. Look for specific build categories
    print("\n3. BUILD CATEGORIES:")
    categories = ['starting', 'core', 'boots', 'situational', 'example']
    
    for category in categories:
        category_elements = soup.find_all(['div', 'span', 'h3', 'h4'], 
                                        string=re.compile(category, re.I))
        category_elements.extend(soup.find_all(['div', 'span'], 
                                             class_=re.compile(category, re.I)))
        
        print(f"  {category.upper()}: Found {len(category_elements)} elements")
        for elem in category_elements[:3]:
            print(f"    - {elem.name}: '{elem.get_text().strip()}'")
    
    # 4. Look for JavaScript/dynamic content
    print("\n4. JAVASCRIPT/DYNAMIC CONTENT:")
    scripts = soup.find_all('script')
    js_with_items = []
    
    for script in scripts:
        if script.string:
            if any(keyword in script.string.lower() for keyword in ['item', 'build', 'lane', 'baron', 'mid']):
                js_with_items.append(script.string[:200] + "...")
    
    print(f"Found {len(js_with_items)} scripts with build-related content")
    for i, js in enumerate(js_with_items[:2]):
        print(f"  Script {i+1}: {js}")
    
    # 5. Look for specific build structure
    print("\n5. ACTUAL BUILD STRUCTURE:")
    
    # Look for the specific build sections we found
    core_sections = soup.find_all(['div', 'h3'], string=re.compile(r'core', re.I))
    boots_sections = soup.find_all(['div', 'h3'], string=re.compile(r'boots', re.I))
    situational_sections = soup.find_all(['div', 'h3'], string=re.compile(r'situational', re.I))
    example_sections = soup.find_all(['div', 'h3'], string=re.compile(r'example', re.I))
    
    print(f"Core sections: {len(core_sections)}")
    print(f"Boots sections: {len(boots_sections)}")
    print(f"Situational sections: {len(situational_sections)}")
    print(f"Example sections: {len(example_sections)}")
    
    # Look for items near these sections
    for section_type, sections in [("Core", core_sections), ("Boots", boots_sections), 
                                  ("Situational", situational_sections), ("Example", example_sections)]:
        print(f"\n{section_type} Items:")
        for i, section in enumerate(sections[:2]):
            # Find parent container
            parent = section.find_parent(['div', 'section'])
            if parent:
                items = parent.find_all('img', alt=True)
                item_names = [img.get('alt') for img in items if img.get('alt') and len(img.get('alt')) > 3]
                print(f"  Section {i+1}: {len(item_names)} items")
                if item_names:
                    print(f"    Items: {item_names[:5]}")
            else:
                print(f"  Section {i+1}: No parent container found")
    
    # 6. Look for tabs or toggles
    print("\n6. TABS/TOGGLES:")
    tab_elements = soup.find_all(['div', 'button', 'a'], 
                                class_=re.compile(r'tab|toggle|switch', re.I))
    
    print(f"Found {len(tab_elements)} tab/toggle elements")
    for elem in tab_elements[:5]:
        print(f"  - {elem.name}: Class: {elem.get('class')}, Text: '{elem.get_text().strip()}'")

if __name__ == "__main__":
    # Test with Kennen (has multiple lanes) and Soraka (support only)
    test_urls = [
        "https://wr-meta.com/58-kennen.html",
        "https://wr-meta.com/392-soraka.html"
    ]
    
    for url in test_urls:
        analyze_champion_page(url)
        print("\n" + "="*100 + "\n")
