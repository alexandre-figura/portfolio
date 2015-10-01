from flask import url_for

from flask_flatpages import FlatPages
from werkzeug.utils import cached_property

from .utils import normalize


class ExtendedFlatPages(FlatPages):
    def get(self, path, default=None):
        if path.startswith('/'):
            pages = self._urls
        else:
            pages = self._pages

        if path.endswith('/'):
            result = [page for page_path, page in pages.items()
                      if page_path.startswith(path)]
        else:
            try:
                result = pages[path]
            except KeyError:
                result = default

        return result

    def _get_page_url(self, page):
        pages = self._pages

        if page.path.startswith('jobs/'):
            company_id = page.meta['company']
            company_name = pages['companies'].meta[company_id]['name']
            company_url = normalize(company_name)
            position_url = normalize(page.meta['name'])

            url = url_for(
                'website.job', company=company_url, position=position_url)
        else:
            url = None

        return url

    @cached_property
    def _pages(self):
        pages = super()._pages
        for page in pages.values():
            page.meta['url'] = self._get_page_url(page)
        return pages

    @cached_property
    def _urls(self):
        pages = self._pages
        return {page.meta['url']: page for page in pages.values()
                if page.meta['url'] is not None}
