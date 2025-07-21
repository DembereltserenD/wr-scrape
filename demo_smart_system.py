#!/usr/bin/env python3
"""
Demo of the Smart Architecture System
Shows how to access detailed item and rune information
"""

from data_loader import DataLoader
import json

def main():
    print("🎯 SMART ARCHITECTURE DEMO")
    print("="*60)
    
    loader = DataLoader()
    
    # Demo 1: Get Rabadon's Deathcap details
    print("📜 RABADON'S DEATHCAP DETAILS:")
    print("-" * 40)
    
    rabadon = loader.get_item("Rabadon's Deathcap")
    if rabadon:
        print(f"🏷️  Name: {rabadon['name']}")
        print(f"💰 Cost: {rabadon['cost']} gold")
        print(f"⭐ Tier: {rabadon['tier']}")
        print(f"📊 Category: {rabadon['category']}")
        
        print(f"\n📈 Stats:")
        for stat_name, stat_data in rabadon['stats'].items():
            value = stat_data['value']
            stat_type = stat_data['type']
            symbol = "%" if stat_type == "percentage" else ""
            print(f"   • {stat_name.replace('_', ' ').title()}: +{value}{symbol}")
        
        print(f"\n🔮 Passive: {rabadon['passive']}")
        print(f"\n📝 Description:")
        print(f"   {rabadon['description']}")
        
        if 'tips' in rabadon:
            print(f"\n💡 Tips:")
            for tip in rabadon['tips']:
                print(f"   • {tip}")
    
    # Demo 2: Compare file sizes
    print(f"\n" + "="*60)
    print("📊 ARCHITECTURE COMPARISON:")
    print("-" * 40)
    
    # Get clean champion data
    blitz_clean = loader.get_champion('blitzcrank_data')
    if blitz_clean:
        clean_size = len(json.dumps(blitz_clean))
        print(f"🧹 Clean Champion File: ~{clean_size:,} characters")
    
    # Get champion with full details
    blitz_detailed = loader.get_champion_with_details('blitzcrank_data')
    if blitz_detailed:
        detailed_size = len(json.dumps(blitz_detailed))
        print(f"🔥 With Full Details: ~{detailed_size:,} characters")
        
        if blitz_clean:
            ratio = detailed_size / clean_size
            print(f"📈 Size Increase: {ratio:.1f}x when loading details")
    
    # Demo 3: Show architecture benefits
    print(f"\n" + "="*60)
    print("✅ SMART ARCHITECTURE BENEFITS:")
    print("-" * 40)
    
    items_count = len(loader.list_items())
    runes_count = len(loader.list_runes())
    
    print(f"📦 {items_count} unique items stored once")
    print(f"🔮 {runes_count} unique runes stored once")
    print(f"👥 188 champions reference items/runes")
    print(f"🚀 No data duplication")
    print(f"⚡ Fast loading - only load what you need")
    print(f"🔧 Easy updates - change item once, affects all champions")
    print(f"📱 Clean champion files for mobile apps")
    print(f"🎯 Perfect separation of concerns")
    
    # Demo 4: Usage examples
    print(f"\n" + "="*60)
    print("🔧 USAGE EXAMPLES:")
    print("-" * 40)
    
    print("# Get item details")
    print("loader = DataLoader()")
    print("item = loader.get_item('Rabadon\\'s Deathcap')")
    print("print(f'Cost: {item[\"cost\"]} gold')")
    
    print("\n# Get champion with items")
    print("champion = loader.get_champion_with_details('blitzcrank_data')")
    print("for item in champion['builds']['starting_items_detailed']:")
    print("    print(f'{item[\"name\"]}: {item[\"cost\"]}g')")
    
    print("\n# Search items")
    print("sword_items = loader.search_items('sword')")
    print("boot_items = loader.list_items(category='boots')")
    
    print(f"\n" + "="*60)
    print("🎉 Your idea was BRILLIANT!")
    print("This architecture is much cleaner and more efficient! 🚀")

if __name__ == "__main__":
    main()