"""
Job Discoverer - Orchestrates job search across multiple platforms
"""

from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class JobDiscoverer:
    """Discovers jobs across multiple platforms"""

    def __init__(self, max_workers: int = 3):
        """Initialize JobDiscoverer

        Args:
            max_workers: Maximum concurrent platform searches
        """
        self.max_workers = max_workers

    def search(
        self,
        profile: Dict,
        platforms: Dict,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for jobs across all platforms

        Args:
            profile: User profile data
            platforms: Dictionary of platform adapters
            filters: Optional search filters

        Returns:
            Combined list of jobs from all platforms
        """
        all_jobs = []

        # Build search parameters from profile
        search_params = self._build_search_params(profile, filters)

        # Search platforms concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_platform = {
                executor.submit(
                    adapter.search,
                    search_params
                ): platform_name
                for platform_name, adapter in platforms.items()
            }

            for future in as_completed(future_to_platform):
                platform_name = future_to_platform[future]
                try:
                    jobs = future.result()
                    print(f"Found {len(jobs)} jobs on {platform_name}")
                    all_jobs.extend(jobs)
                except Exception as e:
                    print(f"Error searching {platform_name}: {e}")

        return self._deduplicate_jobs(all_jobs)

    def _build_search_params(
        self,
        profile: Dict,
        filters: Optional[Dict]
    ) -> Dict:
        """Build search parameters from profile and filters

        Args:
            profile: User profile
            filters: Optional filters

        Returns:
            Search parameters dictionary
        """
        params = {
            'keywords': profile.get('desired_roles', []),
            'locations': profile.get('desired_locations', []),
            'experience_level': self._map_experience_level(
                profile.get('experience_years', 0)
            ),
            'work_type': profile.get('work_type', 'remote'),
            'salary_min': profile.get('salary_min')
        }

        # Apply additional filters
        if filters:
            params.update(filters)

        return params

    def _map_experience_level(self, years: int) -> str:
        """Map years of experience to level category

        Args:
            years: Years of experience

        Returns:
            Experience level string
        """
        if years < 2:
            return 'entry'
        elif years < 5:
            return 'mid'
        elif years < 10:
            return 'senior'
        else:
            return 'lead'

    def _deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate job listings

        Args:
            jobs: List of job listings

        Returns:
            Deduplicated list
        """
        seen = set()
        unique_jobs = []

        for job in jobs:
            # Create unique key from company + title + location
            key = (
                job.get('company', '').lower(),
                job.get('title', '').lower(),
                job.get('location', '').lower()
            )

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs
