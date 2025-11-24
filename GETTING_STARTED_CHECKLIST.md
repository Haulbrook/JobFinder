# Getting Started Checklist

Quick setup guide for your multi-platform job search system.

## ✅ Setup Checklist

### 1. Environment Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Add `ANTHROPIC_API_KEY` (get free key at https://console.anthropic.com/)
- [ ] Add credentials for platforms you want to use (see below)
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Install Playwright: `playwright install chromium`

### 2. Configure Platforms (Choose which to enable)

#### Option A: LinkedIn + Indeed (Recommended starter)
- [ ] Add `LINKEDIN_EMAIL` to `.env`
- [ ] Add `LINKEDIN_PASSWORD` to `.env`
- [ ] Sign up for Indeed Publisher ID at https://www.indeed.com/publisher
- [ ] Add `INDEED_PUBLISHER_ID` to `.env`

#### Option B: All Platforms
- [ ] LinkedIn credentials (email, password)
- [ ] Upwork credentials (email, password)
- [ ] Indeed Publisher ID (free API)
- [ ] Dice credentials (optional - works without)
- [ ] ZipRecruiter credentials (optional - works without)

### 3. First Run
- [ ] Run: `python multi_platform_search.py search`
- [ ] Complete manual login for each platform (first time only)
- [ ] Verify sessions are saved
- [ ] Check `multi_platform_queue.json` was created

### 4. Test Individual Platforms (Optional)
- [ ] Test LinkedIn: `python scripts/automation/linkedin_bot.py`
- [ ] Test Dice: `python scripts/automation/dice_bot.py`
- [ ] Test Remote Jobs: `python scripts/automation/remote_jobs_bot.py`
- [ ] Test ZipRecruiter: `python scripts/automation/ziprecruiter_bot.py`

### 5. Customize Your Profile
Edit these files to match your info:
- [ ] `scripts/automation/linkedin_bot.py` (lines 48-59)
- [ ] `scripts/automation/dice_bot.py` (lines 37-45)
- [ ] `scripts/automation/ziprecruiter_bot.py` (lines 37-45)
- [ ] `scripts/automation/upwork_bot.py` (lines 42-56)

### 6. Daily Usage
- [ ] Run multi-platform search: Double-click `RUN_MULTI_PLATFORM_SEARCH.bat`
- [ ] View queue: Double-click `VIEW_JOB_QUEUE.bat`
- [ ] Export to CSV: Double-click `EXPORT_JOBS.bat`
- [ ] Review jobs and update statuses in queue file

---

## 🚀 Quick Commands Reference

```bash
# Search all platforms
python multi_platform_search.py search "your job title" "Remote" 10

# View all jobs
python multi_platform_search.py view

# View only queued jobs
python multi_platform_search.py view queued

# Export to CSV
python multi_platform_search.py export jobs.csv
```

---

## 📋 Minimum Setup (Fast Start)

Want to get started in 5 minutes? Just do this:

1. **Create `.env` file:**
```bash
cp .env.example .env
```

2. **Add Claude AI key** (get free tier at console.anthropic.com):
```
ANTHROPIC_API_KEY=your_key_here
```

3. **Run without login** (uses public job boards only):
```bash
python multi_platform_search.py search "developer" "Remote" 10
```

This will search:
- ✅ Remote.co
- ✅ We Work Remotely
- ✅ Remote OK
- ✅ Dice.com (public listings)

No login required!

---

## 🎯 Recommended First Search

```bash
# Search for your role
python multi_platform_search.py search "automation developer" "Remote" 15

# View results
python multi_platform_search.py view

# Export to review in Excel/Google Sheets
python multi_platform_search.py export first_search.csv
```

---

## ❗ Common First-Time Issues

### "No module named 'playwright'"
**Fix:** `pip install playwright && playwright install chromium`

### "Missing credentials"
**Fix:** Add credentials to `.env` file (copy from `.env.example`)

### "Login failed"
**Fix:** Run with visible browser first time to complete manual login

### "No jobs found"
**Fix:** Try different search terms or check if platform needs login

---

## 📞 Need Help?

1. Check [MULTI_PLATFORM_GUIDE.md](./MULTI_PLATFORM_GUIDE.md) for detailed docs
2. See [PLATFORMS_ADDED.md](./PLATFORMS_ADDED.md) for what was added
3. Review troubleshooting section in guide

---

## ✨ Next Steps After Setup

Once everything is working:

1. **Customize search terms** for your target roles
2. **Run daily searches** to build your job pipeline
3. **Use AI analysis** on promising jobs (Claude API)
4. **Generate cover letters** with AI
5. **Track applications** in the queue system

---

**Ready to start? Run this:**
```bash
python multi_platform_search.py search
```

Good luck! 🎯
