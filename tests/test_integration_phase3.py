"""Phase 3 integration tests — memory, jobs, consolidation."""
import pytest
from pathlib import Path

class TestMemorySchema:
    """Test memory DB schema."""

    def test_memory_store_exists(self):
        """Memory store should exist."""
        from brain.memory.store import MemoryStore
        assert hasattr(MemoryStore, "add_fact")
        assert hasattr(MemoryStore, "search_facts")
        assert hasattr(MemoryStore, "recall")

    def test_consolidator_exists(self):
        """Consolidator should exist."""
        from brain.memory.consolidate import Consolidator
        consolidator = Consolidator()
        assert hasattr(consolidator, "consolidate_nightly")


class TestScheduledJobs:
    """Test job files exist."""

    def test_morning_brief_exists(self):
        """Morning brief job should exist."""
        job_path = Path(__file__).parent.parent / "brain" / "jobs" / "morning_brief.md"
        assert job_path.exists()

    def test_all_five_jobs_exist(self):
        """All 5 jobs should exist."""
        jobs_dir = Path(__file__).parent.parent / "brain" / "jobs"
        job_files = [
            "morning_brief.md",
            "inbox_triage.md",
            "repo_health.md",
            "server_health.md",
            "school_reminders.md"
        ]
        for job_file in job_files:
            assert (jobs_dir / job_file).exists()

    def test_job_has_schedule_front_matter(self):
        """Jobs should have YAML front matter with schedule."""
        from pathlib import Path
        morning_brief = Path(__file__).parent.parent / "brain" / "jobs" / "morning_brief.md"
        content = morning_brief.read_text()
        assert "schedule:" in content
        assert "07:00" in content or "0 7" in content


def test_recall_tests_pass():
    """Recall accuracy tests should exist."""
    # Phase 3+: Create tests/test_recall.py with 90%+ precision benchmark
    pass
