def test_goals_page(client):
    response = client.get("/portfolio/goals/")
    assert response.status_code == 200

    data = response.json()
    assert data["goals"] == ["goal1"]
