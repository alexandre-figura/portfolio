from flask import Blueprint, render_template, url_for

from . import pages
from .utils import get_url_from_name

website = Blueprint('website', __name__)


@website.route('/')
def home():
    content = {page: pages.get(page) for page in ['about', 'career']}

    for job in content['career']['jobs']:
        company_id, _ = job['id'].split('/', 1)
        job['position'] = pages.get('jobs/' + job['id'])
        job['company'] = pages.get('jobs/companies')[company_id]

        url_parts = {
            'company': get_url_from_name(job['company']['name']),
            'position': get_url_from_name(job['position']['name']),
        }
        job['url'] = url_for('.job', **url_parts)

    return render_template('home.html', **content)


@website.route('/jobs/<company>/<position>')
def job(company, position):
    return ""


@website.route('/projects')
def projects():
    projects = sorted(pages.get('projects/*'),
                      key=lambda p: p['period'][-1], reverse=True)
    content = {'projects': projects}
    return render_template('projects.html', **content)


@website.route('/tags')
def tags():
    tags = sorted(pages.get('tags/*'), key=lambda p: p['name'])
    content = {'tags': tags}
    return render_template('tags.html', **content)
