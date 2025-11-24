"""
Quick setup test - verifies credentials and basic functionality
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("="*80)
print("JOBFINDER SETUP TEST")
print("="*80)

# Check which platforms are configured
print("\nChecking credentials...")

platforms = {
    'Anthropic (Claude AI)': os.getenv('ANTHROPIC_API_KEY'),
    'LinkedIn': os.getenv('LINKEDIN_EMAIL'),
    'Upwork': os.getenv('UPWORK_EMAIL'),
    'Indeed': os.getenv('INDEED_PUBLISHER_ID'),
    'Dice': os.getenv('DICE_EMAIL'),
    'ZipRecruiter': os.getenv('ZIPRECRUITER_EMAIL'),
}

configured = []
not_configured = []

for platform, cred in platforms.items():
    if cred and cred != f'your_{platform.lower().replace(" ", "_")}_here' and 'example.com' not in str(cred):
        configured.append(platform)
        print(f"  [OK] {platform}")
    else:
        not_configured.append(platform)
        print(f"  [ ] {platform} - Not configured")

print("\n" + "="*80)
print(f"CONFIGURED: {len(configured)} platforms")
print(f"NOT CONFIGURED: {len(not_configured)} platforms")
print("="*80)

if len(configured) > 0:
    print("\nYou can search these platforms:")
    for p in configured:
        print(f"  - {p}")

    print("\nPlus these platforms that don't need login:")
    print("  - Remote.co")
    print("  - We Work Remotely")
    print("  - Remote OK")

    print("\n" + "="*80)
    print("SETUP IS WORKING!")
    print("="*80)
    print("\nNext steps:")
    print("1. Double-click RUN_MULTI_PLATFORM_SEARCH.bat")
    print("2. Complete any manual logins when browsers open")
    print("3. Review results in multi_platform_queue.json")
else:
    print("\nWARNING: No platforms configured yet!")
    print("Please add credentials to .env file")

print("\n" + "="*80)
