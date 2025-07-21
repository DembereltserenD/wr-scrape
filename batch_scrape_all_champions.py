#!/usr/bin/env python3
"""
Batch Champion Data Scraper for WR-META.com
Scrapes ALL champions from the WR-META website with real-time item data

Usage: python batch_scrape_all_champions.py
"""

import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup
from enhanced_scrape_champion import RealDataScraper
from champion_url_mapper import ChampionURLMapper
from real_time_item_scraper import RealTimeItemScraper

class BatchChampionScraper:
    def __init__(self):
        self.scraper = RealDataScraper()
        self.url_mapper = ChampionURLMapper()
        self.item_scraper = RealTimeItemScraper()
        self.base_url = "https://wr-meta.com"
        self.champions_data = {}
        self.failed_urls = []
        self.corrected_urls = {}
        self.item_cache = {}  # Cache for scraped item data to avoid duplicate requests
        self.failed_items = []  # Track items that failed to scrape
        self.item_scrape_stats = {'success': 0, 'failed': 0, 'cached': 0}  # Track scraping statistics
        
    def discover_all_champions(self):
        """Discover all champion URLs from WR-META using dynamic discovery"""
        print("Discovering all champions from WR-META...")
        
        # Try to load from pre-discovered file first
        try:
            import json
            with open('discovered_champion_urls.json', 'r') as f:
                champion_urls = json.load(f)
            print(f"Loaded {len(champion_urls)} URLs from discovered_champion_urls.json")
            return champion_urls
        except FileNotFoundError:
            pass
        
        # Use the URL mapper for dynamic discovery
        champion_urls = self.url_mapper.discover_champion_urls()
        
        if not champion_urls:
            raise RuntimeError("Could not discover any champion URLs - site layout may have changed.")
        
        print(f"Found {len(champion_urls)} champion URLs")
        return champion_urls
    
    def scrape_all_champions(self, champion_urls, max_champions=None):
        """Scrape data for all discovered champions"""
        print(f"Starting batch scraping of {len(champion_urls)} champions...")
        
        if max_champions:
            champion_urls = champion_urls[:max_champions]
            print(f"   Limited to first {max_champions} champions for testing")
        
        successful_scrapes = 0
        failed_scrapes = 0
        
        # Create output directory
        output_dir = "scraped_champions"
        os.makedirs(output_dir, exist_ok=True)
        
        for i, url in enumerate(champion_urls, 1):
            try:
                print(f"\n[{i}/{len(champion_urls)}] Scraping: {url}")
                
                # Extract champion data with smart retry
                champion_data = self._scrape_with_retry(url)
                
                if not champion_data:
                    failed_scrapes += 1
                    continue
                
                champion_name = champion_data['champion']['name'].lower()
                
                # Validate that we got the right champion
                expected_slug = url.split('/')[-1].replace('.html', '').split('-', 1)[-1]
                if not self._validate_champion_match(champion_name, expected_slug):
                    print(f"     Champion name mismatch: got '{champion_name}' from URL with slug '{expected_slug}'")
                
                # Save individual champion file
                safe_filename = re.sub(r'[^\w\s-]', '', champion_name).strip().replace(' ', '_')
                filename = f"{output_dir}/{safe_filename}_data.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(champion_data, f, indent=2, ensure_ascii=False)
                
                # Add to master collection
                self.champions_data[champion_name] = champion_data
                
                print(f"    Successfully scraped {champion_data['champion']['name']}")
                print(f"      - Stats: {len(champion_data['stats'])}")
                print(f"      - Abilities: {len(champion_data['abilities'])}")
                
                # Handle build structure
                builds = champion_data['builds']
                starting_count = len(builds.get('starting_items', []))
                core_count = len(builds.get('core_items', []))
                situational_count = len(builds.get('situational_items', []))
                total_items = starting_count + core_count + situational_count
                
                print(f"      - Items: {total_items} (Start: {starting_count}, Core: {core_count}, Situational: {situational_count})")
                print(f"      - Lanes: {len(builds.get('lanes', []))}")
                
                successful_scrapes += 1
                
                # Be respectful to the server
                time.sleep(1)
                
            except Exception as e:
                print(f"    Failed to scrape {url}: {e}")
                self.failed_urls.append(url)
                failed_scrapes += 1
                continue
        
        # Save master collection
        master_filename = f"{output_dir}/all_champions_data.json"
        with open(master_filename, 'w', encoding='utf-8') as f:
            json.dump(self.champions_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nScraping Summary:")
        print(f"    Successful: {successful_scrapes}")
        print(f"    Failed: {failed_scrapes}")
        print(f"    URL Corrections: {len(self.corrected_urls)}")
        print(f"    Data saved to: {output_dir}/")
        print(f"    Master file: {master_filename}")
        
        # Report URL corrections
        if self.corrected_urls:
            print(f"\n URL Corrections Made:")
            for original, corrected in self.corrected_urls.items():
                print(f"   {original} → {corrected}")
        
        # Report failed URLs
        if self.failed_urls:
            print(f"\n Failed URLs:")
            for failed_url in self.failed_urls:
                print(f"   {failed_url}")
        
        # Generate comprehensive error report
        self.generate_error_report()
        self.print_error_summary()
        
        return self.champions_data
    
    def _scrape_with_retry(self, url, max_retries=3):
        """Scrape champion data with smart retry and URL correction"""
        
        for attempt in range(max_retries):
            try:
                # Try main scrape
                champion_data = self.scraper.scrape_champion_data(url)
                
                # Enhance champion data with real-time item data
                if champion_data and 'builds' in champion_data:
                    champion_data = self._enhance_champion_with_real_time_items(champion_data)
                
                return champion_data
                
            except requests.HTTPError as http_e:
                if hasattr(http_e, 'response') and http_e.response.status_code == 404:
                    print(f"     Got 404, attempting to find correct URL...")
                    
                    # Extract champion name from URL slug
                    url_slug = url.split('/')[-1].replace('.html', '').split('-', 1)[-1]
                    
                    # Try to find correct URL
                    corrected_url = self.url_mapper.search_champion_url(url_slug.replace('-', ' '))
                    
                    if corrected_url and corrected_url != url:
                        print(f"       Retrying with corrected URL: {corrected_url}")
                        self.corrected_urls[url] = corrected_url
                        try:
                            champion_data = self.scraper.scrape_champion_data(corrected_url)
                            return champion_data
                        except Exception as retry_e:
                            print(f"       Corrected URL also failed: {retry_e}")
                    
                    # Try brute force search as last resort
                    if attempt == max_retries - 1:
                        print(f"       Attempting brute force search...")
                        brute_force_url = self.url_mapper.brute_force_search(url_slug.replace('-', ' '))
                        if brute_force_url:
                            print(f"       Found via brute force: {brute_force_url}")
                            self.corrected_urls[url] = brute_force_url
                            try:
                                champion_data = self.scraper.scrape_champion_data(brute_force_url)
                                return champion_data
                            except Exception as brute_e:
                                print(f"       Brute force URL also failed: {brute_e}")
                
                # For non-404 errors or if correction failed, retry
                if attempt < max_retries - 1:
                    print(f"     Attempt {attempt + 1} failed, retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    raise
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"     Attempt {attempt + 1} failed: {e}, retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    raise
        
        return None
    
    def _enhance_champion_with_real_time_items(self, champion_data):
        """Enhance champion data with real-time item data from WR-META"""
        try:
            print("      Enhancing with real-time item data...")
            
            if 'builds' not in champion_data:
                return champion_data
            
            # Extract all unique item names from champion build data
            all_item_names = self._extract_item_names_from_builds(champion_data)
            
            if not all_item_names:
                print("        No items found in builds")
                return champion_data
            
            # Fetch current stats and costs for each build item
            enhanced_items = self._fetch_current_stats_and_costs(all_item_names)
            
            # Implement item categorization (starting, core, boots, situational) with real-time data
            builds = self._categorize_items_with_real_time_data(champion_data['builds'], enhanced_items)
            
            # Add real-time item data fetching for champion builds
            builds = self._add_detailed_item_data_with_real_time(builds, enhanced_items)
            
            champion_data['builds'] = builds
            
            # Add metadata about real-time enhancement
            champion_data['real_time_enhancement'] = {
                'enhanced_items_count': len(enhanced_items),
                'total_items_found': len(all_item_names),
                'enhancement_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'success_rate': f"{len(enhanced_items)}/{len(all_item_names)} ({(len(enhanced_items)/len(all_item_names)*100):.1f}%)" if all_item_names else "0/0 (0%)"
            }
            
            print(f"        Enhanced {len(enhanced_items)}/{len(all_item_names)} items with real-time data")
            
        except Exception as e:
            print(f"        Warning: Failed to enhance with real-time item data: {e}")
            # Continue processing champions when individual items fail
            self._log_champion_item_enhancement_failure(champion_data.get('champion', {}).get('name', 'Unknown'), str(e))
        
        return champion_data
    
    def _get_real_time_item_data(self, item_name):
        """Get real-time item data with caching and comprehensive error handling"""
        # Check cache first
        if item_name in self.item_cache:
            self.item_scrape_stats['cached'] += 1
            return self.item_cache[item_name]
        
        # Implement retry logic for failed items
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # Use the real-time item scraper to get current data
                item_data = self.item_scraper.scrape_specific_item(item_name)
                
                if item_data:
                    # Cache the result
                    self.item_cache[item_name] = item_data
                    self.item_scrape_stats['success'] += 1
                    
                    # Add rate limiting to be respectful to the server
                    time.sleep(0.5)
                    
                    return item_data
                else:
                    # If no data returned, try alternative item name variations
                    alternative_names = self._generate_item_name_variations(item_name)
                    for alt_name in alternative_names:
                        if alt_name != item_name and alt_name not in self.item_cache:
                            try:
                                alt_data = self.item_scraper.scrape_specific_item(alt_name)
                                if alt_data:
                                    # Cache both the original and alternative name
                                    self.item_cache[item_name] = alt_data
                                    self.item_cache[alt_name] = alt_data
                                    self.item_scrape_stats['success'] += 1
                                    time.sleep(0.5)
                                    return alt_data
                            except Exception:
                                continue  # Try next variation
                    
                    # If this is the last attempt, log the failure
                    if attempt == max_retries:
                        self._log_failed_item(item_name, "No data returned from scraper after retries")
                    return None
                    
            except requests.RequestException as e:
                # Network-related errors - retry with exponential backoff
                if attempt < max_retries:
                    print(f"          Network error for {item_name}, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    self._log_failed_item(item_name, f"Network error after {max_retries} retries: {e}")
                    return None
            except Exception as e:
                # Other errors - retry once
                if attempt < max_retries:
                    print(f"          Error for {item_name}, retrying...")
                    time.sleep(retry_delay)
                    continue
                else:
                    self._log_failed_item(item_name, f"Scraping error after {max_retries} retries: {e}")
                    return None
        
        return None
    
    def _generate_item_name_variations(self, item_name):
        """Generate alternative item name variations for fallback scraping"""
        variations = []
        
        # Common variations
        variations.append(item_name.replace("'", ""))  # Remove apostrophes
        variations.append(item_name.replace("'", "'"))  # Different apostrophe style
        variations.append(item_name.replace("-", " "))  # Replace hyphens with spaces
        variations.append(item_name.replace(" ", "-"))  # Replace spaces with hyphens
        
        # Handle common item name patterns
        if "Enchant" in item_name:
            # Try without "Enchant"
            base_name = item_name.replace("Enchant", "").strip()
            if base_name:
                variations.append(base_name)
        
        # Handle possessive forms
        if "'s" in item_name:
            variations.append(item_name.replace("'s", "s"))
            variations.append(item_name.replace("'s", ""))
        
        # Remove duplicates and return
        return list(set(variations))
    
    def _log_failed_item(self, item_name, reason):
        """Add logging for items that cannot be scraped with detailed reason and context"""
        failed_item_info = {
            'name': item_name,
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'retry_attempts': getattr(self, '_current_retry_count', 0),
            'fallback_attempted': True
        }
        
        self.failed_items.append(failed_item_info)
        self.item_scrape_stats['failed'] += 1
        
        # Enhanced logging with more context
        print(f"          ✗ Failed to scrape '{item_name}': {reason}")
        
        # Log to file for persistent tracking
        self._log_to_file('failed_items.log', f"[{failed_item_info['timestamp']}] FAILED: {item_name} - {reason}")
        
        # Continue processing champions when individual items fail
        print(f"          → Continuing with fallback data for '{item_name}'")
        
        return failed_item_info
    
    def _log_to_file(self, filename, message):
        """Log messages to file for persistent tracking"""
        try:
            os.makedirs('logs', exist_ok=True)
            log_path = os.path.join('logs', filename)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"          Warning: Could not write to log file {filename}: {e}")
    
    def _log_champion_item_enhancement_failure(self, champion_name, error_message):
        """Add logging for items that cannot be scraped during champion processing"""
        failure_info = {
            'champion': champion_name,
            'error': error_message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to a champion-specific failure log
        if not hasattr(self, 'champion_enhancement_failures'):
            self.champion_enhancement_failures = []
        
        self.champion_enhancement_failures.append(failure_info)
        print(f"        ✗ Champion item enhancement failed for {champion_name}: {error_message}")
    
    def _create_fallback_item_data(self, item_name, reason="Item data unavailable"):
        """Create fallback mechanisms for missing item data"""
        # Try to get basic item information from existing data files
        fallback_data = self._try_load_existing_item_data(item_name)
        
        if fallback_data:
            # Mark as fallback but preserve existing data
            fallback_data["fallback"] = True
            fallback_data["fallback_reason"] = f"Using cached data: {reason}"
            fallback_data["last_updated"] = "cached"
            return fallback_data
        
        # Create minimal fallback structure
        return {
            "name": item_name,
            "stats": {},
            "cost": 0,
            "passive": "",
            "active": "",
            "description": f"Real-time data for {item_name} could not be fetched. Reason: {reason}",
            "category": "unknown",
            "tier": "Unknown",
            "tips": [],
            "fallback": True,  # Mark as fallback data
            "fallback_reason": reason,
            "last_updated": "unavailable"
        }
    
    def _try_load_existing_item_data(self, item_name):
        """Try to load existing item data as fallback"""
        try:
            # Convert item name to filename format
            safe_filename = re.sub(r'[^\w\s-]', '', item_name.lower()).strip().replace(' ', '_')
            item_file_path = f"items/{safe_filename}.json"
            
            if os.path.exists(item_file_path):
                with open(item_file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    print(f"          ↻ Using cached data for {item_name}")
                    return existing_data
        except Exception as e:
            print(f"          Could not load cached data for {item_name}: {e}")
        
        return None
    
    def _handle_champion_processing_continuation(self, champion_data, error):
        """Continue processing champions when individual items fail"""
        champion_name = champion_data.get('champion', {}).get('name', 'Unknown')
        
        # Enhanced logging for champion processing continuation
        print(f"        ⚠ Warning: Item processing failed for {champion_name}, continuing with available data")
        self._log_to_file('champion_processing_errors.log', 
                         f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CHAMPION_ERROR: {champion_name} - {str(error)}")
        
        # Ensure champion still has basic build structure even if item enhancement failed
        if 'builds' not in champion_data:
            champion_data['builds'] = {
                'starting_items': [],
                'core_items': [],
                'boots': [],
                'situational_items': [],
                'enchants': []
            }
        
        # Add error information to champion data for debugging
        if 'processing_errors' not in champion_data:
            champion_data['processing_errors'] = []
        
        champion_data['processing_errors'].append({
            'type': 'item_enhancement_failure',
            'error': str(error),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'recovery_action': 'continued_with_fallback_data',
            'champion_name': champion_name
        })
        
        # Add fallback metadata to indicate partial processing
        champion_data['processing_metadata'] = {
            'partial_processing': True,
            'item_enhancement_failed': True,
            'fallback_data_used': True,
            'processing_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"        → Champion {champion_name} will continue with basic build structure")
        
        return champion_data
    
    def generate_error_report(self):
        """Generate comprehensive error report for missing items and failed processing"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'failed_items': self.failed_items,
            'item_scrape_stats': self.item_scrape_stats,
            'champion_enhancement_failures': getattr(self, 'champion_enhancement_failures', []),
            'summary': {
                'total_failed_items': len(self.failed_items),
                'total_successful_items': self.item_scrape_stats.get('success', 0),
                'total_cached_items': self.item_scrape_stats.get('cached', 0),
                'champion_failures': len(getattr(self, 'champion_enhancement_failures', [])),
                'overall_success_rate': f"{self.item_scrape_stats.get('success', 0)}/{self.item_scrape_stats.get('success', 0) + len(self.failed_items)} ({(self.item_scrape_stats.get('success', 0)/(self.item_scrape_stats.get('success', 0) + len(self.failed_items))*100):.1f}%)" if (self.item_scrape_stats.get('success', 0) + len(self.failed_items)) > 0 else "0/0 (0%)"
            }
        }
        
        # Save error report to file
        try:
            os.makedirs('logs', exist_ok=True)
            report_path = os.path.join('logs', 'error_report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\nError report saved to: {report_path}")
        except Exception as e:
            print(f"Warning: Could not save error report: {e}")
        
        return report
    
    def print_error_summary(self):
        """Print a summary of errors and missing items"""
        print(f"\n=== ERROR SUMMARY ===")
        print(f"Failed Items: {len(self.failed_items)}")
        print(f"Successful Items: {self.item_scrape_stats.get('success', 0)}")
        print(f"Cached Items: {self.item_scrape_stats.get('cached', 0)}")
        print(f"Champion Enhancement Failures: {len(getattr(self, 'champion_enhancement_failures', []))}")
        
        if self.failed_items:
            print(f"\nMost Common Failure Reasons:")
            failure_reasons = {}
            for item in self.failed_items:
                reason = item.get('reason', 'Unknown')
                failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
            
            for reason, count in sorted(failure_reasons.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  - {reason}: {count} items")
        
        print(f"===================\n")
    
    def _categorize_items_with_real_time_data(self, builds, enhanced_items):
        """Implement item categorization (starting, core, boots, situational) using real-time data"""
        
        # Define item categories based on Wild Rift item types and real-time data
        starting_item_names = {
            "doran's blade", "doran's ring", "doran's shield", "relic shield", 
            "spectral sickle", "long sword", "amplifying tome", "ruby crystal",
            "sapphire crystal", "boots", "ancient coin", "tear of the goddess",
            "health potion", "mana potion", "corrupting potion"
        }
        
        boot_keywords = {
            "boots", "treads", "steelcaps", "lucidity", "greaves", "dynamism", "mana"
        }
        
        enchant_keywords = {
            "enchant", "stasis", "protobelt", "quicksilver", "teleport", 
            "repulsor", "locket", "glorious", "meteor", "veil", "stoneplate"
        }
        
        # Enhanced cost thresholds based on real-time data analysis
        starting_item_cost_threshold = 500
        core_item_cost_threshold = 2500
        situational_item_cost_threshold = 1500
        
        # Recategorize items based on their actual type and real-time data
        categorized = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'enchants': []
        }
        
        # Process all items and categorize them properly using real-time data
        all_items = set()
        for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'enchants', 'example_build']:
            if category in builds and isinstance(builds[category], list):
                all_items.update(builds[category])
        
        categorization_stats = {'enhanced': 0, 'fallback': 0}
        
        for item_name in all_items:
            if not item_name or not item_name.strip():
                continue
                
            item_lower = item_name.lower()
            
            # Use real-time data for more accurate categorization
            if item_name in enhanced_items:
                categorization_stats['enhanced'] += 1
                item_data = enhanced_items[item_name]
                item_cost = item_data.get('cost', 0)
                item_category = item_data.get('category', '').lower()
                item_stats = item_data.get('stats', {})
                
                # Enhanced categorization logic using real-time data
                if any(keyword in item_lower for keyword in enchant_keywords):
                    categorized['enchants'].append(item_name)
                elif (any(keyword in item_lower for keyword in boot_keywords) or 
                      item_category == 'boots' or 
                      'movement_speed' in item_stats):
                    categorized['boots'].append(item_name)
                elif (item_lower in starting_item_names or 
                      item_category in ['starting', 'basic', 'consumable'] or 
                      item_cost <= starting_item_cost_threshold):
                    categorized['starting_items'].append(item_name)
                elif (item_cost >= core_item_cost_threshold or 
                      item_category in ['legendary', 'mythic', 'epic']):
                    categorized['core_items'].append(item_name)
                elif (item_cost >= situational_item_cost_threshold or
                      item_category in ['component', 'intermediate']):
                    categorized['situational_items'].append(item_name)
                else:
                    # Items with lower cost are typically situational/early game
                    categorized['situational_items'].append(item_name)
            else:
                categorization_stats['fallback'] += 1
                # Fallback to keyword-based categorization for items without real-time data
                if any(keyword in item_lower for keyword in enchant_keywords):
                    categorized['enchants'].append(item_name)
                elif any(keyword in item_lower for keyword in boot_keywords):
                    categorized['boots'].append(item_name)
                elif item_lower in starting_item_names:
                    categorized['starting_items'].append(item_name)
                else:
                    # Default to core items for unknown items
                    categorized['core_items'].append(item_name)
        
        # Update builds with proper categorization
        for category, items in categorized.items():
            builds[category] = list(set(items))  # Remove duplicates
        
        # Add categorization metadata
        builds['categorization_metadata'] = {
            'enhanced_items': categorization_stats['enhanced'],
            'fallback_items': categorization_stats['fallback'],
            'total_items': len(all_items),
            'categorization_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'real_time_scraper_used': True,
            'categorization_method': 'real_time_data_enhanced'
        }
        
        print(f"        Categorized {len(all_items)} items ({categorization_stats['enhanced']} with real-time data, {categorization_stats['fallback']} fallback)")
        
        return builds
    
    def _categorize_items(self, builds, enhanced_items):
        """Properly categorize items into starting, core, boots, and situational"""
        
        # Define item categories based on Wild Rift item types
        starting_item_names = {
            "doran's blade", "doran's ring", "doran's shield", "relic shield", 
            "spectral sickle", "long sword", "amplifying tome", "ruby crystal",
            "sapphire crystal", "boots", "ancient coin"
        }
        
        boot_keywords = {
            "boots", "treads", "steelcaps", "lucidity", "greaves"
        }
        
        enchant_keywords = {
            "enchant", "stasis", "protobelt", "quicksilver", "teleport", 
            "repulsor", "locket", "glorious", "meteor", "veil", "stoneplate"
        }
        
        # Recategorize items based on their actual type
        categorized = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'enchants': []
        }
        
        # Process all items and categorize them properly
        all_items = set()
        for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build']:
            if category in builds and isinstance(builds[category], list):
                all_items.update(builds[category])
        
        for item_name in all_items:
            if not item_name or not item_name.strip():
                continue
                
            item_lower = item_name.lower()
            
            # Categorize based on item characteristics
            if any(keyword in item_lower for keyword in enchant_keywords):
                categorized['enchants'].append(item_name)
            elif any(keyword in item_lower for keyword in boot_keywords):
                categorized['boots'].append(item_name)
            elif item_lower in starting_item_names:
                categorized['starting_items'].append(item_name)
            elif item_name in enhanced_items:
                # Use the enhanced item data to determine category
                item_data = enhanced_items[item_name]
                if item_data.get('category') == 'boots':
                    categorized['boots'].append(item_name)
                elif item_data.get('category') in ['starting', 'basic']:
                    categorized['starting_items'].append(item_name)
                elif item_data.get('cost', 0) < 1500:  # Lower cost items are often situational/early
                    categorized['situational_items'].append(item_name)
                else:
                    categorized['core_items'].append(item_name)
            else:
                # Default to core items for unknown items
                categorized['core_items'].append(item_name)
        
        # Update builds with proper categorization
        for category, items in categorized.items():
            builds[category] = list(set(items))  # Remove duplicates
        
        return builds
    
    def _add_detailed_item_data_with_real_time(self, builds, enhanced_items):
        """Add detailed item data to builds structure with real-time data integration"""
        
        detailed_items_count = 0
        fallback_items_count = 0
        
        # Add detailed data for each category with real-time information
        for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'enchants']:
            if category in builds and builds[category]:
                detailed_key = f"{category}_detailed"
                builds[detailed_key] = []
                
                for item_name in builds[category]:
                    if item_name in enhanced_items:
                        # Include both item names and detailed item data in champion files
                        item_data = enhanced_items[item_name].copy()
                        
                        # Ensure we have current stats and costs for each build item
                        item_data = self._ensure_current_stats_and_costs(item_data, item_name)
                        
                        # Add metadata about real-time data fetch
                        item_data['real_time_data'] = True
                        item_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        item_data['data_source'] = 'wr-meta.com'
                        item_data['category_assigned'] = category
                        builds[detailed_key].append(item_data)
                        detailed_items_count += 1
                    else:
                        # Create fallback mechanisms for missing item data
                        fallback_item = self._create_fallback_item_data(
                            item_name, 
                            "Item data could not be fetched during champion processing"
                        )
                        fallback_item['category_assigned'] = category
                        builds[detailed_key].append(fallback_item)
                        fallback_items_count += 1
        
        # Process alternative builds with detailed item data
        if 'alternative_builds' in builds:
            for i, alt_build in enumerate(builds['alternative_builds']):
                if isinstance(alt_build, dict):
                    # Process all item categories in alternative builds
                    for alt_category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                        if alt_category in alt_build and alt_build[alt_category]:
                            detailed_alt_key = f"{alt_category}_detailed"
                            alt_build[detailed_alt_key] = []
                            
                            for item_name in alt_build[alt_category]:
                                if item_name in enhanced_items:
                                    item_data = enhanced_items[item_name].copy()
                                    item_data['real_time_data'] = True
                                    item_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                                    item_data['data_source'] = 'wr-meta.com'
                                    item_data['category_assigned'] = alt_category
                                    item_data['alternative_build_index'] = i
                                    alt_build[detailed_alt_key].append(item_data)
                                    detailed_items_count += 1
                                else:
                                    fallback_item = self._create_fallback_item_data(
                                        item_name, 
                                        f"Item data could not be fetched for alternative build {i+1}"
                                    )
                                    fallback_item['category_assigned'] = alt_category
                                    fallback_item['alternative_build_index'] = i
                                    alt_build[detailed_alt_key].append(fallback_item)
                                    fallback_items_count += 1
        
        # Process example build with detailed data
        if 'example_build' in builds and builds['example_build']:
            builds['example_build_detailed'] = []
            for item_name in builds['example_build']:
                if item_name in enhanced_items:
                    item_data = enhanced_items[item_name].copy()
                    item_data['real_time_data'] = True
                    item_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    item_data['data_source'] = 'wr-meta.com'
                    item_data['category_assigned'] = 'example_build'
                    builds['example_build_detailed'].append(item_data)
                    detailed_items_count += 1
                else:
                    fallback_item = self._create_fallback_item_data(
                        item_name,
                        "Item data could not be fetched for example build"
                    )
                    fallback_item['category_assigned'] = 'example_build'
                    builds['example_build_detailed'].append(fallback_item)
                    fallback_items_count += 1
        
        # Process lane-specific builds with detailed data
        if 'lane_specific' in builds:
            for lane_name, lane_data in builds['lane_specific'].items():
                if isinstance(lane_data, dict):
                    for lane_category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                        if lane_category in lane_data and lane_data[lane_category]:
                            detailed_lane_key = f"{lane_category}_detailed"
                            lane_data[detailed_lane_key] = []
                            
                            for item_name in lane_data[lane_category]:
                                if item_name in enhanced_items:
                                    item_data = enhanced_items[item_name].copy()
                                    item_data['real_time_data'] = True
                                    item_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
                                    item_data['data_source'] = 'wr-meta.com'
                                    item_data['category_assigned'] = lane_category
                                    item_data['lane_specific'] = lane_name
                                    lane_data[detailed_lane_key].append(item_data)
                                    detailed_items_count += 1
                                else:
                                    fallback_item = self._create_fallback_item_data(
                                        item_name,
                                        f"Item data could not be fetched for {lane_name} lane build"
                                    )
                                    fallback_item['category_assigned'] = lane_category
                                    fallback_item['lane_specific'] = lane_name
                                    lane_data[detailed_lane_key].append(fallback_item)
                                    fallback_items_count += 1
        
        # Add summary metadata about detailed item processing
        builds['detailed_items_metadata'] = {
            'real_time_items': detailed_items_count,
            'fallback_items': fallback_items_count,
            'total_detailed_items': detailed_items_count + fallback_items_count,
            'real_time_success_rate': f"{detailed_items_count}/{detailed_items_count + fallback_items_count} ({(detailed_items_count/(detailed_items_count + fallback_items_count)*100):.1f}%)" if (detailed_items_count + fallback_items_count) > 0 else "0/0 (0%)",
            'processing_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'includes_both_names_and_data': True,
            'data_structure': 'item_names_list + detailed_data_list'
        }
        
        print(f"        Added detailed data: {detailed_items_count} real-time, {fallback_items_count} fallback")
        
        return builds
    
    def _add_detailed_item_data(self, builds, enhanced_items):
        """Add detailed item data to builds structure"""
        
        # Add detailed data for each category
        for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'enchants']:
            if category in builds:
                detailed_key = f"{category}_detailed"
                builds[detailed_key] = []
                
                for item_name in builds[category]:
                    if item_name in enhanced_items:
                        builds[detailed_key].append(enhanced_items[item_name])
                    else:
                        # Use fallback mechanism for missing items
                        fallback_item = self._create_fallback_item_data(
                            item_name, 
                            "Item data could not be fetched during champion processing"
                        )
                        builds[detailed_key].append(fallback_item)
        
        # Process alternative builds with detailed item data
        if 'alternative_builds' in builds:
            for alt_build in builds['alternative_builds']:
                if isinstance(alt_build, dict) and 'core_items' in alt_build:
                    alt_build['core_items_detailed'] = []
                    for item_name in alt_build['core_items']:
                        if item_name in enhanced_items:
                            alt_build['core_items_detailed'].append(enhanced_items[item_name])
                        else:
                            fallback_item = self._create_fallback_item_data(
                                item_name, 
                                "Item data could not be fetched for alternative build"
                            )
                            alt_build['core_items_detailed'].append(fallback_item)
        
        # Process example build with detailed data
        if 'example_build' in builds:
            builds['example_build_detailed'] = []
            for item_name in builds['example_build']:
                if item_name in enhanced_items:
                    builds['example_build_detailed'].append(enhanced_items[item_name])
                else:
                    fallback_item = {
                        "name": item_name,
                        "stats": {},
                        "cost": 0,
                        "passive": "",
                        "active": "",
                        "description": f"Item data for {item_name} could not be fetched",
                        "category": "unknown",
                        "tier": "Unknown"
                    }
                    builds['example_build_detailed'].append(fallback_item)
        
        return builds
    
    def _extract_item_names_from_builds(self, champion_data):
        """Extract item names from champion build data with comprehensive coverage"""
        item_names = set()
        
        if 'builds' not in champion_data:
            return item_names
        
        builds = champion_data['builds']
        
        # Extract from main build categories
        main_categories = ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build', 'enchants']
        for category in main_categories:
            if category in builds and isinstance(builds[category], list):
                for item in builds[category]:
                    if item and isinstance(item, str) and item.strip():
                        # Clean and normalize item names
                        clean_item_name = item.strip()
                        # Remove any prefixes or suffixes that might interfere with scraping
                        clean_item_name = re.sub(r'^\d+\.\s*', '', clean_item_name)  # Remove numbering
                        clean_item_name = re.sub(r'\s*\([^)]*\)$', '', clean_item_name)  # Remove trailing parentheses
                        if clean_item_name:
                            item_names.add(clean_item_name)
        
        # Extract from alternative builds
        if 'alternative_builds' in builds and isinstance(builds['alternative_builds'], list):
            for alt_build in builds['alternative_builds']:
                if isinstance(alt_build, dict):
                    for key, value in alt_build.items():
                        if key.endswith('_items') and isinstance(value, list):
                            for item in value:
                                if item and isinstance(item, str) and item.strip():
                                    clean_item_name = item.strip()
                                    clean_item_name = re.sub(r'^\d+\.\s*', '', clean_item_name)
                                    clean_item_name = re.sub(r'\s*\([^)]*\)$', '', clean_item_name)
                                    if clean_item_name:
                                        item_names.add(clean_item_name)
        
        # Extract from lane-specific builds
        if 'lane_specific' in builds and isinstance(builds['lane_specific'], dict):
            for lane_data in builds['lane_specific'].values():
                if isinstance(lane_data, dict):
                    for key, value in lane_data.items():
                        if key.endswith('_items') and isinstance(value, list):
                            for item in value:
                                if item and isinstance(item, str) and item.strip():
                                    clean_item_name = item.strip()
                                    clean_item_name = re.sub(r'^\d+\.\s*', '', clean_item_name)
                                    clean_item_name = re.sub(r'\s*\([^)]*\)$', '', clean_item_name)
                                    if clean_item_name:
                                        item_names.add(clean_item_name)
        
        # Extract from any other build-related structures
        for key, value in builds.items():
            if ('build' in key.lower() or 'item' in key.lower()) and isinstance(value, list):
                for item in value:
                    if item and isinstance(item, str) and item.strip():
                        clean_item_name = item.strip()
                        clean_item_name = re.sub(r'^\d+\.\s*', '', clean_item_name)
                        clean_item_name = re.sub(r'\s*\([^)]*\)$', '', clean_item_name)
                        if clean_item_name:
                            item_names.add(clean_item_name)
        
        print(f"        Extracted {len(item_names)} unique item names from champion builds")
        return item_names
    
    def _fetch_current_stats_and_costs(self, item_names):
        """Fetch current stats and costs for each build item with enhanced processing"""
        item_data_map = {}
        
        print(f"      Fetching real-time data for {len(item_names)} unique items...")
        
        for i, item_name in enumerate(item_names, 1):
            try:
                print(f"        [{i}/{len(item_names)}] Fetching: {item_name}")
                
                # Get real-time item data
                item_data = self._get_real_time_item_data(item_name)
                
                if item_data:
                    # Ensure we have the essential fields and process the data
                    processed_data = {
                        "name": item_data.get("name", item_name),
                        "stats": self._process_item_stats(item_data.get("stats", {})),
                        "cost": self._validate_item_cost(item_data.get("cost", 0)),
                        "passive": item_data.get("passive", ""),
                        "active": item_data.get("active", ""),
                        "description": item_data.get("description", ""),
                        "category": item_data.get("category", "unknown"),
                        "tier": item_data.get("tier", "Unknown"),
                        "tips": item_data.get("tips", []),
                        # Add metadata for tracking
                        "scraped_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "source": "wr-meta.com"
                    }
                    
                    item_data_map[item_name] = processed_data
                    
                    # Display detailed stats information
                    stats_summary = self._format_stats_summary(processed_data['stats'])
                    print(f"          ✓ Cost: {processed_data['cost']}, Stats: {stats_summary}")
                else:
                    print(f"          ✗ Failed to fetch data")
                    
            except Exception as e:
                print(f"          ✗ Error: {e}")
                # Continue processing other items even if one fails
                continue
        
        print(f"      Successfully fetched data for {len(item_data_map)} items")
        return item_data_map
    
    def _process_item_stats(self, stats):
        """Process and validate item stats data"""
        if not isinstance(stats, dict):
            return {}
        
        processed_stats = {}
        for stat_name, stat_value in stats.items():
            if stat_value is not None and stat_value != 0:
                # Ensure consistent stat format
                if isinstance(stat_value, dict):
                    processed_stats[stat_name] = stat_value
                else:
                    processed_stats[stat_name] = {
                        "value": stat_value,
                        "type": "flat"
                    }
        
        return processed_stats
    
    def _ensure_current_stats_and_costs(self, item_data, item_name):
        """Ensure we have current stats and costs for each build item"""
        # Validate and process stats
        if 'stats' in item_data:
            item_data['stats'] = self._process_item_stats(item_data['stats'])
        else:
            item_data['stats'] = {}
        
        # Validate and process cost
        if 'cost' in item_data:
            item_data['cost'] = self._validate_item_cost(item_data['cost'])
        else:
            item_data['cost'] = 0
        
        # Ensure essential fields are present
        essential_fields = ['name', 'passive', 'active', 'description', 'category', 'tier', 'tips']
        for field in essential_fields:
            if field not in item_data:
                if field == 'name':
                    item_data[field] = item_name
                elif field == 'tips':
                    item_data[field] = []
                else:
                    item_data[field] = ""
        
        # Add validation metadata
        item_data['validation'] = {
            'stats_processed': bool(item_data['stats']),
            'cost_validated': item_data['cost'] > 0,
            'essential_fields_complete': all(field in item_data for field in essential_fields),
            'validation_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return item_data
    
    def _validate_item_cost(self, cost):
        """Validate and clean item cost data"""
        if isinstance(cost, (int, float)) and cost >= 0:
            return int(cost)
        elif isinstance(cost, str):
            # Try to extract numeric cost from string
            cost_match = re.search(r'(\d+)', cost)
            if cost_match:
                return int(cost_match.group(1))
        return 0
    
    def _format_stats_summary(self, stats):
        """Format stats for display summary"""
        if not stats:
            return "None"
        
        summary_parts = []
        for stat_name, stat_data in stats.items():
            if isinstance(stat_data, dict) and 'value' in stat_data:
                value = stat_data['value']
                if isinstance(value, str) and '%' in value:
                    summary_parts.append(f"{stat_name}: {value}")
                else:
                    summary_parts.append(f"{stat_name}: {value}")
            else:
                summary_parts.append(f"{stat_name}: {stat_data}")
        
        return ", ".join(summary_parts[:3]) + ("..." if len(summary_parts) > 3 else "")
    
    def _validate_champion_match(self, champion_name, expected_slug):
        """Validate that the extracted champion name matches the expected slug"""
        # Normalize both for comparison
        normalized_name = champion_name.lower().replace("'", "").replace(" ", "").replace(".", "")
        normalized_slug = expected_slug.lower().replace("-", "").replace("'", "")
        
        # Check if they match or if one contains the other
        return (normalized_name == normalized_slug or 
                normalized_name in normalized_slug or 
                normalized_slug in normalized_name or
                len(set(normalized_name) & set(normalized_slug)) > len(normalized_name) * 0.6)
    
    def generate_champion_list(self):
        """Generate a list of all available champions"""
        champion_list = []
        
        for champion_name, data in self.champions_data.items():
            champion_info = {
                'id': data['champion']['id'],
                'name': data['champion']['name'],
                'title': data['champion']['title'],
                'role': data['champion']['role'],
                'tier': data['meta']['tier'],
                'image': data['champion']['image']
            }
            champion_list.append(champion_info)
        
        # Sort by name
        champion_list.sort(key=lambda x: x['name'])
        
        # Save champion list
        with open('scraped_champions/champion_list.json', 'w', encoding='utf-8') as f:
            json.dump(champion_list, f, indent=2, ensure_ascii=False)
        
        print(f" Champion list saved with {len(champion_list)} champions")
        return champion_list

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch scrape all Wild Rift champions from WR-META')
    parser.add_argument('--max', type=int, help='Maximum number of champions to scrape (for testing)')
    parser.add_argument('--discover-only', action='store_true', help='Only discover champion URLs, don\'t scrape')
    
    args = parser.parse_args()
    
    scraper = BatchChampionScraper()
    
    try:
        # Discover all champion URLs
        champion_urls = scraper.discover_all_champions()
        
        if args.discover_only:
            print("\n Discovered Champion URLs:")
            for url in champion_urls:
                print(f"   {url}")
            return
        
        # Scrape all champions
        champions_data = scraper.scrape_all_champions(champion_urls, args.max)
        
        # Generate champion list
        champion_list = scraper.generate_champion_list()
        
        print(f"\n Batch scraping completed!")
        print(f"   Total champions: {len(champions_data)}")
        print(f"   Files created: {len(champions_data) + 2}")  # +2 for master file and champion list
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"\n Error during batch scraping: {e}")

if __name__ == "__main__":
    main()