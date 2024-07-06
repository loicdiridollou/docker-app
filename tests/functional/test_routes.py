# tests/functional/test_routes.py
import json

from application import create_app


def test_home_page():
    app = create_app()

    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "healthy"


def test_actor_page():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get("/actors")
        assert response.status_code == 200


def test_movie_page():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get("/movies")
        assert response.status_code == 200


def test_post_patch_delete_actor():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post(
            "/actors",
            data=json.dumps({"name": "John", "age": 25, "gender": "male"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        created_id = json.loads(response.data)["created"]

        response = test_client.patch(
            "/actors/" + str(created_id),
            data=json.dumps({"name": "Johnny"}),
            content_type="application/json",
        )
        assert response.status_code == 200

        response = test_client.delete("/actors/" + str(created_id))
        assert response.status_code == 200
