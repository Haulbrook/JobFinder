"""
Hybrid Mode: Claude AI generates proposals, you apply manually

This avoids all bot detection while still giving you AI-powered proposals!
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pyperclip  # For copying to clipboard

# Load environment
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from anthropic import Anthropic

print("="*80)
print("🤖 HYBRID MODE: AI Proposal Generator")
print("="*80)
print("\nHow it works:")
print("1. You browse Upwork normally in your browser")
print("2. Find a job you like")
print("3. Copy the job description")
print("4. Paste it here")
print("5. Claude AI generates a custom proposal")
print("6. Copy the proposal back to Upwork")
print("7. Submit manually (no bot detection!)")
print("\n" + "="*80)

# Initialize Claude
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if not anthropic_key:
    print("❌ No Claude API key found in .env")
    sys.exit(1)

claude_client = Anthropic(api_key=anthropic_key)
print("\n✅ Claude AI ready!\n")

# Trey's profile
profile = {
    'name': 'Trey Haulbrook',
    'email': 'Haulbrookai@gmail.com',
    'phone': '770-530-7910',
    'hourly_rate': 60,
    'skills': ['Google Apps Script (Advanced)', 'JavaScript', 'Python', 'Web Scraping', 'API Integration'],
    'projects': [
        'Wholesale Plant Inventory Automation - 500+ items, web scraping, automated pricing',
        'Crew Scheduling System - Slack integration, drag-and-drop UI, 15+ hours saved weekly',
        'Multi-System Integration - Google Workspace + Slack + field service management',
        'Tool Management Platform - Asset tracking, checkout workflows, maintenance scheduling'
    ]
}

def analyze_job(job_title, job_budget, job_description):
    """Analyze job with Claude"""
    prompt = f"""Analyze this Upwork job for Trey, a Google Apps Script automation specialist.

Job Title: {job_title}
Budget: {job_budget}
Description: {job_description}

Trey's Skills: Google Apps Script (Advanced), JavaScript, Python, web scraping, API integration
Key Projects: Inventory automation (500+ items), crew scheduling, Slack integration, Google Workspace automation

Analyze and provide:
1. Match score (0-100)
2. Whether it's a good fit (true/false)
3. Brief reason
4. 2-3 highlights
5. Any red flags

Return as JSON:
{{
  "match_score": 85,
  "is_good_fit": true,
  "reason": "Brief explanation",
  "highlights": ["Point 1", "Point 2"],
  "red_flags": ["Concern"] or []
}}"""

    response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    text = response.content[0].text
    json_start = text.find('{')
    json_end = text.rfind('}') + 1
    return json.loads(text[json_start:json_end])


def generate_proposal(job_title, job_budget, job_description):
    """Generate proposal with Claude"""
    prompt = f"""Write a compelling Upwork proposal for Trey Haulbrook.

Job Title: {job_title}
Budget: {job_budget}
Description: {job_description}

Trey's Profile:
- Expert in Google Apps Script, JavaScript, Python, API integration
- Hourly rate: $60
- Key projects:
  1. Inventory automation (500+ plant varieties, web scraping, automated pricing)
  2. Crew scheduling system (Slack integration, 15+ hours saved weekly)
  3. Multi-system integration (Google Workspace, Slack, field service)
  4. Tool management platform (asset tracking, workflows)

Write a personalized proposal that:
1. Opens with relevance to THEIR project
2. References your MOST relevant experience
3. Shows measurable results
4. Outlines clear approach
5. Professional but friendly (200-300 words)

End with:
"Best regards,
Trey Haulbrook
Haulbrookai@gmail.com
770-530-7910"

Write ONLY the proposal text:"""

    response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


# Main loop
while True:
    print("\n" + "="*80)
    print("📋 NEW JOB")
    print("="*80)

    # Get job details from user
    print("\n1️⃣ Enter job title:")
    job_title = input("   > ").strip()

    if not job_title or job_title.lower() in ['quit', 'exit', 'q']:
        print("\n👋 Goodbye!")
        break

    print("\n2️⃣ Enter budget (e.g. '$500-1000' or 'Hourly: $50-75'):")
    job_budget = input("   > ").strip()

    print("\n3️⃣ Paste the job description (press Enter twice when done):")
    print("   (Tip: Copy from Upwork and paste here)")
    description_lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if line.strip():
            description_lines.append(line)
            empty_count = 0
        else:
            empty_count += 1
    job_description = "\n".join(description_lines)

    if not job_description:
        print("⚠️  No description provided, skipping...")
        continue

    # Analyze with Claude
    print("\n🤖 Analyzing with Claude AI...")
    try:
        analysis = analyze_job(job_title, job_budget, job_description)

        print("\n" + "="*80)
        print("🎯 CLAUDE ANALYSIS")
        print("="*80)
        print(f"\n   Match Score: {analysis['match_score']}%")
        print(f"   Good Fit: {'✅ Yes' if analysis['is_good_fit'] else '❌ No'}")
        print(f"   Reason: {analysis['reason']}")

        if analysis.get('highlights'):
            print("\n   ✨ Highlights:")
            for h in analysis['highlights']:
                print(f"      • {h}")

        if analysis.get('red_flags'):
            print("\n   ⚠️  Red Flags:")
            for f in analysis['red_flags']:
                print(f"      • {f}")
        else:
            print("\n   ✅ No red flags")

        # Suggest action based on score
        if analysis['match_score'] < 60:
            print(f"\n   💡 Suggestion: Low match score - consider skipping")
            skip = input("\n   Skip this job? (yes/no): ").strip().lower()
            if skip in ['yes', 'y']:
                print("   ⏭️  Skipped!\n")
                continue

    except Exception as e:
        print(f"   ⚠️  Analysis error: {e}")
        print("   Continuing with proposal generation...")

    # Generate proposal
    print("\n✍️  Generating personalized proposal with Claude AI...")
    try:
        proposal = generate_proposal(job_title, job_budget, job_description)

        print("\n" + "="*80)
        print("📝 PROPOSAL")
        print("="*80)
        print(f"\n{proposal}\n")
        print("="*80)

        # Copy to clipboard
        try:
            import pyperclip
            pyperclip.copy(proposal)
            print("\n✅ Proposal copied to clipboard!")
            print("   Just paste it into Upwork (Cmd+V)")
        except:
            print("\n💡 Tip: Select and copy the proposal above")

        print("\n🎯 Next steps:")
        print("   1. Go to the Upwork job posting")
        print("   2. Click 'Apply Now'")
        print("   3. Paste this proposal (Cmd+V)")
        print("   4. Review and submit")
        print("   5. Come back here for the next one!")

    except Exception as e:
        print(f"\n❌ Error generating proposal: {e}")

    # Next job?
    print("\n" + "="*80)
    another = input("Generate proposal for another job? (yes/no): ").strip().lower()
    if another not in ['yes', 'y']:
        print("\n🎉 Great work! Good luck with your applications!")
        break

print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)
print("\nUsing this hybrid approach:")
print("✅ No bot detection (you apply manually)")
print("✅ AI-powered proposals (Claude generates them)")
print("✅ Fast workflow (copy/paste)")
print("✅ High quality (personalized to each job)")
print("\n💡 Average time: 2-3 minutes per application")
print("💰 Cost: ~$0.01 per proposal")
print("\n" + "="*80)
