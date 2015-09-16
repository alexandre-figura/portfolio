from flask import url_for


class TestExtendedFlatPages:
    def test_get_single_page(self, flatpages):
        page = flatpages.get('tags/tag 1')
        assert page.path == 'tags/tag 1'

    def test_get_multiple_pages(self, flatpages):
        pages = flatpages.get('tags/')
        current_paths = sorted(page.path for page in pages)
        expected_paths = ['tags/tag {}'.format(i) for i in range(1, 4)]
        assert current_paths == expected_paths

    def test_job_page_has_url_in_meta_properties(self, flatpages):
        page = flatpages.get('jobs/job 1')
        assert page['url'] == url_for(
            'website.job', company='indacloud', position='software_developer')
