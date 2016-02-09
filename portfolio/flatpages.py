from copy import deepcopy

from flask import url_for

from flask_flatpages import FlatPages
from werkzeug.utils import cached_property

from .utils import normalize_url_part


class PortfolioFlatPages(FlatPages):
    def get(self, path, default=None):
        if path.startswith('/'):
            pages = self._urls
        else:
            pages = self._pages

        if path.endswith('/'):
            result = self._filter_pages_by_path(pages, path)
        else:
            try:
                result = pages[path]
            except KeyError:
                result = default

        return result

    @cached_property
    def _pages(self):
        original_pages = super()._pages
        denormalized_pages = deepcopy(original_pages)

        for page in denormalized_pages.values():
            url = self._get_page_url(page, original_pages)
            if url is not None:
                page.meta['url'] = url

            self._denormalize_page(page, original_pages, denormalized_pages)

        self.reload()  # Flush original pages
        return denormalized_pages

    @cached_property
    def _urls(self):
        return {page.meta['url']: page
                for page in self._pages.values() if 'url' in page.meta}

    def _filter_pages_by_path(self, pages, path):
        filtered_pages = [page for (page_path, page) in pages.items()
                          if page_path.startswith(path)]

        return sorted(filtered_pages, key=lambda page: page.path)

    def _get_page_url(self, page, all_pages):
        if page.path.startswith('tags/'):
            tag_url = normalize_url_part(page.meta['name'])
            url = url_for('website.tag', tag=tag_url)

        elif page.path.startswith('projects/'):
            project_url = normalize_url_part(page.meta['name'])
            url = url_for('website.project', project=project_url)

        elif page.path.startswith('jobs/'):
            company_id = page.meta['company']
            company_name = all_pages['companies'].meta[company_id]['name']

            company_url = normalize_url_part(company_name)
            position_url = normalize_url_part(page.meta['name'])

            url = url_for(
                'website.job', company=company_url, position=position_url)

        else:
            url = None

        return url

    def _denormalize_page(self, page, original_pages, denormalized_pages):
        if page.path.startswith('tags/'):
            self._denormalize_tag_page(
                page, original_pages, denormalized_pages)

        elif page.path.startswith('projects/'):
            self._denormalize_project_page(
                page, original_pages, denormalized_pages)

        elif page.path.startswith('jobs/'):
            self._denormalize_job_page(
                page, original_pages, denormalized_pages)

    def _denormalize_job_page(self, page, original_pages, denormalized_pages):
        company_name = page.meta['company']
        all_companies = original_pages['companies']
        page.meta['company'] = all_companies.meta[company_name]

        page.meta['projects'] = [
            denormalized_pages['projects/' + project]
            for project in page.meta.get('projects', list())]

        page.meta['tags'] = [
            denormalized_pages['tags/' + tag]
            for tag in page.meta.get('tags', list())]

    def _denormalize_project_page(
            self, page, original_pages, denormalized_pages):
        project_id = page.path.split('/')[-1]

        all_jobs = self._filter_pages_by_path(original_pages, 'jobs/')
        for job_page in all_jobs:
            if project_id in job_page.meta.get('projects', list()):
                job = denormalized_pages[job_page.path]
                break
        else:
            job = None

        page.meta['job'] = job

        page.meta['tags'] = [
            denormalized_pages['tags/' + tag]
            for tag in page.meta.get('tags', list())]

    def _denormalize_tag_page(self, page, original_pages, denormalized_pages):
        tag_id = page.path.split('/')[-1]

        all_jobs = self._filter_pages_by_path(original_pages, 'jobs/')
        page.meta['jobs'] = [
            denormalized_pages[job.path] for job in all_jobs
            if tag_id in job.meta.get('tags', list())]

        all_projects = self._filter_pages_by_path(original_pages, 'projects/')
        page.meta['projects'] = [
            denormalized_pages[project.path] for project in all_projects
            if tag_id in project.meta.get('tags', list())]

        page.meta['related'] = [
            denormalized_pages['tags/' + tag]
            for tag in page.meta.get('related', list())]
