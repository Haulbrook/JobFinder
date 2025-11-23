# JobFinder Skill Documentation

Complete documentation for the JobFinder Claude Code agent.

## Overview

JobFinder is an AI-powered job search agent that integrates with Claude Code to provide comprehensive job hunting assistance. It searches multiple platforms, analyzes job matches, and helps with applications.

## Core Components

### 1. Profile Manager (`storage/profile_manager.py`)

Manages user job search profiles with persistent storage.

**Key Methods:**
- `create_or_update(profile_data)` - Create or update profile
- `get_active_profile()` - Get current profile
- `list_profiles()` - List all profiles
- `delete_profile(profile_id)` - Remove profile

**Profile Structure:**
```python
{
    'name': str,
    'email': str,
    'skills': List[str],
    'experience_years': int,
    'desired_roles': List[str],
    'desired_locations': List[str],
    'salary_min': int,
    'work_type': str,  # remote/hybrid/onsite
    'resume_path': str,
    'linkedin_url': str (optional),
    'portfolio_url': str (optional)
}
```

### 2. Job Database (`storage/job_database.py`)

SQLite-based job storage with advanced querying.

**Key Methods:**
- `save_job(job)` - Save/update job
- `get_job(job_id)` - Retrieve job by ID
- `get_top_matches(limit, min_score)` - Get top matching jobs
- `search_jobs(filters)` - Search with filters
- `update_status(job_id, status)` - Update application status
- `get_application_stats()` - Get statistics

**Job Statuses:**
- `new` - Newly discovered
- `saved` - Saved for later
- `applied` - Application submitted
- `rejected` - Not interested
- `interview` - Interview scheduled

### 3. Job Discoverer (`search/job_discoverer.py`)

Orchestrates parallel searches across platforms.

**Features:**
- Concurrent platform searching
- Automatic deduplication
- Profile-based search parameter building
- Experience level mapping

### 4. Platform Adapters (`search/platform_adapters.py`)

Adapters for different job platforms.

**Supported Platforms:**
- LinkedIn (`LinkedInAdapter`)
- Indeed (`IndeedAdapter`)
- Glassdoor (`GlassdoorAdapter`)

**Standardized Job Format:**
```python
{
    'platform': str,
    'id': str,
    'title': str,
    'company': str,
    'location': str,
    'description': str,
    'requirements': str,
    'salary_min': int,
    'salary_max': int,
    'work_type': str,
    'url': str,
    'posted_date': str,
    'match_score': float
}
```

### 5. Job Scorer (`analysis/job_scorer.py`)

AI-powered job matching algorithm.

**Scoring Weights:**
- Skills match: 35%
- Role match: 25%
- Location match: 15%
- Salary match: 15%
- Work type match: 10%

**Score Calculation:**
- 0.0 - 0.4: Poor match
- 0.4 - 0.6: Fair match
- 0.6 - 0.8: Good match
- 0.8 - 1.0: Excellent match

### 6. Comparison Engine (`analysis/comparison_engine.py`)

Side-by-side job comparison and analysis.

**Features:**
- Multi-job comparison matrix
- Rankings by different criteria
- Pros/cons analysis
- AI-powered recommendations

### 7. Auto Applier (`application/auto_applier.py`)

Job application automation.

**Features:**
- Application preparation
- Browser-assisted application
- Platform-specific handling
- Requirements validation

### 8. Cover Letter Generator (`application/cover_letter_generator.py`)

AI-powered cover letter generation.

**Features:**
- Template-based generation
- AI enhancement (with Anthropic API)
- Job requirement extraction
- Custom message integration

## Usage Examples

### Basic Workflow

```
User: "Create my job search profile"
Assistant: [Collects profile information]

User: "Find me jobs"
Assistant: [Searches all platforms, returns top matches]

User: "Show details for job #12345"
Assistant: [Displays full job details and match analysis]

User: "Compare the top 3 jobs"
Assistant: [Provides detailed comparison]

User: "Apply to job #12345"
Assistant: [Generates cover letter, opens application]
```

### Advanced Features

**Custom Search Filters:**
```
"Find remote Python jobs in San Francisco paying over $150k"
```

**Batch Operations:**
```
"Save jobs #1, #3, and #5 for later review"
```

**Application Tracking:**
```
"Show me all jobs I've applied to this week"
```

**Profile Management:**
```
"Update my profile to include Kubernetes and increase salary to $175k"
```

## API Integration

### Required Environment Variables

```bash
# Job Platform APIs
LINKEDIN_API_KEY=your_linkedin_key
INDEED_PUBLISHER_ID=your_indeed_id
GLASSDOOR_PARTNER_ID=your_glassdoor_partner_id
GLASSDOOR_API_KEY=your_glassdoor_key

# Optional: AI Cover Letters
ANTHROPIC_API_KEY=your_anthropic_key
```

### Platform API Setup

**LinkedIn:**
1. Register at LinkedIn Developer Portal
2. Create app and get API credentials
3. Note: LinkedIn API access may require partnership

**Indeed:**
1. Register as Indeed Publisher
2. Get Publisher ID from dashboard
3. Free tier available with rate limits

**Glassdoor:**
1. Apply for Glassdoor API access
2. Get Partner ID and API Key
3. Review terms of service

## Data Storage

### File Structure
```
~/.jobfinder/
├── profiles/
│   ├── {profile_id}.json
│   └── active_profile.json
└── jobs.db (SQLite)
```

### Database Schema
```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    description TEXT,
    requirements TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    work_type TEXT,
    url TEXT,
    posted_date TEXT,
    match_score REAL,
    status TEXT DEFAULT 'new',
    data TEXT,
    discovered_at TEXT NOT NULL,
    applied_at TEXT
);
```

## Customization

### Adjusting Match Scoring Weights

Edit `scripts/analysis/job_scorer.py`:

```python
self.weights = {
    'skills_match': 0.40,      # Increase skills importance
    'role_match': 0.20,
    'location_match': 0.10,    # Decrease location importance
    'salary_match': 0.20,
    'work_type_match': 0.10
}
```

### Adding New Platforms

1. Create adapter class in `platform_adapters.py`:
```python
class NewPlatformAdapter(PlatformAdapter):
    def search(self, params: Dict) -> List[Dict]:
        # Implement search logic
        pass
```

2. Register in `main.py`:
```python
self.platforms['newplatform'] = NewPlatformAdapter()
```

### Custom Cover Letter Templates

Edit `scripts/application/cover_letter_generator.py`:

```python
def _build_template(self, job, profile, custom_message):
    # Customize template structure
    pass
```

## Error Handling

### Common Issues

**No API Keys:**
- Warning messages displayed
- Platform skipped in search
- Continues with available platforms

**Rate Limiting:**
- Automatic retry with backoff
- Queue management
- Error logging

**Network Errors:**
- Timeout handling
- Graceful degradation
- User notification

## Performance

### Optimization Features

- **Parallel Searches**: Concurrent platform queries
- **Caching**: API response caching (15 min)
- **Database Indexing**: Optimized queries
- **Batch Processing**: Efficient bulk operations

### Scalability

- SQLite handles 100k+ jobs efficiently
- Concurrent searches complete in 3-5 seconds
- Memory-efficient streaming for large results

## Privacy & Security

### Data Protection

- All data stored locally
- No cloud synchronization
- API keys in environment variables
- No telemetry or tracking

### Best Practices

1. Never commit `.env` file
2. Rotate API keys regularly
3. Review platform terms of service
4. Clear old job data periodically

## Troubleshooting

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Commands

```bash
# Check database
sqlite3 ~/.jobfinder/jobs.db "SELECT COUNT(*) FROM jobs;"

# View profiles
ls ~/.jobfinder/profiles/

# Clear cache
rm -rf ~/.jobfinder/cache/

# Reset database
rm ~/.jobfinder/jobs.db
```

## Future Enhancements

### Planned Features

1. **Email Integration**: Job alerts via email
2. **Calendar Sync**: Interview scheduling
3. **Chrome Extension**: One-click saves
4. **Analytics Dashboard**: Job market insights
5. **Salary Intelligence**: Market rate analysis
6. **Network Analysis**: Referral opportunities

### API Roadmap

- GraphQL support
- Webhook notifications
- REST API for external tools
- Export to ATS systems

## Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/Haulbrook/JobFinder.git

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black scripts/
```

### Code Style

- Follow PEP 8
- Type hints for all functions
- Docstrings for public methods
- Unit tests for new features

## Support & Resources

- **GitHub**: https://github.com/Haulbrook/JobFinder
- **Issues**: https://github.com/Haulbrook/JobFinder/issues
- **Documentation**: `/references/` directory
- **Examples**: `/examples/` directory

## License

MIT License - See LICENSE file for full text.

## Changelog

### Version 1.0.0 (Initial Release)
- Multi-platform job search
- AI-powered matching
- Profile management
- Application assistance
- SQLite storage
- Cover letter generation
