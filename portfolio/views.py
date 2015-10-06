from flask import Blueprint, request, render_template

from . import pages

website = Blueprint('website', __name__)


@website.route('/')
def home():
    content = {page: pages.get(page) for page in ['about', 'career']}

    content['jobs'] = sorted([
        {
            'position': job,
            'company': pages.get('companies')[job['company']],
            'url': job.meta['url'],
        }
        for job in pages.get('jobs/')
    ], key=lambda job: job['position']['period'], reverse=True)

    return render_template('home.html', **content)


@website.route('/jobs/<company>/<position>')
def job(company, position):
    position = pages.get_or_404(request.path)

    job = {
        'position': position,
        'company': pages.get('companies')[position['company']]}
    projects = [
        pages.get('projects/' + project)
        for project in position.meta.get('projects', list())]

    return render_template('job.html', job=job, projects=projects)


@website.route('/projects')
def projects():
    projects = sorted(pages.get('projects/'),
                      key=lambda p: p['period'][-1], reverse=True)
    return render_template('projects.html', projects=projects)


@website.route('/projects/<project>')
def project(project):
    return ""


@website.route('/tags')
def tags():
    tags = sorted(pages.get('tags/'), key=lambda p: p['name'])
    return render_template('tags.html', tags=tags)
