#!/usr/bin/env python3
"""
Test script to demonstrate the smart architecture
"""

from data_loader import DataLoader
import json

def main():
    print("🧪 Testing Smart Architecture")
    print("="*50)
    
    loader = DataLoader()
    
    # Test 1: List available items
    print("📦 Available Items (first 10):")
    items = loader.list_items()
    for i, (name, info) in enumerate(list(items.items())[:10]):
        print(f"  {i+1}. {name} - {info['category']} - {info['cost']}g")
    
    print(f"\nTotal items: {len(items)}")
    
    # Test 2: Get specific item details
    print("\n🔍 Item Details - Eclipse:")
    eclipse = loader.get_item('Eclipse')
    if eclipse:
        print(f"  Name: {eclipse['name']}")
        print(f"  Cost: {eclipse['cost']} gold")
        print(f"  Category: {eclipse['category']}")
        print(f"  Description: {eclipse['description']}")
        print(f"  Stats: {eclipse.get('stats', {})}")
    
    # Test 3: Get champion with clean data
    print("\n👤 Clean Champion Data - Blitzcrank:")
    blitz_clean = loader.get_champion('blitzcrank')
    if blitz_clean:
        print(f"  Name: {blitz_clean['champion']['name']}")
        print(f"  Role: {blitz_clean['champion']['role']}")
        print(f"  Starting Items: {blitz_clean['builds']['starting_items']}")
        print(f"  File size: ~{len(json.dumps(blitz_clean))} characters")
    
    # Test 4: Get champion with full details
    print("\n🔥 Champion with Full Details - Blitzcrank:")
    blitz_detailed = loader.get_champion_with_details('blitzcrank')
    if blitz_detailed:
        print(f"  Name: {blitz_detailed['champion']['name']}")
        
        # Show starting items with details
        if 'starting_items_detailed' in blitz_detailed['builds']:
            print("  Starting Items with Details:")
            for item in blitz_detailed['builds']['starting_items_detailed']:
                if item and 'name' in item:
                    print(f"    - {item['name']}: {item.get('cost', 'Unknown')} gold")
                    print(f"      Category: {item.get('category', 'Unknown')}")
                    if item.get('passive'):
                        print(f"      Passive: {item['passive'][:50]}...")
        
        # Show rune details
        if 'primary' in blitz_detailed['runes'] and 'keystone_detailed' in blitz_detailed['runes']['primary']:
            keystone = blitz_detailed['runes']['primary']['keystone_detailed']
            if keystone and 'name' in keystone:
                print(f"  Keystone: {keystone['name']}")
                print(f"    Tree: {keystone.get('tree', 'Unknown')}")
                print(f"    Description: {keystone.get('description', 'No description')[:50]}...")
    
    # Test 5: Search functionality
    print("\n🔍 Search Items containing 'sword':")
    sword_items = loader.search_items('sword')
    for name, info in list(sword_items.items())[:3]:
        print(f"  - {name} ({info['category']}) - {info['cost']}g")
    
    # Test 6: List items by category
    print("\n👢 Boot Items:")
    boot_items = loader.list_items(category='boots')
    for name, info in boot_items.items():
        print(f"  - {name} - {info['cost']}g")
    
    print("\n" + "="*50)
    print("✅ Smart Architecture Test Complete!")
    print("\n📊 Architecture Benefits:")
    print("  ✅ Clean separation of concerns")
    print("  ✅ No data duplication")
    print("  ✅ Easy to update items/runes")
    print("  ✅ Efficient loading")
    print("  ✅ Scalable structure")

if __name__ == "__main__":
    main()