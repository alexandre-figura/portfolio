def test_overall_navigation_through_my_portfolio(live_server, browser):
    # Alice has heard about my website. She goes to check out its homepage.
    browser.get(live_server.url('/'))

    # She pays attention to the page title and sees that my website is a portfolio.
    assert "Alexandre Figura" in browser.title
    assert "Portfolio" in browser.title

    # She is intrigued and decides to explore each page listed in the navigation bar.
    navbar = [('home', '/'),
              ('skills', '/skills'),
              ('realizations', '/realizations'),
              ('experiences', '/experiences')]

    for active_tab, active_url in navbar:
        # When she clicks on a page name, she is taken to a new URL.
        browser.find_element_by_link_text(active_tab.capitalize()).click()
        assert browser.current_url == live_server.url(active_url)
        assert active_tab.capitalize() in browser.title

        # Moreover, the tab corresponding to the current page is highlighted: this is awesome!
        for tab, url in navbar:
            tab_link = browser.find_element_by_link_text(tab.capitalize())
            tab_is_active = "active" in tab_link.find_element_by_xpath('..').get_attribute('class')
            assert tab_is_active if tab == active_tab else not tab_is_active

    # Oh, wait! There are also links toward my social profiles :D
    for profile in ['Linkedin', 'StackOverflow', 'GitHub']:
        browser.find_element_by_link_text(profile).click()
        assert "Alexandre Figura" in browser.title
        assert "not found" not in browser.title.lower()
        browser.back()
