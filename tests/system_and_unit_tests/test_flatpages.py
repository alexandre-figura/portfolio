from flask import url_for


class TestPortfolioFlatPages:
    def test_get_single_page_from_path(self, flatpages):
        page = flatpages.get('tags/tag 1')
        assert page.path == 'tags/tag 1'

    def test_get_single_page_from_url(self, flatpages):
        url = url_for(
            'website.job', company='indacloud', position='software_developer')

        page = flatpages.get(url)
        assert page.path == 'jobs/job 1'

    def test_get_multiple_pages_from_path(self, flatpages):
        pages = flatpages.get('tags/')

        current_paths = sorted(page.path for page in pages)
        expected_paths = ['tags/tag {}'.format(i) for i in range(1, 4)]

        assert current_paths == expected_paths

    def test_get_multiple_pages_from_url(self, flatpages):
        pages = flatpages.get('/jobs/')

        current_paths = sorted(page.path for page in pages)
        expected_paths = ['jobs/job {}'.format(i) for i in range(1, 4)]

        assert current_paths == expected_paths

    def test_page_with_no_associated_view_has_no_url(self, flatpages):
        page = flatpages.get('about')
        assert 'url' not in page.meta

    def test_job_page_has_a_url(self, flatpages):
        page = flatpages.get('jobs/job 1')
        assert page.meta['url'] == url_for(
            'website.job', company='indacloud', position='software_developer')

    def test_project_page_has_a_url(self, flatpages):
        page = flatpages.get('projects/project 1')
        assert page.meta['url'] == url_for(
            'website.project', project='development_of_a_nextgen_website')

    def test_tag_page_has_a_url(self, flatpages):
        page = flatpages.get('tags/tag 1')
        assert page.meta['url'] == url_for(
            'website.tag', tag='python_programming_language')

    def test_denormalization_of_company_in_job_page(self, flatpages):
        page = flatpages.get('jobs/job 1')
        related_company = flatpages.get('companies').meta['company 1']
        assert page.meta['company'] == related_company

    def test_denormalization_of_job_related_pages_when_exist(self, flatpages):
        page = flatpages.get('jobs/job 1')

        related_tags = [flatpages.get('tags/' + tag)
                        for tag in ['tag 1', 'tag 2']]

        related_projects = [flatpages.get('projects/' + project)
                            for project in ['project 1', 'project 2']]

        assert page.meta['tags'] == related_tags
        assert page.meta['projects'] == related_projects

    def test_denormalization_of_job_related_pages_when_not_exist(
            self, flatpages):
        page = flatpages.get('jobs/job 3')

        assert page.meta['tags'] == []
        assert page.meta['projects'] == []

    def test_denormalization_of_project_related_pages_when_exist(
            self, flatpages):
        page = flatpages.get('projects/project 1')

        related_job = flatpages.get('jobs/job 1')

        related_tags = [flatpages.get('tags/' + tag)
                        for tag in ['tag 1', 'tag 2']]

        assert page.meta['job'] == related_job
        assert page.meta['tags'] == related_tags

    def test_denormalization_of_project_related_pages_when_not_exist(
            self, flatpages):
        page = flatpages.get('projects/project 3')
        assert page.meta['tags'] == []

    def test_denormalization_of_tag_related_pages_when_exist(self, flatpages):
        page = flatpages.get('tags/tag 1')

        related_tags = [flatpages.get('tags/' + tag)
                        for tag in ['tag 2', 'tag 3']]

        related_projects = [flatpages.get('projects/' + project)
                            for project in ['project 1', 'project 2']]

        related_jobs = [flatpages.get('jobs/' + project)
                        for project in ['job 1', 'job 2']]

        assert page.meta['related'] == related_tags
        assert page.meta['projects'] == related_projects
        assert page.meta['jobs'] == related_jobs

    def test_denormalization_of_tag_related_pages_when_not_exist(
            self, flatpages):
        page = flatpages.get('tags/tag 3')

        assert page.meta['related'] == []
        assert page.meta['projects'] == []
        assert page.meta['jobs'] == []
