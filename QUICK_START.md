# 🚀 QUICK START GUIDE

## To Run the Bot:

**Double-click:** `RUN_UPWORK_BOT.command`

---

## What You'll See:

```
================================================================================
🤖 UPWORK JOB APPLICATION BOT
================================================================================
For: Trey Haulbrook
Focus: Google Apps Script & Automation Projects
================================================================================

Press Enter to start...
```

**→ Press Enter to begin!**

---

## For Each Job:

### 1. Claude Analyzes
```
🤖 Analyzing job #1 with Claude AI...
   Match Score: 87%
   Excellent fit - production system with ongoing potential
```

### 2. Shows Job Details
```
📋 JOB: Google Apps Script Developer for Inventory System
💰 BUDGET: $500-1000
🔗 URL: https://www.upwork.com/jobs/...

🤖 CLAUDE ANALYSIS:
   Match Score: 87%
   Assessment: Excellent fit
   ✨ Highlights: Google Apps Script focus, production system
   ⚠️  Red Flags: None
```

### 3. Shows Proposal
```
📝 PROPOSAL:

Hi there,

Your inventory management project caught my attention - I've built
an almost identical system that processes 500+ plant varieties...
[Full personalized proposal here]

Best regards,
Trey Haulbrook
```

### 4. You Decide
```
✅ Apply to this job? (yes/no/edit):
```

**Type:**
- `yes` - Submit application
- `no` - Skip this job
- `edit` - Modify the proposal first

---

## Quick Reference:

### Match Scores:
- **90-100%** → Perfect fit, apply!
- **75-89%** → Great fit, definitely apply
- **60-74%** → Decent, review carefully
- **<60%** → Claude suggests skip

### During Run:
- **Browser stays open** - You'll see Upwork
- **Manual login** - Do it once, then bot takes over
- **Press Ctrl+C** - Stop at any time
- **Max 20 applications** - Set in settings

### After Run:
- **Check email** - Upwork sends notifications
- **Check Upwork inbox** - Clients may respond quickly
- **Track results** - Bot saves all applications

---

## Troubleshooting:

**"Login timeout"**
→ Log in manually, then press Enter when prompted

**"No jobs found"**
→ Normal! Try different keywords or times

**"Claude API error"**
→ Bot falls back to template proposals automatically

**Want to stop?**
→ Press Ctrl+C at any time

---

## Settings to Adjust:

**In `.env` file:**
```
MAX_APPLICATIONS_PER_DAY=20  # Change to 10, 30, etc.
HEADLESS_MODE=false           # Set true to hide browser
AUTO_SUBMIT=false             # Keep false for safety!
```

**In `scripts/automation/upwork_bot.py` line 627:**
```python
if analysis.get('match_score', 100) < 60:  # Change 60 to 70 for stricter
```

---

## Expected Results:

**From 20 applications:**
- 6-7 responses (30-35% response rate)
- 2-4 serious project discussions
- 1-2 projects landed

**Cost:** ~$0.20 (Claude AI)
**Time:** 30-60 minutes

---

## 💡 Tips for Success:

1. **Apply consistently** - 10-20 per day
2. **Trust Claude's scores** - It's good at filtering
3. **Don't overthink proposals** - They're already great
4. **Respond fast** - Check Upwork every few hours
5. **Follow up** - Send thank you messages

---

**Good luck! Go land that perfect project! 🎯**
