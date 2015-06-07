from portfolio import helpers


def test_rst_to_html():
    html = helpers.rst_to_html('test')
    assert '<p>test</p>' in html
