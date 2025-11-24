"""
Dice.com Job Application Bot
Automates job discovery on Dice.com (tech-focused job board)
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from anthropic import Anthropic

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Initialize Claude API
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
claude_client = Anthropic(api_key=anthropic_key) if anthropic_key else None


class DiceBot:
    """Automated Dice.com job search assistant"""

    def __init__(self, headless=False):
        """
        Initialize Dice bot

        Args:
            headless: Run browser in background (default: False for testing)
        """
        self.headless = headless
        self.email = os.getenv('DICE_EMAIL')
        self.password = os.getenv('DICE_PASSWORD')
        self.browser = None
        self.page = None
        self.context = None

        # User profile data
        self.profile = {
            'name': 'Trey Haulbrook',
            'email': 'Haulbrookai@gmail.com',
            'phone': '770-530-7910',
            'location': 'Atlanta/North Georgia',
            'title': 'Automation Developer | Google Apps Script Specialist',
            'skills': [
                'Google Apps Script', 'JavaScript', 'API Integration',
                'Workflow Automation', 'Python', 'Slack API',
                'Google Workspace', 'Web Scraping', 'LLM Integration'
            ]
        }

        # Credentials are optional for Dice (can browse without login)
        if not self.email or not self.password:
            print("⚠️  Dice credentials not found. Will browse jobs without login (limited features).")

    def start(self):
        """Start the browser with anti-detection features"""
        print("🚀 Starting Dice Bot...")
        print(f"   Headless mode: {self.headless}")

        playwright = sync_playwright().start()

        # Create persistent context directory for cookies/session
        user_data_dir = Path.home() / '.dice_bot_session'
        user_data_dir.mkdir(exist_ok=True)

        # Launch with anti-detection features
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )

        # Use persistent context to save cookies/session
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            storage_state=str(user_data_dir / 'state.json') if (user_data_dir / 'state.json').exists() else None
        )

        self.page = self.context.new_page()

        # Add script to hide webdriver property
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            window.chrome = {
                runtime: {}
            };

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)

        print("✅ Browser started with stealth mode")
        print(f"   Session saved to: {user_data_dir}")

    def stop(self):
        """Stop the browser and save session"""
        if self.context:
            user_data_dir = Path.home() / '.dice_bot_session'
            user_data_dir.mkdir(exist_ok=True)
            try:
                self.context.storage_state(path=str(user_data_dir / 'state.json'))
                print("💾 Session saved for next run")
            except Exception as e:
                print(f"⚠️  Could not save session: {e}")

        if self.browser:
            self.browser.close()
            print("🛑 Browser closed")

    def login(self):
        """Log into Dice (optional - can search without login)"""
        if not self.email or not self.password:
            print("⚠️  No credentials provided. Skipping login.")
            return True

        print("\n🔐 Logging into Dice...")

        try:
            # Go to Dice login
            self.page.goto('https://www.dice.com/dashboard/login', timeout=30000)
            time.sleep(2)

            # Check if already logged in
            if 'dashboard' in self.page.url or 'profile' in self.page.url:
                print("✅ Already logged in (session restored)!")
                return True

            print("\n" + "="*80)
            print("🤖 MANUAL LOGIN REQUIRED")
            print("="*80)
            print("\nPlease log in manually in the browser.")
            print(f"Email: {self.email}")
            print("\nThe bot will wait for you...")
            print("="*80)

            # Wait for manual login
            max_wait = 300
            start_time = time.time()

            while (time.time() - start_time) < max_wait:
                time.sleep(3)
                current_url = self.page.url
                if any(keyword in current_url for keyword in ['dashboard', 'profile', 'jobs']):
                    print("\n✅ Login detected!")
                    time.sleep(2)
                    print("✅ Login successful! Session will be saved for next time.")
                    return True

            print("\n⚠️  Login timeout. Continuing without login...")
            return True

        except Exception as e:
            print(f"\n⚠️  Login error: {e}")
            print("   Continuing without login...")
            return True

    def search_jobs(self, keyword='automation developer', location='Remote', limit=25):
        """
        Search for jobs on Dice

        Args:
            keyword: Search keyword (default: 'automation developer')
            location: Location filter (default: 'Remote')
            limit: Max number of jobs to return (default: 25)

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching Dice for '{keyword}' jobs in '{location}'...")

        try:
            # Build search URL
            # Dice search format: /jobs/q-{keyword}-l-{location}-jobs
            keyword_slug = keyword.replace(' ', '-').lower()
            location_slug = location.replace(' ', '-').lower()
            search_url = f'https://www.dice.com/jobs/q-{keyword_slug}-l-{location_slug}-jobs'

            self.page.goto(search_url, timeout=30000)
            self.page.wait_for_load_state('networkidle')

            time.sleep(3)  # Let results load

            # Scroll to load more jobs
            for i in range(3):
                self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)

            # Get job cards - Dice uses various card selectors
            job_elements = self.page.locator('div[data-cy="card"], div.card, div[class*="search-card"]').all()

            if not job_elements:
                print("⚠️  No job cards found with primary selector, trying alternative...")
                # Try alternative selector
                job_elements = self.page.locator('div[id^="position"]').all()

            if not job_elements:
                print("❌ No jobs found. Page structure may have changed.")
                return []

            print(f"✅ Found {len(job_elements)} job cards")

            jobs = []
            for idx, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Extract job details (Dice structure)
                    title_elem = job_elem.locator('h5 a, a[data-cy="card-title-link"]').first
                    company_elem = job_elem.locator('a[data-cy="search-result-company-name"], span[class*="company"]').first
                    location_elem = job_elem.locator('span[data-cy="search-result-location"], span[class*="location"]').first
                    desc_elem = job_elem.locator('div[data-cy="card-summary"], div[class*="description"]').first

                    # Get text content
                    title = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'
                    company = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'
                    location = location_elem.inner_text() if location_elem.count() > 0 else 'N/A'
                    description = desc_elem.inner_text() if desc_elem.count() > 0 else ''
                    url = title_elem.get_attribute('href') if title_elem.count() > 0 else ''

                    # Fix relative URLs
                    if url and url.startswith('/'):
                        url = f'https://www.dice.com{url}'

                    job = {
                        'title': title.strip(),
                        'company': company.strip(),
                        'location': location.strip(),
                        'description': description.strip()[:500],
                        'url': url,
                        'platform': 'dice',
                        'index': idx + 1
                    }

                    jobs.append(job)
                    print(f"   {idx + 1}. {title} at {company}")

                except Exception as e:
                    print(f"   ⚠️  Error parsing job {idx + 1}: {e}")
                    continue

            print(f"\n✅ Successfully extracted {len(jobs)} jobs")
            return jobs

        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

    def get_job_details(self, job_url):
        """
        Get detailed information about a specific job

        Args:
            job_url: URL of the job posting

        Returns:
            Dictionary with job details including description
        """
        print(f"\n📄 Fetching job details...")

        try:
            self.page.goto(job_url, timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)

            # Extract job details
            details = {}

            # Title
            title_elem = self.page.locator('h1[data-cy="jobTitle"], h1.jobTitle').first
            details['title'] = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'

            # Company
            company_elem = self.page.locator('a[data-cy="companyNameLink"], span[class*="companyName"]').first
            details['company'] = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'

            # Location
            location_elem = self.page.locator('li[data-cy="location"], span[class*="location"]').first
            details['location'] = location_elem.inner_text() if location_elem.count() > 0 else 'N/A'

            # Description
            desc_elem = self.page.locator('div[data-cy="jobDescription"], div#jobdescSec').first
            details['description'] = desc_elem.inner_text() if desc_elem.count() > 0 else 'N/A'

            # Employment type
            emp_type_elem = self.page.locator('span[data-cy="employmentType"]').first
            details['employment_type'] = emp_type_elem.inner_text() if emp_type_elem.count() > 0 else 'N/A'

            details['url'] = job_url

            print(f"✅ Fetched details for: {details['title']}")
            return details

        except Exception as e:
            print(f"❌ Error fetching job details: {e}")
            return None


def main():
    """Main execution function for testing"""
    print("="*80)
    print("Dice.com Job Search Bot - Test Mode")
    print("="*80)

    bot = DiceBot(headless=False)

    try:
        bot.start()

        # Optional login
        if bot.email and bot.password:
            bot.login()

        # Search for jobs
        jobs = bot.search_jobs(
            keyword='automation developer',
            location='Remote',
            limit=5
        )

        if jobs:
            print(f"\n📊 Found {len(jobs)} jobs")
            print("\nFirst few jobs:")
            for job in jobs[:3]:
                print(f"\n{job['index']}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   URL: {job['url']}")

        input("\n\nPress Enter to close browser...")

    finally:
        bot.stop()


if __name__ == '__main__':
    main()
