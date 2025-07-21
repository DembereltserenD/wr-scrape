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
from enhanced_scrape_champion import WRMetaScraper
from champion_url_mapper import ChampionURLMapper
from real_time_item_scraper import RealTimeItemScraper

class BatchChampionScraper:
    def __init__(self):
        self.scraper = WRMetaScraper()
        self.url_mapper = ChampionURLMapper()
        self.base_url = "https://wr-meta.com"
        self.champions_data = {}
        self.failed_urls = []
        self.corrected_urls = {}
        
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
        
        return self.champions_data
    
    def _scrape_with_retry(self, url, max_retries=3):
        """Scrape champion data with smart retry and URL correction"""
        
        for attempt in range(max_retries):
            try:
                # Try main scrape
                champion_data = self.scraper.scrape_champion_data(url)
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
