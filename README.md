# JobFinder - AI-Powered Job Search Agent

JobFinder is an intelligent job search agent for Claude Code that helps you find, analyze, and apply to jobs matching your profile across multiple platforms.

## Features

### 🎯 Intelligent Job Discovery
- Multi-platform search (LinkedIn, Indeed, Glassdoor)
- Automated job discovery based on your profile
- Real-time job notifications
- Smart deduplication across platforms

### 📊 Advanced Job Analysis
- AI-powered match scoring
- Skills and requirements analysis
- Salary comparison
- Side-by-side job comparison
- Personalized recommendations

### 📝 Application Assistance
- AI-generated cover letters
- Auto-fill application forms (where supported)
- Application tracking
- Interview preparation tips

### 💾 Smart Data Management
- Persistent job database
- Profile management
- Application history tracking
- Export capabilities

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Haulbrook/JobFinder.git
cd JobFinder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys (see [API Setup Guide](references/API_SETUP.md)):
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Add to Claude Code:
```bash
# In Claude Code
/plugin marketplace add ./
```

## Quick Start

### 1. Create Your Profile
```
"Create my job search profile with the following:
- Name: John Doe
- Skills: Python, React, AWS, Docker
- Experience: 5 years
- Desired roles: Senior Software Engineer, Tech Lead
- Locations: San Francisco, Remote
- Salary: $150,000+
- Work type: Remote"
```

### 2. Search for Jobs
```
"Find me jobs that match my profile"
```

### 3. View Top Matches
```
"Show me the top 10 matching jobs"
```

### 4. Compare Jobs
```
"Compare jobs #1, #2, and #3"
```

### 5. Apply to a Job
```
"Apply to job #1 with a custom cover letter highlighting my AWS experience"
```

## Configuration

### API Keys Required

- **LinkedIn API**: For LinkedIn job searches
- **Indeed Publisher ID**: For Indeed job searches
- **Glassdoor API**: For Glassdoor job searches
- **Anthropic API**: For AI-powered cover letters (optional)

See [API_SETUP.md](references/API_SETUP.md) for detailed setup instructions.

## How It Works

1. **Profile Creation**: JobFinder stores your skills, preferences, and requirements
2. **Job Discovery**: Searches multiple platforms using your profile
3. **Smart Scoring**: Analyzes each job against your profile (skills, location, salary, etc.)
4. **Storage**: Saves jobs to local database with match scores
5. **Analysis**: Provides comparisons and recommendations
6. **Application**: Assists with cover letters and application submission

## Architecture

```
JobFinder/
├── scripts/
│   ├── main.py                  # Main orchestration
│   ├── storage/                 # Profile & data management
│   │   ├── profile_manager.py   # User profiles
│   │   └── job_database.py      # Job storage (SQLite)
│   ├── search/                  # Job discovery
│   │   ├── job_discoverer.py    # Multi-platform search
│   │   └── platform_adapters.py # Platform integrations
│   ├── analysis/                # Job analysis
│   │   ├── job_scorer.py        # Match scoring
│   │   └── comparison_engine.py # Job comparison
│   └── application/             # Application automation
│       ├── auto_applier.py      # Application submission
│       └── cover_letter_generator.py # AI cover letters
└── references/                  # Documentation
```

## Data Storage

JobFinder stores data locally in `~/.jobfinder/`:
- `profiles/` - Your job search profiles
- `jobs.db` - SQLite database of discovered jobs

## Privacy & Security

- All data stored locally on your machine
- API keys stored in `.env` file (not committed to git)
- No data sent to third parties except job platforms
- Optional AI features require Anthropic API key

## Roadmap

- [ ] Additional platform support (ZipRecruiter, Monster, etc.)
- [ ] Browser automation for one-click applications
- [ ] Email alerts for new matching jobs
- [ ] Interview preparation assistant
- [ ] Salary negotiation guidance
- [ ] Application follow-up reminders
- [ ] Integration with calendar for interview scheduling

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- GitHub Issues: https://github.com/Haulbrook/JobFinder/issues
- Documentation: [USER_GUIDE.md](references/USER_GUIDE.md)

## Acknowledgments

Built with:
- Claude Code - Anthropic's AI coding assistant
- Python 3.x
- SQLite for data storage
- Various job platform APIs
