"""
Job Scorer - Calculates match scores for jobs based on profile
"""

from typing import Dict, List
import re


class JobScorer:
    """Scores jobs based on profile match"""

    def __init__(self):
        """Initialize JobScorer with default weights"""
        self.weights = {
            'skills_match': 0.35,
            'role_match': 0.25,
            'location_match': 0.15,
            'salary_match': 0.15,
            'work_type_match': 0.10
        }

    def score(self, job: Dict, profile: Dict) -> float:
        """Calculate match score for a single job

        Args:
            job: Job listing data
            profile: User profile data

        Returns:
            Match score between 0 and 1
        """
        scores = {
            'skills_match': self._score_skills(job, profile),
            'role_match': self._score_role(job, profile),
            'location_match': self._score_location(job, profile),
            'salary_match': self._score_salary(job, profile),
            'work_type_match': self._score_work_type(job, profile)
        }

        # Calculate weighted total
        total_score = sum(
            scores[key] * self.weights[key]
            for key in scores
        )

        return round(total_score, 3)

    def score_batch(self, jobs: List[Dict], profile: Dict) -> List[Dict]:
        """Score multiple jobs

        Args:
            jobs: List of job listings
            profile: User profile data

        Returns:
            Jobs with match_score added
        """
        for job in jobs:
            job['match_score'] = self.score(job, profile)

        return jobs

    def _score_skills(self, job: Dict, profile: Dict) -> float:
        """Score skills match

        Args:
            job: Job data
            profile: Profile data

        Returns:
            Skills match score (0-1)
        """
        profile_skills = set(
            skill.lower()
            for skill in profile.get('skills', [])
        )

        if not profile_skills:
            return 0.5  # Neutral score if no skills specified

        # Extract skills from job description and requirements
        job_text = ' '.join([
            job.get('description', ''),
            job.get('requirements', ''),
            job.get('title', '')
        ]).lower()

        matched_skills = sum(
            1 for skill in profile_skills
            if skill in job_text
        )

        return matched_skills / len(profile_skills)

    def _score_role(self, job: Dict, profile: Dict) -> float:
        """Score role/title match

        Args:
            job: Job data
            profile: Profile data

        Returns:
            Role match score (0-1)
        """
        desired_roles = profile.get('desired_roles', [])

        if not desired_roles:
            return 0.5

        job_title = job.get('title', '').lower()

        # Check for exact or partial matches
        for desired_role in desired_roles:
            desired_role_lower = desired_role.lower()

            # Exact match
            if desired_role_lower == job_title:
                return 1.0

            # Partial match
            if desired_role_lower in job_title or job_title in desired_role_lower:
                return 0.8

            # Keyword match (any word from desired role in job title)
            desired_words = set(re.findall(r'\w+', desired_role_lower))
            title_words = set(re.findall(r'\w+', job_title))

            if desired_words & title_words:
                overlap = len(desired_words & title_words) / len(desired_words)
                return 0.5 + (overlap * 0.3)

        return 0.0

    def _score_location(self, job: Dict, profile: Dict) -> float:
        """Score location match

        Args:
            job: Job data
            profile: Profile data

        Returns:
            Location match score (0-1)
        """
        desired_locations = profile.get('desired_locations', [])
        job_location = job.get('location', '').lower()
        work_type = job.get('work_type', '').lower()

        # Remote jobs match all locations
        if work_type == 'remote':
            return 1.0

        if not desired_locations:
            return 0.5

        for desired_location in desired_locations:
            desired_lower = desired_location.lower()

            # Check for city, state, or country match
            if desired_lower in job_location or job_location in desired_lower:
                return 1.0

            # Partial match
            desired_words = set(desired_lower.split())
            location_words = set(job_location.split())

            if desired_words & location_words:
                return 0.6

        return 0.0

    def _score_salary(self, job: Dict, profile: Dict) -> float:
        """Score salary match

        Args:
            job: Job data
            profile: Profile data

        Returns:
            Salary match score (0-1)
        """
        desired_min = profile.get('salary_min')
        job_min = job.get('salary_min')
        job_max = job.get('salary_max')

        # If no salary data, return neutral
        if not desired_min:
            return 0.5

        if not job_min and not job_max:
            return 0.5

        # If job offers more than desired minimum
        if job_min and job_min >= desired_min:
            return 1.0

        # If job max is in acceptable range
        if job_max and job_max >= desired_min:
            return 0.8

        # If job salary is below desired
        if job_max and job_max < desired_min:
            gap = (desired_min - job_max) / desired_min
            return max(0, 1 - gap)

        return 0.5

    def _score_work_type(self, job: Dict, profile: Dict) -> float:
        """Score work type match (remote/hybrid/onsite)

        Args:
            job: Job data
            profile: Profile data

        Returns:
            Work type match score (0-1)
        """
        desired_type = profile.get('work_type', '').lower()
        job_type = job.get('work_type', '').lower()

        if not desired_type:
            return 0.5

        if desired_type == job_type:
            return 1.0

        # Partial matches
        if desired_type == 'remote' and job_type == 'hybrid':
            return 0.7

        if desired_type == 'hybrid':
            return 0.6  # Hybrid is flexible

        return 0.0
