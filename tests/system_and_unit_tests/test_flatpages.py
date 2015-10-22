from flask import url_for


class TestExtendedFlatPages:
    def test_get_single_page_from_path(self, flatpages):
        page = flatpages.get('tags/tag 1')
        assert page.path == 'tags/tag 1'

    def test_get_single_page_from_url(self, flatpages):
        page = flatpages.get(url_for(
            'website.job', company='indacloud', position='software_developer'))
        assert page.path == 'jobs/job 1'

    def test_get_multiple_pages_from_path(self, flatpages):
        pages = flatpages.get('tags/')
        current_paths = sorted(page.path for page in pages)
        expected_paths = ['tags/tag {}'.format(i) for i in range(1, 4)]
        assert current_paths == expected_paths

    def test_get_multiple_pages_from_url(self, flatpages):
        pages = flatpages.get('/jobs/')
        current_paths = sorted(page.path for page in pages)
        expected_paths = ['jobs/job {}'.format(i) for i in range(1, 3)]
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
