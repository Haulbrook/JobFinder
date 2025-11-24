# Multi-Platform Job Search Guide

Complete guide for using JobFinder across multiple job boards.

## 🌐 Supported Platforms

### Browser Automation (Playwright)
1. **Upwork** - Freelance marketplace
2. **LinkedIn** - Professional network
3. **Dice.com** - Tech-focused jobs
4. **Remote Jobs** - Remote.co, We Work Remotely, Remote OK
5. **ZipRecruiter** - General job board

### API Integration
6. **Indeed** - Job aggregator (API)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**Required for each platform:**
- **Upwork**: `UPWORK_EMAIL`, `UPWORK_PASSWORD`
- **LinkedIn**: `LINKEDIN_EMAIL`, `LINKEDIN_PASSWORD`
- **Dice**: `DICE_EMAIL`, `DICE_PASSWORD` (optional - can browse without login)
- **ZipRecruiter**: `ZIPRECRUITER_EMAIL`, `ZIPRECRUITER_PASSWORD` (optional)
- **Indeed**: `INDEED_PUBLISHER_ID` (free at https://www.indeed.com/publisher)
- **Remote boards**: No credentials needed

**Optional:**
- `ANTHROPIC_API_KEY` - For AI-powered job analysis and cover letters

### 3. Run Multi-Platform Search

Search all configured platforms at once:

```bash
python multi_platform_search.py search "automation developer" "Remote" 10
```

This will:
1. Search all enabled platforms
2. Save results to `multi_platform_queue.json`
3. Show summary of findings

---

## 📋 Platform-Specific Usage

### Upwork Bot

```python
from scripts.automation.upwork_bot import UpworkBot

bot = UpworkBot(headless=False)
bot.start()
bot.login()  # Manual login required first time
jobs = bot.search_jobs(keyword='google apps script', limit=10)
bot.stop()
```

**Features:**
- Session persistence (stays logged in)
- AI-powered job analysis
- AI-powered proposal generation
- Batch application support

### LinkedIn Bot

```python
from scripts.automation.linkedin_bot import LinkedInBot

bot = LinkedInBot(headless=False)
bot.start()
bot.login()  # Manual login required first time
jobs = bot.search_jobs(keyword='automation developer', location='Remote', limit=25)
job_details = bot.get_job_details(jobs[0]['url'])
analysis = bot.analyze_job_with_claude(job_details)
cover_letter = bot.generate_cover_letter(job_details)
bot.stop()
```

**Features:**
- Remote job filtering
- Detailed job information extraction
- AI job analysis
- AI cover letter generation

### Dice Bot

```python
from scripts.automation.dice_bot import DiceBot

bot = DiceBot(headless=False)
bot.start()
# Login optional for Dice
jobs = bot.search_jobs(keyword='automation developer', location='Remote', limit=25)
bot.stop()
```

**Features:**
- Tech-focused job search
- Works without login
- Detailed job descriptions

### Remote Jobs Bot

```python
from scripts.automation.remote_jobs_bot import RemoteJobsBot

bot = RemoteJobsBot(headless=False)
bot.start()
# No login needed
jobs = bot.search_all_platforms(keyword='developer', limit_per_platform=10)
# Or search individual platforms:
# wwr_jobs = bot.search_weworkremotely(category='programming', limit=10)
# rok_jobs = bot.search_remoteok(tag='dev', limit=10)
# rco_jobs = bot.search_remoteco(keyword='developer', limit=10)
bot.stop()
```

**Features:**
- Searches 3 remote job boards
- No login required
- 100% remote jobs

### ZipRecruiter Bot

```python
from scripts.automation.ziprecruiter_bot import ZipRecruiterBot

bot = ZipRecruiterBot(headless=False)
bot.start()
# Login optional
jobs = bot.search_jobs(keyword='automation developer', location='Remote', limit=25)
bot.stop()
```

**Features:**
- Large job database
- Works without login
- Detailed job information

### Indeed API

```python
from scripts.search.platform_adapters import IndeedAdapter

adapter = IndeedAdapter()
params = {
    'keywords': ['automation developer'],
    'locations': ['Remote']
}
jobs = adapter.search(params)
```

**Features:**
- Fast API-based search
- Free tier available
- Large job database

---

## 🎯 Multi-Platform Search Commands

### Search All Platforms

```bash
# Basic search
python multi_platform_search.py search

# Custom keyword and location
python multi_platform_search.py search "python developer" "New York" 15

# Search with defaults (automation developer, Remote, limit 10)
python multi_platform_search.py search
```

### View Queue

```bash
# View all jobs
python multi_platform_search.py view

# Filter by status
python multi_platform_search.py view queued
python multi_platform_search.py view applied
python multi_platform_search.py view skipped
```

### Export to CSV

```bash
# Export to default filename (jobs_export.csv)
python multi_platform_search.py export

# Export to custom filename
python multi_platform_search.py export my_jobs.csv
```

---

## 🤖 AI-Powered Features

### Job Analysis

Analyze jobs using Claude AI to get match scores and insights:

```python
analysis = bot.analyze_job_with_claude(job_details)
print(f"Match Score: {analysis['match_score']}/100")
print(f"Good Fit: {analysis['is_good_fit']}")
print(f"Reason: {analysis['reason']}")
print(f"Highlights: {analysis['highlights']}")
print(f"Red Flags: {analysis['red_flags']}")
```

### Cover Letter Generation

Generate personalized cover letters:

```python
cover_letter = bot.generate_cover_letter(job_details)
# Copy to clipboard or save to file
```

---

## 📊 Queue File Format

Jobs are saved to `multi_platform_queue.json`:

```json
[
  {
    "platform": "linkedin",
    "title": "Automation Developer",
    "company": "Tech Corp",
    "location": "Remote",
    "description": "...",
    "url": "https://...",
    "added_at": "2025-11-24T10:30:00",
    "status": "queued",
    "match_score": null,
    "analysis": null,
    "cover_letter": null,
    "applied_at": null
  }
]
```

**Status values:**
- `queued` - Job added to queue
- `reviewed` - Job reviewed but not applied
- `applied` - Application submitted
- `skipped` - Job skipped (not a good fit)

---

## 🔧 Advanced Configuration

### Headless Mode

Run browsers in background (no window):

```python
bot = LinkedInBot(headless=True)
```

### Custom Search Parameters

Each platform has different search options:

**LinkedIn:**
- `keyword` - Job title/keyword
- `location` - City, state, or "Remote"
- `limit` - Max results (default: 25)

**Dice:**
- `keyword` - Job keyword
- `location` - Location or "Remote"
- `limit` - Max results (default: 25)

**Remote Jobs:**
- `keyword` - Search term
- `limit_per_platform` - Results per board (default: 10)

**Indeed API:**
- `keywords` - List of keywords
- `locations` - List of locations
- `experience_level` - Entry, mid, senior
- `work_type` - Remote, hybrid, onsite

---

## 🛡️ Bot Detection & Best Practices

### Anti-Detection Features

All browser bots include:
- Stealth mode (hides automation markers)
- Realistic user agents
- Session persistence
- Human-like delays
- Manual login support

### Best Practices

1. **Use Manual Login**: First time login requires manual verification to avoid detection
2. **Add Delays**: Don't search too frequently (wait 5-10 minutes between searches)
3. **Rotate Platforms**: Don't hammer one platform repeatedly
4. **Use Headless Sparingly**: Visible browser is less suspicious
5. **Save Sessions**: Let bots save cookies to avoid re-login
6. **Monitor Rate Limits**: Respect platform rate limits

### Session Storage

Sessions are saved in your home directory:
- `~/.upwork_bot_session/`
- `~/.linkedin_bot_session/`
- `~/.dice_bot_session/`
- `~/.ziprecruiter_bot_session/`

To clear sessions:
```bash
rm -rf ~/.{upwork,linkedin,dice,ziprecruiter}_bot_session/
```

---

## 📈 Workflow Examples

### Daily Job Search Routine

```bash
# Morning: Search all platforms
python multi_platform_search.py search "automation developer" "Remote" 10

# Afternoon: Review queue
python multi_platform_search.py view queued

# Export to CSV for review
python multi_platform_search.py export daily_jobs.csv
```

### Platform-Specific Deep Dive

```python
# Focus on LinkedIn with AI analysis
from scripts.automation.linkedin_bot import LinkedInBot

bot = LinkedInBot(headless=False)
bot.start()
bot.login()

jobs = bot.search_jobs(keyword='automation', location='Remote', limit=50)

for job in jobs:
    details = bot.get_job_details(job['url'])
    analysis = bot.analyze_job_with_claude(details)

    if analysis['match_score'] > 70:
        cover_letter = bot.generate_cover_letter(details)
        print(f"\n✨ High Match: {details['title']}")
        print(f"Score: {analysis['match_score']}/100")
        print(f"\nCover Letter:\n{cover_letter}")
        input("Press Enter to continue...")

bot.stop()
```

### Hybrid Mode (Manual Application)

For platforms with strong bot detection:

1. Use bot to find and analyze jobs
2. Generate cover letters with AI
3. Apply manually in browser

```python
# Find and analyze
jobs = bot.search_jobs(keyword='developer', limit=10)
for job in jobs:
    details = bot.get_job_details(job['url'])
    analysis = bot.analyze_job_with_claude(details)
    if analysis['is_good_fit']:
        cover_letter = bot.generate_cover_letter(details)
        # Copy to clipboard (requires pyperclip)
        import pyperclip
        pyperclip.copy(cover_letter)
        print(f"Cover letter copied! Apply at: {job['url']}")
        input("Press Enter when done...")
```

---

## 🐛 Troubleshooting

### "No jobs found" Error

**Possible causes:**
1. Website structure changed (selectors outdated)
2. Need to log in first
3. Search returned no results

**Solutions:**
- Try with `headless=False` to see what's happening
- Check if login is required
- Try different search terms

### Login Issues

**Problem:** Can't log in / Session expired

**Solutions:**
1. Delete session files: `rm -rf ~/.{platform}_bot_session/`
2. Run with `headless=False` to log in manually
3. Check credentials in `.env` file
4. Complete CAPTCHA/2FA manually

### Rate Limiting

**Problem:** Platform blocks requests

**Solutions:**
1. Add delays between requests
2. Use different IP (VPN)
3. Switch to hybrid/manual mode
4. Wait 24 hours before retrying

### Playwright Errors

**Problem:** Browser won't start

**Solutions:**
```bash
# Reinstall browsers
playwright install chromium

# Install system dependencies
playwright install-deps
```

---

## 📚 Additional Resources

- [Upwork Bot Documentation](./WORKING_FULLTIME_WORKFLOW.md)
- [Queue Mode Guide](./QUICK_START.md)
- [Hybrid Mode Guide](./hybrid_mode.py)
- [Indeed API Docs](https://opensource.indeedeng.io/api-documentation/)
- [Playwright Docs](https://playwright.dev/python/)

---

## 🎓 Tips for Success

1. **Start Small**: Test each platform individually before running multi-platform search
2. **Customize Profiles**: Update profile data in each bot class
3. **Use AI Wisely**: Claude API costs money - use for high-value jobs
4. **Track Applications**: Update job status in queue file
5. **Be Patient**: Manual login is required first time for each platform
6. **Stay Updated**: Job board layouts change - update selectors as needed

---

## 🤝 Contributing

Found a bug or want to add a platform? Please contribute!

**Adding a new platform:**
1. Create bot in `scripts/automation/{platform}_bot.py`
2. Follow existing bot structure
3. Add credentials to `.env.example`
4. Register in `multi_platform_search.py`
5. Test thoroughly
6. Update this guide

---

## ⚠️ Disclaimer

This tool is for personal job searching only. Respect platform terms of service:
- Don't spam applications
- Don't scrape excessively
- Use manual verification when required
- Respect rate limits
- Use responsibly

**Remember:** These bots assist with job searching but should not replace genuine interest and effort in applications.

---

## 📞 Support

Having issues? Check:
1. [Troubleshooting section](#-troubleshooting) above
2. [GitHub Issues](https://github.com/Haulbrook/JobFinder/issues)
3. Existing documentation files

Good luck with your job search! 🎯
