"""
Comparison Engine - Compares multiple jobs side-by-side
"""

from typing import Dict, List


class ComparisonEngine:
    """Compares jobs across multiple dimensions"""

    def compare(self, jobs: List[Dict], profile: Dict) -> Dict:
        """Compare multiple jobs

        Args:
            jobs: List of jobs to compare
            profile: User profile for context

        Returns:
            Comparison analysis with rankings and insights
        """
        if not jobs:
            return {'error': 'No jobs provided for comparison'}

        comparison = {
            'jobs': jobs,
            'comparison_matrix': self._build_comparison_matrix(jobs),
            'rankings': self._rank_jobs(jobs),
            'pros_cons': self._analyze_pros_cons(jobs, profile),
            'recommendation': self._generate_recommendation(jobs, profile)
        }

        return comparison

    def _build_comparison_matrix(self, jobs: List[Dict]) -> Dict:
        """Build comparison matrix across key attributes

        Args:
            jobs: List of jobs

        Returns:
            Comparison matrix
        """
        matrix = {
            'companies': [job.get('company') for job in jobs],
            'titles': [job.get('title') for job in jobs],
            'locations': [job.get('location') for job in jobs],
            'work_types': [job.get('work_type') for job in jobs],
            'salaries': [
                self._format_salary_range(job)
                for job in jobs
            ],
            'match_scores': [job.get('match_score', 0) for job in jobs],
            'platforms': [job.get('platform') for job in jobs]
        }

        return matrix

    def _rank_jobs(self, jobs: List[Dict]) -> Dict:
        """Rank jobs by different criteria

        Args:
            jobs: List of jobs

        Returns:
            Rankings dictionary
        """
        # Sort by match score
        by_match = sorted(
            enumerate(jobs),
            key=lambda x: x[1].get('match_score', 0),
            reverse=True
        )

        # Sort by salary
        by_salary = sorted(
            enumerate(jobs),
            key=lambda x: x[1].get('salary_max', 0) or x[1].get('salary_min', 0),
            reverse=True
        )

        return {
            'by_match_score': [
                {
                    'index': idx,
                    'company': jobs[idx].get('company'),
                    'title': jobs[idx].get('title'),
                    'score': jobs[idx].get('match_score', 0)
                }
                for idx, _ in by_match
            ],
            'by_salary': [
                {
                    'index': idx,
                    'company': jobs[idx].get('company'),
                    'title': jobs[idx].get('title'),
                    'salary': self._format_salary_range(jobs[idx])
                }
                for idx, _ in by_salary
            ]
        }

    def _analyze_pros_cons(self, jobs: List[Dict], profile: Dict) -> List[Dict]:
        """Analyze pros and cons for each job

        Args:
            jobs: List of jobs
            profile: User profile

        Returns:
            List of pros/cons for each job
        """
        analyses = []

        for job in jobs:
            pros = []
            cons = []

            # Match score
            score = job.get('match_score', 0)
            if score >= 0.8:
                pros.append(f"Excellent match ({score:.0%})")
            elif score < 0.5:
                cons.append(f"Lower match score ({score:.0%})")

            # Salary
            desired_salary = profile.get('salary_min')
            job_salary = job.get('salary_min') or job.get('salary_max')

            if desired_salary and job_salary:
                if job_salary >= desired_salary:
                    pros.append(f"Meets salary expectations")
                else:
                    cons.append(f"Below salary expectations")

            # Work type
            desired_work_type = profile.get('work_type')
            job_work_type = job.get('work_type')

            if desired_work_type == job_work_type:
                pros.append(f"{job_work_type.capitalize()} work (as preferred)")
            elif job_work_type:
                cons.append(f"{job_work_type.capitalize()} work (prefer {desired_work_type})")

            # Location
            if job.get('work_type') == 'remote':
                pros.append("Remote position (flexible location)")

            analyses.append({
                'job_id': job.get('id'),
                'company': job.get('company'),
                'title': job.get('title'),
                'pros': pros,
                'cons': cons
            })

        return analyses

    def _generate_recommendation(self, jobs: List[Dict], profile: Dict) -> str:
        """Generate recommendation based on comparison

        Args:
            jobs: List of jobs
            profile: User profile

        Returns:
            Recommendation text
        """
        if not jobs:
            return "No jobs to compare"

        # Find best match
        best_job = max(jobs, key=lambda j: j.get('match_score', 0))

        recommendation = f"Based on your profile, '{best_job.get('title')}' at "
        recommendation += f"{best_job.get('company')} appears to be the strongest match "
        recommendation += f"({best_job.get('match_score', 0):.0%} compatibility). "

        # Add context
        if best_job.get('work_type') == profile.get('work_type'):
            recommendation += f"It offers your preferred {best_job.get('work_type')} work arrangement. "

        salary = best_job.get('salary_min') or best_job.get('salary_max')
        desired_salary = profile.get('salary_min')

        if salary and desired_salary and salary >= desired_salary:
            recommendation += "The salary range meets your expectations. "

        return recommendation

    def _format_salary_range(self, job: Dict) -> str:
        """Format salary range for display

        Args:
            job: Job data

        Returns:
            Formatted salary string
        """
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')

        if salary_min and salary_max:
            return f"${salary_min:,} - ${salary_max:,}"
        elif salary_min:
            return f"${salary_min:,}+"
        elif salary_max:
            return f"Up to ${salary_max:,}"
        else:
            return "Not specified"
