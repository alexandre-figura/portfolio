def test_relations_between_content_items(live_server, browser):
    # Alice has heard about my website. She goes to check out its homepage.
    browser.get(live_server.url('/'))

    # She view my career evolution through a time-line
    # and is intrigued by a job title:
    # there is currently a similar position to fulfill in her company.
    browser.find_element_by_xpath(
        "//a[@class='job__link' and contains(text(), 'Software Developer at "
        "InDaCloud')]"
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
    assert related_projects == ['Project 1', 'Project 2']

    # Moreover, other tags are associated with the current tag:
    # a good idea to find related technologies.
    related_tags = browser.find_elements_by_class_name('tag__link')
    assert [tag.text for tag in related_tags] == ['Tag 2', 'Tag 3']

    # The name of one of those tags draws the attention of Alice:
    # she decides to take a look at.
    related_tags[0].click()

    # The tag page references a list of related jobs.
    related_jobs = browser.find_elements_by_class_name('job__link')
    assert [job.text for job in related_jobs] == ['Job 1', 'Job 2']

    # A job of this list is the one with which Alice started her exploration.
    # In fact, if Alice comes back to the job page,
    # she can find related tags too. Hence, the loop is completed!
    related_jobs[0].click()
    related_tags = [
        tag.text for tag in browser.find_elements_by_class_name('tag__link')
    ]
    assert related_tags == ['Tag 2', 'Tag 3']
