"""
Profile Manager - Handles user profile creation and management
"""

import json
import os
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime


class ProfileManager:
    """Manages user job search profiles"""

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize ProfileManager

        Args:
            storage_path: Path to store profile data
        """
        if storage_path is None:
            storage_path = os.path.join(
                Path.home(),
                '.jobfinder',
                'profiles'
            )

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.active_profile_file = self.storage_path / 'active_profile.json'

    def create_or_update(self, profile_data: Dict) -> Dict:
        """Create or update a profile

        Args:
            profile_data: Profile information including:
                - name: User's name
                - email: Contact email
                - skills: List of skills
                - experience_years: Years of experience
                - desired_roles: List of desired job titles
                - desired_locations: List of preferred locations
                - salary_min: Minimum desired salary
                - work_type: remote/hybrid/onsite
                - resume_path: Path to resume file

        Returns:
            Created/updated profile with metadata
        """
        profile_id = profile_data.get('id', self._generate_profile_id())

        profile = {
            'id': profile_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            **profile_data
        }

        # Save profile
        profile_file = self.storage_path / f'{profile_id}.json'
        with open(profile_file, 'w') as f:
            json.dump(profile, f, indent=2)

        # Set as active profile
        self._set_active_profile(profile_id)

        return profile

    def get_active_profile(self) -> Optional[Dict]:
        """Get the currently active profile

        Returns:
            Active profile data or None
        """
        if not self.active_profile_file.exists():
            return None

        with open(self.active_profile_file, 'r') as f:
            data = json.load(f)
            profile_id = data.get('active_profile_id')

        if not profile_id:
            return None

        return self.get_profile(profile_id)

    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Get a specific profile by ID

        Args:
            profile_id: Profile identifier

        Returns:
            Profile data or None
        """
        profile_file = self.storage_path / f'{profile_id}.json'

        if not profile_file.exists():
            return None

        with open(profile_file, 'r') as f:
            return json.load(f)

    def list_profiles(self) -> list:
        """List all available profiles

        Returns:
            List of profile summaries
        """
        profiles = []

        for profile_file in self.storage_path.glob('*.json'):
            if profile_file.name == 'active_profile.json':
                continue

            with open(profile_file, 'r') as f:
                profile = json.load(f)
                profiles.append({
                    'id': profile['id'],
                    'name': profile.get('name', 'Unnamed'),
                    'created_at': profile.get('created_at'),
                    'updated_at': profile.get('updated_at')
                })

        return profiles

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile

        Args:
            profile_id: Profile identifier

        Returns:
            True if deleted, False if not found
        """
        profile_file = self.storage_path / f'{profile_id}.json'

        if not profile_file.exists():
            return False

        profile_file.unlink()

        # Clear active profile if it was this one
        active = self.get_active_profile()
        if active and active['id'] == profile_id:
            self.active_profile_file.unlink()

        return True

    def _set_active_profile(self, profile_id: str) -> None:
        """Set the active profile

        Args:
            profile_id: Profile identifier
        """
        with open(self.active_profile_file, 'w') as f:
            json.dump({'active_profile_id': profile_id}, f)

    def _generate_profile_id(self) -> str:
        """Generate a unique profile ID

        Returns:
            Unique identifier
        """
        import uuid
        return str(uuid.uuid4())
