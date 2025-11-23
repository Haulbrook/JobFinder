"""
Job Database - Stores and manages discovered jobs
"""

import json
import sqlite3
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class JobDatabase:
    """SQLite-based job storage and retrieval"""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize JobDatabase

        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = Path.home() / '.jobfinder' / 'jobs.db'
        else:
            db_path = Path(db_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    description TEXT,
                    requirements TEXT,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    work_type TEXT,
                    url TEXT,
                    posted_date TEXT,
                    match_score REAL,
                    status TEXT DEFAULT 'new',
                    data TEXT,
                    discovered_at TEXT NOT NULL,
                    applied_at TEXT
                )
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_match_score
                ON jobs(match_score DESC)
            ''')

            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_status
                ON jobs(status)
            ''')

            conn.commit()

    def save_job(self, job: Dict) -> str:
        """Save or update a job listing

        Args:
            job: Job data dictionary

        Returns:
            Job ID
        """
        job_id = job.get('id', self._generate_job_id(job))

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO jobs (
                    id, platform, title, company, location, description,
                    requirements, salary_min, salary_max, work_type, url,
                    posted_date, match_score, status, data, discovered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_id,
                job.get('platform'),
                job.get('title'),
                job.get('company'),
                job.get('location'),
                job.get('description'),
                job.get('requirements'),
                job.get('salary_min'),
                job.get('salary_max'),
                job.get('work_type'),
                job.get('url'),
                job.get('posted_date'),
                job.get('match_score', 0.0),
                job.get('status', 'new'),
                json.dumps(job),
                datetime.now().isoformat()
            ))
            conn.commit()

        return job_id

    def get_job(self, job_id: str) -> Optional[Dict]:
        """Retrieve a job by ID

        Args:
            job_id: Job identifier

        Returns:
            Job data or None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT data FROM jobs WHERE id = ?',
                (job_id,)
            )
            row = cursor.fetchone()

            if row:
                return json.loads(row[0])

        return None

    def get_top_matches(self, limit: int = 10, min_score: float = 0.0) -> List[Dict]:
        """Get top matching jobs

        Args:
            limit: Maximum number of jobs to return
            min_score: Minimum match score threshold

        Returns:
            List of top matching jobs
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT data FROM jobs
                WHERE match_score >= ? AND status != 'rejected'
                ORDER BY match_score DESC, discovered_at DESC
                LIMIT ?
            ''', (min_score, limit))

            return [json.loads(row[0]) for row in cursor.fetchall()]

    def search_jobs(self, filters: Dict) -> List[Dict]:
        """Search jobs with filters

        Args:
            filters: Search filters (title, company, location, etc.)

        Returns:
            List of matching jobs
        """
        query = 'SELECT data FROM jobs WHERE 1=1'
        params = []

        if 'title' in filters:
            query += ' AND title LIKE ?'
            params.append(f'%{filters["title"]}%')

        if 'company' in filters:
            query += ' AND company LIKE ?'
            params.append(f'%{filters["company"]}%')

        if 'location' in filters:
            query += ' AND location LIKE ?'
            params.append(f'%{filters["location"]}%')

        if 'min_score' in filters:
            query += ' AND match_score >= ?'
            params.append(filters['min_score'])

        if 'status' in filters:
            query += ' AND status = ?'
            params.append(filters['status'])

        query += ' ORDER BY match_score DESC, discovered_at DESC'

        if 'limit' in filters:
            query += ' LIMIT ?'
            params.append(filters['limit'])

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            return [json.loads(row[0]) for row in cursor.fetchall()]

    def update_status(self, job_id: str, status: str) -> bool:
        """Update job application status

        Args:
            job_id: Job identifier
            status: New status (new/saved/applied/rejected/interview)

        Returns:
            True if updated, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'UPDATE jobs SET status = ? WHERE id = ?',
                (status, job_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_application_stats(self) -> Dict:
        """Get application statistics

        Returns:
            Dictionary with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT
                    status,
                    COUNT(*) as count
                FROM jobs
                GROUP BY status
            ''')

            stats = {row[0]: row[1] for row in cursor.fetchall()}

            cursor = conn.execute('SELECT COUNT(*) FROM jobs')
            total = cursor.fetchone()[0]

            cursor = conn.execute('''
                SELECT AVG(match_score) FROM jobs
                WHERE status != 'rejected'
            ''')
            avg_score = cursor.fetchone()[0] or 0.0

            return {
                'total': total,
                'by_status': stats,
                'average_match_score': avg_score
            }

    def _generate_job_id(self, job: Dict) -> str:
        """Generate a unique job ID

        Args:
            job: Job data

        Returns:
            Unique identifier
        """
        import hashlib
        content = f"{job.get('platform')}:{job.get('company')}:{job.get('title')}:{job.get('url')}"
        return hashlib.md5(content.encode()).hexdigest()
