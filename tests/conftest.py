"""Shared fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    application = create_app(tmp_path / "test-banking.db")
    with TestClient(application) as test_client:
        yield test_client
