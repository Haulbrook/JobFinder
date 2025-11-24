"""
Multi-Platform Job Search
Searches all configured job boards: Upwork, LinkedIn, Indeed, Dice, Remote boards, ZipRecruiter
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

# Load environment variables
load_dotenv()

# Import all bots
from scripts.automation.upwork_bot import UpworkBot
from scripts.automation.linkedin_bot import LinkedInBot
from scripts.automation.dice_bot import DiceBot
from scripts.automation.remote_jobs_bot import RemoteJobsBot
from scripts.automation.ziprecruiter_bot import ZipRecruiterBot

# Import Indeed adapter
from scripts.search.platform_adapters import IndeedAdapter


class MultiPlatformJobSearch:
    """Unified job search across multiple platforms"""

    def __init__(self):
        """Initialize multi-platform search"""
        self.queue_file = Path('multi_platform_queue.json')
        self.platforms_config = {
            'upwork': {
                'enabled': bool(os.getenv('UPWORK_EMAIL')),
                'bot_class': UpworkBot,
                'type': 'browser'
            },
            'linkedin': {
                'enabled': bool(os.getenv('LINKEDIN_EMAIL')),
                'bot_class': LinkedInBot,
                'type': 'browser'
            },
            'dice': {
                'enabled': bool(os.getenv('DICE_EMAIL')) or True,  # Can work without login
                'bot_class': DiceBot,
                'type': 'browser'
            },
            'remote': {
                'enabled': True,  # No login required
                'bot_class': RemoteJobsBot,
                'type': 'browser'
            },
            'ziprecruiter': {
                'enabled': bool(os.getenv('ZIPRECRUITER_EMAIL')) or True,  # Can work without login
                'bot_class': ZipRecruiterBot,
                'type': 'browser'
            },
            'indeed': {
                'enabled': bool(os.getenv('INDEED_PUBLISHER_ID')),
                'adapter_class': IndeedAdapter,
                'type': 'api'
            }
        }

    def get_enabled_platforms(self):
        """Get list of enabled platforms"""
        return [name for name, config in self.platforms_config.items() if config['enabled']]

    def search_all_platforms(self, keyword='automation developer', location='Remote', limit_per_platform=10):
        """
        Search all enabled platforms

        Args:
            keyword: Search keyword
            location: Location filter
            limit_per_platform: Max jobs per platform

        Returns:
            Dictionary with jobs organized by platform
        """
        print("\n" + "="*80)
        print("MULTI-PLATFORM JOB SEARCH")
        print("="*80)
        print(f"Keyword: {keyword}")
        print(f"Location: {location}")
        print(f"Limit per platform: {limit_per_platform}")

        enabled = self.get_enabled_platforms()
        print(f"\nEnabled platforms: {', '.join(enabled)}")
        print("="*80)

        all_jobs = {}

        # Search browser-based platforms
        for platform_name, config in self.platforms_config.items():
            if not config['enabled']:
                print(f"\n⏭️  Skipping {platform_name} (not configured)")
                continue

            if config['type'] == 'browser':
                try:
                    print(f"\n{'='*80}")
                    print(f"Searching {platform_name.upper()}...")
                    print(f"{'='*80}")

                    bot = config['bot_class'](headless=True)
                    bot.start()

                    # Platform-specific search
                    if platform_name == 'upwork':
                        # Upwork uses keyword-based search
                        jobs = bot.search_jobs(keyword=keyword, limit=limit_per_platform)
                    elif platform_name == 'linkedin':
                        jobs = bot.search_jobs(keyword=keyword, location=location, limit=limit_per_platform)
                    elif platform_name == 'dice':
                        jobs = bot.search_jobs(keyword=keyword, location=location, limit=limit_per_platform)
                    elif platform_name == 'remote':
                        jobs = bot.search_all_platforms(keyword=keyword, limit_per_platform=limit_per_platform)
                    elif platform_name == 'ziprecruiter':
                        jobs = bot.search_jobs(keyword=keyword, location=location, limit=limit_per_platform)
                    else:
                        jobs = []

                    all_jobs[platform_name] = jobs
                    print(f"✅ Found {len(jobs)} jobs on {platform_name}")

                    bot.stop()

                except Exception as e:
                    print(f"❌ Error searching {platform_name}: {e}")
                    all_jobs[platform_name] = []

            elif config['type'] == 'api' and platform_name == 'indeed':
                try:
                    print(f"\n{'='*80}")
                    print(f"Searching {platform_name.upper()} (API)...")
                    print(f"{'='*80}")

                    adapter = config['adapter_class']()
                    params = {
                        'keywords': [keyword],
                        'locations': [location]
                    }
                    jobs = adapter.search(params)
                    all_jobs[platform_name] = jobs[:limit_per_platform]
                    print(f"✅ Found {len(all_jobs[platform_name])} jobs on {platform_name}")

                except Exception as e:
                    print(f"❌ Error searching {platform_name}: {e}")
                    all_jobs[platform_name] = []

        # Print summary
        print("\n" + "="*80)
        print("SEARCH SUMMARY")
        print("="*80)
        total = 0
        for platform, jobs in all_jobs.items():
            count = len(jobs)
            total += count
            print(f"  {platform.ljust(15)} : {count} jobs")
        print(f"\n  TOTAL          : {total} jobs")
        print("="*80)

        return all_jobs

    def save_to_queue(self, jobs_by_platform):
        """
        Save jobs to unified queue file

        Args:
            jobs_by_platform: Dictionary with jobs organized by platform
        """
        # Load existing queue
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                queue = json.load(f)
        else:
            queue = []

        # Add new jobs
        added_count = 0
        for platform, jobs in jobs_by_platform.items():
            for job in jobs:
                # Check if job already exists (by URL)
                if not any(q['url'] == job.get('url') for q in queue):
                    queue_item = {
                        'platform': platform,
                        'title': job.get('title', 'N/A'),
                        'company': job.get('company', 'N/A'),
                        'location': job.get('location', 'N/A'),
                        'description': job.get('description', '')[:500],
                        'url': job.get('url', ''),
                        'added_at': datetime.now().isoformat(),
                        'status': 'queued',  # queued, reviewed, applied, skipped
                        'match_score': None,
                        'analysis': None,
                        'cover_letter': None,
                        'applied_at': None
                    }
                    queue.append(queue_item)
                    added_count += 1

        # Save queue
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)

        print(f"\nAdded {added_count} new jobs to queue")
        print(f"Total jobs in queue: {len(queue)}")
        print(f"Queue file: {self.queue_file.absolute()}")

    def view_queue(self, status_filter=None):
        """
        View jobs in queue

        Args:
            status_filter: Filter by status (queued, reviewed, applied, skipped)
        """
        if not self.queue_file.exists():
            print("❌ No queue file found. Run search first.")
            return

        with open(self.queue_file, 'r') as f:
            queue = json.load(f)

        if status_filter:
            queue = [j for j in queue if j['status'] == status_filter]

        print("\n" + "="*80)
        print(f"JOB QUEUE ({len(queue)} jobs)")
        if status_filter:
            print(f"Filter: {status_filter}")
        print("="*80)

        # Group by status
        by_status = {}
        for job in queue:
            status = job['status']
            by_status[status] = by_status.get(status, 0) + 1

        print("\nStatus breakdown:")
        for status, count in sorted(by_status.items()):
            print(f"  {status.ljust(10)} : {count}")

        # Group by platform
        by_platform = {}
        for job in queue:
            platform = job['platform']
            by_platform[platform] = by_platform.get(platform, 0) + 1

        print("\nPlatform breakdown:")
        for platform, count in sorted(by_platform.items()):
            print(f"  {platform.ljust(15)} : {count}")

        # Show some jobs
        print("\n" + "-"*80)
        print("Sample jobs:")
        print("-"*80)
        for idx, job in enumerate(queue[:10], 1):
            print(f"\n{idx}. [{job['status'].upper()}] {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Platform: {job['platform']}")
            print(f"   Location: {job['location']}")
            if job['match_score']:
                print(f"   Match Score: {job['match_score']}/100")
            print(f"   URL: {job['url'][:80]}")

        print("\n" + "="*80)

    def export_queue_csv(self, output_file='jobs_export.csv'):
        """Export queue to CSV file"""
        if not self.queue_file.exists():
            print("❌ No queue file found.")
            return

        import csv

        with open(self.queue_file, 'r') as f:
            queue = json.load(f)

        # Write CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if not queue:
                print("❌ Queue is empty.")
                return

            fieldnames = ['platform', 'title', 'company', 'location', 'status', 'match_score', 'url', 'added_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()
            for job in queue:
                writer.writerow(job)

        print(f"✅ Exported {len(queue)} jobs to {output_file}")


def main():
    """Main execution"""
    import sys

    searcher = MultiPlatformJobSearch()

    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("Multi-Platform Job Search")
        print("="*80)
        print("\nUsage:")
        print("  python multi_platform_search.py search [keyword] [location] [limit]")
        print("  python multi_platform_search.py view [status]")
        print("  python multi_platform_search.py export [filename]")
        print("\nExamples:")
        print("  python multi_platform_search.py search \"automation developer\" \"Remote\" 10")
        print("  python multi_platform_search.py view queued")
        print("  python multi_platform_search.py export jobs.csv")
        print("\nEnabled platforms:")
        for platform in searcher.get_enabled_platforms():
            print(f"  ✅ {platform}")
        print("="*80)
        return

    command = sys.argv[1]

    if command == 'search':
        keyword = sys.argv[2] if len(sys.argv) > 2 else 'automation developer'
        location = sys.argv[3] if len(sys.argv) > 3 else 'Remote'
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10

        # Search all platforms
        jobs = searcher.search_all_platforms(keyword, location, limit)

        # Save to queue
        searcher.save_to_queue(jobs)

        # View queue
        searcher.view_queue()

    elif command == 'view':
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        searcher.view_queue(status_filter)

    elif command == 'export':
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'jobs_export.csv'
        searcher.export_queue_csv(output_file)

    else:
        print(f"❌ Unknown command: {command}")
        print("   Valid commands: search, view, export")


if __name__ == '__main__':
    main()
