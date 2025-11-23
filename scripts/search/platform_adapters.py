"""
Platform Adapters - Adapters for different job search platforms
"""

import os
import requests
from typing import Dict, List
from abc import ABC, abstractmethod


class PlatformAdapter(ABC):
    """Base class for platform adapters"""

    @abstractmethod
    def search(self, params: Dict) -> List[Dict]:
        """Search for jobs on the platform

        Args:
            params: Search parameters

        Returns:
            List of job listings
        """
        pass

    def _standardize_job(self, raw_job: Dict, platform: str) -> Dict:
        """Convert platform-specific job format to standard format

        Args:
            raw_job: Platform-specific job data
            platform: Platform name

        Returns:
            Standardized job dictionary
        """
        return {
            'platform': platform,
            'id': raw_job.get('id'),
            'title': raw_job.get('title'),
            'company': raw_job.get('company'),
            'location': raw_job.get('location'),
            'description': raw_job.get('description'),
            'requirements': raw_job.get('requirements'),
            'salary_min': raw_job.get('salary_min'),
            'salary_max': raw_job.get('salary_max'),
            'work_type': raw_job.get('work_type'),
            'url': raw_job.get('url'),
            'posted_date': raw_job.get('posted_date'),
            'raw_data': raw_job
        }


class LinkedInAdapter(PlatformAdapter):
    """LinkedIn job search adapter"""

    def __init__(self):
        """Initialize LinkedIn adapter"""
        self.api_key = os.getenv('LINKEDIN_API_KEY')
        self.base_url = 'https://api.linkedin.com/v2'

    def search(self, params: Dict) -> List[Dict]:
        """Search LinkedIn for jobs

        Args:
            params: Search parameters

        Returns:
            List of standardized job listings
        """
        if not self.api_key:
            print("Warning: LinkedIn API key not configured")
            return []

        jobs = []

        try:
            # Build search query
            keywords = params.get('keywords', [])
            locations = params.get('locations', [])

            for keyword in keywords:
                for location in locations:
                    response = self._make_request(keyword, location, params)
                    if response:
                        jobs.extend(self._parse_response(response))

        except Exception as e:
            print(f"LinkedIn search error: {e}")

        return jobs

    def _make_request(self, keyword: str, location: str, params: Dict) -> Dict:
        """Make API request to LinkedIn

        Args:
            keyword: Job title/keyword
            location: Location filter
            params: Additional parameters

        Returns:
            API response
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        query_params = {
            'keywords': keyword,
            'location': location,
            'experience': params.get('experience_level'),
            'jobType': params.get('work_type')
        }

        # Note: This is a placeholder for the actual LinkedIn API endpoint
        # You'll need to use the official LinkedIn Jobs API or a service like RapidAPI
        url = f"{self.base_url}/jobSearch"

        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"LinkedIn API request failed: {e}")
            return None

    def _parse_response(self, response: Dict) -> List[Dict]:
        """Parse LinkedIn API response

        Args:
            response: API response

        Returns:
            List of standardized jobs
        """
        jobs = []
        elements = response.get('elements', [])

        for element in elements:
            job = self._standardize_job({
                'id': element.get('id'),
                'title': element.get('title'),
                'company': element.get('company', {}).get('name'),
                'location': element.get('location'),
                'description': element.get('description'),
                'work_type': element.get('workRemoteAllowed') and 'remote' or 'onsite',
                'url': element.get('applyUrl'),
                'posted_date': element.get('listedAt')
            }, 'linkedin')
            jobs.append(job)

        return jobs


class IndeedAdapter(PlatformAdapter):
    """Indeed job search adapter"""

    def __init__(self):
        """Initialize Indeed adapter"""
        self.api_key = os.getenv('INDEED_API_KEY')
        self.publisher_id = os.getenv('INDEED_PUBLISHER_ID')
        self.base_url = 'https://api.indeed.com/ads/apisearch'

    def search(self, params: Dict) -> List[Dict]:
        """Search Indeed for jobs

        Args:
            params: Search parameters

        Returns:
            List of standardized job listings
        """
        if not self.publisher_id:
            print("Warning: Indeed Publisher ID not configured")
            return []

        jobs = []

        try:
            keywords = params.get('keywords', [])
            locations = params.get('locations', [])

            for keyword in keywords:
                for location in locations:
                    response = self._make_request(keyword, location, params)
                    if response:
                        jobs.extend(self._parse_response(response))

        except Exception as e:
            print(f"Indeed search error: {e}")

        return jobs

    def _make_request(self, keyword: str, location: str, params: Dict) -> Dict:
        """Make API request to Indeed

        Args:
            keyword: Job title/keyword
            location: Location filter
            params: Additional parameters

        Returns:
            API response
        """
        query_params = {
            'publisher': self.publisher_id,
            'q': keyword,
            'l': location,
            'format': 'json',
            'v': '2',
            'limit': 25
        }

        try:
            response = requests.get(self.base_url, params=query_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Indeed API request failed: {e}")
            return None

    def _parse_response(self, response: Dict) -> List[Dict]:
        """Parse Indeed API response

        Args:
            response: API response

        Returns:
            List of standardized jobs
        """
        jobs = []
        results = response.get('results', [])

        for result in results:
            job = self._standardize_job({
                'id': result.get('jobkey'),
                'title': result.get('jobtitle'),
                'company': result.get('company'),
                'location': result.get('formattedLocation'),
                'description': result.get('snippet'),
                'url': result.get('url'),
                'posted_date': result.get('date')
            }, 'indeed')
            jobs.append(job)

        return jobs


class GlassdoorAdapter(PlatformAdapter):
    """Glassdoor job search adapter"""

    def __init__(self):
        """Initialize Glassdoor adapter"""
        self.api_key = os.getenv('GLASSDOOR_API_KEY')
        self.partner_id = os.getenv('GLASSDOOR_PARTNER_ID')
        self.base_url = 'https://api.glassdoor.com/api/api.htm'

    def search(self, params: Dict) -> List[Dict]:
        """Search Glassdoor for jobs

        Args:
            params: Search parameters

        Returns:
            List of standardized job listings
        """
        if not self.partner_id or not self.api_key:
            print("Warning: Glassdoor API credentials not configured")
            return []

        jobs = []

        try:
            keywords = params.get('keywords', [])
            locations = params.get('locations', [])

            for keyword in keywords:
                for location in locations:
                    response = self._make_request(keyword, location, params)
                    if response:
                        jobs.extend(self._parse_response(response))

        except Exception as e:
            print(f"Glassdoor search error: {e}")

        return jobs

    def _make_request(self, keyword: str, location: str, params: Dict) -> Dict:
        """Make API request to Glassdoor

        Args:
            keyword: Job title/keyword
            location: Location filter
            params: Additional parameters

        Returns:
            API response
        """
        query_params = {
            'v': '1',
            't.p': self.partner_id,
            't.k': self.api_key,
            'action': 'jobs-prog',
            'q': keyword,
            'l': location,
            'format': 'json'
        }

        try:
            response = requests.get(self.base_url, params=query_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Glassdoor API request failed: {e}")
            return None

    def _parse_response(self, response: Dict) -> List[Dict]:
        """Parse Glassdoor API response

        Args:
            response: API response

        Returns:
            List of standardized jobs
        """
        jobs = []
        job_listings = response.get('response', {}).get('jobListings', [])

        for listing in job_listings:
            job_data = listing.get('jobListing', {})
            job = self._standardize_job({
                'id': job_data.get('jobListingId'),
                'title': job_data.get('jobTitle'),
                'company': job_data.get('employerName'),
                'location': job_data.get('location'),
                'description': job_data.get('jobDescription'),
                'url': job_data.get('jobViewUrl'),
                'posted_date': job_data.get('discoverDate')
            }, 'glassdoor')
            jobs.append(job)

        return jobs
