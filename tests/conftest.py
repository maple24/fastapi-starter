"""
Test configuration and utilities
"""

import pytest
from fastapi.testclient import TestClient

from app.core.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_user():
    """Sample test user data"""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
    }


@pytest.fixture
def test_item():
    """Sample test item data"""
    return {"title": "Test Item", "description": "This is a test item"}
