def test_goals_page(client):
    response = client.get("/portfolio/goals/")
    assert response.status_code == 200

    data = response.get_json()
    assert data["goals"] == ["goal1"]
