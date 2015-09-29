from flask import url_for


class TestHomePage:
    def test_all_jobs_are_listed(self, client):
        page = client.get(url_for('website.home'))
        current_jobs = [job.text.strip()
                        for job in page.lxml.xpath('//a[@class="job__link"]')]
        # Jobs are sorted in descending chronological order.
        expected_jobs = ['Chief Technology Officer at WeKnowYouWantIt',
                         'Software Developer at InDaCloud']
        assert current_jobs == expected_jobs

    def test_all_social_profiles_are_listed(self, client):
        page = client.get(url_for('website.home'))
        social_profiles = [link.text.strip()
                           for link in page.lxml.xpath('//a[@rel="me"]')]
        assert social_profiles == ['Profile 1', 'Profile 2']


def test_all_projects_are_listed_on_projects_page(client):
    page = client.get(url_for('website.projects'))
    projects = [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]
    # Projects are sorted in descending chronological order.
    assert projects == ['Project 2', 'Project 1']


def test_all_tags_are_listed_on_tags_page(client):
    page = client.get(url_for('website.tags'))
    tags = [tag.text.strip()
            for tag in page.lxml.xpath('//a[@class="tag__link"]')]
    assert tags == ['Tag 1', 'Tag 2', 'Tag 3']
