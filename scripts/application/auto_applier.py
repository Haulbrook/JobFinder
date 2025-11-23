"""
Auto Applier - Handles job application submission
"""

from typing import Dict, Optional
import webbrowser


class AutoApplier:
    """Automates job application process"""

    def __init__(self):
        """Initialize AutoApplier"""
        self.supported_platforms = ['linkedin', 'indeed', 'glassdoor']

    def apply(
        self,
        job: Dict,
        profile: Dict,
        cover_letter: Optional[str] = None
    ) -> Dict:
        """Apply to a job

        Args:
            job: Job listing data
            profile: User profile
            cover_letter: Optional cover letter text

        Returns:
            Application result
        """
        platform = job.get('platform')

        if platform not in self.supported_platforms:
            return {
                'status': 'manual',
                'message': f'Platform {platform} requires manual application',
                'url': job.get('url')
            }

        # For now, we'll open the job URL in browser
        # In a full implementation, this would use platform APIs
        # or browser automation (Selenium/Playwright)

        result = self._prepare_application(job, profile, cover_letter)

        # Open job URL
        job_url = job.get('url')
        if job_url:
            webbrowser.open(job_url)
            result['browser_opened'] = True

        return result

    def _prepare_application(
        self,
        job: Dict,
        profile: Dict,
        cover_letter: Optional[str]
    ) -> Dict:
        """Prepare application data

        Args:
            job: Job data
            profile: User profile
            cover_letter: Cover letter text

        Returns:
            Application preparation result
        """
        application_data = {
            'status': 'prepared',
            'job_id': job.get('id'),
            'job_title': job.get('title'),
            'company': job.get('company'),
            'applicant_name': profile.get('name'),
            'applicant_email': profile.get('email'),
            'resume_path': profile.get('resume_path'),
            'cover_letter': cover_letter,
            'application_method': 'browser_assisted'
        }

        # Platform-specific preparation
        platform = job.get('platform')

        if platform == 'linkedin':
            application_data['linkedin_profile'] = profile.get('linkedin_url')
        elif platform == 'indeed':
            application_data['indeed_resume'] = profile.get('indeed_resume_id')

        return application_data

    def can_auto_apply(self, job: Dict) -> bool:
        """Check if job supports auto-application

        Args:
            job: Job listing data

        Returns:
            True if auto-apply is supported
        """
        platform = job.get('platform')
        return platform in self.supported_platforms

    def get_application_requirements(self, job: Dict) -> Dict:
        """Get application requirements for a job

        Args:
            job: Job listing data

        Returns:
            Requirements dictionary
        """
        requirements = {
            'resume': True,
            'cover_letter': job.get('requires_cover_letter', False),
            'portfolio': False,
            'additional_questions': False
        }

        # Platform-specific requirements
        platform = job.get('platform')

        if platform == 'linkedin':
            requirements['linkedin_profile'] = True

        return requirements
