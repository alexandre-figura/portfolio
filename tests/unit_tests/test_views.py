import flask


def test_home_page(app):
    with app.test_client() as c:
        rv = c.get('/')
        assert flask.request.endpoint == 'home'
    assert rv.status_code == 200
