# JobFinder User Guide

Complete guide to using JobFinder for your job search.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Your Profile](#creating-your-profile)
3. [Searching for Jobs](#searching-for-jobs)
4. [Analyzing Results](#analyzing-results)
5. [Applying to Jobs](#applying-to-jobs)
6. [Managing Applications](#managing-applications)
7. [Advanced Features](#advanced-features)
8. [Tips & Best Practices](#tips--best-practices)

## Getting Started

### Installation

1. Ensure JobFinder is installed:
```bash
cd /path/to/JobFinder
pip install -r requirements.txt
```

2. Configure API keys (see [API_SETUP.md](API_SETUP.md))

3. Verify installation:
```bash
python scripts/main.py
```

### First Run

When you first use JobFinder, you'll need to create a profile.

## Creating Your Profile

### Basic Profile

The simplest way to create a profile:

```
"Create my job search profile:
- Name: Jane Smith
- Email: jane.smith@email.com
- Skills: Python, JavaScript, React, Node.js, AWS
- Experience: 5 years
- Desired roles: Software Engineer, Full Stack Developer
- Locations: New York, Remote
- Minimum salary: $120,000
- Work type: Remote"
```

### Detailed Profile

For better job matching, include more details:

```
"Create my job search profile with:
- Name: Jane Smith
- Email: jane.smith@email.com
- Phone: 555-0123
- Skills: Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL, MongoDB, Redis, CI/CD, Git
- Experience: 5 years
- Desired roles: Senior Software Engineer, Full Stack Developer, Backend Engineer, Tech Lead
- Desired locations: New York City, San Francisco, Austin, Remote
- Minimum salary: $140,000
- Maximum salary: $180,000
- Work type: Remote
- Resume path: /Users/jane/Documents/resume.pdf
- LinkedIn: https://linkedin.com/in/janesmith
- Portfolio: https://janesmith.dev
- GitHub: https://github.com/janesmith"
```

### Updating Your Profile

Update specific fields:

```
"Update my profile to increase minimum salary to $150,000"

"Add TypeScript and GraphQL to my skills"

"Change work type preference to hybrid"
```

### Managing Multiple Profiles

Create different profiles for different job types:

```
"Create a new profile for frontend roles"
"Switch to my backend engineer profile"
"List all my profiles"
"Delete my old profile"
```

## Searching for Jobs

### Basic Search

Search using your active profile:

```
"Find me jobs"
"Search for jobs matching my profile"
"Look for new job opportunities"
```

JobFinder will:
- Search all configured platforms (LinkedIn, Indeed, Glassdoor)
- Match jobs to your profile
- Calculate match scores
- Save results to database

### Custom Search Filters

Override profile settings for specific searches:

```
"Find remote Python jobs in Seattle"

"Search for senior engineer roles paying over $150k"

"Look for contract positions in fintech"

"Find jobs at startups in San Francisco"
```

### Platform-Specific Search

Search specific platforms:

```
"Search LinkedIn for software engineer jobs"
"Find jobs on Indeed in New York"
"Search Glassdoor for companies with good ratings"
```

## Analyzing Results

### Viewing Top Matches

```
"Show me the top 10 matching jobs"
"Display my best job matches"
"What are the highest-scoring jobs?"
```

Output includes:
- Match score (0-100%)
- Job title and company
- Location and work type
- Salary range (if available)
- Key requirements match

### Detailed Job View

```
"Show details for job #12345"
"Tell me more about the Netflix Senior Engineer position"
"What are the requirements for job #3?"
```

Detailed view shows:
- Full job description
- Requirements and qualifications
- Company information
- Match breakdown by category
- Pros and cons based on your profile

### Comparing Jobs

Compare multiple jobs side-by-side:

```
"Compare jobs #1, #2, and #3"
"Compare the top 3 jobs"
"Show me a comparison of Google, Meta, and Amazon positions"
```

Comparison includes:
- Match scores
- Salary ranges
- Work arrangements
- Location differences
- Pros and cons for each
- Recommendation

### Filtering Results

```
"Show only remote jobs with match score above 80%"
"Filter for jobs paying over $150k"
"Show jobs posted in the last week"
"Display only jobs I've saved"
```

## Applying to Jobs

### Generating Cover Letters

```
"Generate a cover letter for job #12345"

"Create a cover letter for the Google position highlighting my cloud experience"

"Write a cover letter emphasizing my leadership skills"
```

The AI will:
- Analyze job requirements
- Match with your profile
- Generate personalized letter
- Include relevant achievements
- Suggest customizations

### Submitting Applications

```
"Apply to job #12345"
"Submit application for the Netflix position"
"Apply to job #12345 with a custom message about my open source work"
```

JobFinder will:
- Generate cover letter
- Prepare application data
- Open job URL in browser
- Assist with form filling (where supported)
- Mark job as "applied" in database

### Application Assistance

```
"What do I need to apply to this job?"
"Check if I can auto-apply to job #12345"
"Prepare application materials for Meta position"
```

## Managing Applications

### Tracking Applications

```
"Show all jobs I've applied to"
"List applications from this week"
"Show my application statistics"
```

### Updating Status

```
"Mark job #12345 as interview scheduled"
"Update job #67890 status to rejected"
"Save job #11111 for later"
```

**Available Statuses:**
- `new` - Just discovered
- `saved` - Saved for review
- `applied` - Application submitted
- `interview` - Interview scheduled
- `rejected` - Decided not to pursue

### Application Stats

```
"Show my job search statistics"
"How many jobs have I applied to?"
"What's my average match score?"
```

Statistics include:
- Total jobs discovered
- Applications submitted
- Average match score
- Jobs by status
- Platform breakdown

## Advanced Features

### Custom Scoring Weights

Adjust what matters most in job matching:

```python
# Edit scripts/analysis/job_scorer.py
self.weights = {
    'skills_match': 0.40,      # Prioritize skills
    'role_match': 0.20,
    'location_match': 0.05,    # Location less important
    'salary_match': 0.25,      # Salary more important
    'work_type_match': 0.10
}
```

### Saved Searches

Create reusable search queries:

```
"Save this search as 'Remote Python Senior'"
"Run my saved search 'Remote Python Senior'"
"List my saved searches"
```

### Batch Operations

Perform operations on multiple jobs:

```
"Save jobs #1, #3, #5, and #7 for later"
"Mark jobs #10-15 as not interested"
"Apply to all jobs with match score above 90%"
```

### Exporting Data

Export job data for external analysis:

```
"Export all jobs to CSV"
"Export my applications to JSON"
"Save top 20 jobs to spreadsheet"
```

### Scheduling Searches

Set up automated searches:

```
"Search for new jobs every morning at 9am"
"Send me weekly job digest"
"Alert me when high-match jobs are found"
```

## Tips & Best Practices

### Profile Optimization

1. **Be Specific with Skills**
   - List all relevant technologies
   - Include frameworks and tools
   - Add soft skills if relevant

2. **Multiple Job Titles**
   - List variations (Engineer, Developer, etc.)
   - Include seniority levels you're open to
   - Consider related roles

3. **Location Flexibility**
   - Include all acceptable cities
   - Specify remote preference
   - Consider hybrid options

4. **Realistic Salary Range**
   - Research market rates
   - Account for location differences
   - Include minimum you'll accept

### Search Strategy

1. **Regular Searches**
   - Run searches daily or weekly
   - Jobs appear and disappear quickly
   - Early applications get more attention

2. **Cast Wide Net**
   - Don't filter too strictly initially
   - Review lower match scores
   - Hidden opportunities exist

3. **Multiple Platforms**
   - Different jobs on each platform
   - Some companies favor certain sites
   - Maximize coverage

### Application Strategy

1. **Quality Over Quantity**
   - Focus on 70%+ match scores
   - Customize cover letters
   - Research companies first

2. **Timing Matters**
   - Apply early in job posting lifecycle
   - Weekday mornings get more attention
   - Follow up after 1 week

3. **Personalization**
   - Mention specific company projects
   - Reference job requirements
   - Show genuine interest

### Organization

1. **Regular Database Cleanup**
   - Archive old searches
   - Remove irrelevant jobs
   - Update application statuses

2. **Notes and Tags**
   ```
   "Add note to job #12345: Great company culture, spoke with recruiter"
   "Tag job #67890 as priority"
   ```

3. **Follow-up Reminders**
   ```
   "Remind me to follow up on Meta application in 1 week"
   "Set reminder to prepare for Google interview"
   ```

## Common Workflows

### Daily Job Hunter

```
Morning routine:
1. "Find new jobs posted yesterday"
2. "Show me jobs with 80%+ match"
3. "Compare the top 3"
4. "Apply to job #[best match]"
5. "Save jobs #[others] for review"
```

### Targeted Search

```
Focused search:
1. "Find senior Python roles at FAANG companies"
2. "Filter for remote only with $150k+ salary"
3. "Show detailed comparison of top 5"
4. "Generate cover letters for top 3"
5. "Apply to all with custom messages"
```

### Weekly Review

```
Weekend review:
1. "Show application statistics for this week"
2. "List all saved jobs"
3. "Review jobs I applied to"
4. "Update statuses based on responses"
5. "Plan applications for next week"
```

## Troubleshooting

### No Jobs Found

**Possible causes:**
- Profile too restrictive
- API keys not configured
- Platform temporarily down
- No matching jobs available

**Solutions:**
```
"Broaden my search criteria"
"Search without salary filter"
"Try specific platforms individually"
"Check API configuration"
```

### Low Match Scores

**Possible causes:**
- Skills mismatch
- Location restrictions
- Salary expectations
- Experience level

**Solutions:**
```
"Update my skills to include [missing tech]"
"Expand location preferences"
"Lower salary minimum temporarily"
"Review job requirements manually"
```

### Application Errors

**Possible causes:**
- Missing resume file
- Invalid profile data
- Platform restrictions
- Network issues

**Solutions:**
```
"Update resume path in profile"
"Verify profile completeness"
"Try manual application"
"Check internet connection"
```

## Getting Help

### In-App Help

```
"How do I use JobFinder?"
"What commands are available?"
"Explain match scoring"
"Show example searches"
```

### Documentation

- **API Setup**: [API_SETUP.md](API_SETUP.md)
- **Technical Details**: [SKILL.md](../SKILL.md)
- **README**: [README.md](../README.md)

### Community Support

- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share tips
- Examples: Check `/examples` directory

## Privacy & Data

### What's Stored

- Your profile information (local only)
- Job listings discovered
- Search history
- Application tracking
- Cover letters generated

### What's Shared

- Search queries (with job platforms)
- API requests (with configured services)
- Nothing shared with third parties

### Data Control

```
"Delete all my data"
"Export my profile"
"Clear job database"
"Remove old applications"
```

## Keyboard Shortcuts & Commands

Quick commands for common tasks:

```
/jobs search              # Quick search
/jobs top                 # Show top matches
/jobs status              # Application stats
/profile update           # Update profile
/help jobfinder           # Show help
```

## Advanced Customization

### Custom Filters

Create complex filter logic:

```python
# In scripts/search/job_discoverer.py
def custom_filter(self, jobs):
    return [
        job for job in jobs
        if job.get('company') in PREFERRED_COMPANIES
        and job.get('match_score') > 0.75
        and 'remote' in job.get('work_type', '')
    ]
```

### Integration with Other Tools

**Calendar Integration:**
```python
# Add interview to calendar
from gcsa.google_calendar import GoogleCalendar
```

**Email Notifications:**
```python
# Send job alerts via email
import smtplib
from email.mime.text import MIMEText
```

**Slack Integration:**
```python
# Post high-match jobs to Slack
from slack_sdk import WebClient
```

## FAQ

**Q: How often should I run searches?**
A: Daily for active search, weekly for passive search.

**Q: What's a good match score?**
A: 70%+ is good, 80%+ is excellent, 90%+ is perfect.

**Q: Should I apply to jobs below 70% match?**
A: Only if something specific interests you.

**Q: How many jobs should I apply to?**
A: Quality over quantity. 5-10 well-targeted applications better than 50 random ones.

**Q: Can I use JobFinder for freelance work?**
A: Yes, configure platforms like Upwork and Freelancer.

**Q: Is my data safe?**
A: Yes, everything stored locally. No cloud sync.

**Q: Can I use JobFinder in multiple locations?**
A: Yes, sync profile via git or export/import.

## Next Steps

1. **Create your profile** with detailed information
2. **Run your first search** with broad criteria
3. **Review and refine** based on results
4. **Apply to top matches** with customized materials
5. **Track progress** and adjust strategy

Happy job hunting! 🎯

---

For technical questions, see [SKILL.md](../SKILL.md)
For API setup, see [API_SETUP.md](API_SETUP.md)
For issues, visit https://github.com/Haulbrook/JobFinder/issues
