from flask import url_for


def find_links(page, xpath):
    return [link.attrib.get('href', None) for link in page.lxml.xpath(xpath)]


class TestHomePage:
    def test_all_jobs_are_listed(self, client):
        page = client.get(url_for('website.home'))
        actual_jobs = find_links(page, '//a[@class="job__link"]')

        # Jobs are sorted in descending chronological order.
        expected_jobs = [
            url_for('website.job', company=company, position=position)
            for company, position in [
                ('weknowyouwantit', 'chief_technology_officer'),
                ('indacloud', 'lead_developer'),
                ('indacloud', 'software_developer')]]

        assert actual_jobs == expected_jobs

    def test_all_social_profiles_are_listed(self, client):
        page = client.get(url_for('website.home'))
        actual_profiles = find_links(page, '//a[@rel="me"]')

        expected_profiles = [
            'www.website_1.social/profile', 'www.website_2.social/profile']

        assert actual_profiles == expected_profiles


class TestJobPage:
    @staticmethod
    def find_related_projects(page):
        return find_links(page, '//a[@class="project__link"]')

    @staticmethod
    def find_related_tags(page):
        return find_links(page, '//a[@class="tag__link"]')

    def test_job_not_found_returns_404(self, client):
        url = url_for('website.job', company='unknown', position='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_projects_are_referenced(self, client):
        url = url_for(
            'website.job', company='indacloud', position='software_developer')

        page = client.get(url)
        actual_projects = self.find_related_projects(page)

        expected_projects = [
            url_for('website.project', project=project)
            for project in [
                'development_of_a_nextgen_website', 'modeling_the_future']]

        assert actual_projects == expected_projects

    def test_related_tags_are_referenced(self, client):
        url = url_for(
            'website.job', company='indacloud', position='software_developer')

        page = client.get(url)
        actual_tags = self.find_related_tags(page)

        expected_tags = [
            url_for('website.tag', tag=tag)
            for tag in ['python_programming_language', 'flask_web_framework']]

        assert actual_tags == expected_tags


class TestProjectPage:
    @staticmethod
    def find_related_job(page):
        try:
            return find_links(page, '//a[@class="job__link"]')[0]
        except IndexError:
            return None

    @staticmethod
    def find_related_tags(page):
        return find_links(page, '//a[@class="tag__link"]')

    def test_project_not_found_returns_404(self, client):
        url = url_for('website.project', project='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_job_is_referenced(self, client):
        url = url_for(
            'website.project', project='development_of_a_nextgen_website')

        page = client.get(url)
        actual_job = self.find_related_job(page)

        expected_job = url_for(
            'website.job', company='indacloud', position='software_developer')

        assert actual_job == expected_job

    def test_related_tags_are_referenced(self, client):
        url = url_for('website.project',
                      project='development_of_a_nextgen_website')

        page = client.get(url)
        actual_tags = self.find_related_tags(page)

        expected_tags = [
            url_for('website.tag', tag=tag)
            for tag in ['python_programming_language', 'flask_web_framework']]

        assert actual_tags == expected_tags


class TestTagPage:
    @staticmethod
    def find_related_projects(page):
        return find_links(page, '//a[@class="project__link"]')

    @staticmethod
    def find_related_tags(page):
        return find_links(page, '//a[@class="tag__link"]')

    @staticmethod
    def find_related_jobs(page):
        return find_links(page, '//a[@class="job__link"]')

    def test_tag_not_found_returns_404(self, client):
        url = url_for('website.tag', tag='unknown')
        page = client.get(url, status='*')
        assert page.status_code == 404

    def test_related_projects_are_referenced(self, client):
        url = url_for('website.tag', tag='python_programming_language')

        page = client.get(url)
        actual_projects = self.find_related_projects(page)

        # Projects are sorted in descending chronological order.
        expected_projects = [
            url_for('website.project', project=project)
            for project in [
                'modeling_the_future', 'development_of_a_nextgen_website']]

        assert actual_projects == expected_projects

    def test_related_tags_are_referenced(self, client):
        url = url_for('website.tag', tag='python_programming_language')

        page = client.get(url)
        actual_tags = self.find_related_tags(page)

        expected_tags = [
            url_for('website.tag', tag=tag)
            for tag in [
                'flask_web_framework', 'extreme_programming_methodology']]

        assert actual_tags == expected_tags

    def test_related_jobs_are_referenced(self, client):
        url = url_for('website.tag', tag='flask_web_framework')

        page = client.get(url)
        actual_jobs = self.find_related_jobs(page)

        expected_jobs = [
            url_for('website.job', company=company, position=position)
            for company, position in [
                ('indacloud', 'lead_developer'),
                ('indacloud', 'software_developer')]]

        # Jobs are sorted in descending chronological order.
        assert actual_jobs == expected_jobs


def test_all_projects_are_listed_on_projects_page(client):
    page = client.get(url_for('website.projects'))
    actual_projects = find_links(page, '//a[@class="project__link"]')

    expected_projects = [
        url_for('website.project', project=project)
        for project in [
            'modeling_the_future', 'development_of_a_nextgen_website',
            'developed_my_portfolio']]

    # Projects are sorted in descending chronological order.
    assert actual_projects == expected_projects


def test_all_tags_are_listed_on_tags_page(client):
    page = client.get(url_for('website.tags'))
    actual_tags = find_links(page, '//a[@class="tag__link"]')

    expected_tags = [
        url_for('website.tag', tag=tag)
        for tag in [
            'extreme_programming_methodology', 'flask_web_framework',
            'python_programming_language']]

    # Tags are sorted by alphabetical order (case insensitive).
    assert actual_tags == expected_tags
