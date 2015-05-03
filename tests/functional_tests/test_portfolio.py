from flask import url_for


def test_navigate_through_my_portfolio(browser):
    # Alice has heard about my website. She goes to check out its homepage.
    browser.get(url_for('home', _external=True))

    # She notices that the page content mentions that my website is a portfolio.
    assert "Portfolio" in browser.title
    assert "Alexandre Figura" in browser.title
