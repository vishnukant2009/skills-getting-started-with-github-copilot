"""
Pytest configuration and shared fixtures for test data isolation.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for making requests to the API."""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Provide a clean activities database for each test.
    Resets to initial state after each test for data isolation.
    """
    # Save original state
    original_state = {
        k: {"participants": v["participants"].copy(), **{k2: v2 for k2, v2 in v.items() if k2 != "participants"}}
        for k, v in activities.items()
    }
    
    # Reset to initial state before test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })
    
    yield activities
    
    # Restore original state after test
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def student_email():
    """Provide a test student email for signup tests."""
    return "testuser@mergington.edu"