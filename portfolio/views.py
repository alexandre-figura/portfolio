from flask import Blueprint, render_template, url_for

from . import pages

website = Blueprint('website', __name__)


@website.route('/')
def home():
    content = {page: pages.get(page) for page in ['about', 'career']}

    content['jobs'] = sorted([
        {
            'position': job,
            'company': pages.get('companies')[job['company']],
            'url': job['url'],
        }
        for job in pages.get('jobs/*')
    ], key=lambda job: job['position']['period'], reverse=True)

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
