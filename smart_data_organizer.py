#!/usr/bin/env python3
"""
Smart Data Organizer for Wild Rift
Integrates real-time data scraping with batch processing
"""

import os
import json
import time
import subprocess
import logging
import re
from pathlib import Path
from real_time_item_scraper import RealTimeItemScraper

class SmartDataOrganizer:
    def __init__(self):
        self.item_scraper = RealTimeItemScraper()
        
        # Enhanced directory structure management
        self.items_dir = Path("items")
        self.runes_dir = Path("runes")
        self.champions_dir = Path("scraped_champions")  # Consolidated to one champions directory
        self.logs_dir = Path("logs")
        
        # Known Wild Rift champion names to filter out from item extraction
        self.champion_names = {
            'Ahri', 'Akali', 'Akshan', 'Alistar', 'Ammu', 'Anivia', 'Annie', 'Ashe', 'Aurelion Sol',
            'Azir', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Corki', 'Darius', 'Diana',
            'Dr. Mundo', 'Draven', 'Ekko', 'Evelynn', 'Ezreal', 'Fiora', 'Fizz', 'Galio', 'Garen',
            'Gragas', 'Graves', 'Irelia', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx',
            'Kai\'Sa', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kennen', 'Kha\'Zix',
            'Lee Sin', 'Leona', 'Lulu', 'Lux', 'Malphite', 'Master Yi', 'Miss Fortune', 'Nami',
            'Nasus', 'Nautilus', 'Olaf', 'Orianna', 'Pantheon', 'Pyke', 'Rakan', 'Rammus', 'Renekton',
            'Riven', 'Seraphine', 'Shyvana', 'Singed', 'Sona', 'Soraka', 'Teemo', 'Thresh', 'Tristana',
            'Tryndamere', 'Twisted Fate', 'Varus', 'Vayne', 'Veigar', 'Vi', 'Wukong', 'Xayah',
            'Yasuo', 'Yone', 'Yuumi', 'Zed', 'Ziggs', 'Zilean', 'Zyra', 'Senna', 'Lucian', 'Morgana',
            'Janna', 'Sett', 'Akshan', 'Vex', 'Jayce', 'Caitlyn', 'Jinx', 'Vi', 'Ekko', 'Heimerdinger',
            'Warwick', 'Singed', 'Dr. Mundo', 'Mundo', 'Cassiopeia', 'Malzahar', 'Vel\'Koz', 'Xerath',
            'Azir', 'Taliyah', 'Aurelion Sol', 'Kled', 'Ivern', 'Camille', 'Xayah', 'Rakan', 'Kayn',
            'Ornn', 'Zoe', 'Pyke', 'Neeko', 'Sylas', 'Yuumi', 'Qiyana', 'Senna', 'Aphelios', 'Sett',
            'Lillia', 'Yone', 'Samira', 'Seraphine', 'Rell', 'Viego', 'Gwen', 'Akshan', 'Vex',
            'Zeri', 'Renata Glasc', 'Bel\'veth', 'Nilah', 'K\'Sante', 'Briar', 'Naafiri', 'Smolder',
            'Aurora', 'Ambessa', 'Mel', 'Warwick', 'Swain', 'Tahm Kench', 'Udyr', 'Leblanc', 'Quinn',
            'Rek\'sai', 'Nidalee', 'Illaoi', 'Renata Glasc', 'Malzahar', 'Taliyah', 'Karthus', 'Xerath',
            'Neeko', 'Cassiopeia', 'Dr. Mundo', 'Smolder', 'Gangplank', 'K\'sante', 'Qiyana', 'Ivern',
            'Naafiri', 'Elise', 'Shaco', 'Taric', 'Yorick', 'Bel\'veth', 'Cho\'gath', 'Briar', 'Azir',
            'Skarner', 'Trundle', 'Yunara', 'Sylas', 'Hwei', 'Sejuani', 'Kog\'maw'
        }
        
        # Create comprehensive directory structure
        self._setup_directory_structure()
        
        # Initialize logging
        self._setup_logging()
        
        # Track processing statistics
        self.stats = {
            'champions_processed': 0,
            'items_updated': 0,
            'validation_issues': 0,
            'errors': []
        }
    
    def _setup_directory_structure(self):
        """Create and manage directory structure for items, runes, and champions"""
        directories = [
            self.items_dir,
            self.runes_dir, 
            self.champions_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            
        # Create subdirectories for better organization
        (self.logs_dir / "errors").mkdir(exist_ok=True)
        (self.logs_dir / "validation").mkdir(exist_ok=True)
        
        print(f"Directory structure initialized:")
        for directory in directories:
            print(f"  ✓ {directory}")
    
    def _setup_logging(self):
        """Setup logging for the data organizer"""
        log_file = self.logs_dir / "smart_organizer.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_batch_scrape_champions(self, max_champions=None):
        """Enhanced batch champion scraper with progress reporting and error handling"""
        self.logger.info(f"Starting batch champion scraping (max_champions: {max_champions})")
        print("📊 Starting batch champion scraping with real-time data...")
        
        cmd = ["python", "batch_scrape_all_champions.py"]
        if max_champions:
            cmd.extend(["--max", str(max_champions)])
        
        try:
            # Run with real-time output capture
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress and capture output
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    output_lines.append(output.strip())
                    # Show progress for important lines
                    if any(keyword in output.lower() for keyword in ['processing', 'scraping', 'completed', 'error', 'failed']):
                        print(f"  {output.strip()}")
            
            return_code = process.poll()
            
            if return_code == 0:
                self.logger.info("Batch champion scraping completed successfully")
                print("✅ Batch champion scraping completed successfully")
                
                # Try to extract statistics from output
                champions_processed = 0
                for line in output_lines:
                    if "successfully scraped" in line.lower():
                        match = re.search(r'(\d+)', line)
                        if match:
                            champions_processed = int(match.group(1))
                            break
                
                self.stats['champions_processed'] = champions_processed
                return True
            else:
                error_msg = f"Batch champion scraper failed with return code {return_code}"
                self.logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                print(f"❌ {error_msg}")
                
                # Log error output
                error_output = '\n'.join(output_lines[-10:])  # Last 10 lines
                self.logger.error(f"Error output: {error_output}")
                
                return False
                
        except FileNotFoundError:
            error_msg = "batch_scrape_all_champions.py not found"
            self.logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
        except Exception as e:
            error_msg = f"Exception running batch champion scraper: {e}"
            self.logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def run_sequential_workflow(self, max_champions=None, continue_on_failure=True):
        """
        Enhanced sequential execution with comprehensive progress reporting and error aggregation
        Implements continuation on partial failures with detailed final reporting
        """
        workflow_start_time = time.time()
        
        self.logger.info("=" * 80)
        self.logger.info("STARTING SEQUENTIAL WORKFLOW ORCHESTRATION")
        self.logger.info("=" * 80)
        
        print("🚀 Starting comprehensive Wild Rift data workflow orchestration...")
        print(f"📋 Configuration: max_champions={max_champions}, continue_on_failure={continue_on_failure}")
        
        # Initialize workflow tracking
        workflow_steps = [
            {
                'name': 'Champion Discovery & Scraping',
                'function': lambda: self.run_batch_scrape_champions(max_champions),
                'critical': True,
                'completed': False,
                'success': False,
                'duration': 0,
                'errors': []
            },
            {
                'name': 'Item Data Update',
                'function': self.update_item_data,
                'critical': False,
                'completed': False,
                'success': False,
                'duration': 0,
                'errors': []
            },
            {
                'name': 'Data Consistency Validation',
                'function': self.validate_data_consistency,
                'critical': False,
                'completed': False,
                'success': False,
                'duration': 0,
                'errors': []
            }
        ]
        
        # Execute workflow steps
        overall_success = True
        completed_steps = 0
        
        for i, step in enumerate(workflow_steps, 1):
            step_start_time = time.time()
            
            print(f"\n{'='*60}")
            print(f"📋 Step {i}/{len(workflow_steps)}: {step['name']}")
            print(f"{'='*60}")
            
            self.logger.info(f"Starting workflow step {i}: {step['name']}")
            
            try:
                # Execute the step function
                if step['name'] == 'Data Consistency Validation':
                    result = step['function']()
                    step['success'] = len(result) == 0  # Success if no issues found
                    if not step['success']:
                        step['errors'] = result[:5]  # Store first 5 issues
                else:
                    result = step['function']()
                    step['success'] = bool(result)
                
                step['completed'] = True
                step['duration'] = time.time() - step_start_time
                
                if step['success']:
                    completed_steps += 1
                    self.logger.info(f"Step {i} completed successfully in {step['duration']:.1f}s")
                    print(f"✅ Step {i} completed successfully ({step['duration']:.1f}s)")
                else:
                    self.logger.warning(f"Step {i} completed with issues in {step['duration']:.1f}s")
                    print(f"⚠️ Step {i} completed with issues ({step['duration']:.1f}s)")
                    
                    if step['critical'] and not continue_on_failure:
                        self.logger.error(f"Critical step {i} failed, stopping workflow")
                        print(f"❌ Critical step failed, stopping workflow")
                        overall_success = False
                        break
                
            except Exception as e:
                step['completed'] = True
                step['success'] = False
                step['duration'] = time.time() - step_start_time
                error_msg = f"Step {i} failed with exception: {e}"
                step['errors'].append(error_msg)
                
                self.logger.error(f"Step {i} failed: {e}")
                self.stats['errors'].append(error_msg)
                print(f"❌ Step {i} failed: {e}")
                
                if step['critical'] and not continue_on_failure:
                    self.logger.error(f"Critical step {i} failed, stopping workflow")
                    print(f"❌ Critical step failed, stopping workflow")
                    overall_success = False
                    break
            
            # Brief pause between steps
            if i < len(workflow_steps):
                time.sleep(1)
        
        # Generate comprehensive final report
        self._generate_workflow_report(workflow_steps, workflow_start_time, overall_success, completed_steps)
        
        return overall_success and completed_steps == len(workflow_steps)
    
    def _generate_workflow_report(self, workflow_steps, start_time, overall_success, completed_steps):
        """Generate comprehensive workflow execution report"""
        total_duration = time.time() - start_time
        
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE WORKFLOW EXECUTION REPORT")
        print(f"{'='*80}")
        
        # Overall statistics
        print(f"⏱️  Total execution time: {total_duration:.1f} seconds")
        print(f"✅ Completed steps: {completed_steps}/{len(workflow_steps)}")
        print(f"📊 Overall success: {'✅ YES' if overall_success else '❌ NO'}")
        
        # Step-by-step breakdown
        print(f"\n📋 Step-by-Step Breakdown:")
        for i, step in enumerate(workflow_steps, 1):
            status_icon = "✅" if step['success'] else "❌" if step['completed'] else "⏸️"
            print(f"  {status_icon} Step {i}: {step['name']}")
            print(f"     Duration: {step['duration']:.1f}s")
            print(f"     Status: {'Success' if step['success'] else 'Failed' if step['completed'] else 'Not Started'}")
            
            if step['errors']:
                print(f"     Errors: {len(step['errors'])} issues")
                for error in step['errors'][:2]:  # Show first 2 errors
                    print(f"       • {error}")
                if len(step['errors']) > 2:
                    print(f"       ... and {len(step['errors']) - 2} more")
        
        # Data statistics
        print(f"\n📈 Data Processing Statistics:")
        print(f"  🏆 Champions processed: {self.stats['champions_processed']}")
        print(f"  📦 Items updated: {self.stats['items_updated']}")
        print(f"  ⚠️  Validation issues: {self.stats['validation_issues']}")
        print(f"  ❌ Total errors: {len(self.stats['errors'])}")
        
        # Error summary
        if self.stats['errors']:
            print(f"\n🔍 Error Summary:")
            error_categories = {}
            for error in self.stats['errors']:
                category = error.split(':')[0] if ':' in error else 'General'
                error_categories[category] = error_categories.get(category, 0) + 1
            
            for category, count in error_categories.items():
                print(f"  • {category}: {count} errors")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if not overall_success:
            print("  • Review error logs for specific failure details")
            print("  • Consider running individual steps separately")
            print("  • Check network connectivity and website availability")
        
        if self.stats['validation_issues'] > 0:
            print("  • Review validation report for data consistency issues")
            print("  • Consider running data fixing utilities")
        
        if self.stats['items_updated'] == 0:
            print("  • Check item scraper functionality")
            print("  • Verify champion build data contains item references")
        
        # Success message
        if overall_success:
            print(f"\n🎉 Workflow completed successfully!")
            print("   All data has been updated and validated.")
        else:
            print(f"\n⚠️  Workflow completed with issues.")
            print("   Check logs and consider re-running failed steps.")
        
        # Log comprehensive report
        self.logger.info("=" * 80)
        self.logger.info("WORKFLOW EXECUTION COMPLETED")
        self.logger.info(f"Total duration: {total_duration:.1f}s")
        self.logger.info(f"Completed steps: {completed_steps}/{len(workflow_steps)}")
        self.logger.info(f"Overall success: {overall_success}")
        self.logger.info(f"Champions processed: {self.stats['champions_processed']}")
        self.logger.info(f"Items updated: {self.stats['items_updated']}")
        self.logger.info(f"Validation issues: {self.stats['validation_issues']}")
        self.logger.info(f"Total errors: {len(self.stats['errors'])}")
        self.logger.info("=" * 80)
    
    def _get_champion_names_filter(self):
        """Get comprehensive list of champion names to filter out from item extraction"""
        champion_names = {
            # Current Wild Rift Champions (as of 2024)
            "Ahri", "Akali", "Akshan", "Alistar", "Ammu", "Anivia", "Annie", "Ashe", "Aurelion Sol", "Azir",
            "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille", "Corki", "Darius", "Diana", "Dr. Mundo",
            "Draven", "Ekko", "Evelynn", "Ezreal", "Fiora", "Fizz", "Galio", "Garen", "Gragas", "Graves",
            "Irelia", "Janna", "Jarvan IV", "Jax", "Jayce", "Jhin", "Jinx", "Kai'Sa", "Karma", "Karthus",
            "Kassadin", "Katarina", "Kayle", "Kennen", "Kha'Zix", "Kindred", "Lee Sin", "Leona", "Lulu",
            "Lux", "Malphite", "Master Yi", "Miss Fortune", "Morgana", "Nami", "Nasus", "Nautilus", "Olaf",
            "Orianna", "Pantheon", "Pyke", "Rakan", "Rammus", "Renekton", "Rengar", "Riven", "Seraphine",
            "Shyvana", "Singed", "Sion", "Sivir", "Sona", "Soraka", "Teemo", "Thresh", "Tristana", "Tryndamere",
            "Twisted Fate", "Varus", "Vayne", "Veigar", "Vi", "Vladimir", "Wukong", "Xayah", "Yasuo", "Yuumi",
            "Zed", "Ziggs", "Zilean", "Zyra",
            
            # Newer additions and variants
            "Senna", "Aphelios", "Sett", "Lillia", "Yone", "Samira", "Seraphine", "Rell", "Viego", "Gwen",
            "Akshan", "Vex", "Zeri", "Renata Glasc", "Bel'Veth", "Nilah", "K'Sante", "Naafiri", "Briar",
            "Ambessa", "Mel", "Warwick", "Smolder", "Aurora", "Hwei", "Briar", "Ambessa",
            
            # Champions not in Wild Rift but might appear in data
            "Aatrox", "Azir", "Cassiopeia", "Cho'Gath", "Elise", "Gangplank", "Heimerdinger", "Illaoi",
            "Ivern", "Kalista", "Kled", "Kog'Maw", "LeBlanc", "Malzahar", "Maokai", "Neeko", "Nidalee",
            "Nocturne", "Poppy", "Qiyana", "Quinn", "Ryze", "Sejuani", "Shaco", "Skarner", "Swain",
            "Sylas", "Tahm Kench", "Taliyah", "Taric", "Udyr", "Urgot", "Vel'Koz", "Viktor", "Volibear",
            "Xerath", "Xin Zhao", "Yorick", "Zac", "Trundle", "Fiddlesticks", "Janna", "Kayn", "Ornn",
            "Pyke", "Rakan", "Zoe", "Kai'Sa", "Irelia", "Akali", "Aatrox", "Nunu", "Neeko", "Sylas",
            "Yuumi", "Qiyana", "Senna", "Aphelios", "Sett", "Lillia", "Yone", "Samira", "Seraphine",
            "Rell", "Viego", "Gwen", "Akshan", "Vex", "Zeri", "Renata Glasc", "Bel'Veth", "Nilah",
            "K'Sante", "Naafiri", "Briar", "Ambessa", "Mel", "Smolder", "Aurora", "Hwei", "Yunara",
            "Rek'Sai", "Rek'sai"  # Add the missing champions that were passing through
        }
        
        # Add common variations and formatting
        variations = set()
        for name in champion_names:
            variations.add(name.lower())
            variations.add(name.upper())
            variations.add(name.replace("'", ""))
            variations.add(name.replace(" ", ""))
            variations.add(name.replace(".", ""))
            
        champion_names.update(variations)
        return champion_names

    def _is_valid_item_name(self, name):
        """Check if a name is a valid item (not a champion or other non-item)"""
        if not name or not isinstance(name, str):
            return False
            
        # Get champion names filter
        champion_names = self._get_champion_names_filter()
        
        # Filter out champion names
        if name in champion_names:
            return False
            
        # Filter out common non-item patterns
        non_item_patterns = [
            r'^[A-Z][a-z]+$',  # Single capitalized word (likely champion name)
            r'^\d+$',          # Just numbers
            r'^[A-Z]{2,}$',    # All caps abbreviations
        ]
        
        for pattern in non_item_patterns:
            if re.match(pattern, name):
                return False
        
        # Valid item names typically contain certain keywords or patterns
        item_indicators = [
            'enchant', 'boots', 'sword', 'staff', 'blade', 'armor', 'shield', 'crystal', 'tome',
            'cloak', 'crown', 'gauntlet', 'heart', 'orb', 'scepter', 'wand', 'edge', 'force',
            'reaver', 'cleaver', 'hydra', 'hurricane', 'ghostblade', 'deathcap', 'thornmail',
            'warmog', 'guardian', 'infinity', 'trinity', 'rabadon', 'void', 'lich', 'nashor',
            'rylai', 'luden', 'morello', 'zhonya', 'banshee', 'maw', 'youmuu', 'black',
            'bloodthirster', 'essence', 'navori', 'collector', 'eclipse', 'duskblade',
            'divine', 'sterak', 'titanic', 'ravenous', 'sunfire', 'frozen', 'dead',
            'randuin', 'spirit', 'abyssal', 'force', 'nature', 'anathema', 'hullbreaker',
            'serpent', 'axiom', 'chempunk', 'serylda', 'dominik', 'mortal', 'reminder',
            'kraken', 'galeforce', 'immortal', 'shieldbow', 'phantom', 'runaan', 'rapid',
            'statikk', 'stormrazor', 'wit', 'terminus', 'sundered', 'heartsteel', 'iceborn',
            'malignance', 'horizon', 'cosmic', 'demonic', 'shadowflame', 'crown', 'everfrost',
            'night', 'harvester', 'riftmaker', 'hextech', 'rocketbelt', 'protobelt', 'locket',
            'redemption', 'mikael', 'shurelya', 'imperial', 'mandate', 'moonstone', 'renewer',
            'flowing', 'water', 'ardent', 'censer', 'chemtech', 'putrifier', 'bulwark',
            'mountain', 'relic', 'spectral', 'sickle', 'ancient', 'coin', 'tear', 'goddess',
            'manamune', 'muramana', 'archangel', 'seraph', 'embrace', 'rod', 'ages',
            'thornmail', 'boots'  # Add specific items that were missed
        ]
        
        # Specific known item names that should always pass
        known_items = {
            'Boots', 'Thornmail', 'Boots of Mana', 'Boots of Dynamism', 'Plated Steelcaps',
            'Mercury\'s Treads', 'Berserker\'s Greaves', 'Ionian Boots of Lucidity',
            'Gluttonous Greaves'
        }
        
        # Check if it's a known item first
        if name in known_items:
            return True
            
        name_lower = name.lower()
        if any(indicator in name_lower for indicator in item_indicators):
            return True
            
        # Check if it contains "enchant" or common item suffixes
        if any(suffix in name_lower for suffix in ['enchant', "'s", 'of the', 'of']):
            return True
            
        # If it's a multi-word name with mixed case, likely an item
        if ' ' in name and any(c.isupper() for c in name) and any(c.islower() for c in name):
            return True
            
        return False

    def update_item_data(self):
        """Enhanced method for processing all champion build items with real-time data and champion name filtering"""
        self.logger.info("Starting comprehensive item data update process...")
        print("Updating all item data with real-time information...")
        
        # Get list of all items from champion builds
        items_to_update = set()
        champion_files_processed = 0
        filtered_out_count = 0
        
        # Scan champion files for items
        for champion_file in self.champions_dir.glob("*_data_enhanced.json"):
            try:
                with open(champion_file, 'r', encoding='utf-8') as f:
                    champion_data = json.load(f)
                
                champion_files_processed += 1
                
                if 'builds' in champion_data:
                    builds = champion_data['builds']
                    
                    # Collect items from all build categories with filtering
                    for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                        if category in builds and builds[category]:
                            for item_name in builds[category]:
                                if item_name and isinstance(item_name, str):
                                    if self._is_valid_item_name(item_name):
                                        items_to_update.add(item_name)
                                    else:
                                        filtered_out_count += 1
                                        self.logger.debug(f"Filtered out non-item: {item_name}")
                
                # Also check for items in alternative build formats
                if 'item_builds' in champion_data:
                    for build in champion_data['item_builds']:
                        if isinstance(build, dict) and 'items' in build:
                            for item in build['items']:
                                if isinstance(item, str):
                                    items_to_update.add(item)
                                elif isinstance(item, dict) and 'name' in item:
                                    items_to_update.add(item['name'])
                                    
            except Exception as e:
                error_msg = f"Error reading {champion_file}: {e}"
                self.logger.error(error_msg)
                self.stats['errors'].append(error_msg)
        
        # Also scan regular champion files as fallback
        for champion_file in self.champions_dir.glob("*_data.json"):
            if not champion_file.name.endswith("_enhanced.json"):
                try:
                    with open(champion_file, 'r', encoding='utf-8') as f:
                        champion_data = json.load(f)
                    
                    champion_files_processed += 1
                    
                    if 'builds' in champion_data:
                        builds = champion_data['builds']
                        
                        for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                            if category in builds and builds[category]:
                                for item_name in builds[category]:
                                    if item_name and isinstance(item_name, str):
                                        items_to_update.add(item_name)
                                        
                except Exception as e:
                    error_msg = f"Error reading {champion_file}: {e}"
                    self.logger.error(error_msg)
                    self.stats['errors'].append(error_msg)
        
        # Add critical items that should always be updated
        critical_items = [
            "Rabadon's Deathcap", "Infinity Edge", "Trinity Force", 
            "Guardian Angel", "Void Staff", "Thornmail", "Warmog's Armor"
        ]
        items_to_update.update(critical_items)
        
        self.logger.info(f"Processed {champion_files_processed} champion files")
        self.logger.info(f"Found {len(items_to_update)} unique items to update")
        self.logger.info(f"Filtered out {filtered_out_count} non-item entries (champion names, etc.)")
        print(f"Found {len(items_to_update)} unique items to update from {champion_files_processed} champion files")
        print(f"Filtered out {filtered_out_count} non-item entries (champion names, etc.)")
        
        # Update each item with progress tracking
        updated_count = 0
        failed_count = 0
        
        for i, item_name in enumerate(items_to_update, 1):
            print(f"\n[{i}/{len(items_to_update)}] Updating item: {item_name}")
            self.logger.info(f"Processing item {i}/{len(items_to_update)}: {item_name}")
            
            try:
                # Scrape real-time data
                item_data = self.item_scraper.scrape_specific_item(item_name)
                
                if item_data:
                    updated_count += 1
                    self.stats['items_updated'] += 1
                    self.logger.info(f"Successfully updated: {item_name}")
                else:
                    failed_count += 1
                    error_msg = f"Failed to scrape data for: {item_name}"
                    self.logger.warning(error_msg)
                    self.stats['errors'].append(error_msg)
                
            except Exception as e:
                failed_count += 1
                error_msg = f"Exception while updating {item_name}: {e}"
                self.logger.error(error_msg)
                self.stats['errors'].append(error_msg)
            
            # Rate limiting to respect website
            time.sleep(1.5)
        
        # Log final results
        success_rate = (updated_count / len(items_to_update)) * 100 if items_to_update else 0
        result_msg = f"Item update completed: {updated_count}/{len(items_to_update)} items updated ({success_rate:.1f}% success rate)"
        
        self.logger.info(result_msg)
        print(f"\n{result_msg}")
        
        if failed_count > 0:
            print(f"Failed to update {failed_count} items - check logs for details")
        
        return updated_count
    
    def validate_data_consistency(self):
        """Enhanced data consistency validation with comprehensive checks and reporting"""
        self.logger.info("Starting comprehensive data consistency validation...")
        print("🔍 Validating data consistency across all files...")
        
        issues = []
        validation_stats = {
            'items_checked': 0,
            'champions_checked': 0,
            'runes_checked': 0,
            'critical_issues': 0,
            'warnings': 0
        }
        
        # Validate item files with comprehensive checks
        print("  📦 Validating item files...")
        item_issues = self._validate_item_files(validation_stats)
        issues.extend(item_issues)
        
        # Validate champion files with detailed structure checks
        print("  🏆 Validating champion files...")
        champion_issues = self._validate_champion_files(validation_stats)
        issues.extend(champion_issues)
        
        # Validate rune files
        print("  🔮 Validating rune files...")
        rune_issues = self._validate_rune_files(validation_stats)
        issues.extend(rune_issues)
        
        # Cross-reference validation (items referenced in champion builds should exist)
        print("  🔗 Validating cross-references...")
        cross_ref_issues = self._validate_cross_references(validation_stats)
        issues.extend(cross_ref_issues)
        
        # Generate detailed validation report
        self._generate_validation_report(issues, validation_stats)
        
        return issues
    
    def _validate_item_files(self, stats):
        """Validate item files with comprehensive field and structure checks"""
        issues = []
        
        for item_file in self.items_dir.glob("*.json"):
            stats['items_checked'] += 1
            
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                
                # Check required fields
                required_fields = ['name', 'stats', 'cost']
                for field in required_fields:
                    if field not in item_data:
                        issue = f"CRITICAL: Missing required field '{field}' in {item_file.name}"
                        issues.append(issue)
                        stats['critical_issues'] += 1
                    elif not item_data[field] and field != 'stats':  # stats can be empty dict
                        issue = f"WARNING: Empty required field '{field}' in {item_file.name}"
                        issues.append(issue)
                        stats['warnings'] += 1
                
                # Validate stats structure
                if 'stats' in item_data:
                    if not isinstance(item_data['stats'], dict):
                        issue = f"CRITICAL: Stats field must be a dictionary in {item_file.name}"
                        issues.append(issue)
                        stats['critical_issues'] += 1
                    else:
                        for stat_name, stat_value in item_data['stats'].items():
                            if not isinstance(stat_value, dict):
                                issue = f"WARNING: Stat '{stat_name}' should be a dictionary in {item_file.name}"
                                issues.append(issue)
                                stats['warnings'] += 1
                            elif 'value' not in stat_value:
                                issue = f"WARNING: Stat '{stat_name}' missing 'value' field in {item_file.name}"
                                issues.append(issue)
                                stats['warnings'] += 1
                
                # Validate cost field
                if 'cost' in item_data:
                    if not isinstance(item_data['cost'], (int, float)) or item_data['cost'] < 0:
                        issue = f"WARNING: Invalid cost value in {item_file.name}"
                        issues.append(issue)
                        stats['warnings'] += 1
                
                # Check for recommended fields
                recommended_fields = ['description', 'passive', 'active', 'category']
                for field in recommended_fields:
                    if field not in item_data:
                        issue = f"INFO: Missing recommended field '{field}' in {item_file.name}"
                        issues.append(issue)
                
                # Validate specific critical items
                if 'name' in item_data:
                    item_name = item_data['name']
                    if "Rabadon's Deathcap" in item_name:
                        if item_data.get('cost') != 3400:
                            issue = f"CRITICAL: Rabadon's Deathcap cost should be 3400, found {item_data.get('cost')} in {item_file.name}"
                            issues.append(issue)
                            stats['critical_issues'] += 1
                
            except json.JSONDecodeError as e:
                issue = f"CRITICAL: Invalid JSON in {item_file.name}: {e}"
                issues.append(issue)
                stats['critical_issues'] += 1
            except Exception as e:
                issue = f"ERROR: Exception reading {item_file.name}: {e}"
                issues.append(issue)
                stats['critical_issues'] += 1
        
        return issues
    
    def _validate_champion_files(self, stats):
        """Validate champion files with detailed structure checks"""
        issues = []
        
        # Check both enhanced and regular champion files
        champion_patterns = ["*_data_enhanced.json", "*_data.json"]
        
        for pattern in champion_patterns:
            for champion_file in self.champions_dir.glob(pattern):
                # Skip if we already processed the enhanced version
                if pattern == "*_data.json" and (champion_file.parent / f"{champion_file.stem}_enhanced.json").exists():
                    continue
                    
                stats['champions_checked'] += 1
                
                try:
                    with open(champion_file, 'r', encoding='utf-8') as f:
                        champion_data = json.load(f)
                    
                    # Check required sections
                    required_sections = ['champion', 'stats', 'abilities', 'builds']
                    for section in required_sections:
                        if section not in champion_data:
                            issue = f"CRITICAL: Missing required section '{section}' in {champion_file.name}"
                            issues.append(issue)
                            stats['critical_issues'] += 1
                    
                    # Validate champion section structure
                    if 'champion' in champion_data:
                        champion_info = champion_data['champion']
                        if not isinstance(champion_info, dict):
                            issue = f"CRITICAL: Champion section must be a dictionary in {champion_file.name}"
                            issues.append(issue)
                            stats['critical_issues'] += 1
                        else:
                            required_champion_fields = ['name', 'id']
                            for field in required_champion_fields:
                                if field not in champion_info:
                                    issue = f"WARNING: Missing champion field '{field}' in {champion_file.name}"
                                    issues.append(issue)
                                    stats['warnings'] += 1
                    
                    # Validate builds section
                    if 'builds' in champion_data:
                        builds = champion_data['builds']
                        if not isinstance(builds, dict):
                            issue = f"CRITICAL: Builds section must be a dictionary in {champion_file.name}"
                            issues.append(issue)
                            stats['critical_issues'] += 1
                        else:
                            expected_build_categories = ['starting_items', 'core_items', 'boots', 'situational_items']
                            for category in expected_build_categories:
                                if category not in builds:
                                    issue = f"WARNING: Missing build category '{category}' in {champion_file.name}"
                                    issues.append(issue)
                                    stats['warnings'] += 1
                                elif not isinstance(builds[category], list):
                                    issue = f"WARNING: Build category '{category}' should be a list in {champion_file.name}"
                                    issues.append(issue)
                                    stats['warnings'] += 1
                    
                    # Validate abilities section
                    if 'abilities' in champion_data:
                        abilities = champion_data['abilities']
                        if not isinstance(abilities, dict):
                            issue = f"WARNING: Abilities section should be a dictionary in {champion_file.name}"
                            issues.append(issue)
                            stats['warnings'] += 1
                    
                except json.JSONDecodeError as e:
                    issue = f"CRITICAL: Invalid JSON in {champion_file.name}: {e}"
                    issues.append(issue)
                    stats['critical_issues'] += 1
                except Exception as e:
                    issue = f"ERROR: Exception reading {champion_file.name}: {e}"
                    issues.append(issue)
                    stats['critical_issues'] += 1
        
        return issues
    
    def _validate_rune_files(self, stats):
        """Validate rune files structure"""
        issues = []
        
        for rune_file in self.runes_dir.glob("*.json"):
            stats['runes_checked'] += 1
            
            try:
                with open(rune_file, 'r', encoding='utf-8') as f:
                    rune_data = json.load(f)
                
                # Check basic rune structure
                if not isinstance(rune_data, dict):
                    issue = f"CRITICAL: Rune file should contain a dictionary in {rune_file.name}"
                    issues.append(issue)
                    stats['critical_issues'] += 1
                    continue
                
                # Check for common rune fields
                recommended_rune_fields = ['name', 'description', 'tree']
                for field in recommended_rune_fields:
                    if field not in rune_data:
                        issue = f"INFO: Missing recommended rune field '{field}' in {rune_file.name}"
                        issues.append(issue)
                
            except json.JSONDecodeError as e:
                issue = f"CRITICAL: Invalid JSON in {rune_file.name}: {e}"
                issues.append(issue)
                stats['critical_issues'] += 1
            except Exception as e:
                issue = f"ERROR: Exception reading {rune_file.name}: {e}"
                issues.append(issue)
                stats['critical_issues'] += 1
        
        return issues
    
    def _validate_cross_references(self, stats):
        """Validate that items referenced in champion builds exist in item database"""
        issues = []
        
        # Get list of all available items
        available_items = set()
        for item_file in self.items_dir.glob("*.json"):
            try:
                with open(item_file, 'r', encoding='utf-8') as f:
                    item_data = json.load(f)
                if 'name' in item_data:
                    available_items.add(item_data['name'])
                # Also add filename without extension as potential match
                available_items.add(item_file.stem.replace('_', ' ').title())
            except:
                continue
        
        # Check champion builds for missing items
        missing_items = set()
        
        for champion_file in self.champions_dir.glob("*_data*.json"):
            try:
                with open(champion_file, 'r', encoding='utf-8') as f:
                    champion_data = json.load(f)
                
                if 'builds' in champion_data:
                    builds = champion_data['builds']
                    for category in ['starting_items', 'core_items', 'boots', 'situational_items']:
                        if category in builds and isinstance(builds[category], list):
                            for item_name in builds[category]:
                                if (item_name and 
                                    isinstance(item_name, str) and 
                                    item_name not in available_items):
                                    missing_items.add(item_name)
                                    
            except:
                continue
        
        # Report missing items
        for missing_item in missing_items:
            issue = f"WARNING: Item '{missing_item}' referenced in champion builds but not found in item database"
            issues.append(issue)
            stats['warnings'] += 1
        
        return issues
    
    def _generate_validation_report(self, issues, stats):
        """Generate detailed validation report with statistics and issue categorization"""
        
        # Categorize issues
        critical_issues = [issue for issue in issues if issue.startswith('CRITICAL:')]
        warnings = [issue for issue in issues if issue.startswith('WARNING:')]
        info_issues = [issue for issue in issues if issue.startswith('INFO:')]
        errors = [issue for issue in issues if issue.startswith('ERROR:')]
        
        # Print summary
        print(f"\n📊 Validation Summary:")
        print(f"  📦 Items checked: {stats['items_checked']}")
        print(f"  🏆 Champions checked: {stats['champions_checked']}")
        print(f"  🔮 Runes checked: {stats['runes_checked']}")
        print(f"  🔴 Critical issues: {len(critical_issues)}")
        print(f"  🟡 Warnings: {len(warnings)}")
        print(f"  🔵 Info items: {len(info_issues)}")
        print(f"  ❌ Errors: {len(errors)}")
        
        # Show detailed issues if any exist
        if issues:
            print(f"\n🔍 Detailed Issues ({len(issues)} total):")
            
            # Show critical issues first
            if critical_issues:
                print(f"\n🔴 Critical Issues ({len(critical_issues)}):")
                for issue in critical_issues[:5]:
                    print(f"  • {issue}")
                if len(critical_issues) > 5:
                    print(f"  ... and {len(critical_issues) - 5} more critical issues")
            
            # Show warnings
            if warnings:
                print(f"\n🟡 Warnings ({len(warnings)}):")
                for issue in warnings[:5]:
                    print(f"  • {issue}")
                if len(warnings) > 5:
                    print(f"  ... and {len(warnings) - 5} more warnings")
            
            # Show errors
            if errors:
                print(f"\n❌ Errors ({len(errors)}):")
                for issue in errors[:3]:
                    print(f"  • {issue}")
                if len(errors) > 3:
                    print(f"  ... and {len(errors) - 3} more errors")
        else:
            print("\n✅ No data consistency issues found! All data is valid.")
        
        # Log detailed results
        self.logger.info(f"Validation completed: {len(issues)} total issues found")
        self.logger.info(f"Critical: {len(critical_issues)}, Warnings: {len(warnings)}, Info: {len(info_issues)}, Errors: {len(errors)}")
        
        # Save detailed report to file
        if issues:
            report_file = self.logs_dir / "validation" / f"detailed_validation_report_{int(time.time())}.json"
            report_data = {
                'timestamp': time.time(),
                'stats': stats,
                'summary': {
                    'total_issues': len(issues),
                    'critical_issues': len(critical_issues),
                    'warnings': len(warnings),
                    'info_issues': len(info_issues),
                    'errors': len(errors)
                },
                'issues': {
                    'critical': critical_issues,
                    'warnings': warnings,
                    'info': info_issues,
                    'errors': errors
                }
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"\n📄 Detailed validation report saved to: {report_file}")
            self.logger.info(f"Detailed validation report saved to: {report_file}")
    
    def run_full_data_update(self, max_champions=None):
        """Enhanced orchestration method for complete data update process"""
        start_time = time.time()
        
        self.logger.info("=" * 60)
        self.logger.info("STARTING FULL DATA UPDATE PROCESS")
        self.logger.info("=" * 60)
        
        print("🚀 Starting comprehensive Wild Rift data update process...")
        print("This will update champions, items, and validate all data consistency")
        
        # Reset statistics
        self.stats = {
            'champions_processed': 0,
            'items_updated': 0,
            'validation_issues': 0,
            'errors': []
        }
        
        success_steps = 0
        total_steps = 3
        
        # Step 1: Run batch champion scraping
        print(f"\n📊 Step 1/{total_steps}: Running batch champion scraping...")
        self.logger.info("Step 1: Starting batch champion scraping")
        
        try:
            success = self.run_batch_scrape_champions(max_champions)
            if success:
                success_steps += 1
                self.logger.info("Step 1: Batch champion scraping completed successfully")
                print("✅ Champion scraping completed successfully")
            else:
                self.logger.error("Step 1: Batch champion scraping failed")
                print("❌ Champion scraping failed - continuing with remaining steps")
                self.stats['errors'].append("Batch champion scraping failed")
        except Exception as e:
            error_msg = f"Step 1 exception: {e}"
            self.logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            print(f"❌ Champion scraping failed with exception: {e}")
        
        # Step 2: Update item data
        print(f"\n🔄 Step 2/{total_steps}: Updating item data with real-time information...")
        self.logger.info("Step 2: Starting item data update")
        
        try:
            updated_items = self.update_item_data()
            if updated_items > 0:
                success_steps += 1
                self.logger.info(f"Step 2: Item data update completed - {updated_items} items updated")
                print(f"✅ Item data update completed - {updated_items} items updated")
            else:
                self.logger.warning("Step 2: No items were updated")
                print("⚠️ No items were updated - check logs for details")
        except Exception as e:
            error_msg = f"Step 2 exception: {e}"
            self.logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            print(f"❌ Item data update failed with exception: {e}")
        
        # Step 3: Validate data consistency
        print(f"\n🔍 Step 3/{total_steps}: Validating data consistency...")
        self.logger.info("Step 3: Starting data consistency validation")
        
        try:
            issues = self.validate_data_consistency()
            self.stats['validation_issues'] = len(issues)
            
            if len(issues) == 0:
                success_steps += 1
                self.logger.info("Step 3: Data validation completed - no issues found")
                print("✅ Data validation completed - no issues found")
            else:
                self.logger.warning(f"Step 3: Data validation found {len(issues)} issues")
                print(f"⚠️ Data validation found {len(issues)} issues that need attention")
                
                # Save validation issues to log file
                validation_log = self.logs_dir / "validation" / f"validation_issues_{int(time.time())}.json"
                with open(validation_log, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': time.time(),
                        'total_issues': len(issues),
                        'issues': issues
                    }, f, indent=2)
                    
        except Exception as e:
            error_msg = f"Step 3 exception: {e}"
            self.logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            print(f"❌ Data validation failed with exception: {e}")
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Generate final report
        print("\n" + "=" * 60)
        print("📋 FULL DATA UPDATE PROCESS SUMMARY")
        print("=" * 60)
        
        print(f"⏱️  Execution time: {execution_time:.1f} seconds")
        print(f"✅ Successful steps: {success_steps}/{total_steps}")
        print(f"📊 Items updated: {self.stats['items_updated']}")
        print(f"⚠️  Validation issues: {self.stats['validation_issues']}")
        print(f"❌ Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print(f"\n🔍 Error details:")
            for i, error in enumerate(self.stats['errors'][:5], 1):
                print(f"  {i}. {error}")
            if len(self.stats['errors']) > 5:
                print(f"  ... and {len(self.stats['errors']) - 5} more errors (check logs)")
        
        # Log final summary
        self.logger.info("=" * 60)
        self.logger.info("FULL DATA UPDATE PROCESS COMPLETED")
        self.logger.info(f"Success rate: {success_steps}/{total_steps} steps")
        self.logger.info(f"Items updated: {self.stats['items_updated']}")
        self.logger.info(f"Validation issues: {self.stats['validation_issues']}")
        self.logger.info(f"Errors: {len(self.stats['errors'])}")
        self.logger.info(f"Execution time: {execution_time:.1f} seconds")
        self.logger.info("=" * 60)
        
        # Determine overall success
        overall_success = (success_steps == total_steps and 
                          len(self.stats['errors']) == 0 and 
                          self.stats['validation_issues'] == 0)
        
        if overall_success:
            print("\n🎉 All data is consistent and up-to-date!")
        else:
            print(f"\n⚠️  Process completed with {total_steps - success_steps} failed steps and {len(self.stats['errors'])} errors")
            print("Check logs for detailed information and consider running individual steps")
        
        return overall_success

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Data Organizer for Wild Rift')
    parser.add_argument('--full-update', action='store_true', help='Run full data update process (legacy)')
    parser.add_argument('--workflow', action='store_true', help='Run complete workflow orchestration (recommended)')
    parser.add_argument('--update-items', action='store_true', help='Update all item data')
    parser.add_argument('--validate', action='store_true', help='Validate data consistency')
    parser.add_argument('--scrape-champions', action='store_true', help='Run batch champion scraping only')
    parser.add_argument('--max', type=int, help='Maximum number of champions to process')
    parser.add_argument('--continue-on-failure', action='store_true', default=True, 
                       help='Continue workflow execution even if non-critical steps fail')
    
    args = parser.parse_args()
    
    organizer = SmartDataOrganizer()
    
    if args.workflow:
        # Run the enhanced sequential workflow orchestration
        success = organizer.run_sequential_workflow(
            max_champions=args.max,
            continue_on_failure=args.continue_on_failure
        )
        exit(0 if success else 1)
    elif args.full_update:
        # Legacy full update method
        success = organizer.run_full_data_update(args.max)
        exit(0 if success else 1)
    elif args.scrape_champions:
        success = organizer.run_batch_scrape_champions(args.max)
        exit(0 if success else 1)
    elif args.update_items:
        updated_count = organizer.update_item_data()
        exit(0 if updated_count > 0 else 1)
    elif args.validate:
        issues = organizer.validate_data_consistency()
        exit(0 if len(issues) == 0 else 1)
    else:
        print("🚀 Smart Data Organizer for Wild Rift")
        print("=" * 50)
        print("Available actions:")
        print("  --workflow              Run complete workflow orchestration (recommended)")
        print("  --full-update           Run full data update process (legacy)")
        print("  --scrape-champions      Run batch champion scraping only")
        print("  --update-items          Update all item data")
        print("  --validate              Validate data consistency")
        print("")
        print("Options:")
        print("  --max N                 Maximum number of champions to process")
        print("  --continue-on-failure   Continue even if non-critical steps fail")
        print("")
        print("Examples:")
        print("  python smart_data_organizer.py --workflow")
        print("  python smart_data_organizer.py --workflow --max 10")
        print("  python smart_data_organizer.py --validate")

if __name__ == "__main__":
    main()