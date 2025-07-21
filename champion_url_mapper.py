#!/usr/bin/env python3
"""
Champion URL Mapper and Discovery Utility for WR-META.com
Discovers and validates champion URLs, provides mapping corrections
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup

class ChampionURLMapper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://wr-meta.com"
        
        # Known corrections for problematic champions
        self.manual_corrections = {
            "kennen": "58-kennen",
            "leona": "59-leona", 
            "malphite": "71-malphite",
            "miss-fortune": "378-miss-fortune",
            "master-yi": "377-master-yi",
            "kha-zix": "371-kha-zix",
            "lee-sin": "372-lee-sin",
            "jarvan-iv": "361-jarvan-iv",
            "aurelion-sol": "339-aurelion-sol",
            "dr-mundo": "348-dr-mundo",
            "twisted-fate": "398-twisted-fate",
            "kai-sa": "366-kai-sa"
        }
    
    def discover_champion_urls(self):
        """Discover all real champion URLs from the website"""
        print("Discovering champion URLs from WR-META...")
        
        discovery_urls = [
            "https://wr-meta.com/",
            "https://wr-meta.com/meta/",
            "https://wr-meta.com/fighters/",
            "https://wr-meta.com/assassins/",
            "https://wr-meta.com/mages/",
            "https://wr-meta.com/marksmans/",
            "https://wr-meta.com/supports/",
            "https://wr-meta.com/tanks/"
        ]
        
        champion_urls = set()
        
        for url in discovery_urls:
            try:
                print(f"   Checking: {url}")
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    # Look for champion links - they can be full URLs or relative
                    # Pattern for full URLs: https://wr-meta.com/123-champion.html
                    full_url_links = re.findall(r'href="(https://wr-meta\.com/(\d+)-([a-z0-9-]+)\.html)"', response.text, re.IGNORECASE)
                    for full_url, champion_id, slug in full_url_links:
                        champion_urls.add(full_url.lower())
                    
                    # Pattern for relative URLs: /123-champion.html
                    relative_links = re.findall(r'href="(/(\d+)-([a-z0-9-]+)\.html)"', response.text, re.IGNORECASE)
                    for relative_link, champion_id, slug in relative_links:
                        full_url = f"{self.base_url}{relative_link.lower()}"
                        champion_urls.add(full_url)
                        
                time.sleep(1)  # Be respectful to the server
                
            except Exception as e:
                print(f"   Warning: Error checking {url}: {e}")
                continue
        
        print(f"Discovered {len(champion_urls)} champion URLs")
        return sorted(list(champion_urls))
    
    def validate_url(self, url):
        """Validate if a champion URL is accessible"""
        try:
            response = self.session.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def search_champion_url(self, champion_name):
        """Search for a champion's correct URL"""
        search_slug = champion_name.lower().replace(" ", "-").replace("'", "")
        
        # Try manual corrections first
        if search_slug in self.manual_corrections:
            corrected_url = f"{self.base_url}/{self.manual_corrections[search_slug]}.html"
            if self.validate_url(corrected_url):
                return corrected_url
        
        # Try search on the website
        try:
            search_url = f"{self.base_url}/?s={champion_name}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                # Look for champion links in search results
                champion_links = re.findall(r'href="(/(\d+)-([a-z0-9-]+)\.html)"', response.text, re.IGNORECASE)
                
                for full_link, champion_id, slug in champion_links:
                    if search_slug in slug or slug in search_slug:
                        candidate_url = f"{self.base_url}{full_link.lower()}"
                        if self.validate_url(candidate_url):
                            return candidate_url
        except Exception as e:
            print(f"   Warning: Search failed for {champion_name}: {e}")
        
        return None
    
    def brute_force_search(self, champion_name, max_id=600):
        """Brute force search for champion URL by trying different IDs"""
        search_slug = champion_name.lower().replace(" ", "-").replace("'", "")
        
        print(f"   Brute force searching for {champion_name}...")
        
        # Try common ID ranges first (most champions are in these ranges)
        priority_ranges = [
            range(1, 100),      # Early champions
            range(300, 410),    # Main champion range
            range(50, 200),     # Mid-range champions
            range(200, 300),    # Extended range
            range(410, max_id)  # Latest champions
        ]
        
        for id_range in priority_ranges:
            for champion_id in id_range:
                test_url = f"{self.base_url}/{champion_id}-{search_slug}.html"
                if self.validate_url(test_url):
                    print(f"   Found: {test_url}")
                    return test_url
                
                # Also try without hyphens for compound names
                if "-" in search_slug:
                    alt_slug = search_slug.replace("-", "")
                    alt_url = f"{self.base_url}/{champion_id}-{alt_slug}.html"
                    if self.validate_url(alt_url):
                        print(f"   Found: {alt_url}")
                        return alt_url
        
        return None
    
    def create_champion_mapping(self, discovered_urls):
        """Create a mapping of champion names to URLs"""
        mapping = {}
        
        for url in discovered_urls:
            # Extract champion name from URL
            url_parts = url.split('/')[-1].replace('.html', '').split('-', 1)
            if len(url_parts) == 2:
                champion_id, slug = url_parts
                champion_name = slug.replace('-', ' ').title()
                mapping[champion_name.lower()] = url
        
        return mapping
    
    def save_mapping(self, mapping, filename="champion_url_mapping.json"):
        """Save champion URL mapping to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        print(f"Champion URL mapping saved to {filename}")

def main():
    mapper = ChampionURLMapper()
    
    try:
        # Discover all champion URLs
        discovered_urls = mapper.discover_champion_urls()
        
        # Validate URLs (sample first 20 for speed)
        print(f"\nValidating discovered URLs (checking first 20 of {len(discovered_urls)})...")
        valid_urls = []
        invalid_urls = []
        
        # Check first 20 URLs for validation, assume rest are valid if pattern holds
        sample_urls = discovered_urls[:20]
        for i, url in enumerate(sample_urls):
            print(f"   Validating {i+1}/20: {url.split('/')[-1]}")
            if mapper.validate_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        # If most of the sample is valid, assume the rest are too
        if len(valid_urls) > len(invalid_urls):
            print(f"   Sample validation successful, assuming remaining {len(discovered_urls) - 20} URLs are valid")
            valid_urls.extend(discovered_urls[20:])
        else:
            print("   Sample validation failed, checking all URLs...")
            for url in discovered_urls[20:]:
                if mapper.validate_url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
        
        print(f"Valid URLs: {len(valid_urls)}")
        print(f"Invalid URLs: {len(invalid_urls)}")
        
        if invalid_urls:
            print("\nInvalid URLs found:")
            for url in invalid_urls:
                print(f"   {url}")
        
        # Create and save mapping
        mapping = mapper.create_champion_mapping(valid_urls)
        mapper.save_mapping(mapping)
        
        print(f"\nChampion URL discovery completed!")
        print(f"   Total valid URLs: {len(valid_urls)}")
        print(f"   Mapping created with {len(mapping)} champions")
        
        return valid_urls, mapping
        
    except Exception as e:
        print(f"Error during URL discovery: {e}")
        return [], {}

if __name__ == "__main__":
    main()
