# 🤖 JobFinder Automation Setup

**Full browser automation for job applications!**

## ✅ What's Installed

- ✅ Playwright (browser automation)
- ✅ Selenium-Wire (advanced web automation)
- ✅ Upwork Bot (ready to use!)

## 🚀 Quick Start

### Step 1: Add Your Upwork Credentials

Edit the `.env` file and add your Upwork login:

```bash
# Open .env file
open .env

# Add your credentials:
UPWORK_EMAIL=your.email@example.com
UPWORK_PASSWORD=your_password_here
```

**Security:** Your `.env` file is gitignored and stays private on your machine.

### Step 2: Run the Upwork Bot

```bash
cd "/Users/thehaulbrooks/Desktop/JOB FINDER"
python scripts/automation/upwork_bot.py
```

## 🎯 What the Bot Does

### Automated Actions:
1. ✅ Opens browser (you can see everything!)
2. ✅ Logs into Upwork
3. ✅ Searches for "Google Apps Script" jobs
4. ✅ For each job:
   - Extracts job details
   - Generates custom proposal using YOUR profile
   - Shows you the proposal
   - **YOU approve** each application
   - Fills out the application form
   - Submits when you say "yes"

### Safety Features:
- ✅ **You review every application** before submission
- ✅ Browser window visible (not headless by default)
- ✅ Pause between applications
- ✅ Custom proposal for each job
- ✅ Can skip any job
- ✅ Edit proposals before sending

## ⚙️ Configuration

### .env Settings

```bash
# Browser Automation Settings
HEADLESS_MODE=false      # true = run in background, false = show browser
AUTO_SUBMIT=false        # true = auto-submit, false = you approve each
MAX_APPLICATIONS_PER_DAY=10  # Max jobs to apply to per run
```

### Recommended for First Time:
- `HEADLESS_MODE=false` - See what's happening
- `AUTO_SUBMIT=false` - You approve each application
- `MAX_APPLICATIONS_PER_DAY=5` - Start small to test

## 📋 Usage Examples

### Example 1: Apply to 5 Jobs (with approval)
```bash
# Default mode - you approve each one
python scripts/automation/upwork_bot.py
```

**What happens:**
1. Bot logs into Upwork
2. Finds 5 Google Apps Script jobs
3. For each job:
   - Shows you the job details
   - Generates a custom proposal
   - Asks: "Apply to this job? (yes/no/edit)"
   - You type "yes" to apply
   - Bot fills out and submits application
4. Reports results

### Example 2: Search Different Keywords

Edit `upwork_bot.py` line 396:
```python
keyword='workflow automation'  # Instead of 'google apps script'
```

### Example 3: Auto-Submit Mode (ADVANCED)

**Only use after testing!**

```bash
# In .env file:
AUTO_SUBMIT=true
```

Then run:
```bash
python scripts/automation/upwork_bot.py
```

Bot will apply to jobs automatically (still pauses 5 seconds between applications).

## 🎓 First Run Tutorial

### What You'll See:

```
================================================================================
🤖 UPWORK JOB APPLICATION BOT
================================================================================
For: Trey Haulbrook
Focus: Google Apps Script & Automation Projects
================================================================================

⚙️  SETTINGS:
   Headless mode: False
   Auto-submit: False
   Max applications: 5

   📋 You'll review each application before submitting

Press Enter to start...

🚀 Starting Upwork Bot...
   Headless mode: False
✅ Browser started

🔐 Logging into Upwork...
   Entering email...
   Entering password...
   Waiting for login...
✅ Login successful!

🔍 Searching for 'google apps script' jobs...
✅ Found 10 jobs
   #1: Google Apps Script Developer Needed...
   #2: Automation Expert - Google Workspace...
   #3: Script Development for Google Sheets...
   ...

🎯 Ready to apply to 5 jobs
   Auto-submit: NO (you approve each one)

================================================================================
📋 APPLICATION PREVIEW
================================================================================

🎯 JOB: Google Apps Script Developer Needed for Inventory System
💰 BUDGET: $500-1000
🔗 URL: https://www.upwork.com/jobs/...

📝 PROPOSAL:

Hi there,

I saw your project "Google Apps Script Developer Needed for Inventory System"
and I'm confident I can deliver exactly what you need.

I've been building Google Apps Script automation systems for 4+ years, with a
focus on production-ready solutions. I've built inventory automation systems
that process 500+ items daily with automated updates.

For your project, I would:
1. Review your current workflow and requirements in detail
2. Design an automation solution using Google Apps Script
3. Implement with clean, well-documented code
4. Test thoroughly to ensure reliability
5. Provide documentation and support

I estimate this would take approximately 8-12 hours at $60/hour.

I'm available to start immediately and respond within 4 hours to messages.

Looking forward to discussing your project!

Best regards,
Trey Haulbrook
Haulbrookai@gmail.com
770-530-7910

================================================================================

✅ Apply to this job? (yes/no/edit):
```

### Your Options:
- Type **yes** - Apply with this proposal
- Type **no** - Skip this job
- Type **edit** - Write your own proposal
- Type **skip** - Skip to next job

### After You Say "Yes":

```
📤 Applying to: Google Apps Script Developer Needed for Inventory System
   ✅ Proposal filled in
   ✅ Hourly rate set to $60

   ⏸️  PAUSED - Review the application in the browser
      1. Check the proposal
      2. Adjust bid/rate if needed
      3. Add any attachments
      4. Type 'submit' to continue, or 'skip' to skip this job: submit

   ⏳ Submitting...
   ✅ Application submitted successfully!

   ⏸️  Waiting 5 seconds before next application...
```

## 🎯 Tips for Success

### 1. Start Small
- First run: Apply to 2-3 jobs manually
- Review how proposals look
- Adjust if needed
- Then increase to 5-10 per session

### 2. Customize Proposals
- When bot shows proposal, type "edit" if needed
- Add specific details about the project
- Mention relevant experience
- Personalize for better response rate

### 3. Best Times to Run
- Morning (8-10 AM EST) - New jobs posted
- After lunch (1-2 PM EST) - More posts
- Evening (6-8 PM EST) - International clients

### 4. Monitor Results
- Check Upwork dashboard after each session
- Respond to messages within 2-4 hours
- Track which proposal styles get responses
- Refine your approach

## 🔧 Troubleshooting

### "Missing Upwork credentials"
→ Make sure you added UPWORK_EMAIL and UPWORK_PASSWORD to .env file

### "Login failed"
→ Check your credentials are correct
→ If 2FA is enabled, complete it in browser when prompted
→ Bot will wait 60 seconds for you to enter code

### "No jobs found"
→ Try different search keywords
→ Check Upwork website manually to confirm jobs exist
→ May need to adjust search_jobs() function

### "Apply Now button not found"
→ You may have already applied to this job
→ Job may be closed
→ Skip and continue to next job

### Browser won't close
→ Press Ctrl+C to stop
→ Close browser window manually
→ Bot will clean up on next run

## 🚀 Next Steps

### After Upwork Works:

1. **LinkedIn Automation** (Next)
   - Easy Apply bot
   - Same approval process
   - Higher volume of applications

2. **Indeed Automation**
   - Batch applications
   - Quick Apply support
   - Resume auto-upload

3. **Custom Job Boards**
   - Remote.co
   - We Work Remotely
   - AngelList/Wellfound

## 📊 Expected Results

### First Session (5 applications):
- Time: 30-45 minutes
- Learn the system
- Refine proposals
- Get comfortable with process

### Daily Sessions (10 applications):
- Time: 45-60 minutes
- Consistent applications
- Build momentum
- Track what works

### Weekly Results (50+ applications):
- Responses: 10-20 (20-40%)
- Interviews: 3-8 (6-16%)
- Offers: 1-3 (2-6%)

## 🎉 You're Ready!

Everything is set up. Just need to:
1. Add your Upwork credentials to `.env`
2. Run: `python scripts/automation/upwork_bot.py`
3. Review and approve applications
4. Land that first freelance project!

---

**Questions? Check the code comments in `scripts/automation/upwork_bot.py`**

**Want to customize? The bot is fully configurable and well-documented!**

**Ready to expand? We can add LinkedIn, Indeed, and more platforms!**
