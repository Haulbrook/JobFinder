"""Test Claude AI integration without browser automation"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from anthropic import Anthropic

print("="*80)
print("🤖 CLAUDE AI INTEGRATION TEST")
print("="*80)

# Initialize Claude
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if not anthropic_key:
    print("❌ No Claude API key found")
    sys.exit(1)

claude_client = Anthropic(api_key=anthropic_key)
print("\n✅ Claude client initialized")

# Test job (realistic example)
test_job = {
    'title': 'Google Apps Script Developer for Inventory Management System',
    'description': '''We need an experienced Google Apps Script developer to build an automated inventory management system for our wholesale plant nursery.

Requirements:
- Automate pricing updates from 3 supplier websites
- Integrate with our existing Google Sheets workflow
- Handle 500+ plant varieties with daily price changes
- Set up error notifications and data validation
- Experience with web scraping and data enrichment APIs

Budget: $800-1200
Timeline: 2-3 weeks
This is a production system that will need ongoing maintenance and feature additions.

Please share examples of similar automation projects you've built.''',
    'budget': '$800-1200',
    'url': 'https://www.upwork.com/jobs/example'
}

# Profile info (from TREY_PROFILE.md)
profile = {
    'name': 'Trey Haulbrook',
    'hourly_rate': 60,
    'skills': ['Google Apps Script (Advanced)', 'JavaScript', 'Python', 'Web Scraping', 'API Integration'],
    'experience': [
        {
            'title': 'Wholesale Plant Inventory Automation',
            'description': 'Automated pricing system processing 500+ plant varieties from multiple wholesalers with web scraping, data enrichment, and Google Sheets integration'
        },
        {
            'title': 'Crew Scheduling & Communication Bot',
            'description': 'Google Apps Script system managing 25+ crew members with Slack integration and automated scheduling'
        }
    ]
}

print("\n" + "="*80)
print("📋 TEST JOB:")
print("="*80)
print(f"Title: {test_job['title']}")
print(f"Budget: {test_job['budget']}")
print(f"\nDescription Preview:")
print(test_job['description'][:200] + "...")

# Test 1: Job Analysis
print("\n" + "="*80)
print("🔍 TEST 1: CLAUDE JOB ANALYSIS")
print("="*80)
print("\n⏳ Analyzing job with Claude AI...")

try:
    analysis_response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Analyze this Upwork job posting for Trey, a Google Apps Script automation specialist.

Job Title: {test_job['title']}
Budget: {test_job['budget']}
Description: {test_job['description']}

Trey's Profile:
- Expert in: Google Apps Script, JavaScript, web scraping, API integration
- Hourly Rate: ${profile['hourly_rate']}
- Key Project: Built inventory automation for 500+ plant varieties with supplier data scraping and Google Sheets integration
- Looking for: Interesting technical challenges, production systems, ongoing work potential, good clients

Analyze if this is a good fit and provide:
1. Match score (0-100) based on skills match, interesting work, and client quality
2. Whether it's a good fit (true/false)
3. Brief reason why/why not
4. 2-3 highlights (what makes this appealing)
5. Any red flags (concerns)

Return as JSON:
{{
  "match_score": 85,
  "is_good_fit": true,
  "reason": "Brief explanation",
  "highlights": ["Point 1", "Point 2"],
  "red_flags": ["Concern 1"] or []
}}"""
        }]
    )

    # Extract and parse JSON response
    import json
    analysis_text = analysis_response.content[0].text
    # Find JSON in response
    json_start = analysis_text.find('{')
    json_end = analysis_text.rfind('}') + 1
    analysis = json.loads(analysis_text[json_start:json_end])

    print(f"\n✅ Analysis Complete!\n")
    print(f"   🎯 Match Score: {analysis['match_score']}%")
    print(f"   {'✅' if analysis['is_good_fit'] else '❌'} Good Fit: {analysis['is_good_fit']}")
    print(f"   📝 Reason: {analysis['reason']}")

    if analysis.get('highlights'):
        print(f"\n   ✨ Highlights:")
        for highlight in analysis['highlights']:
            print(f"      • {highlight}")

    if analysis.get('red_flags'):
        print(f"\n   ⚠️  Red Flags:")
        for flag in analysis['red_flags']:
            print(f"      • {flag}")
    else:
        print(f"\n   ✅ No red flags detected")

except Exception as e:
    print(f"❌ Analysis failed: {e}")
    sys.exit(1)

# Test 2: Proposal Generation
print("\n" + "="*80)
print("✍️  TEST 2: CLAUDE PROPOSAL GENERATION")
print("="*80)
print("\n⏳ Generating personalized proposal with Claude AI...")

try:
    proposal_response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""Write a highly personalized Upwork proposal for this job.

Job: {test_job['title']}
Description: {test_job['description']}
Budget: {test_job['budget']}

Write as Trey Haulbrook:
- Expert in Google Apps Script automation
- Built an almost identical system: inventory automation for 500+ plant varieties with supplier data scraping and Google Sheets
- Also built crew scheduling system with Slack integration
- Hourly rate: ${profile['hourly_rate']}
- Contact: Haulbrookai@gmail.com, 770-530-7910

Requirements:
- Start with confidence and relevance to THEIR specific project
- Reference the most relevant project (the inventory automation is PERFECT for this!)
- Show you understand their problem
- Mention measurable results from your similar project
- Brief technical approach (4-5 steps)
- Time/cost estimate based on ${profile['hourly_rate']}/hour
- Professional but friendly tone
- 200-300 words
- End with contact info

Be specific about the inventory system you built - this is the exact same use case!"""
        }]
    )

    proposal = proposal_response.content[0].text.strip()

    print(f"\n✅ Proposal Generated!\n")
    print("="*80)
    print(proposal)
    print("="*80)

except Exception as e:
    print(f"❌ Proposal generation failed: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("🎉 CLAUDE AI INTEGRATION TEST COMPLETE!")
print("="*80)
print("\n✅ Job Analysis: Working perfectly")
print("✅ Proposal Generation: Working perfectly")
print("\n💡 The bot will use these AI features for every job application!")
print("\nNext step: Run the bot interactively by double-clicking:")
print("   RUN_UPWORK_BOT.command")
print("\nThe bot will:")
print("   1. Search for Google Apps Script jobs on Upwork")
print("   2. Analyze each with Claude AI (match scores + highlights)")
print("   3. Generate custom proposals for good matches")
print("   4. Show you previews for approval before submitting")
print("\n" + "="*80)
