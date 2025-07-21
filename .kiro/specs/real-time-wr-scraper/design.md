# Design Document

## Overview

The Real-Time Wild Rift Scraper system is designed to extract accurate, up-to-date champion and item data directly from WR-META.com, replacing the current hardcoded and outdated information. The system consists of multiple specialized components that work together to scrape, validate, organize, and test Wild Rift game data.

## Architecture

The system follows a modular architecture with the following key components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Smart Data Organizer                     │
│                   (Orchestration Layer)                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│ Real-Time Item │  │ Batch Champion  │  │ Data Validator  │
│    Scraper     │  │    Scraper      │  │   & Tester      │
└────────────────┘  └─────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────▼─────────────────────┐
        │              Data Storage                 │
        │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │
        │  │  Items  │ │ Champions│ │  Runes  │     │
        │  │   JSON  │ │   JSON   │ │  JSON   │     │
        │  └─────────┘ └─────────┘ └─────────┘     │
        └───────────────────────────────────────────┘
```

## Components and Interfaces

### 1. RealTimeItemScraper

**Purpose**: Extracts accurate item data directly from WR-META.com

**Key Methods**:

- `scrape_all_items()`: Scrapes all items from the items page
- `scrape_specific_item(item_name)`: Scrapes a single item by name
- `extract_item_data(container)`: Parses item data from HTML container
- `save_item_data(item_data)`: Saves item data to JSON file

**Data Extraction Patterns**:

```python
stat_patterns = {
    'ability_power': r'(\+?\d+)\s*(?:Ability Power|AP)',
    'attack_damage': r'(\+?\d+)\s*(?:Attack Damage|AD)',
    'health': r'(\+?\d+)\s*Health',
    'armor': r'(\+?\d+)\s*Armor',
    'magic_resistance': r'(\+?\d+)\s*(?:Magic Resist|MR)',
    'cost': r'(\d{3,4})\s*(?:gold|cost)'
}
```

### 2. SmartDataOrganizer

**Purpose**: Orchestrates the entire data update process

**Key Methods**:

- `run_full_data_update()`: Executes complete data refresh
- `update_item_data()`: Updates all items with real-time data
- `validate_data_consistency()`: Checks data integrity
- `run_batch_scrape_champions()`: Triggers champion scraping

**Workflow**:

1. Discover champion URLs
2. Scrape champion data
3. Extract item names from builds
4. Update item data with real-time information
5. Validate data consistency
6. Generate reports

### 3. DataValidator

**Purpose**: Validates scraped data against website sources

**Key Methods**:

- `validate_item(item_name)`: Compares local vs website data
- `validate_all_items()`: Validates entire item database
- `fix_rabadon()`: Specifically fixes Rabadon's Deathcap data

**Validation Logic**:

```python
# Compare key fields
if website_cost and local_data.get('cost') != website_cost:
    discrepancies.append(f"Cost mismatch: Local={local_cost}, Website={website_cost}")

if website_ap and local_ap != website_ap:
    discrepancies.append(f"AP mismatch: Local={local_ap}, Website={website_ap}")
```

### 4. ItemDataFixer

**Purpose**: Automatically corrects outdated item information

**Key Methods**:

- `fix_all_items()`: Updates all items with real data
- `fix_specific_items(item_names)`: Updates specified items
- `fix_critical_items()`: Updates high-priority items

**Update Process**:

1. Load existing item data
2. Scrape current website data
3. Merge data (preserve structure, update content)
4. Save updated JSON file
5. Apply rate limiting between requests

### 5. DataTester

**Purpose**: Verifies final data quality and completeness

**Key Methods**:

- `test_item_data(item_name)`: Tests individual item structure
- `test_critical_items()`: Tests high-priority items
- `test_champion_data(champion_name)`: Tests champion data structure

**Test Criteria**:

- Required fields present
- Valid data types
- Proper JSON structure
- Cross-references between champions and items

## Data Models

### Item Data Structure

```json
{
  "name": "Rabadon's Deathcap",
  "stats": {
    "ability_power": { "value": 100, "type": "flat" },
    "magic_penetration": { "value": 7, "type": "percentage" }
  },
  "cost": 3400,
  "passive": "Overkill: Increases Ability Power by 20-45%",
  "active": "",
  "description": "This item is perfect for mages who rely on high ability power ratios...",
  "category": "legendary",
  "tier": "S",
  "tips": [
    "Build after other AP items to maximize the bonus effect",
    "The passive applies to ALL ability power from items and runes"
  ]
}
```

### Champion Data Structure

```json
{
  "champion": {
    "id": "332-aatrox",
    "name": "Aatrox",
    "title": "The Darkin Blade",
    "role": "Fighter"
  },
  "stats": {
    /* base stats */
  },
  "abilities": {
    /* ability details */
  },
  "builds": {
    "starting_items": ["Doran's Blade", "Health Potion"],
    "core_items": ["Trinity Force", "Sterak's Gage"],
    "boots": ["Plated Steelcaps", "Mercury's Treads"],
    "situational_items": ["Guardian Angel", "Death's Dance"]
  }
}
```

## Error Handling

### Network Errors

- Implement retry logic with exponential backoff
- Timeout handling for slow responses
- Graceful degradation when website is unavailable

### Data Parsing Errors

- Continue processing other items when one fails
- Log specific parsing errors with context
- Provide fallback data structures

### File System Errors

- Create directories if they don't exist
- Handle permission issues gracefully
- Backup existing data before updates

### Rate Limiting

- Implement delays between requests (1-2 seconds)
- Respect website's robots.txt if available
- Monitor for rate limiting responses

## Testing Strategy

### Unit Tests

- Test individual scraping functions
- Validate data parsing logic
- Test error handling scenarios

### Integration Tests

- Test complete scraping workflows
- Validate data consistency across components
- Test batch processing with sample data

### Data Validation Tests

- Compare scraped data with known correct values
- Test critical items (Rabadon's, Infinity Edge, etc.)
- Validate JSON structure and required fields

### Performance Tests

- Measure scraping speed and memory usage
- Test with large datasets
- Validate rate limiting effectiveness

## Security Considerations

### Web Scraping Ethics

- Respect website's terms of service
- Implement appropriate delays between requests
- Use proper User-Agent headers
- Monitor for anti-scraping measures

### Data Validation

- Sanitize extracted data to prevent injection
- Validate data types and ranges
- Handle malformed HTML gracefully

### File System Security

- Validate file paths to prevent directory traversal
- Use safe JSON parsing methods
- Implement proper error logging without exposing sensitive data

## Performance Optimization

### Caching Strategy

- Cache website responses to reduce requests
- Store intermediate parsing results
- Implement smart cache invalidation

### Parallel Processing

- Process multiple items concurrently where possible
- Use connection pooling for HTTP requests
- Implement queue-based processing for large datasets

### Memory Management

- Stream large datasets instead of loading entirely in memory
- Clean up temporary data structures
- Monitor memory usage during batch operations

## Monitoring and Logging

### Logging Levels

- INFO: Successful operations and progress updates
- WARN: Recoverable errors and data inconsistencies
- ERROR: Failed operations and critical issues
- DEBUG: Detailed parsing and validation information

### Metrics Collection

- Track scraping success/failure rates
- Monitor processing times
- Count data validation issues
- Measure data freshness

### Alerting

- Alert on high failure rates
- Notify when critical items fail validation
- Monitor for website structure changes

## Deployment and Maintenance

### Scheduled Updates

- Daily updates for critical items
- Weekly full data refresh
- On-demand updates for specific items

### Data Backup

- Backup existing data before updates
- Maintain historical versions
- Implement rollback capabilities

### Monitoring Website Changes

- Detect changes in website structure
- Adapt scraping patterns automatically where possible
- Alert when manual intervention is needed

This design provides a robust, scalable solution for maintaining accurate Wild Rift data through real-time web scraping while ensuring data quality and system reliability.
