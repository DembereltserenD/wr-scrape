#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json

def analyze_dynamic_content(url):
    """Analyze how dynamic content changes with lanes"""
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f"Analyzing dynamic content: {url}")
    print("=" * 80)
    
    # 1. Look for JavaScript that handles lane switching
    print("1. JAVASCRIPT ANALYSIS:")
    scripts = soup.find_all('script')
    
    lane_related_js = []
    for script in scripts:
        if script.string:
            script_content = script.string.lower()
            if any(keyword in script_content for keyword in ['lane', 'baron', 'mid', 'jungle', 'dragon', 'support', 'tab', 'switch']):
                # Extract relevant parts
                lines = script.string.split('\n')
                relevant_lines = [line.strip() for line in lines if any(keyword in line.lower() for keyword in ['lane', 'baron', 'mid', 'tab', 'data'])]
                if relevant_lines:
                    lane_related_js.extend(relevant_lines[:10])  # Limit output
    
    print(f"Found {len(lane_related_js)} relevant JS lines:")
    for line in lane_related_js[:15]:
        print(f"  {line}")
    
    # 2. Look for data attributes that might contain build data
    print("\n2. DATA ATTRIBUTES:")
    elements_with_data = soup.find_all(attrs=lambda x: x and any(attr.startswith('data-') for attr in x.keys()) if isinstance(x, dict) else False)
    
    relevant_data = []
    for elem in elements_with_data:
        for attr, value in elem.attrs.items():
            if attr.startswith('data-') and isinstance(value, str):
                if any(keyword in value.lower() for keyword in ['item', 'build', 'lane', 'baron', 'mid']):
                    relevant_data.append((elem.name, attr, value[:100]))  # Truncate long values
    
    print(f"Found {len(relevant_data)} relevant data attributes:")
    for tag, attr, value in relevant_data[:10]:
        print(f"  {tag}[{attr}]: {value}")
    
    # 3. Look for hidden/multiple build sections
    print("\n3. MULTIPLE BUILD SECTIONS:")
    
    # Count occurrences of build sections
    core_sections = soup.find_all(['div', 'h3'], string=re.compile(r'core', re.I))
    boots_sections = soup.find_all(['div', 'h3'], string=re.compile(r'boots', re.I))
    situational_sections = soup.find_all(['div', 'h3'], string=re.compile(r'situational', re.I))
    example_sections = soup.find_all(['div', 'h3'], string=re.compile(r'example', re.I))
    
    print(f"Core sections: {len(core_sections)}")
    print(f"Boots sections: {len(boots_sections)}")
    print(f"Situational sections: {len(situational_sections)}")
    print(f"Example sections: {len(example_sections)}")
    
    # Analyze if sections have different content
    if len(core_sections) > 1:
        print("\nAnalyzing multiple Core sections:")
        for i, section in enumerate(core_sections[:3]):
            parent = section.find_parent(['div', 'section'])
            if parent:
                items = parent.find_all('img', alt=True)
                item_names = [img.get('alt') for img in items if img.get('alt') and len(img.get('alt')) > 3]
                print(f"  Core section {i+1}: {len(item_names)} items")
                if item_names:
                    print(f"    Items: {item_names[:5]}")
    
    # 4. Look for tab/lane switching elements
    print("\n4. TAB/LANE SWITCHING:")
    
    # Look for elements that might be lane selectors
    potential_lane_selectors = []
    
    # Check for buttons, divs, or spans with lane-related text
    for tag in ['button', 'div', 'span', 'a']:
        elements = soup.find_all(tag, string=re.compile(r'baron|mid|jungle|dragon|support', re.I))
        for elem in elements:
            classes = elem.get('class', [])
            onclick = elem.get('onclick', '')
            potential_lane_selectors.append({
                'tag': tag,
                'text': elem.get_text().strip(),
                'classes': classes,
                'onclick': onclick
            })
    
    print(f"Found {len(potential_lane_selectors)} potential lane selectors:")
    for selector in potential_lane_selectors[:10]:
        print(f"  {selector['tag']}: '{selector['text']}' | Classes: {selector['classes']} | OnClick: {selector['onclick']}")
    
    # 5. Look for CSS classes that might hide/show content
    print("\n5. CSS CLASSES FOR DYNAMIC CONTENT:")
    
    # Look for elements with classes that suggest they're part of a tab system
    tab_related_classes = []
    for elem in soup.find_all(class_=True):
        classes = elem.get('class', [])
        for cls in classes:
            if any(keyword in cls.lower() for keyword in ['tab', 'active', 'hidden', 'show', 'hide', 'lane', 'baron', 'mid']):
                if cls not in tab_related_classes:
                    tab_related_classes.append(cls)
    
    print(f"Found {len(tab_related_classes)} tab-related CSS classes:")
    for cls in tab_related_classes[:15]:
        print(f"  .{cls}")

if __name__ == "__main__":
    # Test with Kennen (multi-lane) and a single-lane champion
    test_urls = [
        "https://wr-meta.com/58-kennen.html",
        "https://wr-meta.com/332-aatrox.html"
    ]
    
    for url in test_urls:
        analyze_dynamic_content(url)
        print("\n" + "="*100 + "\n")
