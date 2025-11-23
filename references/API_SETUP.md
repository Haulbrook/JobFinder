# API Setup Guide

Complete guide for setting up API credentials for JobFinder.

## Overview

JobFinder integrates with multiple job platforms and services. This guide walks you through obtaining and configuring API credentials.

## Required APIs

### 1. LinkedIn API

**Purpose**: Search LinkedIn job postings

**Setup Steps:**

1. **Create LinkedIn Developer Account**
   - Go to https://www.linkedin.com/developers/
   - Sign in with your LinkedIn account
   - Accept Developer Terms of Service

2. **Create an App**
   - Click "Create App"
   - Fill in app details:
     - App name: "JobFinder"
     - LinkedIn Page: Your company/personal page
     - Privacy policy URL: (required)
     - App logo: (optional)

3. **Get API Credentials**
   - Navigate to "Auth" tab
   - Copy "Client ID" and "Client Secret"
   - Note: LinkedIn has restricted API access; you may need to apply for partnership

4. **Configure Products**
   - Request "Sign In with LinkedIn" product
   - Request "Jobs" product (if available)

**Alternative**: Use LinkedIn's public job search or services like RapidAPI's LinkedIn API

**Environment Variable:**
```bash
LINKEDIN_API_KEY=your_client_secret_here
```

### 2. Indeed API

**Purpose**: Search Indeed job listings

**Setup Steps:**

1. **Register as Publisher**
   - Go to https://www.indeed.com/publisher
   - Click "Sign Up"
   - Fill in registration form
   - Agree to terms of service

2. **Get Publisher ID**
   - Log in to Publisher Portal
   - Navigate to "Account" or "Settings"
   - Copy your Publisher ID

3. **Review Documentation**
   - Read API documentation: https://opensource.indeedeng.io/api-documentation/
   - Note rate limits and usage guidelines
   - Review prohibited use cases

**Environment Variables:**
```bash
INDEED_PUBLISHER_ID=your_publisher_id_here
```

**API Endpoint:**
```
https://api.indeed.com/ads/apisearch
```

**Rate Limits:**
- Free tier: Limited queries per day
- Check current limits in your publisher dashboard

### 3. Glassdoor API

**Purpose**: Search Glassdoor job postings and company reviews

**Setup Steps:**

1. **Apply for API Access**
   - Go to https://www.glassdoor.com/developer/index.htm
   - Click "Request API Access"
   - Fill in application form:
     - Describe your use case
     - Provide business information
     - Explain how you'll use the data

2. **Wait for Approval**
   - Glassdoor reviews applications manually
   - Approval can take 1-2 weeks
   - Check email for approval notification

3. **Get Credentials**
   - Once approved, log in to Developer Portal
   - Copy Partner ID and API Key

4. **Review Terms**
   - Attribution requirements
   - Data usage restrictions
   - Display guidelines

**Environment Variables:**
```bash
GLASSDOOR_PARTNER_ID=your_partner_id_here
GLASSDOOR_API_KEY=your_api_key_here
```

**Note**: Glassdoor has strict terms of service. Review carefully before using.

## Optional APIs

### 4. Anthropic API (Claude)

**Purpose**: AI-powered cover letter generation and job analysis

**Setup Steps:**

1. **Create Anthropic Account**
   - Go to https://console.anthropic.com/
   - Sign up or log in
   - Verify your email

2. **Get API Key**
   - Navigate to "API Keys" section
   - Click "Create Key"
   - Copy the API key (shown only once!)
   - Store securely

3. **Set Up Billing**
   - Add payment method
   - Choose plan (Pay-as-you-go or subscription)
   - Review pricing: https://www.anthropic.com/pricing

**Environment Variable:**
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

**Usage in JobFinder:**
- Cover letter enhancement
- Job description analysis
- Personalized recommendations
- Interview preparation

## Alternative Services

If official APIs are unavailable or restrictive:

### RapidAPI

Many job platform APIs available through RapidAPI:
- Go to https://rapidapi.com/
- Search for "LinkedIn Jobs API", "Indeed API", etc.
- Subscribe to APIs
- Get RapidAPI key
- Modify adapter code to use RapidAPI endpoints

### Web Scraping (Use with Caution)

If APIs unavailable, consider:
- **SerpAPI**: Google Jobs search API
- **ScraperAPI**: Proxy-based scraping
- **Bright Data**: Job data feeds

**Important**: Always review terms of service and robots.txt before scraping.

## Environment Configuration

### 1. Create .env File

Copy the example file:
```bash
cp .env.example .env
```

### 2. Edit .env File

```bash
# Job Platform APIs
LINKEDIN_API_KEY=sk-linkedin-xxxxxxxxxxxxx
INDEED_PUBLISHER_ID=1234567890
GLASSDOOR_PARTNER_ID=123456
GLASSDOOR_API_KEY=xxxxxxxxxx

# Optional: AI Features
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Optional: Additional Services
RAPIDAPI_KEY=xxxxxxxxxxxxx
SERPAPI_KEY=xxxxxxxxxxxxx
```

### 3. Security Best Practices

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Set appropriate permissions
chmod 600 .env

# Use environment variables in production
export $(cat .env | xargs)
```

## Testing API Connections

### Test Script

Create `test_apis.py`:

```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_linkedin():
    api_key = os.getenv('LINKEDIN_API_KEY')
    if api_key:
        print("✓ LinkedIn API key configured")
    else:
        print("✗ LinkedIn API key missing")

def test_indeed():
    publisher_id = os.getenv('INDEED_PUBLISHER_ID')
    if publisher_id:
        # Test Indeed API
        url = "https://api.indeed.com/ads/apisearch"
        params = {
            'publisher': publisher_id,
            'q': 'python',
            'l': 'san francisco',
            'format': 'json',
            'v': '2',
            'limit': 1
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("✓ Indeed API working")
            else:
                print(f"✗ Indeed API error: {response.status_code}")
        except Exception as e:
            print(f"✗ Indeed API error: {e}")
    else:
        print("✗ Indeed Publisher ID missing")

def test_anthropic():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print("✓ Anthropic API key configured")
    else:
        print("⚠ Anthropic API key missing (optional)")

if __name__ == "__main__":
    print("Testing API Connections...\n")
    test_linkedin()
    test_indeed()
    test_anthropic()
```

Run tests:
```bash
python test_apis.py
```

## Rate Limits & Best Practices

### Indeed
- **Limit**: Varies by account (typically 1000/day free tier)
- **Best Practice**: Cache results, limit searches
- **Monitoring**: Check publisher dashboard

### LinkedIn
- **Limit**: Based on app permissions
- **Best Practice**: Use OAuth, respect rate limits
- **Monitoring**: Check API response headers

### Glassdoor
- **Limit**: Defined in partnership agreement
- **Best Practice**: Review attribution requirements
- **Monitoring**: Track API usage

### Anthropic (Claude)
- **Limit**: Based on plan
- **Cost**: ~$3 per million tokens (Claude Haiku)
- **Best Practice**: Cache cover letters, use templates
- **Monitoring**: Check console.anthropic.com

## Troubleshooting

### Common Issues

**401 Unauthorized:**
- Check API key is correct
- Verify key hasn't expired
- Check account status

**429 Rate Limited:**
- Reduce request frequency
- Implement exponential backoff
- Upgrade API plan

**403 Forbidden:**
- Check API permissions
- Review terms of service
- Verify account approval

**Connection Errors:**
- Check internet connection
- Verify API endpoint URLs
- Check firewall settings

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Cost Estimation

### Free Tier Usage

- **Indeed**: ~1000 searches/day
- **LinkedIn**: Limited (varies)
- **Glassdoor**: Varies by agreement
- **Anthropic**: $5 free credit (new accounts)

### Typical Monthly Costs

**Light Usage** (10 searches/day):
- Indeed: Free
- LinkedIn: Free (if available)
- Glassdoor: Free (if available)
- Anthropic: ~$5-10 (cover letters)
- **Total**: $5-10/month

**Heavy Usage** (100 searches/day):
- Indeed: May need paid tier
- LinkedIn: Varies
- Glassdoor: Varies
- Anthropic: ~$20-30
- **Total**: $30-50/month

## Privacy & Data Usage

### API Data Collection

- Job listings (public data)
- User profile (stored locally)
- Search queries (sent to platforms)
- Application data (stored locally)

### Third-Party Data Sharing

- JobFinder doesn't share data with third parties
- Platform APIs collect search analytics
- Review each platform's privacy policy

### GDPR Compliance

- All data stored locally
- User controls all data
- Data deletion available
- Export capabilities included

## Support & Resources

### Platform Documentation

- **Indeed**: https://opensource.indeedeng.io/api-documentation/
- **LinkedIn**: https://docs.microsoft.com/en-us/linkedin/
- **Glassdoor**: https://www.glassdoor.com/developer/
- **Anthropic**: https://docs.anthropic.com/

### Community Resources

- Stack Overflow tags: `indeed-api`, `linkedin-api`
- Reddit: r/jobsearching, r/APIs
- GitHub: Search for job search projects

## Updates & Maintenance

### Keeping APIs Current

1. **Monitor Platform Changes**
   - Subscribe to API newsletters
   - Check developer blogs
   - Review changelog regularly

2. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Test Regularly**
   - Run test suite monthly
   - Verify API responses
   - Check for deprecation notices

### Version Compatibility

- JobFinder tracks API versions
- Update platform adapters as needed
- Review migration guides

## Getting Help

### Issues with APIs

1. **Check API Status**: Platform status pages
2. **Review Documentation**: Official docs
3. **Search Community**: Stack Overflow, forums
4. **Contact Support**: Platform support teams

### JobFinder Issues

- GitHub Issues: https://github.com/Haulbrook/JobFinder/issues
- Documentation: This guide and SKILL.md
- Community: Discussions tab

---

Last updated: 2024
For the latest information, check platform documentation and JobFinder repository.
