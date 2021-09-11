from application import create_app
import json

def test_home_page():
    app = create_app()

    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data['message'] == 'healthy'

        response = test_client.get('/actors')
        assert response.status_code == 200

        response = test_client.get('/movies')
        assert response.status_code == 200
