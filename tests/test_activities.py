"""
Tests for get_activities endpoint using AAA pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_all_activities_success(self, client, clean_activities):
        """
        Arrange: Set up clean activities database
        Act: Make request to GET /activities
        Assert: Verify response contains all activities with correct data
        """
        # Arrange
        expected_activity_names = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == 3
        assert set(data.keys()) == set(expected_activity_names)
    
    def test_get_activities_chess_club_data(self, client, clean_activities):
        """
        Arrange: Set up clean activities database
        Act: Make request to GET /activities
        Assert: Verify Chess Club has correct structure and data
        """
        # Arrange
        expected_description = "Learn strategies and compete in chess tournaments"
        expected_schedule = "Fridays, 3:30 PM - 5:00 PM"
        expected_max_participants = 12
        
        # Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        assert chess_club["description"] == expected_description
        assert chess_club["schedule"] == expected_schedule
        assert chess_club["max_participants"] == expected_max_participants
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_programming_class_data(self, client, clean_activities):
        """
        Arrange: Set up clean activities database
        Act: Make request to GET /activities
        Assert: Verify Programming Class has correct structure and data
        """
        # Arrange
        expected_description = "Learn programming fundamentals and build software projects"
        expected_schedule = "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
        expected_max_participants = 20
        
        # Act
        response = client.get("/activities")
        data = response.json()
        programming_class = data["Programming Class"]
        
        # Assert
        assert response.status_code == 200
        assert programming_class["description"] == expected_description
        assert programming_class["schedule"] == expected_schedule
        assert programming_class["max_participants"] == expected_max_participants
        assert isinstance(programming_class["participants"], list)
    
    def test_get_activities_gym_class_data(self, client, clean_activities):
        """
        Arrange: Set up clean activities database
        Act: Make request to GET /activities
        Assert: Verify Gym Class has correct structure and data
        """
        # Arrange
        expected_description = "Physical education and sports activities"
        expected_schedule = "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM"
        expected_max_participants = 30
        
        # Act
        response = client.get("/activities")
        data = response.json()
        gym_class = data["Gym Class"]
        
        # Assert
        assert response.status_code == 200
        assert gym_class["description"] == expected_description
        assert gym_class["schedule"] == expected_schedule
        assert gym_class["max_participants"] == expected_max_participants
        assert isinstance(gym_class["participants"], list)