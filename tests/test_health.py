"""
Test health endpoints
"""


def test_health_check(client):
    """Test basic health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "uptime" in data


def test_detailed_health_check(client):
    """Test detailed health check endpoint"""
    response = client.get("/health/detailed")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "system_info" in data
    assert "memory_usage" in data
    assert "disk_usage" in data


def test_ping(client):
    """Test ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
