#!/usr/bin/env python3
"""
Check what bildtitle2 sections actually exist
"""

import requests
from bs4 import BeautifulSoup

def check_sections():
    url = "https://wr-meta.com/528-ambessa.html"
    
    print(f"Fetching: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("\n=== ALL BILDTITLE2 SECTIONS ===")
    bildtitle2_headers = soup.find_all('div', class_='bildtitle2')
    
    for i, header in enumerate(bildtitle2_headers):
        header_text = header.get_text().strip()
        print(f"{i+1}. '{header_text}'")

if __name__ == "__main__":
    check_sections()
