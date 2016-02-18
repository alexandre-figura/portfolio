def test_access_job_page_from_home_page(live_server, browser):
    # Tom has heard about my website and decides to take a look.
    browser.get(live_server.url('/'))

    # He notices a navigation bar and goes to the home page.
    browser.find_element_by_xpath(
        "//a[@rel='navigate' and contains(text(), 'Home')]"
    ).click()
    assert 'Home' in browser.title

    # On the page, there is my career evolution.
    # Tom wants to know what I did in my last position.
    browser.find_element_by_xpath(
        "//a[@class='job__link' and "
        "contains(text(), 'Chief Technology Officer at WeKnowYouWantIt')]"
    ).click()
    assert 'Chief Technology Officer' in browser.title


def test_access_project_page_from_projects_page(live_server, browser):
    # Tom has heard about my website and decides to take a look.
    browser.get(live_server.url('/'))

    # He notices a navigation bar and goes to the projects page.
    browser.find_element_by_xpath(
        "//a[@rel='navigate' and contains(text(), 'Projects')]"
    ).click()
    assert 'Projects' in browser.title

    # On the page, all projects I made are listed.
    # Tom is intrigued by one as he made a similar project recently.
    browser.find_element_by_xpath(
        "//a[@class='project__link' and "
        "contains(text(), 'Development of a nextgen website')]"
    ).click()
    assert 'Development of a nextgen website' in browser.title


def test_access_tag_page_from_tags_page(live_server, browser):
    # Tom has heard about my website and decides to take a look.
    browser.get(live_server.url('/'))

    # He notices a navigation bar and goes to the tags page.
    browser.find_element_by_xpath(
        "//a[@rel='navigate' and contains(text(), 'Tags')]"
    ).click()
    assert 'Tags' in browser.title

    # On the page, all technologies I used in the past are listed.
    # Tom is intrigued by one which has a fancy name.
    browser.find_element_by_xpath(
        "//a[@class='tag__link' and contains(text(), 'Flask Web Framework')]"
    ).click()
    assert 'Flask Web Framework' in browser.title


def test_access_item_page_from_related_pages(live_server, browser):
    # Alice has heard about my website. She goes to check out its homepage.
    browser.get(live_server.url('/'))

    # She view my career evolution through a time-line
    # and is intrigued by a job title:
    # there is currently a similar position to fulfill in her company.
    browser.find_element_by_xpath(
        "//a[@class='job__link' "
        "and contains(text(), 'Software Developer at InDaCloud')]"
    ).click()

    # On the job page, there is a list of projects I made.
    projects = browser.find_elements_by_class_name('project__link')
    project_names = [project.text for project in projects]
    assert project_names == ['Development of a nextgen website',
                             'Modeling the future']
    # One of them looks like a project that her team planned to build
    # during the next quarter.
    projects[0].click()

    # The project page references the job page, too.
    related_job = browser.find_element_by_class_name('job__link').text
    assert related_job == 'Software Developer at InDaCloud'

    # The project description goes deeply into details.
    # Hopefully, used technologies are summarized in a list of tags.
    tags = browser.find_elements_by_class_name('tag__link')
    tag_names = [tag.text for tag in tags]
    assert tag_names == ['Python Programming Language', 'Flask Web Framework']

    # Alice notices a cutting edge technology among tags.
    # She wonders if I made other projects with.
    tags[0].click()

    # The tag page references the project page too.
    related_projects = [
        project.text
        for project in browser.find_elements_by_class_name('project__link')
    ]
    assert related_projects == ['Modeling the future',
                                'Development of a nextgen website']

    # Moreover, other tags are associated with the current tag:
    # a good idea to find related technologies.
    related_tags = browser.find_elements_by_class_name('tag__link')
    tag_names = [tag.text for tag in related_tags]
    assert tag_names == ['Flask Web Framework',
                         'eXtreme Programming Methodology']

    # The name of one of those tags draws the attention of Alice:
    # she decides to take a look at.
    related_tags[0].click()

    # The tag page references a list of related jobs.
    related_jobs = browser.find_elements_by_class_name('job__link')
    job_names = [job.text for job in related_jobs]
    assert job_names == ['Lead Developer', 'Software Developer']

    # A job of this list is the one with which Alice started her exploration.
    # In fact, if Alice comes back to the job page,
    # she can find related tags too. Hence, the loop is completed!
    related_jobs[1].click()
    related_tags = [
        tag.text for tag in browser.find_elements_by_class_name('tag__link')
    ]
    assert related_tags == ['Python Programming Language',
                            'Flask Web Framework']
