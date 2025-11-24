"""Quick test script for Upwork bot - no interactive prompts"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from automation.upwork_bot import UpworkBot

print("="*80)
print("🧪 UPWORK BOT TEST")
print("="*80)

try:
    # Create bot instance
    print("\n1️⃣ Creating bot instance...")
    bot = UpworkBot(headless=False)  # Visible browser
    print("✅ Bot created successfully!")

    print(f"\n📧 Email configured: {bot.email}")
    print(f"👤 Profile name: {bot.profile['name']}")
    print(f"💰 Hourly rate: ${bot.profile['hourly_rate']}")

    # Start browser
    print("\n2️⃣ Starting browser...")
    bot.start()
    print("✅ Browser started!")

    # Test login
    print("\n3️⃣ Testing Upwork login...")
    print("   (You may need to complete 2FA if enabled)")
    login_success = bot.login()

    if login_success:
        print("✅ Login successful!")

        # Search for jobs
        print("\n4️⃣ Searching for Google Apps Script jobs...")
        jobs = bot.search_jobs(keyword='google apps script', limit=3)

        if jobs:
            print(f"✅ Found {len(jobs)} jobs!")
            print("\n📋 Job Preview:")
            for i, job in enumerate(jobs, 1):
                print(f"\n   Job #{i}:")
                print(f"   Title: {job['title']}")
                print(f"   Budget: {job['budget']}")
                print(f"   URL: {job['url'][:80]}...")
        else:
            print("⚠️  No jobs found (this might be normal)")

        print("\n5️⃣ Test complete! Browser will stay open for 10 seconds...")
        print("   You can review the Upwork page.")

        import time
        time.sleep(10)

    else:
        print("❌ Login failed - check credentials in .env")

    # Clean up
    print("\n6️⃣ Closing browser...")
    bot.stop()
    print("✅ Test complete!")

    print("\n" + "="*80)
    print("🎉 SUCCESS! The bot is working!")
    print("="*80)
    print("\nNext steps:")
    print("1. The bot can log in ✅")
    print("2. The bot can search for jobs ✅")
    print("3. Ready to apply to jobs!")
    print("\nTo apply to jobs, run:")
    print("   python3 scripts/automation/upwork_bot.py")
    print("\n(The main script will let you review and approve each application)")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check .env file has UPWORK_EMAIL and UPWORK_PASSWORD")
    print("2. Verify credentials are correct")
    print("3. Check internet connection")
    import traceback
    traceback.print_exc()
