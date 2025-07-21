# Requirements Document

## Introduction

This feature implements a comprehensive real-time Wild Rift data scraping system that extracts accurate, up-to-date champion and item information directly from WR-META.com. The system addresses the current issue of hardcoded, outdated item data (like Rabadon's Deathcap showing incorrect cost and stats) by implementing live web scraping with validation and data consistency checks.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to scrape real-time item data from WR-META.com, so that I have accurate stats, costs, and descriptions instead of hardcoded outdated information.

#### Acceptance Criteria

1. WHEN the real-time item scraper is executed THEN the system SHALL extract current item data directly from WR-META.com
2. WHEN scraping Rabadon's Deathcap THEN the system SHALL capture the correct cost (3400), ability power (100), magic penetration (7%), and passive effect (20-45% AP increase)
3. WHEN extracting item stats THEN the system SHALL parse all stat types including ability power, attack damage, health, armor, magic resistance, and movement speed
4. WHEN processing item descriptions THEN the system SHALL extract actual in-game tips and descriptions rather than fabricated content
5. IF an item cannot be found on the website THEN the system SHALL log the failure and continue processing other items

### Requirement 2

**User Story:** As a developer, I want to validate scraped data against the website source, so that I can ensure data accuracy and detect discrepancies.

#### Acceptance Criteria

1. WHEN validation is performed THEN the system SHALL compare local item data with website data for cost, stats, and passive effects
2. WHEN discrepancies are found THEN the system SHALL report specific differences between local and website data
3. WHEN validating Rabadon's Deathcap THEN the system SHALL verify cost matches 3400, AP matches 100, and passive contains "20-45%" text
4. IF validation passes THEN the system SHALL display a success message with checkmark
5. IF validation fails THEN the system SHALL list all discrepancies found

### Requirement 3

**User Story:** As a developer, I want to batch process all champions with real-time item data, so that champion builds contain accurate item information.

#### Acceptance Criteria

1. WHEN batch processing champions THEN the system SHALL scrape each champion's build items using real-time data
2. WHEN processing champion builds THEN the system SHALL categorize items into starting_items, core_items, boots, and situational_items
3. WHEN encountering build items THEN the system SHALL fetch current stats and costs for each item
4. WHEN saving champion data THEN the system SHALL include both item names and detailed item data structures
5. IF an item in a champion build cannot be scraped THEN the system SHALL log the failure but continue processing the champion

### Requirement 4

**User Story:** As a developer, I want to organize and validate all scraped data, so that the final dataset is consistent and complete.

#### Acceptance Criteria

1. WHEN organizing data THEN the system SHALL create separate directories for items, runes, and champions
2. WHEN validating data consistency THEN the system SHALL check for required fields in all JSON files
3. WHEN detecting missing data THEN the system SHALL report specific files and fields that need attention
4. WHEN processing is complete THEN the system SHALL provide a summary of successful vs failed operations
5. IF data inconsistencies are found THEN the system SHALL offer options to fix the issues automatically

### Requirement 5

**User Story:** As a developer, I want to test the final scraped data, so that I can verify accuracy and completeness before using it in applications.

#### Acceptance Criteria

1. WHEN testing item data THEN the system SHALL verify all required fields (name, stats, cost, description) are present
2. WHEN testing critical items THEN the system SHALL validate high-priority items like Rabadon's Deathcap, Infinity Edge, and Trinity Force
3. WHEN testing champion data THEN the system SHALL verify all required sections (champion, stats, abilities, builds) exist
4. WHEN testing builds THEN the system SHALL confirm all referenced items exist in the item database
5. IF testing reveals issues THEN the system SHALL provide specific error messages and suggested fixes

### Requirement 6

**User Story:** As a developer, I want to fix incorrect item data automatically, so that I can update outdated information with current website data.

#### Acceptance Criteria

1. WHEN fixing item data THEN the system SHALL update cost, stats, passive, active, and description fields with current website data
2. WHEN processing Rabadon's Deathcap THEN the system SHALL correct the cost from 3600 to 3400 and passive from "40%" to "20-45%"
3. WHEN updating multiple items THEN the system SHALL implement rate limiting to respect the website's server
4. WHEN saving fixed data THEN the system SHALL preserve the original JSON structure while updating content
5. IF fixing fails for an item THEN the system SHALL log the error and continue with remaining items

### Requirement 7

**User Story:** As a developer, I want to run a complete data update process, so that I can refresh all champion and item data in a single operation.

#### Acceptance Criteria

1. WHEN running full update THEN the system SHALL execute champion scraping, item updating, and validation in sequence
2. WHEN processing champions THEN the system SHALL discover champion URLs automatically and scrape each one
3. WHEN updating items THEN the system SHALL process all items found in champion builds plus critical items
4. WHEN validation completes THEN the system SHALL report the total number of issues found and resolved
5. IF any step fails THEN the system SHALL continue with remaining steps and report all failures at the end
