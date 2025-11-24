"""
Job Queue Mode: Save jobs during the day, apply to all later

Perfect for people working full-time!

How it works:
1. During the day: When you see a job, just paste the URL → saved to queue
2. Evening/lunch: Process entire queue at once with AI proposals
3. Apply to 10 jobs in 15-20 minutes
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from anthropic import Anthropic

# Initialize Claude
anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if not anthropic_key:
    print("❌ No Claude API key found in .env")
    sys.exit(1)

claude_client = Anthropic(api_key=anthropic_key)

# Queue file
QUEUE_FILE = Path(__file__).parent / 'job_queue.json'

def load_queue():
    """Load job queue from file"""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_queue(queue):
    """Save job queue to file"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

def add_to_queue():
    """Add jobs to queue (quick mode for during work)"""
    print("="*80)
    print("📥 ADD JOBS TO QUEUE - Quick Mode")
    print("="*80)
    print("\nPerfect for adding jobs during your workday!")
    print("Just paste the job details and I'll save them for later.\n")

    queue = load_queue()
    added = 0

    while True:
        print("\n" + "-"*80)
        print(f"Queue: {len(queue)} jobs | Just added: {added}")
        print("-"*80)

        print("\n1️⃣ Job title:")
        title = input("   > ").strip()

        if not title or title.lower() in ['done', 'quit', 'q', 'exit']:
            break

        print("\n2️⃣ Budget:")
        budget = input("   > ").strip()

        print("\n3️⃣ Paste description (press Enter twice when done):")
        description_lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line.strip():
                description_lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
        description = "\n".join(description_lines)

        print("\n4️⃣ Upwork URL (optional, press Enter to skip):")
        url = input("   > ").strip()

        # Save to queue
        job = {
            'title': title,
            'budget': budget,
            'description': description,
            'url': url or 'Not provided',
            'added_at': datetime.now().isoformat(),
            'status': 'queued'
        }

        queue.append(job)
        save_queue(queue)
        added += 1

        print(f"\n✅ Added to queue! ({len(queue)} total)")
        print("\nAdd another? (Enter job title, or type 'done' to finish)")

    print(f"\n✅ Queue saved! {len(queue)} jobs ready to process.")
    print(f"\nRun 'python3 job_queue_mode.py process' to generate proposals for all.")

def process_queue():
    """Process all jobs in queue with AI proposals"""
    queue = load_queue()

    if not queue:
        print("\n📭 Queue is empty! Add some jobs first.")
        print("   Run: python3 job_queue_mode.py add")
        return

    # Filter to only queued jobs
    pending = [j for j in queue if j.get('status') == 'queued']

    if not pending:
        print("\n✅ All jobs processed!")
        print(f"   {len([j for j in queue if j.get('status') == 'completed'])} completed")
        print(f"   {len([j for j in queue if j.get('status') == 'skipped'])} skipped")
        return

    print("="*80)
    print(f"🚀 PROCESSING {len(pending)} JOBS FROM QUEUE")
    print("="*80)
    print("\nI'll analyze each job and generate proposals.")
    print("You review and decide: apply, skip, or edit.\n")

    for i, job in enumerate(pending, 1):
        print("\n" + "="*80)
        print(f"📋 JOB {i} of {len(pending)}")
        print("="*80)
        print(f"\nTitle: {job['title']}")
        print(f"Budget: {job['budget']}")
        print(f"Added: {job['added_at'][:10]}")
        if job['url'] != 'Not provided':
            print(f"URL: {job['url']}")

        # Analyze with Claude
        print("\n🤖 Analyzing with Claude AI...")
        try:
            analysis = analyze_job(job['title'], job['budget'], job['description'])

            print(f"\n   Match Score: {analysis['match_score']}%")
            print(f"   Good Fit: {'✅ Yes' if analysis['is_good_fit'] else '❌ No'}")
            print(f"   {analysis['reason']}")

            if analysis.get('highlights'):
                print("\n   ✨ Highlights:")
                for h in analysis['highlights']:
                    print(f"      • {h}")

            if analysis.get('red_flags'):
                print("\n   ⚠️  Red Flags:")
                for f in analysis['red_flags']:
                    print(f"      • {f}")

            # Suggest skip if low score
            if analysis['match_score'] < 60:
                print(f"\n   💡 Low match score - suggest skipping")
                skip = input("\n   Skip this job? (yes/no): ").strip().lower()
                if skip in ['yes', 'y']:
                    job['status'] = 'skipped'
                    save_queue(queue)
                    print("   ⏭️  Skipped!")
                    continue

        except Exception as e:
            print(f"   ⚠️  Analysis error: {e}")

        # Generate proposal
        print("\n✍️  Generating proposal...")
        try:
            proposal = generate_proposal(job['title'], job['budget'], job['description'])

            print("\n" + "="*80)
            print("📝 PROPOSAL")
            print("="*80)
            print(f"\n{proposal}\n")
            print("="*80)

            # Copy to clipboard
            try:
                import pyperclip
                pyperclip.copy(proposal)
                print("\n✅ Copied to clipboard!")
            except:
                pass

            print("\n🎯 What do you want to do?")
            print("   'apply' - Mark as applied (you'll paste in Upwork)")
            print("   'skip' - Skip this job")
            print("   'later' - Leave in queue for later")
            print("   'edit' - Show me the proposal again to copy manually")

            action = input("\n   > ").strip().lower()

            if action == 'apply':
                job['status'] = 'completed'
                job['proposal'] = proposal
                job['applied_at'] = datetime.now().isoformat()
                save_queue(queue)
                print("\n   ✅ Marked as applied!")

                if job['url'] != 'Not provided':
                    print(f"\n   🔗 Open this URL to apply: {job['url']}")
                    print("   📋 Proposal is in your clipboard - just paste!")

            elif action == 'skip':
                job['status'] = 'skipped'
                save_queue(queue)
                print("\n   ⏭️  Skipped!")

            elif action == 'edit':
                print("\n" + "="*80)
                print(proposal)
                print("="*80)
                print("\n   Select and copy the text above")
                input("   Press Enter when ready to continue...")

            else:
                print("\n   💾 Left in queue")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Leaving in queue")

    # Show summary
    completed = len([j for j in queue if j.get('status') == 'completed'])
    skipped = len([j for j in queue if j.get('status') == 'skipped'])
    remaining = len([j for j in queue if j.get('status') == 'queued'])

    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"\n   ✅ Applied: {completed}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   📋 Remaining: {remaining}")
    print("\n" + "="*80)

def view_queue():
    """View current queue"""
    queue = load_queue()

    if not queue:
        print("\n📭 Queue is empty!")
        return

    queued = [j for j in queue if j.get('status') == 'queued']
    completed = [j for j in queue if j.get('status') == 'completed']
    skipped = [j for j in queue if j.get('status') == 'skipped']

    print("\n" + "="*80)
    print("📋 JOB QUEUE STATUS")
    print("="*80)

    if queued:
        print(f"\n📥 QUEUED ({len(queued)} jobs):")
        for i, job in enumerate(queued, 1):
            print(f"\n   {i}. {job['title']}")
            print(f"      Budget: {job['budget']}")
            print(f"      Added: {job['added_at'][:10]}")

    if completed:
        print(f"\n✅ APPLIED ({len(completed)} jobs):")
        for job in completed[:5]:  # Show last 5
            print(f"   • {job['title']} - {job.get('applied_at', '')[:10]}")
        if len(completed) > 5:
            print(f"   ... and {len(completed) - 5} more")

    if skipped:
        print(f"\n⏭️  SKIPPED ({len(skipped)} jobs)")

    print("\n" + "="*80)

def clear_completed():
    """Clear completed/skipped jobs from queue"""
    queue = load_queue()
    new_queue = [j for j in queue if j.get('status') == 'queued']

    removed = len(queue) - len(new_queue)
    save_queue(new_queue)

    print(f"\n✅ Removed {removed} completed/skipped jobs")
    print(f"   {len(new_queue)} jobs remaining in queue")

def analyze_job(job_title, job_budget, job_description):
    """Analyze job with Claude"""
    prompt = f"""Analyze this Upwork job for Trey, a Google Apps Script automation specialist.

Job Title: {job_title}
Budget: {job_budget}
Description: {job_description}

Trey's Skills: Google Apps Script (Advanced), JavaScript, Python, web scraping, API integration
Key Projects: Inventory automation (500+ items), crew scheduling, Slack integration, Google Workspace automation

Return JSON:
{{
  "match_score": 85,
  "is_good_fit": true,
  "reason": "Brief explanation",
  "highlights": ["Point 1", "Point 2"],
  "red_flags": [] or ["Concern"]
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

Write personalized proposal (200-300 words):
1. Relevant to THEIR project
2. Reference MOST relevant experience
3. Measurable results
4. Clear approach
5. Professional but friendly

End with:
"Best regards,
Trey Haulbrook
Haulbrookai@gmail.com
770-530-7910"

Write ONLY the proposal:"""

    response = claude_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()

# Main
if __name__ == "__main__":
    print("="*80)
    print("📋 JOB QUEUE MODE - Work-Friendly Job Application System")
    print("="*80)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'add':
            add_to_queue()
        elif command == 'process':
            process_queue()
        elif command == 'view':
            view_queue()
        elif command == 'clear':
            clear_completed()
        else:
            print(f"\n❌ Unknown command: {command}")
            print("\nCommands:")
            print("  add     - Add jobs to queue (quick!)")
            print("  process - Process all queued jobs")
            print("  view    - View queue status")
            print("  clear   - Clear completed jobs")
    else:
        print("\n🎯 Choose a mode:")
        print("\n1. ADD jobs to queue (during work - takes 1 min per job)")
        print("2. PROCESS queue (evening/lunch - apply to all)")
        print("3. VIEW queue status")
        print("4. CLEAR completed jobs")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            add_to_queue()
        elif choice == '2':
            process_queue()
        elif choice == '3':
            view_queue()
        elif choice == '4':
            clear_completed()
        else:
            print("\n❌ Invalid choice")
