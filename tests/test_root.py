"""
Tests for root endpoint (/) using AAA pattern.
"""

import pytest


class TestRootEndpoint:
    """Test suite for GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Arrange: Create test client
        Act: Make request to root endpoint with follow_redirects=False
        Assert: Verify redirect response and location header
        """
        # Arrange
        expected_redirect_path = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_path
    
    def test_root_redirect_follows_to_static_page(self, client):
        """
        Arrange: Create test client
        Act: Make request to root endpoint with follow_redirects=True
        Assert: Verify final response is successful
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200