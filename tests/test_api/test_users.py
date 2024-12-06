


def test_read_item(create_user, req):
    response = req.get("/api/v1/users")
    assert response.status_code == 200