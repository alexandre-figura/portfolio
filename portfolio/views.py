from flask import Blueprint, request, render_template

from . import pages

website = Blueprint('website', __name__)


@website.route('/')
def home():
    content = {page: pages.get(page) for page in ['about', 'career']}

    content['jobs'] = sorted(
        pages.get('jobs/'), key=lambda job: job.meta['period'], reverse=True)

    return render_template('home.html', **content)


@website.route('/jobs/<company>/<position>')
def job(company, position):
    job = pages.get_or_404(request.path)
    return render_template('job.html', job=job)


@website.route('/projects')
def projects():
    projects = sorted(
        pages.get('projects/'),
        key=lambda project: project.meta['period'][-1], reverse=True)

    return render_template('projects.html', projects=projects)


@website.route('/projects/<project>')
def project(project):
    project = pages.get_or_404(request.path)
    return render_template('project.html', project=project)


@website.route('/tags')
def tags():
    tags = sorted(pages.get('tags/'), key=lambda tag: tag.meta['name'].lower())
    return render_template('tags.html', tags=tags)


@website.route('/tags/<tag>')
def tag(tag):
    tag = pages.get_or_404(request.path)

    jobs = sorted(
        tag.meta['jobs'], key=lambda job: job.meta['period'], reverse=True)

    projects = sorted(
        tag.meta['projects'],
        key=lambda project: project.meta['period'][-1], reverse=True)

    return render_template('tag.html', tag=tag, jobs=jobs,  projects=projects)
