"""
Upwork Job Application Bot
Automates job applications on Upwork for Google Apps Script projects
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


class UpworkBot:
    """Automated Upwork job application bot"""

    def __init__(self, headless=False):
        """
        Initialize Upwork bot

        Args:
            headless: Run browser in background (default: False for testing)
        """
        self.headless = headless
        self.email = os.getenv('UPWORK_EMAIL')
        self.password = os.getenv('UPWORK_PASSWORD')
        self.browser = None
        self.page = None
        self.context = None

        # Trey's profile data
        self.profile = {
            'name': 'Trey Haulbrook',
            'email': 'Haulbrookai@gmail.com',
            'phone': '770-530-7910',
            'location': 'Atlanta/North Georgia',
            'hourly_rate': 60,
            'title': 'Automation Developer | Google Apps Script Specialist',
            'overview': self._get_profile_overview(),
            'skills': [
                'Google Apps Script', 'JavaScript', 'API Integration',
                'Workflow Automation', 'Python', 'Slack API',
                'Google Workspace', 'Web Scraping', 'LLM Integration'
            ]
        }

        # Validate credentials
        if not self.email or not self.password:
            raise ValueError(
                "Missing Upwork credentials! "
                "Please add UPWORK_EMAIL and UPWORK_PASSWORD to .env file"
            )

    def _get_profile_overview(self):
        """Get Trey's Upwork profile overview text"""
        return """Automation Developer | Google Apps Script Specialist

I build production automation systems that eliminate manual work and create measurable business efficiency gains.

EXPERTISE:
• Google Apps Script (Advanced) - 4+ years building production systems
• API Integration - 10+ APIs including Slack, Google Workspace, LLM services
• Workflow Automation - Saved 20+ hours weekly through custom solutions
• JavaScript/Python - Full-stack automation development

PROVEN RESULTS:
→ Built crew scheduling system processing multiple teams with Slack integration
→ Automated inventory management for 500+ items with daily updates
→ Integrated 10+ APIs including botanical databases, payment systems, field service software
→ Reduced administrative overhead by 15+ hours weekly

I don't just write scripts - I solve business problems with reliable, production-ready automation.

Available for: Contract projects, hourly consulting, ongoing automation development
Response time: Within 4 hours
Location: Atlanta/North Georgia (US-based)"""

    def start(self):
        """Start the browser"""
        print("🚀 Starting Upwork Bot...")
        print(f"   Headless mode: {self.headless}")

        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()

        print("✅ Browser started")

    def stop(self):
        """Stop the browser"""
        if self.browser:
            self.browser.close()
            print("🛑 Browser closed")

    def login(self):
        """Log into Upwork"""
        print("\n🔐 Logging into Upwork...")

        try:
            # Go to Upwork login
            self.page.goto('https://www.upwork.com/ab/account-security/login')
            self.page.wait_for_load_state('networkidle')

            # Check if already logged in
            if 'feed' in self.page.url or 'home' in self.page.url:
                print("✅ Already logged in!")
                return True

            # Enter email/username
            print("   Entering email...")
            email_input = self.page.locator('#login_username')
            email_input.fill(self.email)

            # Click continue
            continue_btn = self.page.locator('button[type="submit"]')
            continue_btn.click()

            # Wait for password page
            time.sleep(2)

            # Enter password
            print("   Entering password...")
            password_input = self.page.locator('#login_password')
            password_input.fill(self.password)

            # Click login
            login_btn = self.page.locator('button[type="submit"]')
            login_btn.click()

            # Wait for navigation
            print("   Waiting for login...")
            self.page.wait_for_load_state('networkidle', timeout=15000)

            # Check for 2FA or security questions
            if 'security' in self.page.url or 'verify' in self.page.url:
                print("\n⚠️  TWO-FACTOR AUTHENTICATION REQUIRED")
                print("    Please complete 2FA in the browser window")
                print("    (Check your email/phone for code)")
                print("\n    Waiting 60 seconds for you to complete 2FA...")
                time.sleep(60)

            # Verify login success
            time.sleep(3)
            if 'feed' in self.page.url or 'home' in self.page.url or 'jobs' in self.page.url:
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login may have failed. Current URL: {self.page.url}")
                print("    Please check the browser window")
                input("    Press Enter once you're logged in...")
                return True

        except Exception as e:
            print(f"❌ Login error: {e}")
            print("   The browser will stay open. Please log in manually.")
            input("   Press Enter once you're logged in...")
            return True

    def search_jobs(self, keyword='google apps script', limit=10):
        """
        Search for jobs on Upwork

        Args:
            keyword: Search keyword (default: 'google apps script')
            limit: Max number of jobs to return (default: 10)

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching for '{keyword}' jobs...")

        try:
            # Go to job search
            search_url = f'https://www.upwork.com/nx/search/jobs/?q={keyword.replace(" ", "%20")}'
            self.page.goto(search_url)
            self.page.wait_for_load_state('networkidle')

            time.sleep(3)  # Let results load

            # Get job cards
            job_elements = self.page.locator('article[data-test="job-tile"]').all()

            if not job_elements:
                print("❌ No jobs found. The page structure may have changed.")
                return []

            print(f"✅ Found {len(job_elements)} jobs")

            jobs = []
            for i, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Extract job details
                    title_elem = job_elem.locator('h2, h3, [data-test="job-tile-title"]').first
                    title = title_elem.inner_text() if title_elem else 'Unknown Title'

                    # Get job link
                    link_elem = job_elem.locator('a[href*="/jobs/"]').first
                    href = link_elem.get_attribute('href') if link_elem else ''
                    full_url = f'https://www.upwork.com{href}' if href and href.startswith('/') else href

                    # Get description
                    desc_elem = job_elem.locator('[data-test="job-description"]').first
                    description = desc_elem.inner_text() if desc_elem else ''

                    # Get budget/hourly rate
                    budget_elem = job_elem.locator('[data-test="budget"]').first
                    budget = budget_elem.inner_text() if budget_elem else 'Not specified'

                    job = {
                        'title': title.strip(),
                        'url': full_url,
                        'description': description.strip()[:500],  # First 500 chars
                        'budget': budget.strip(),
                        'index': i + 1
                    }

                    jobs.append(job)
                    print(f"   #{i+1}: {title[:60]}...")

                except Exception as e:
                    print(f"   ⚠️  Error extracting job #{i+1}: {e}")
                    continue

            return jobs

        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

    def generate_proposal(self, job):
        """
        Generate a custom proposal for a job

        Args:
            job: Job dictionary

        Returns:
            Proposal text
        """
        title = job.get('title', 'this project')
        description = job.get('description', '')

        # Analyze job requirements
        keywords = description.lower()

        # Determine relevant skills
        relevant_skills = []
        skill_matches = {
            'google apps script': ['Google Apps Script', 'automation'],
            'api': ['API integration', 'REST APIs'],
            'slack': ['Slack API integration'],
            'google sheets': ['Google Sheets automation'],
            'google workspace': ['Google Workspace APIs'],
            'automation': ['workflow automation'],
            'web scraping': ['web scraping', 'data extraction'],
            'python': ['Python development'],
            'javascript': ['JavaScript programming']
        }

        for keyword, skills in skill_matches.items():
            if keyword in keywords:
                relevant_skills.extend(skills)

        # Build proposal
        proposal = f"""Hi there,

I saw your project "{title}" and I'm confident I can deliver exactly what you need.

I've been building Google Apps Script automation systems for 4+ years, with a focus on production-ready solutions. """

        # Add relevant experience
        if 'slack' in keywords:
            proposal += "Most recently, I built a crew scheduling system with Slack API integration that sends real-time notifications to teams. "
        elif 'inventory' in keywords or 'database' in keywords:
            proposal += "I've built inventory automation systems that process 500+ items daily with automated updates. "
        elif 'integration' in keywords:
            proposal += "I've integrated 10+ APIs including Google Workspace, Slack, and various third-party services. "
        else:
            proposal += "I've built production systems that automated 20+ hours of manual work weekly. "

        proposal += f"""

For your project, I would:
1. Review your current workflow and requirements in detail
2. Design an automation solution using Google Apps Script
3. Implement with clean, well-documented code
4. Test thoroughly to ensure reliability
5. Provide documentation and support

I estimate this would take {'a few hours' if 'small' in keywords or 'simple' in keywords else 'approximately 8-12 hours'} at $60/hour.

I'm available to start immediately and respond within 4 hours to messages.

Looking forward to discussing your project!

Best regards,
Trey Haulbrook
Haulbrookai@gmail.com
770-530-7910"""

        return proposal

    def preview_application(self, job, proposal):
        """
        Show application preview to user for approval

        Args:
            job: Job dictionary
            proposal: Generated proposal

        Returns:
            True if user approves, False otherwise
        """
        print("\n" + "="*80)
        print("📋 APPLICATION PREVIEW")
        print("="*80)
        print(f"\n🎯 JOB: {job['title']}")
        print(f"💰 BUDGET: {job['budget']}")
        print(f"🔗 URL: {job['url']}")
        print(f"\n📝 PROPOSAL:\n")
        print(proposal)
        print("\n" + "="*80)

        response = input("\n✅ Apply to this job? (yes/no/edit): ").lower().strip()

        if response == 'edit':
            print("\n📝 Enter your custom proposal (end with empty line):")
            lines = []
            while True:
                line = input()
                if line == '':
                    break
                lines.append(line)
            return '\n'.join(lines) if lines else proposal

        return response in ['yes', 'y']

    def apply_to_job(self, job, proposal, auto_submit=False):
        """
        Apply to a job on Upwork

        Args:
            job: Job dictionary
            proposal: Proposal text
            auto_submit: Automatically submit (default: False)

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"\n📤 Applying to: {job['title']}")

            # Navigate to job
            self.page.goto(job['url'])
            self.page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Click "Apply Now" button
            apply_button = self.page.locator('button:has-text("Apply Now"), button:has-text("Submit a Proposal")').first
            if not apply_button.is_visible():
                print("⚠️  'Apply Now' button not found. You may have already applied or the job is closed.")
                return False

            apply_button.click()
            time.sleep(3)

            # Fill in cover letter/proposal
            proposal_field = self.page.locator('textarea[aria-label="Cover Letter"], textarea[name="cover_letter"]').first
            if proposal_field.is_visible():
                proposal_field.fill(proposal)
                print("   ✅ Proposal filled in")

            # Set hourly rate (if applicable)
            try:
                rate_field = self.page.locator('input[aria-label*="rate"], input[name*="rate"]').first
                if rate_field.is_visible():
                    rate_field.fill(str(self.profile['hourly_rate']))
                    print(f"   ✅ Hourly rate set to ${self.profile['hourly_rate']}")
            except:
                pass  # Not all jobs have rate field

            if not auto_submit:
                print("\n   ⏸️  PAUSED - Review the application in the browser")
                print("      1. Check the proposal")
                print("      2. Adjust bid/rate if needed")
                print("      3. Add any attachments")
                response = input("      4. Type 'submit' to continue, or 'skip' to skip this job: ").lower().strip()

                if response != 'submit':
                    print("   ⏭️  Skipped")
                    return False

            # Click submit
            submit_button = self.page.locator('button:has-text("Submit"), button[type="submit"]').last
            submit_button.click()

            print("   ⏳ Submitting...")
            time.sleep(5)

            # Verify submission
            if 'success' in self.page.url.lower() or self.page.locator('text="successfully submitted"').count() > 0:
                print("   ✅ Application submitted successfully!")
                return True
            else:
                print("   ⚠️  Application may have been submitted. Please verify in your Upwork dashboard.")
                return True

        except Exception as e:
            print(f"   ❌ Error applying: {e}")
            return False

    def run_application_batch(self, keyword='google apps script', num_jobs=5, auto_submit=False):
        """
        Run a batch of job applications

        Args:
            keyword: Search keyword
            num_jobs: Number of jobs to apply to
            auto_submit: Automatically submit applications

        Returns:
            Statistics dictionary
        """
        stats = {
            'searched': 0,
            'reviewed': 0,
            'applied': 0,
            'skipped': 0,
            'failed': 0
        }

        try:
            # Login
            self.start()
            if not self.login():
                print("❌ Login failed")
                return stats

            # Search for jobs
            jobs = self.search_jobs(keyword, limit=num_jobs)
            stats['searched'] = len(jobs)

            if not jobs:
                print("\n❌ No jobs found")
                return stats

            print(f"\n🎯 Ready to apply to {len(jobs)} jobs")
            print(f"   Auto-submit: {'YES' if auto_submit else 'NO (you approve each one)'}")

            # Apply to each job
            for job in jobs:
                stats['reviewed'] += 1

                # Generate proposal
                proposal = self.generate_proposal(job)

                # Preview and get approval
                if not auto_submit:
                    approved = self.preview_application(job, proposal)
                    if not approved:
                        stats['skipped'] += 1
                        print(f"⏭️  Skipped: {job['title']}")
                        continue

                # Apply
                success = self.apply_to_job(job, proposal, auto_submit)

                if success:
                    stats['applied'] += 1
                else:
                    stats['failed'] += 1

                # Pause between applications
                if stats['reviewed'] < len(jobs):
                    print("\n   ⏸️  Waiting 5 seconds before next application...")
                    time.sleep(5)

            return stats

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return stats
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            return stats
        finally:
            input("\nPress Enter to close browser...")
            self.stop()


def main():
    """Main entry point"""
    print("="*80)
    print("🤖 UPWORK JOB APPLICATION BOT")
    print("="*80)
    print("For: Trey Haulbrook")
    print("Focus: Google Apps Script & Automation Projects")
    print("="*80)

    # Configuration
    HEADLESS = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
    AUTO_SUBMIT = os.getenv('AUTO_SUBMIT', 'false').lower() == 'true'
    MAX_JOBS = int(os.getenv('MAX_APPLICATIONS_PER_DAY', '10'))

    print(f"\n⚙️  SETTINGS:")
    print(f"   Headless mode: {HEADLESS}")
    print(f"   Auto-submit: {AUTO_SUBMIT}")
    print(f"   Max applications: {MAX_JOBS}")

    if not AUTO_SUBMIT:
        print("\n   📋 You'll review each application before submitting")

    input("\nPress Enter to start...")

    # Create bot
    bot = UpworkBot(headless=HEADLESS)

    # Run applications
    stats = bot.run_application_batch(
        keyword='google apps script',
        num_jobs=MAX_JOBS,
        auto_submit=AUTO_SUBMIT
    )

    # Print results
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    print(f"   Jobs found: {stats['searched']}")
    print(f"   Jobs reviewed: {stats['reviewed']}")
    print(f"   Applications submitted: {stats['applied']}")
    print(f"   Jobs skipped: {stats['skipped']}")
    print(f"   Failed: {stats['failed']}")
    print("="*80)

    if stats['applied'] > 0:
        print(f"\n🎉 SUCCESS! Applied to {stats['applied']} jobs!")
        print("   Check your Upwork dashboard for responses")
    else:
        print("\n⚠️  No applications submitted")

    print("\n✅ Done!")


if __name__ == '__main__':
    main()
