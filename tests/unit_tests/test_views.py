from flask import url_for


def test_home_page(client):
    view = client.get(url_for('home'))
    assert view.status_code == 200
