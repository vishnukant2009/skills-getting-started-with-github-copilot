"""
Tests for signup and unregister endpoints using AAA pattern.
"""

import pytest


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_successful(self, client, clean_activities, student_email):
        """
        Arrange: Set up clean activities and test email
        Act: Make POST request to signup endpoint
        Assert: Verify successful response and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        initial_participants = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert student_email in data["message"]
        assert student_email in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_participants + 1
    
    def test_signup_activity_not_found(self, client, clean_activities, student_email):
        """
        Arrange: Set up test email
        Act: Make POST request to non-existent activity
        Assert: Verify 404 response with appropriate error message
        """
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student_email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert data["detail"] == "Activity not found"
    
    def test_signup_duplicate_participant(self, client, clean_activities, student_email):
        """
        Arrange: Sign up student first, then try again
        Act: Make duplicate POST request to signup endpoint
        Assert: Verify participant is added again (API allows duplicates)
        """
        # Arrange
        activity_name = "Chess Club"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act - Try to signup again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200  # API allows duplicates
        assert len(clean_activities[activity_name]["participants"]) == initial_count + 1  # Added again


class TestUnregisterEndpoint:
    """Test suite for DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_successful(self, client, clean_activities, student_email):
        """
        Arrange: Sign up student first, then unregister
        Act: Make DELETE request to unregister endpoint
        Assert: Verify successful response and participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        initial_participants = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert student_email in data["message"]
        assert student_email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_participants - 1
    
    def test_unregister_activity_not_found(self, client, clean_activities, student_email):
        """
        Arrange: Set up test email
        Act: Make DELETE request to non-existent activity
        Assert: Verify 404 response with appropriate error message
        """
        # Arrange
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student_email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert data["detail"] == "Activity not found"
    
    def test_unregister_participant_not_found(self, client, clean_activities):
        """
        Arrange: Set up non-existent participant email
        Act: Make DELETE request to unregister non-existent participant
        Assert: Verify 404 response with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": nonexistent_email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert data["detail"] == "Participant not found"