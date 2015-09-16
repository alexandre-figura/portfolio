from flask import url_for


class TestExtendedFlatPages:
    def test_job_page_has_url_in_meta_properties(self, flatpages):
        page = flatpages.get('jobs/job 1')
        assert page['url'] == url_for(
            'website.job', company='indacloud', position='software_developer')
