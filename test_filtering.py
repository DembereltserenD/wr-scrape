#!/usr/bin/env python3
"""Test the champion name filtering functionality"""

from smart_data_organizer import SmartDataOrganizer

def test_filtering():
    organizer = SmartDataOrganizer()
    
    print("Testing champion name filtering...")
    print("=" * 50)
    
    # Test champion names (should be filtered out)
    champion_tests = [
        "Dr. Mundo",
        "Nidalee", 
        "Xerath",
        "Karthus",
        "Leblanc",
        "Udyr",
        "Quinn",
        "Rek'sai",
        "Malzahar",
        "Taliyah",
        "Cassiopeia",
        "Gangplank",
        "K'sante",
        "Qiyana",
        "Ivern",
        "Neeko",
        "Smolder",
        "Renata Glasc",
        "Anivia",
        "Illaoi",
        "Naafiri",
        "Briar",
        "Elise",
        "Zac",
        "Aphelios",
        "Skarner",
        "Azir"
    ]
    
    # Test valid item names (should pass)
    item_tests = [
        "Trinity Force",
        "Rabadon's Deathcap", 
        "Boots",
        "Duskblade Of Draktharr",
        "Infinity Edge",
        "Guardian Angel",
        "Thornmail",
        "Warmog's Armor",
        "Void Staff",
        "Quicksilver Enchant",
        "Protobelt Enchant",
        "Glorious Enchant",
        "Stasis Enchant",
        "Locket Enchant",
        "Veil Enchant",
        "Long Sword",
        "Ruby Crystal",
        "Amplifying Tome"
    ]
    
    print("Champion Names (should be FALSE):")
    champion_filtered = 0
    for name in champion_tests:
        is_valid = organizer._is_valid_item_name(name)
        print(f"  {name}: {is_valid}")
        if not is_valid:
            champion_filtered += 1
    
    print(f"\nFiltered out {champion_filtered}/{len(champion_tests)} champion names")
    
    print("\nItem Names (should be TRUE):")
    items_passed = 0
    for name in item_tests:
        is_valid = organizer._is_valid_item_name(name)
        print(f"  {name}: {is_valid}")
        if is_valid:
            items_passed += 1
    
    print(f"\nPassed {items_passed}/{len(item_tests)} item names")
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Champion filtering success rate: {champion_filtered}/{len(champion_tests)} ({champion_filtered/len(champion_tests)*100:.1f}%)")
    print(f"Item recognition success rate: {items_passed}/{len(item_tests)} ({items_passed/len(item_tests)*100:.1f}%)")

if __name__ == "__main__":
    test_filtering()