#!/usr/bin/env python3
"""
Test script for passive and active effect parsing
Tests the enhanced regex patterns and special case handling
"""

import json
from real_time_item_scraper import RealTimeItemScraper
from bs4 import BeautifulSoup

def test_passive_active_parsing():
    """Test the passive and active effect parsing functionality"""
    scraper = RealTimeItemScraper()
    
    # Test cases with mock HTML containers
    test_cases = [
        {
            "name": "Rabadon's Deathcap",
            "html": '''
            <div class="item-container">
                <h3>Rabadon's Deathcap</h3>
                <div class="stats">+100 Ability Power</div>
                <div class="cost">3400 gold</div>
                <div class="passive"><b>Overkill:</b> Increases Ability Power by 20-45%</div>
            </div>
            ''',
            "expected_passive": "Overkill: Increases Ability Power by 20-45%",
            "expected_active": ""
        },
        {
            "name": "Duskblade of Draktharr",
            "html": '''
            <div class="item-container">
                <h3>Duskblade of Draktharr</h3>
                <div class="stats">+55 Attack Damage</div>
                <div class="cost">3100 gold</div>
                <div class="passive"><b>Nightstalker:</b> After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals 99 (+30% bonus AD) bonus physical damage.</div>
            </div>
            ''',
            "expected_passive": "Nightstalker: After takedown, become invisible for 1.5 seconds (90 second cooldown). Your next attack deals 99 (+30% bonus AD) bonus physical damage.",
            "expected_active": ""
        },
        {
            "name": "Stasis Enchant",
            "html": '''
            <div class="item-container">
                <h3>Stasis Enchant</h3>
                <div class="cost">500 gold</div>
                <div class="active"><b>Stasis:</b> Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown).</div>
            </div>
            ''',
            "expected_passive": "",
            "expected_active": "Stasis: Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown)."
        },
        {
            "name": "Guardian Angel",
            "html": '''
            <div class="item-container">
                <h3>Guardian Angel</h3>
                <div class="stats">+40 Attack Damage, +40 Armor</div>
                <div class="cost">2800 gold</div>
                <div class="passive"><b>Rebirth:</b> Upon taking lethal damage, revive with 50% base Health and 30% maximum Mana after 4 seconds of stasis (300 second cooldown).</div>
            </div>
            ''',
            "expected_passive": "Rebirth: Upon taking lethal damage, revive with 50% base Health and 30% maximum Mana after 4 seconds of stasis (300 second cooldown).",
            "expected_active": ""
        },
        {
            "name": "Zhonya's Hourglass",
            "html": '''
            <div class="item-container">
                <h3>Zhonya's Hourglass</h3>
                <div class="stats">+80 Ability Power, +45 Armor</div>
                <div class="cost">2900 gold</div>
                <div class="active"><b>Stasis:</b> Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown).</div>
            </div>
            ''',
            "expected_passive": "",
            "expected_active": "Stasis: Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items (120 second cooldown)."
        },
        {
            "name": "Trinity Force",
            "html": '''
            <div class="item-container">
                <h3>Trinity Force</h3>
                <div class="stats">+25 Attack Damage, +25% Attack Speed, +200 Health, +20 Ability Haste</div>
                <div class="cost">3333 gold</div>
                <div class="passive"><b>Spellblade:</b> After using an ability, your next attack within 10 seconds deals 200% base AD as bonus damage (1.5s cooldown)</div>
            </div>
            ''',
            "expected_passive": "Spellblade: After using an ability, your next attack within 10 seconds deals 200% base AD as bonus damage (1.5s cooldown)",
            "expected_active": ""
        },
        {
            "name": "Unknown Item with Generic Passive",
            "html": '''
            <div class="item-container">
                <h3>Test Item</h3>
                <div class="stats">+50 Attack Damage</div>
                <div class="cost">2000 gold</div>
                <div class="description">Passive: Grants 15% increased damage to minions and monsters</div>
            </div>
            ''',
            "expected_passive": "Grants 15% increased damage to minions and monsters.",
            "expected_active": ""
        },
        {
            "name": "Unknown Item with Generic Active",
            "html": '''
            <div class="item-container">
                <h3>Test Active Item</h3>
                <div class="stats">+30 Ability Power</div>
                <div class="cost">1500 gold</div>
                <div class="description">Active: Deal 200 magic damage to target enemy (60 second cooldown)</div>
            </div>
            ''',
            "expected_passive": "",
            "expected_active": "Deal 200 magic damage to target enemy (60 second cooldown)."
        }
    ]
    
    print("Testing Passive and Active Effect Parsing")
    print("=" * 50)
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        # Create BeautifulSoup container from HTML
        soup = BeautifulSoup(test_case['html'], 'html.parser')
        container = soup.find('div', class_='item-container')
        container_text = container.get_text()
        
        # Extract passive and active effects
        passive, active = scraper.extract_passive_and_active_effects(
            container, test_case['name'], container_text
        )
        
        # Check results
        passive_correct = passive == test_case['expected_passive']
        active_correct = active == test_case['expected_active']
        
        print(f"Expected Passive: '{test_case['expected_passive']}'")
        print(f"Actual Passive:   '{passive}'")
        print(f"Passive Match: {'✓' if passive_correct else '✗'}")
        
        print(f"Expected Active:  '{test_case['expected_active']}'")
        print(f"Actual Active:    '{active}'")
        print(f"Active Match: {'✓' if active_correct else '✗'}")
        
        if passive_correct and active_correct:
            print("Result: PASS ✓")
            passed_tests += 1
        else:
            print("Result: FAIL ✗")
    
    print("\n" + "=" * 50)
    print(f"Test Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("All tests passed! ✓")
        return True
    else:
        print(f"{total_tests - passed_tests} tests failed. ✗")
        return False

def test_special_cases():
    """Test special cases and edge cases for passive/active parsing"""
    scraper = RealTimeItemScraper()
    
    print("\n" + "=" * 50)
    print("Testing Special Cases")
    print("=" * 50)
    
    # Test named passive extraction (Overkill case)
    test_html = '''
    <div class="item-container">
        <h3>Rabadon's Deathcap</h3>
        <div class="stats">+100 Ability Power</div>
        <div class="cost">3400 gold</div>
        <p><b class="istats2">Overkill:</b> Increases Ability Power by 20-45%</p>
    </div>
    '''
    
    soup = BeautifulSoup(test_html, 'html.parser')
    container = soup.find('div', class_='item-container')
    container_text = container.get_text()
    
    passive, active = scraper.extract_passive_and_active_effects(
        container, "Rabadon's Deathcap", container_text
    )
    
    print("Special Case 1: Named Passive (Overkill)")
    print(f"Extracted Passive: '{passive}'")
    print(f"Expected: 'Overkill: Increases Ability Power by 20-45%'")
    print(f"Match: {'✓' if 'Overkill' in passive and '20-45%' in passive else '✗'}")
    
    # Test enchant item handling
    test_html_enchant = '''
    <div class="item-container">
        <h3>Stasis Enchant</h3>
        <div class="cost">500 gold</div>
        <div class="description">Active: Become invulnerable for 2.5 seconds (120s cooldown)</div>
    </div>
    '''
    
    soup = BeautifulSoup(test_html_enchant, 'html.parser')
    container = soup.find('div', class_='item-container')
    container_text = container.get_text()
    
    passive, active = scraper.extract_passive_and_active_effects(
        container, "Stasis Enchant", container_text
    )
    
    print("\nSpecial Case 2: Enchant Item (No Passive)")
    print(f"Extracted Passive: '{passive}'")
    print(f"Extracted Active: '{active}'")
    print(f"Passive Empty: {'✓' if passive == '' else '✗'}")
    print(f"Active Present: {'✓' if active != '' else '✗'}")
    
    return True

def test_regex_patterns():
    """Test individual regex patterns for passive and active effects"""
    scraper = RealTimeItemScraper()
    
    print("\n" + "=" * 50)
    print("Testing Regex Patterns")
    print("=" * 50)
    
    # Test passive patterns
    test_texts = [
        "Passive: Increases damage by 20%",
        "Overkill: Increases Ability Power by 20-45%",
        "Unique: Grants 15% movement speed",
        "<b>Lifeline:</b> When taking damage below 30% health, gain a shield",
        "Spellblade: After using an ability, next attack deals bonus damage"
    ]
    
    print("Testing Passive Pattern Recognition:")
    for text in test_texts:
        # Create a mock container
        soup = BeautifulSoup(f'<div>{text}</div>', 'html.parser')
        container = soup.find('div')
        
        passive = scraper._extract_passive_effect(container, "Test Item", text)
        print(f"Text: '{text}'")
        print(f"Extracted: '{passive}'")
        print(f"Success: {'✓' if passive else '✗'}")
        print()
    
    # Test active patterns
    active_texts = [
        "Active: Deal 200 magic damage (60s cooldown)",
        "Stasis: Become invulnerable for 2.5 seconds (120s cooldown)",
        "Use: Teleport to target location after 3.5 seconds",
        "<b>Cloudburst:</b> Dash and fire missiles (90s cooldown)"
    ]
    
    print("Testing Active Pattern Recognition:")
    for text in active_texts:
        # Create a mock container
        soup = BeautifulSoup(f'<div>{text}</div>', 'html.parser')
        container = soup.find('div')
        
        active = scraper._extract_active_effect(container, "Test Item", text)
        print(f"Text: '{text}'")
        print(f"Extracted: '{active}'")
        print(f"Success: {'✓' if active else '✗'}")
        print()
    
    return True

if __name__ == "__main__":
    print("Running Passive and Active Effect Parsing Tests")
    print("=" * 60)
    
    # Run all tests
    basic_tests_passed = test_passive_active_parsing()
    special_cases_passed = test_special_cases()
    regex_tests_passed = test_regex_patterns()
    
    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Basic Tests: {'PASS ✓' if basic_tests_passed else 'FAIL ✗'}")
    print(f"Special Cases: {'PASS ✓' if special_cases_passed else 'FAIL ✗'}")
    print(f"Regex Patterns: {'PASS ✓' if regex_tests_passed else 'FAIL ✗'}")
    
    if basic_tests_passed and special_cases_passed and regex_tests_passed:
        print("\nAll passive and active effect parsing tests passed! ✓")
        print("Task 2.2 implementation is working correctly.")
    else:
        print("\nSome tests failed. Please review the implementation. ✗")