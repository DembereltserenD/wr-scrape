#!/usr/bin/env python3
"""
Selenium-Enhanced Champion Data Scraper for WR-META.com
Handles dynamic content and lane-specific builds using browser automation.

Usage: python selenium_enhanced_scraper.py <champion-url>
Example: python selenium_enhanced_scraper.py https://wr-meta.com/58-kennen.html
"""

import time
import json
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from enhanced_scrape_champion import WRMetaScraper

class SeleniumWRMetaScraper(WRMetaScraper):
    def __init__(self, headless=True):
        super().__init__()
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_champion_data_selenium(self, champion_url):
        """Scrape champion data using Selenium for dynamic content"""
        try:
            self.setup_driver()
            print(f"Loading page with Selenium: {champion_url}")
            
            self.driver.get(champion_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait a bit more for dynamic content
            time.sleep(3)
            
            # Get the page source after JavaScript execution
            page_source = self.driver.page_source
            
            # Detect available lanes
            lane_builds = self.extract_lane_specific_builds(page_source)
            
            # If we found multiple lanes, extract each one
            if len(lane_builds) > 1:
                print(f"Found {len(lane_builds)} different lane builds")
                return self.process_multi_lane_data(champion_url, lane_builds)
            else:
                print("Single lane detected, using standard extraction")
                return self.scrape_champion_data(champion_url)
                
        except Exception as e:
            print(f"Selenium scraping failed: {e}")
            print("Falling back to standard scraping...")
            return self.scrape_champion_data(champion_url)
        finally:
            self.close_driver()
    
    def extract_lane_specific_builds(self, page_source):
        """Extract lane-specific builds from the page"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        lane_builds = {}
        
        # Look for lane selector elements
        lane_selectors = soup.find_all('span', class_='tabs-fg-sel')
        if not lane_selectors:
            # Try alternative selectors
            lane_selectors = soup.find_all('div', class_='tabs-fg-sel')
        
        # Look for lane icons to identify available lanes
        solo_icons = soup.find_all('i', class_='demo-icon solo-lineicon-')
        mid_icons = soup.find_all('i', class_='demo-icon mid-lineicon-')
        jungle_icons = soup.find_all('i', class_='demo-icon jungle-lineicon-')
        
        detected_lanes = []
        if solo_icons:
            detected_lanes.append('Solo Baron')
        if mid_icons:
            detected_lanes.append('Mid Lane')
        if jungle_icons:
            detected_lanes.append('Jungle')
        
        print(f"Detected lanes: {detected_lanes}")
        
        # If we have multiple lanes, try to extract builds for each
        if len(detected_lanes) > 1:
            for lane in detected_lanes:
                build_data = self.extract_build_for_lane(soup, lane)
                if build_data:
                    lane_builds[lane] = build_data
        
        return lane_builds
    
    def extract_build_for_lane(self, soup, lane_name):
        """Extract build data for a specific lane"""
        # Look for sections that contain the lane name
        lane_sections = []
        
        # Search for headings that mention the lane
        if lane_name == 'Solo Baron':
            lane_sections = soup.find_all(['h2', 'h3'], string=re.compile(r'Solo Baron.*Build', re.I))
        elif lane_name == 'Mid Lane':
            lane_sections = soup.find_all(['h2', 'h3'], string=re.compile(r'Mid.*Build', re.I))
        elif lane_name == 'Jungle':
            lane_sections = soup.find_all(['h2', 'h3'], string=re.compile(r'Jungle.*Build', re.I))
        
        if not lane_sections:
            return None
        
        # Extract build data from the section
        build_data = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'example_build': [],
            'enchants': []
        }
        
        # Find the parent container for this lane's build
        for section in lane_sections:
            parent_container = section.find_parent(['div', 'section'])
            if parent_container:
                # Extract items from this container
                build_data = self.extract_items_from_container(parent_container)
                break
        
        return build_data
    
    def extract_items_from_container(self, container):
        """Extract items from a specific container"""
        build_data = {
            'starting_items': [],
            'core_items': [],
            'boots': [],
            'situational_items': [],
            'example_build': [],
            'enchants': []
        }
        
        # Look for different sections within the container
        sections = {
            'starting_items': container.find_all(string=re.compile(r'Start', re.I)),
            'core_items': container.find_all(string=re.compile(r'Core', re.I)),
            'boots': container.find_all(string=re.compile(r'Boots', re.I)),
            'situational_items': container.find_all(string=re.compile(r'Situational', re.I)),
            'example_build': container.find_all(string=re.compile(r'Example', re.I))
        }
        
        for category, section_elements in sections.items():
            items = []
            for element in section_elements:
                if hasattr(element, 'parent'):
                    parent = element.parent
                    # Find item images in this section
                    item_imgs = parent.find_all('img', alt=True)
                    for img in item_imgs:
                        alt_text = img.get('alt', '').strip()
                        if self._is_item_image(img, alt_text):
                            item_name = self._clean_item_name(alt_text)
                            if item_name and item_name not in items:
                                items.append(item_name)
            
            build_data[category] = items[:6]  # Limit to 6 items per category
        
        return build_data
    
    def process_multi_lane_data(self, champion_url, lane_builds):
        """Process and structure multi-lane champion data"""
        # Get base champion data using standard scraping
        base_data = self.scrape_champion_data(champion_url)
        
        # Update the builds section with lane-specific data
        if lane_builds:
            base_data['builds']['lane_specific'] = lane_builds
            
            # Update the main lanes list
            base_data['champion']['lanes'] = list(lane_builds.keys())
            
            # Set the primary build to the first lane's build
            first_lane = list(lane_builds.keys())[0]
            if first_lane in lane_builds:
                for category in ['starting_items', 'core_items', 'boots', 'situational_items', 'example_build', 'enchants']:
                    if category in lane_builds[first_lane]:
                        base_data['builds'][category] = lane_builds[first_lane][category]
        
        return base_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python selenium_enhanced_scraper.py <champion-url>")
        print("Example: python selenium_enhanced_scraper.py https://wr-meta.com/58-kennen.html")
        sys.exit(1)
    
    champion_url = sys.argv[1]
    
    try:
        scraper = SeleniumWRMetaScraper(headless=True)
        champion_data = scraper.scrape_champion_data_selenium(champion_url)
        
        # Extract champion name for filename
        champion_name = champion_data['champion']['name'].lower().replace(' ', '_').replace("'", "")
        filename = f"{champion_name}_selenium_data.json"
        
        # Save the data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(champion_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to: {filename}")
        print(f"Champion: {champion_data['champion']['name']}")
        print(f"Lanes: {champion_data['champion']['lanes']}")
        
        if 'lane_specific' in champion_data['builds']:
            print(f"Lane-specific builds found: {list(champion_data['builds']['lane_specific'].keys())}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
