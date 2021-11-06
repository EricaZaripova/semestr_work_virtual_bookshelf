from virtual_bookshelf import app


def test_main():
    app.testing = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
