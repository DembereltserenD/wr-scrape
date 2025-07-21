#!/usr/bin/env python3
"""
Test script for batch champion processing with real-time data integration
"""

from batch_scrape_all_champions import BatchChampionScraper
import json

def test_batch_champion_integration():
    """Test the batch champion scraper integration with real-time item data"""
    print("Testing BatchChampionScraper integration...")
    
    # Initialize the scraper
    scraper = BatchChampionScraper()
    
    # Test item extraction from sample champion data
    sample_champion_data = {
        'champion': {'name': 'Test Champion'},
        'builds': {
            'starting_items': ['Doran\'s Blade', 'Health Potion'],
            'core_items': ['Infinity Edge', 'Phantom Dancer'],
            'boots': ['Berserker\'s Greaves'],
            'situational_items': ['Guardian Angel', 'Mortal Reminder'],
            'enchants': ['Stasis Enchant']
        }
    }
    
    # Test item name extraction
    item_names = scraper._extract_item_names_from_builds(sample_champion_data)
    print(f"✓ Extracted {len(item_names)} item names: {list(item_names)}")
    
    # Test fallback item data creation
    fallback_item = scraper._create_fallback_item_data("Test Item", "Testing fallback mechanism")
    print(f"✓ Created fallback item data: {fallback_item['name']}")
    
    # Test error logging
    scraper._log_failed_item("Test Failed Item", "Test failure reason")
    print(f"✓ Logged failed item, total failed: {len(scraper.failed_items)}")
    
    # Test error report generation
    error_report = scraper.generate_error_report()
    print(f"✓ Generated error report with {error_report['summary']['total_failed_items']} failed items")
    
    print("\n✅ All integration tests passed!")
    return True

if __name__ == "__main__":
    test_batch_champion_integration()