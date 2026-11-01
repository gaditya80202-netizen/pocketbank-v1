"""Health and root endpoint tests."""


def test_health_endpoint_reports_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_describes_the_demo_api(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "PocketBank Demo API"
    assert response.json()["docs"] == "/docs"
