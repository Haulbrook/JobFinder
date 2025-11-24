"""
Remote Jobs Bot
Searches remote-focused job boards: Remote.co, We Work Remotely, Remote OK
No login required - these are public job boards
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


class RemoteJobsBot:
    """Bot for searching remote-focused job boards"""

    def __init__(self, headless=False):
        """
        Initialize Remote Jobs bot

        Args:
            headless: Run browser in background (default: False for testing)
        """
        self.headless = headless
        self.browser = None
        self.page = None
        self.context = None

        self.platforms = {
            'weworkremotely': 'https://weworkremotely.com',
            'remoteok': 'https://remoteok.com',
            'remoteco': 'https://remote.co/remote-jobs'
        }

    def start(self):
        """Start the browser"""
        print("🚀 Starting Remote Jobs Bot...")

        playwright = sync_playwright().start()

        # Launch browser
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )

        self.page = self.context.new_page()

        # Add script to hide webdriver property
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        print("✅ Browser started")

    def stop(self):
        """Stop the browser"""
        if self.browser:
            self.browser.close()
            print("🛑 Browser closed")

    def search_weworkremotely(self, category='programming', limit=25):
        """
        Search We Work Remotely

        Args:
            category: Job category (programming, design, marketing, etc.)
            limit: Max number of jobs to return

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching We Work Remotely - {category}...")

        try:
            # Go to category page
            url = f'https://weworkremotely.com/categories/remote-{category}-jobs'
            self.page.goto(url, timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Get job listings
            job_elements = self.page.locator('li.feature, li[class*="job"]').all()

            if not job_elements:
                # Try alternative selector
                job_elements = self.page.locator('section.jobs article').all()

            print(f"✅ Found {len(job_elements)} jobs on We Work Remotely")

            jobs = []
            for idx, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Extract details
                    title_elem = job_elem.locator('span.title, h2, a[class*="title"]').first
                    company_elem = job_elem.locator('span.company, a[class*="company"]').first
                    link_elem = job_elem.locator('a').first

                    title = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'
                    company = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'
                    url = link_elem.get_attribute('href') if link_elem.count() > 0 else ''

                    # Fix relative URLs
                    if url and url.startswith('/'):
                        url = f'https://weworkremotely.com{url}'

                    job = {
                        'title': title.strip(),
                        'company': company.strip(),
                        'location': 'Remote',
                        'url': url,
                        'platform': 'weworkremotely',
                        'index': idx + 1
                    }

                    jobs.append(job)
                    print(f"   {idx + 1}. {title} at {company}")

                except Exception as e:
                    print(f"   ⚠️  Error parsing job {idx + 1}: {e}")
                    continue

            return jobs

        except Exception as e:
            print(f"❌ We Work Remotely search error: {e}")
            return []

    def search_remoteok(self, tag='dev', limit=25):
        """
        Search Remote OK

        Args:
            tag: Job tag/category (dev, design, marketing, sales, etc.)
            limit: Max number of jobs to return

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching Remote OK - {tag}...")

        try:
            # Go to tag page
            url = f'https://remoteok.com/remote-{tag}-jobs'
            self.page.goto(url, timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)

            # Remote OK uses table rows for jobs
            job_elements = self.page.locator('tr.job').all()

            print(f"✅ Found {len(job_elements)} jobs on Remote OK")

            jobs = []
            for idx, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Skip ads
                    if 'ad' in job_elem.get_attribute('class') or '':
                        continue

                    # Extract details
                    title_elem = job_elem.locator('h2, td.company_and_position h2').first
                    company_elem = job_elem.locator('h3, td.company_and_position h3').first
                    link_elem = job_elem.locator('a.preventLink').first

                    title = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'
                    company = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'
                    url = link_elem.get_attribute('href') if link_elem.count() > 0 else ''

                    # Fix relative URLs
                    if url and url.startswith('/'):
                        url = f'https://remoteok.com{url}'

                    job = {
                        'title': title.strip(),
                        'company': company.strip(),
                        'location': 'Remote (Worldwide)',
                        'url': url,
                        'platform': 'remoteok',
                        'index': idx + 1
                    }

                    jobs.append(job)
                    print(f"   {idx + 1}. {title} at {company}")

                except Exception as e:
                    print(f"   ⚠️  Error parsing job {idx + 1}: {e}")
                    continue

            return jobs

        except Exception as e:
            print(f"❌ Remote OK search error: {e}")
            return []

    def search_remoteco(self, keyword='developer', limit=25):
        """
        Search Remote.co

        Args:
            keyword: Search keyword
            limit: Max number of jobs to return

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching Remote.co - {keyword}...")

        try:
            # Go to jobs page
            url = f'https://remote.co/remote-jobs/search/?search_keywords={keyword}'
            self.page.goto(url, timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)

            # Get job cards
            job_elements = self.page.locator('div.job_listing, div.card, article[class*="job"]').all()

            if not job_elements:
                # Try alternative selector
                job_elements = self.page.locator('li.job').all()

            print(f"✅ Found {len(job_elements)} jobs on Remote.co")

            jobs = []
            for idx, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Extract details
                    title_elem = job_elem.locator('h3, h2, a[class*="title"]').first
                    company_elem = job_elem.locator('span[class*="company"], div[class*="company"]').first
                    link_elem = job_elem.locator('a').first

                    title = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'
                    company = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'
                    url = link_elem.get_attribute('href') if link_elem.count() > 0 else ''

                    # Fix relative URLs
                    if url and url.startswith('/'):
                        url = f'https://remote.co{url}'

                    job = {
                        'title': title.strip(),
                        'company': company.strip(),
                        'location': 'Remote',
                        'url': url,
                        'platform': 'remoteco',
                        'index': idx + 1
                    }

                    jobs.append(job)
                    print(f"   {idx + 1}. {title} at {company}")

                except Exception as e:
                    print(f"   ⚠️  Error parsing job {idx + 1}: {e}")
                    continue

            return jobs

        except Exception as e:
            print(f"❌ Remote.co search error: {e}")
            return []

    def search_all_platforms(self, keyword='developer', limit_per_platform=10):
        """
        Search all remote job platforms

        Args:
            keyword: Search keyword
            limit_per_platform: Max jobs per platform

        Returns:
            Combined list of jobs from all platforms
        """
        print("\n" + "="*80)
        print("🌍 SEARCHING ALL REMOTE JOB PLATFORMS")
        print("="*80)

        all_jobs = []

        # We Work Remotely (use 'programming' category for developer jobs)
        wwr_jobs = self.search_weworkremotely(category='programming', limit=limit_per_platform)
        all_jobs.extend(wwr_jobs)

        # Remote OK
        rok_jobs = self.search_remoteok(tag='dev', limit=limit_per_platform)
        all_jobs.extend(rok_jobs)

        # Remote.co
        rco_jobs = self.search_remoteco(keyword=keyword, limit=limit_per_platform)
        all_jobs.extend(rco_jobs)

        print("\n" + "="*80)
        print(f"📊 TOTAL: Found {len(all_jobs)} remote jobs across {len(self.platforms)} platforms")
        print("="*80)

        return all_jobs

    def get_job_details(self, job):
        """
        Get detailed information about a specific job

        Args:
            job: Job dictionary with URL and platform

        Returns:
            Dictionary with job details including description
        """
        print(f"\n📄 Fetching job details from {job['platform']}...")

        try:
            self.page.goto(job['url'], timeout=30000)
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)

            details = job.copy()

            # Try to get description (varies by platform)
            desc_selectors = [
                'div.listing-container',  # We Work Remotely
                'div.markdown',  # Remote OK
                'div.job_description',  # Remote.co
                'div.description',
                'article',
                'main'
            ]

            description = ''
            for selector in desc_selectors:
                desc_elem = self.page.locator(selector).first
                if desc_elem.count() > 0:
                    description = desc_elem.inner_text()
                    break

            details['description'] = description if description else 'N/A'

            print(f"✅ Fetched details ({len(description)} chars)")
            return details

        except Exception as e:
            print(f"❌ Error fetching job details: {e}")
            return job


def main():
    """Main execution function for testing"""
    print("="*80)
    print("Remote Jobs Bot - Test Mode")
    print("="*80)

    bot = RemoteJobsBot(headless=False)

    try:
        bot.start()

        # Search all platforms
        jobs = bot.search_all_platforms(keyword='automation developer', limit_per_platform=5)

        if jobs:
            print(f"\n📋 Sample jobs found:")
            for job in jobs[:10]:
                print(f"\n{job['index']}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Platform: {job['platform']}")
                print(f"   URL: {job['url']}")

        input("\n\nPress Enter to close browser...")

    finally:
        bot.stop()


if __name__ == '__main__':
    main()
