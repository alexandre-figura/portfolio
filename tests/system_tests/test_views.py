import flask


def test_home_page(client):
    page = client.get('/')
    assert flask.request.endpoint == 'home'
    assert page.status_code == 200

    assert "Who is Alexandre Figura?" in page.get_data(as_text=True)


def test_skills_page(client):
    page = client.get('/skills')
    assert flask.request.endpoint == 'skills'
    assert page.status_code == 200


def test_realizations_page(client):
    page = client.get('/realizations')
    assert flask.request.endpoint == 'realizations'
    assert page.status_code == 200


def test_experiences_page(client):
    page = client.get('/experiences')
    assert flask.request.endpoint == 'experiences'
    assert page.status_code == 200
