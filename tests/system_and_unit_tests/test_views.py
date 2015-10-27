from flask import url_for


class TestHomePage:
    def test_all_jobs_are_listed(self, client):
        page = client.get(url_for('website.home'))
        current_jobs = [job.text.strip()
                        for job in page.lxml.xpath('//a[@class="job__link"]')]
        # Jobs are sorted in descending chronological order.
        expected_jobs = ['Chief Technology Officer at WeKnowYouWantIt',
                         'Lead Developer at InDaCloud',
                         'Software Developer at InDaCloud']
        assert current_jobs == expected_jobs

    def test_all_social_profiles_are_listed(self, client):
        page = client.get(url_for('website.home'))
        social_profiles = [link.text.strip()
                           for link in page.lxml.xpath('//a[@rel="me"]')]
        assert social_profiles == ['Profile 1', 'Profile 2']


class TestJobPage:
    @staticmethod
    def find_related_projects(page):
        return [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]

    def test_job_not_found_returns_404(self, client):
        url = url_for('website.job', company='unknown', position='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_projects_are_listed_if_exist(self, client):
        url = url_for('website.job', company='indacloud',
                      position='software_developer')
        page = client.get(url)
        projects = self.find_related_projects(page)
        assert projects == ['Development of a nextgen website',
                            'Modeling the future']

    def test_related_projects_are_not_listed_if_not_exist(self, client):
        url = url_for('website.job', company='indacloud',
                      position='lead_developer')
        page = client.get(url)
        projects = self.find_related_projects(page)
        assert projects == []


class TestProjectPage:
    @staticmethod
    def find_related_job(page):
        try:
            return page.lxml.xpath('//a[@class="job__link"]')[0].text.strip()
        except IndexError:
            return None

    @staticmethod
    def find_related_tags(page):
        return [tag.text.strip()
                for tag in page.lxml.xpath('//a[@class="tag__link"]')]

    def test_project_not_found_returns_404(self, client):
        url = url_for('website.project', project='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_job_is_referenced_if_exists(self, client):
        url = url_for('website.project',
                      project='development_of_a_nextgen_website')
        page = client.get(url)
        job = self.find_related_job(page)
        assert job == 'Software Developer at InDaCloud'

    def test_related_job_is_not_referenced_if_not_exists(self, client):
        url = url_for('website.project', project='developed_my_portfolio')
        page = client.get(url)
        job = self.find_related_job(page)
        assert job is None

    def test_related_tags_are_referenced_if_exist(self, client):
        url = url_for('website.project',
                      project='development_of_a_nextgen_website')
        page = client.get(url)
        tags = self.find_related_tags(page)
        assert tags == ['Python Programming Language', 'Flask Web Framework']

    def test_related_tags_are_not_referenced_if_not_exist(self, client):
        url = url_for('website.project', project='developed_my_portfolio')
        page = client.get(url)
        tags = self.find_related_tags(page)
        assert tags == []


class TestTagPage:
    @staticmethod
    def find_related_projects(page):
        return [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]

    @staticmethod
    def find_related_tags(page):
        return [tag.text.strip()
                for tag in page.lxml.xpath('//a[@class="tag__link"]')]

    def test_tag_not_found_returns_404(self, client):
        url = url_for('website.tag', tag='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_projects_are_referenced_if_exist(self, client):
        url = url_for('website.tag', tag='python_programming_language')
        page = client.get(url)
        projects = self.find_related_projects(page)
        # Projects are sorted in descending chronological order.
        assert projects == ['Modeling the future',
                            'Development of a nextgen website']

    def test_related_projects_are_not_referenced_if_not_exist(self, client):
        url = url_for('website.tag', tag='extreme_programming_methodology')
        page = client.get(url)
        projects = self.find_related_projects(page)
        assert projects == []

    def test_related_tags_are_referenced_if_exist(self, client):
        url = url_for('website.tag', tag='python_programming_language')
        page = client.get(url)
        tags = self.find_related_tags(page)
        assert tags == ['Flask Web Framework',
                        'eXtreme Programming Methodology']

    def test_related_tags_are_not_referenced_if_not_exist(self, client):
        url = url_for('website.tag', tag='flask_web_framework')
        page = client.get(url)
        tags = self.find_related_tags(page)
        assert tags == []


def test_all_projects_are_listed_on_projects_page(client):
    page = client.get(url_for('website.projects'))
    projects = [project.text.strip()
                for project in page.lxml.xpath('//a[@class="project__link"]')]
    # Projects are sorted in descending chronological order.
    assert projects == ['Modeling the future',
                        'Development of a nextgen website',
                        'Developed my portfolio']


def test_all_tags_are_listed_on_tags_page(client):
    page = client.get(url_for('website.tags'))
    tags = [tag.text.strip()
            for tag in page.lxml.xpath('//a[@class="tag__link"]')]
    # Tags are sorted by alphabetical order (case insensitive).
    assert tags == ['eXtreme Programming Methodology', 'Flask Web Framework',
                    'Python Programming Language']
