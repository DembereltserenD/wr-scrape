#!/usr/bin/env python3
"""
Test script for lane-specific build extraction
"""

import json
from enhanced_scrape_champion import WRMetaScraper
from lane_specific_builds_extractor import LaneSpecificBuildsExtractor

def test_lane_build_extraction():
    """Test lane-specific build extraction on known champions"""
    
    test_cases = [
        {
            'name': 'Kennen (Multi-lane)',
            'url': 'https://wr-meta.com/58-kennen.html',
            'expected_lanes': 2,
            'should_have_differences': True
        },
        {
            'name': 'Soraka (Support only)',
            'url': 'https://wr-meta.com/34-soraka.html',
            'expected_lanes': 1,
            'should_have_differences': False
        },
        {
            'name': 'Ahri (Mid primarily)',
            'url': 'https://wr-meta.com/1-ahri.html',
            'expected_lanes': 1,
            'should_have_differences': False
        }
    ]
    
    # Test with enhanced scraper
    enhanced_scraper = WRMetaScraper()
    lane_extractor = LaneSpecificBuildsExtractor()
    
    print("🧪 Testing Lane-Specific Build Extraction")
    print("="*60)
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"🔗 URL: {test_case['url']}")
        
        try:
            # Test enhanced scraper
            print("\n1️⃣ Enhanced Scraper Results:")
            enhanced_data = enhanced_scraper.scrape_champion_data(test_case['url'])
            
            lanes = enhanced_data['champion']['lanes']
            print(f"   Detected lanes: {lanes}")
            
            if 'lane_specific' in enhanced_data['builds']:
                lane_builds = enhanced_data['builds']['lane_specific']
                print(f"   Lane-specific builds: {list(lane_builds.keys())}")
                
                # Check for differences
                if len(lane_builds) > 1:
                    comparison = lane_extractor.compare_lane_builds(lane_builds)
                    if comparison['identical']:
                        print(f"   ⚠️  Builds are identical across lanes")
                    else:
                        print(f"   ✨ Found differences in {len(comparison['differences'])} categories")
                        for diff in comparison['differences']:
                            print(f"      - {diff['category']}")
            else:
                print(f"   📝 Single build extracted")
            
            # Test lane-specific extractor
            print("\n2️⃣ Lane-Specific Extractor Results:")
            response = lane_extractor.session.get(test_case['url'])
            lane_builds = lane_extractor.extract_lane_builds_from_html(response.text)
            
            if lane_builds:
                print(f"   Extracted builds for: {list(lane_builds.keys())}")
                summary = lane_extractor.generate_lane_build_summary(lane_builds)
                print(f"   Summary: {summary.split('Found builds for')[1].split('Note:')[0].strip()}")
            else:
                print(f"   No lane-specific builds found")
            
            # Validation
            print("\n✅ Validation:")
            expected_lanes = test_case['expected_lanes']
            actual_lanes = len(lanes)
            
            if actual_lanes >= expected_lanes:
                print(f"   ✓ Lane count: Expected ≥{expected_lanes}, got {actual_lanes}")
            else:
                print(f"   ❌ Lane count: Expected ≥{expected_lanes}, got {actual_lanes}")
            
            if test_case['should_have_differences']:
                has_lane_specific = 'lane_specific' in enhanced_data['builds']
                if has_lane_specific:
                    print(f"   ✓ Lane differences: Found as expected")
                else:
                    print(f"   ⚠️  Lane differences: Expected but not found")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 60)
    
    print("\n🎯 Test Summary Complete!")

def compare_extraction_methods(champion_url):
    """Compare different extraction methods on a single champion"""
    print(f"🔍 Comparing extraction methods for: {champion_url}")
    
    # Method 1: Enhanced scraper
    enhanced_scraper = WRMetaScraper()
    enhanced_data = enhanced_scraper.scrape_champion_data(champion_url)
    
    # Method 2: Lane-specific extractor
    lane_extractor = LaneSpecificBuildsExtractor()
    response = lane_extractor.session.get(champion_url)
    lane_builds = lane_extractor.extract_lane_builds_from_html(response.text)
    
    print(f"\n📊 Comparison Results:")
    print(f"Enhanced Scraper:")
    print(f"  - Lanes: {enhanced_data['champion']['lanes']}")
    print(f"  - Core items: {len(enhanced_data['builds'].get('core_items', []))}")
    print(f"  - Lane-specific builds: {'Yes' if 'lane_specific' in enhanced_data['builds'] else 'No'}")
    
    print(f"\nLane-Specific Extractor:")
    print(f"  - Detected lanes: {list(lane_builds.keys()) if lane_builds else 'None'}")
    if lane_builds:
        for lane, build in lane_builds.items():
            core_count = len(build.get('core_items', []))
            print(f"  - {lane}: {core_count} core items")
    
    # Save comparison results
    comparison_data = {
        'enhanced_scraper': enhanced_data,
        'lane_extractor': lane_builds
    }
    
    champion_name = enhanced_data['champion']['name'].lower().replace(' ', '_')
    filename = f"comparison_{champion_name}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Comparison saved to: {filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Compare methods for specific champion
        champion_url = sys.argv[1]
        compare_extraction_methods(champion_url)
    else:
        # Run full test suite
        test_lane_build_extraction()
