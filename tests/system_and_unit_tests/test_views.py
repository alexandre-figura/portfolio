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


class TestJobPage:
    @staticmethod
    def find_projects(page):
        return [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]

    def test_job_not_found_returns_404(self, client):
        url = url_for('website.job', company='unknown', position='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_projects_are_listed_if_exist(self, client):
        url = url_for('website.job', company='indacloud',
                      position='software_developer')
        page = client.get(url)
        projects = self.find_projects(page)
        assert projects == ['Development of a nextgen website',
                            'Modeling the future']

    def test_projects_are_not_listed_if_not_exist(self, client):
        url = url_for('website.job', company='weknowyouwantit',
                      position='chief_technology_officer')
        page = client.get(url)
        projects = self.find_projects(page)
        assert projects == []


def test_all_projects_are_listed_on_projects_page(client):
    page = client.get(url_for('website.projects'))
    projects = [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]
    # Projects are sorted in descending chronological order.
    assert projects == ['Modeling the future',
                        'Development of a nextgen website']


def test_all_tags_are_listed_on_tags_page(client):
    page = client.get(url_for('website.tags'))
    tags = [tag.text.strip()
            for tag in page.lxml.xpath('//a[@class="tag__link"]')]
    assert tags == ['Tag 1', 'Tag 2', 'Tag 3']
