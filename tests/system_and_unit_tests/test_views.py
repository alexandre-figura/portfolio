from flask import url_for


def test_home_page(client):
    page = client.get(url_for('home'))
    assert "Home" in page.html.title.string
    assert page.status_int == 200


def test_skills_page(client):
    page = client.get(url_for('skills'))
    assert "Skills" in page.html.title.string
    assert page.status_int == 200


def test_realizations_page(client):
    page = client.get(url_for('realizations'))
    assert "Realizations" in page.html.title.string
    assert page.status_int == 200


def test_experiences_page(client):
    page = client.get(url_for('experiences'))
    assert "Experiences" in page.html.title.string
    assert page.status_int == 200
