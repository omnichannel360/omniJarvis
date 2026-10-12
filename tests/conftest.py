"""Pytest fixtures for Jarvis tests."""
import pytest
from pathlib import Path
from policy.gate import Gate


@pytest.fixture
def workspace_tmp(tmp_path):
    """Mock workspace directory."""
    return tmp_path / "workspace"


@pytest.fixture
def audit_log(tmp_path):
    """Mock audit log."""
    return tmp_path / "audit.jsonl"


@pytest.fixture
def gate(audit_log):
    """Gate instance with temp audit log."""
    return Gate(str(audit_log))
