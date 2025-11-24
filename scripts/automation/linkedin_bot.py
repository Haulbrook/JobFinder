"""
LinkedIn Job Application Bot
Automates job discovery and application assistance on LinkedIn
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


class LinkedInBot:
    """Automated LinkedIn job search and application assistant"""

    def __init__(self, headless=False):
        """
        Initialize LinkedIn bot

        Args:
            headless: Run browser in background (default: False for testing)
        """
        self.headless = headless
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        self.browser = None
        self.page = None
        self.context = None

        # User profile data - customize this with your own info
        self.profile = {
            'name': 'Trey Haulbrook',
            'email': 'Haulbrookai@gmail.com',
            'phone': '770-530-7910',
            'location': 'Atlanta/North Georgia',
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
                "Missing LinkedIn credentials! "
                "Please add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to .env file"
            )

    def _get_profile_overview(self):
        """Get professional profile overview text"""
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
        """Start the browser with anti-detection features"""
        print("🚀 Starting LinkedIn Bot...")
        print(f"   Headless mode: {self.headless}")

        playwright = sync_playwright().start()

        # Create persistent context directory for cookies/session
        user_data_dir = Path.home() / '.linkedin_bot_session'
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

            // Add realistic chrome property
            window.chrome = {
                runtime: {}
            };

            // Realistic plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Realistic languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)

        print("✅ Browser started with stealth mode")
        print(f"   Session saved to: {user_data_dir}")

    def stop(self):
        """Stop the browser and save session"""
        if self.context:
            # Save session state for next run
            user_data_dir = Path.home() / '.linkedin_bot_session'
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
        """Log into LinkedIn with manual verification support"""
        print("\n🔐 Logging into LinkedIn...")

        try:
            # Go to LinkedIn login
            self.page.goto('https://www.linkedin.com/login', timeout=30000)
            time.sleep(2)

            # Check if already logged in
            if 'feed' in self.page.url or 'mynetwork' in self.page.url or 'jobs' in self.page.url:
                print("✅ Already logged in (session restored)!")
                return True

            print("\n" + "="*80)
            print("🤖 MANUAL LOGIN REQUIRED")
            print("="*80)
            print("\nLinkedIn has bot detection - please log in manually in the browser.")
            print("\nSteps:")
            print(f"1. Enter your email: {self.email}")
            print("2. Enter your password")
            print("3. Complete any verification challenges")
            print("4. Complete 2FA if prompted")
            print("5. Wait until you see the LinkedIn homepage/feed")
            print("\nThe bot will wait for you...")
            print("="*80)

            # Wait for user to log in manually
            max_wait = 300  # 5 minutes
            start_time = time.time()

            while (time.time() - start_time) < max_wait:
                time.sleep(3)

                # Check if logged in
                current_url = self.page.url
                if any(keyword in current_url for keyword in ['feed', 'mynetwork', 'jobs', 'in/']):
                    print("\n✅ Login detected!")
                    time.sleep(2)  # Let page fully load
                    print("✅ Login successful! Session will be saved for next time.")
                    return True

            # Timeout
            print("\n⚠️  Login timeout. Please make sure you're logged in.")
            input("Press Enter once you're logged in...")
            return True

        except Exception as e:
            print(f"\n❌ Login error: {e}")
            print("   The browser will stay open. Please log in manually.")
            input("   Press Enter once you're logged in...")
            return True

    def search_jobs(self, keyword='automation developer', location='Remote', limit=25):
        """
        Search for jobs on LinkedIn

        Args:
            keyword: Search keyword (default: 'automation developer')
            location: Location filter (default: 'Remote')
            limit: Max number of jobs to return (default: 25)

        Returns:
            List of job dictionaries
        """
        print(f"\n🔍 Searching for '{keyword}' jobs in '{location}'...")

        try:
            # Go to LinkedIn Jobs search
            # f_WT=2 filters for Remote jobs
            search_url = f'https://www.linkedin.com/jobs/search/?keywords={keyword.replace(" ", "%20")}&location={location.replace(" ", "%20")}&f_WT=2'
            self.page.goto(search_url, timeout=30000)
            self.page.wait_for_load_state('networkidle')

            time.sleep(3)  # Let results load

            # Scroll to load more jobs
            for i in range(3):
                self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)

            # Get job cards
            job_elements = self.page.locator('div.job-search-card, div.base-card').all()

            if not job_elements:
                print("❌ No jobs found. The page structure may have changed or you need to log in.")
                return []

            print(f"✅ Found {len(job_elements)} job cards")

            jobs = []
            for idx, job_elem in enumerate(job_elements[:limit]):
                try:
                    # Extract job details
                    title_elem = job_elem.locator('h3.base-search-card__title, a.job-search-card__title').first
                    company_elem = job_elem.locator('h4.base-search-card__subtitle, a.job-search-card__subtitle-link').first
                    location_elem = job_elem.locator('span.job-search-card__location').first
                    link_elem = job_elem.locator('a.base-card__full-link, a.job-search-card__link-wrapper').first

                    # Get text content
                    title = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'
                    company = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'
                    location = location_elem.inner_text() if location_elem.count() > 0 else 'N/A'
                    url = link_elem.get_attribute('href') if link_elem.count() > 0 else ''

                    # Clean up URL (remove tracking parameters)
                    if url and '?' in url:
                        url = url.split('?')[0]

                    job = {
                        'title': title.strip(),
                        'company': company.strip(),
                        'location': location.strip(),
                        'url': url,
                        'platform': 'linkedin',
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

            # Try to click "Show more" button if it exists
            try:
                show_more = self.page.locator('button:has-text("Show more"), button:has-text("See more")').first
                if show_more.count() > 0:
                    show_more.click()
                    time.sleep(1)
            except:
                pass

            # Extract job details
            details = {}

            # Title
            title_elem = self.page.locator('h1.job-details-jobs-unified-top-card__job-title, h1.t-24').first
            details['title'] = title_elem.inner_text() if title_elem.count() > 0 else 'N/A'

            # Company
            company_elem = self.page.locator('a.job-details-jobs-unified-top-card__company-name, span.job-details-jobs-unified-top-card__company-name').first
            details['company'] = company_elem.inner_text() if company_elem.count() > 0 else 'N/A'

            # Location
            location_elem = self.page.locator('span.job-details-jobs-unified-top-card__bullet').first
            details['location'] = location_elem.inner_text() if location_elem.count() > 0 else 'N/A'

            # Description
            desc_elem = self.page.locator('div.jobs-description-content__text, div.show-more-less-html__markup').first
            details['description'] = desc_elem.inner_text() if desc_elem.count() > 0 else 'N/A'

            # Workplace type (Remote, Hybrid, On-site)
            workplace_elem = self.page.locator('span.job-details-jobs-unified-top-card__workplace-type').first
            details['workplace_type'] = workplace_elem.inner_text() if workplace_elem.count() > 0 else 'N/A'

            details['url'] = job_url

            print(f"✅ Fetched details for: {details['title']}")
            return details

        except Exception as e:
            print(f"❌ Error fetching job details: {e}")
            return None

    def analyze_job_with_claude(self, job):
        """
        Analyze a job posting using Claude AI

        Args:
            job: Job dictionary with title, company, description

        Returns:
            Dictionary with analysis results
        """
        if not claude_client:
            print("⚠️  Claude AI not configured. Skipping analysis.")
            return {
                'match_score': 50,
                'is_good_fit': True,
                'reason': 'Analysis skipped - Claude API not configured',
                'red_flags': [],
                'highlights': []
            }

        print(f"\n🤖 Analyzing job with Claude AI...")

        try:
            prompt = f"""Analyze this job posting for Trey, an Automation Developer specializing in Google Apps Script:

JOB POSTING:
Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Description: {job.get('description', 'N/A')[:1000]}

TREY'S PROFILE:
{self.profile['overview']}

Please analyze:
1. Match score (0-100) - How well does this job match Trey's skills and experience?
2. Is this a good fit? (yes/no)
3. Brief reason (2-3 sentences)
4. Red flags (list any concerning aspects)
5. Highlights (list positive aspects that match Trey's skills)

Format your response as:
MATCH_SCORE: [number]
GOOD_FIT: [yes/no]
REASON: [your analysis]
RED_FLAGS: [flag1], [flag2], ...
HIGHLIGHTS: [highlight1], [highlight2], ...
"""

            message = claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Parse response
            analysis = {
                'match_score': 50,
                'is_good_fit': True,
                'reason': '',
                'red_flags': [],
                'highlights': []
            }

            for line in response_text.split('\n'):
                if 'MATCH_SCORE:' in line:
                    try:
                        analysis['match_score'] = int(''.join(filter(str.isdigit, line)))
                    except:
                        pass
                elif 'GOOD_FIT:' in line:
                    analysis['is_good_fit'] = 'yes' in line.lower()
                elif 'REASON:' in line:
                    analysis['reason'] = line.split('REASON:', 1)[1].strip()
                elif 'RED_FLAGS:' in line:
                    flags = line.split('RED_FLAGS:', 1)[1].strip()
                    analysis['red_flags'] = [f.strip() for f in flags.split(',') if f.strip() and f.strip().lower() != 'none']
                elif 'HIGHLIGHTS:' in line:
                    highlights = line.split('HIGHLIGHTS:', 1)[1].strip()
                    analysis['highlights'] = [h.strip() for h in highlights.split(',') if h.strip()]

            print(f"✅ Analysis complete:")
            print(f"   Match Score: {analysis['match_score']}/100")
            print(f"   Good Fit: {'Yes' if analysis['is_good_fit'] else 'No'}")
            print(f"   Reason: {analysis['reason']}")

            return analysis

        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return {
                'match_score': 50,
                'is_good_fit': True,
                'reason': f'Analysis failed: {str(e)}',
                'red_flags': [],
                'highlights': []
            }

    def generate_cover_letter(self, job):
        """
        Generate a personalized cover letter using Claude AI

        Args:
            job: Job dictionary with title, company, description

        Returns:
            String with cover letter text
        """
        if not claude_client:
            print("⚠️  Claude AI not configured. Using template.")
            return self._get_template_cover_letter(job)

        print(f"\n✍️  Generating cover letter with Claude AI...")

        try:
            prompt = f"""Write a compelling, personalized cover letter for this job application:

JOB POSTING:
Title: {job.get('title')}
Company: {job.get('company')}
Description: {job.get('description', 'N/A')[:1500]}

CANDIDATE PROFILE:
{self.profile['overview']}

Instructions:
- Write in first person
- Keep it concise (250-350 words)
- Focus on relevant experience and measurable results
- Be professional but conversational
- Show genuine interest in their specific project/role
- Include 1-2 specific examples from my experience that relate to their needs
- End with a clear call to action

Do not include a salutation or signature - just the body of the letter."""

            message = claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            cover_letter = message.content[0].text.strip()

            print(f"✅ Cover letter generated ({len(cover_letter)} characters)")
            return cover_letter

        except Exception as e:
            print(f"❌ Cover letter generation error: {e}")
            return self._get_template_cover_letter(job)

    def _get_template_cover_letter(self, job):
        """Get a template cover letter"""
        return f"""I'm excited to apply for the {job.get('title')} position at {job.get('company')}.

With 4+ years of experience building production automation systems using Google Apps Script and modern development tools, I specialize in creating reliable solutions that eliminate manual work and drive measurable business results.

My recent work includes building crew scheduling systems with Slack integration, automating inventory management for 500+ items, and integrating 10+ APIs including botanical databases, payment systems, and field service software. These projects have collectively saved over 20 hours weekly in administrative overhead.

I focus on production-ready code with proper error handling, user-friendly interfaces, and comprehensive documentation. My approach combines technical expertise with business understanding to deliver automation that actually works in real-world scenarios.

I'd love to discuss how my experience can help {job.get('company')} achieve its automation goals. I'm available for a call at your convenience and can typically start within a few days.

Best regards,
{self.profile['name']}
{self.profile['email']}
{self.profile['phone']}"""


def main():
    """Main execution function for testing"""
    print("="*80)
    print("LinkedIn Job Search Bot - Test Mode")
    print("="*80)

    bot = LinkedInBot(headless=False)

    try:
        bot.start()
        bot.login()

        # Search for jobs
        jobs = bot.search_jobs(
            keyword='automation developer',
            location='Remote',
            limit=5
        )

        if jobs:
            print(f"\n📊 Found {len(jobs)} jobs. Analyzing first job...")

            # Get details and analyze first job
            first_job = jobs[0]
            job_details = bot.get_job_details(first_job['url'])

            if job_details:
                # Analyze
                analysis = bot.analyze_job_with_claude(job_details)

                # Generate cover letter
                cover_letter = bot.generate_cover_letter(job_details)

                print("\n" + "="*80)
                print("COVER LETTER:")
                print("="*80)
                print(cover_letter)

        input("\n\nPress Enter to close browser...")

    finally:
        bot.stop()


if __name__ == '__main__':
    main()
