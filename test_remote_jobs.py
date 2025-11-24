"""
Quick test of remote job boards (no login required)
"""

import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from scripts.automation.remote_jobs_bot import RemoteJobsBot

print("="*80)
print("TESTING REMOTE JOB BOARDS (No login required)")
print("="*80)

bot = RemoteJobsBot(headless=True)

try:
    print("\nStarting browser...")
    bot.start()

    print("\nSearching remote job boards...")
    jobs = bot.search_all_platforms(keyword='developer', limit_per_platform=3)

    print(f"\n\nFOUND {len(jobs)} JOBS!")
    print("="*80)

    if jobs:
        print("\nSample jobs:")
        for job in jobs[:5]:
            print(f"\n- {job['title']}")
            print(f"  Company: {job['company']}")
            print(f"  Platform: {job['platform']}")
            print(f"  URL: {job['url'][:60]}...")

    bot.stop()
    print("\nSUCCESS! Remote job search is working!")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    bot.stop()
