"""
JobFinder - AI-Powered Job Search Agent
Main orchestration module
"""

import os
import sys
from typing import Dict, List, Optional
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from storage.profile_manager import ProfileManager
from storage.job_database import JobDatabase
from search.job_discoverer import JobDiscoverer
from search.platform_adapters import LinkedInAdapter, IndeedAdapter, GlassdoorAdapter
from analysis.job_scorer import JobScorer
from analysis.comparison_engine import ComparisonEngine
from application.auto_applier import AutoApplier
from application.cover_letter_generator import CoverLetterGenerator


class JobFinder:
    """Main JobFinder orchestration class"""

    def __init__(self):
        """Initialize JobFinder with all components"""
        self.profile_manager = ProfileManager()
        self.job_database = JobDatabase()
        self.job_discoverer = JobDiscoverer()
        self.job_scorer = JobScorer()
        self.comparison_engine = ComparisonEngine()
        self.auto_applier = AutoApplier()
        self.cover_letter_generator = CoverLetterGenerator()

        # Initialize platform adapters
        self.platforms = {
            'linkedin': LinkedInAdapter(),
            'indeed': IndeedAdapter(),
            'glassdoor': GlassdoorAdapter()
        }

    def create_profile(self, profile_data: Dict) -> Dict:
        """Create or update user profile

        Args:
            profile_data: Dictionary containing profile information

        Returns:
            Created/updated profile
        """
        return self.profile_manager.create_or_update(profile_data)

    def search_jobs(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Search for jobs across all platforms

        Args:
            filters: Optional search filters

        Returns:
            List of job listings
        """
        profile = self.profile_manager.get_active_profile()
        if not profile:
            raise ValueError("No active profile found. Please create a profile first.")

        # Discover jobs from all platforms
        jobs = self.job_discoverer.search(
            profile=profile,
            platforms=self.platforms,
            filters=filters
        )

        # Score jobs based on profile match
        scored_jobs = self.job_scorer.score_batch(jobs, profile)

        # Save to database
        for job in scored_jobs:
            self.job_database.save_job(job)

        return scored_jobs

    def get_top_matches(self, limit: int = 10) -> List[Dict]:
        """Get top matching jobs from database

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of top matching jobs
        """
        return self.job_database.get_top_matches(limit)

    def compare_jobs(self, job_ids: List[str]) -> Dict:
        """Compare multiple jobs

        Args:
            job_ids: List of job IDs to compare

        Returns:
            Comparison analysis
        """
        jobs = [self.job_database.get_job(job_id) for job_id in job_ids]
        profile = self.profile_manager.get_active_profile()

        return self.comparison_engine.compare(jobs, profile)

    def apply_to_job(self, job_id: str, custom_message: Optional[str] = None) -> Dict:
        """Apply to a specific job

        Args:
            job_id: Job ID to apply to
            custom_message: Optional custom message for application

        Returns:
            Application result
        """
        job = self.job_database.get_job(job_id)
        profile = self.profile_manager.get_active_profile()

        # Generate cover letter
        cover_letter = self.cover_letter_generator.generate(
            job=job,
            profile=profile,
            custom_message=custom_message
        )

        # Submit application
        result = self.auto_applier.apply(
            job=job,
            profile=profile,
            cover_letter=cover_letter
        )

        # Update job status in database
        self.job_database.update_status(job_id, 'applied')

        return result

    def get_application_status(self) -> Dict:
        """Get overview of application statuses

        Returns:
            Dictionary with application statistics
        """
        return self.job_database.get_application_stats()


def main():
    """Main entry point for JobFinder agent"""
    print("JobFinder Agent initialized!")
    print("Use Claude Code to interact with JobFinder")
    print("\nExample commands:")
    print('  "Create my job search profile..."')
    print('  "Find me jobs that match my profile"')
    print('  "Show me the top 10 matching jobs"')
    print('  "Compare these 3 jobs..."')
    print('  "Apply to job #12345"')


if __name__ == "__main__":
    main()
