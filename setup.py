#!/usr/bin/env python3
"""
Setup script for Wild Rift Champion Scraping Toolkit
"""

import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        sys.exit(1)

def test_installation():
    """Test if all packages are working"""
    print("🧪 Testing installation...")
    try:
        import requests
        import bs4
        print("✅ All packages working correctly!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)

def main():
    print("🚀 Wild Rift Champion Scraping Toolkit Setup")
    print("=" * 50)
    
    install_requirements()
    test_installation()
    
    print("\n🎉 Setup completed successfully!")
    print("\nUsage:")
    print("  Single champion: python enhanced_scrape_champion.py <url>")
    print("  All champions:   python batch_scrape_all_champions.py")
    print("  Documentation:   See SCRAPING_GUIDE.md")

if __name__ == "__main__":
    main()
