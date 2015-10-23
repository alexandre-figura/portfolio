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
    project = pages.get_or_404(request.path)

    project_id = project.path.split('/')[-1]
    for page in pages.get('jobs/'):
        if project_id in page.meta.get('projects', list()):
            job = {
                'position': page,
                'company': pages.get('companies')[page['company']],
                'url': page.meta['url']}
            break
    else:
        job = None

    tags = [pages.get('tags/' + tag)
            for tag in project.meta.get('tags', list())]

    return render_template('project.html', project=project, job=job, tags=tags)


@website.route('/tags')
def tags():
    tags = sorted(pages.get('tags/'), key=lambda p: p['name'].lower())
    return render_template('tags.html', tags=tags)


@website.route('/tags/<tag>')
def tag(tag):
    tag = pages.get_or_404(request.path)

    tag_id = tag.path.split('/')[-1]
    projects = sorted((
        project for project in pages.get('projects/')
        if tag_id in project.meta.get('tags', list())
    ), key=lambda p: p['period'][-1], reverse=True)

    return render_template('tag.html', tag=tag, projects=projects)
