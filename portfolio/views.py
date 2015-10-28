from flask import Blueprint, request, render_template

from . import pages

website = Blueprint('website', __name__)


@website.route('/')
def home():
    content = {page: pages.get(page) for page in ['about', 'career']}

    companies = pages.get('companies')
    content['jobs'] = sorted((
        {
            'position': job,
            'company': companies.meta[job.meta['company']],
            'url': job.meta['url'],
        }
        for job in pages.get('jobs/')
    ), key=lambda job: job['position'].meta['period'], reverse=True)

    return render_template('home.html', **content)


@website.route('/jobs/<company>/<position>')
def job(company, position):
    position = pages.get_or_404(request.path)

    companies = pages.get('companies')
    job = {
        'position': position,
        'company': companies.meta[position.meta['company']]}
    projects = [
        pages.get('projects/' + project)
        for project in position.meta.get('projects', list())]

    return render_template('job.html', job=job, projects=projects)


@website.route('/projects')
def projects():
    projects = sorted(
        pages.get('projects/'),
        key=lambda project: project.meta['period'][-1], reverse=True)
    return render_template('projects.html', projects=projects)


@website.route('/projects/<project>')
def project(project):
    project = pages.get_or_404(request.path)

    companies = pages.get('companies')
    project_id = project.path.split('/')[-1]
    for page in pages.get('jobs/'):
        if project_id in page.meta.get('projects', list()):
            job = {
                'position': page,
                'company': companies.meta[page.meta['company']],
                'url': page.meta['url']}
            break
    else:
        job = None

    tags = [pages.get('tags/' + tag)
            for tag in project.meta.get('tags', list())]

    return render_template('project.html', project=project, job=job, tags=tags)


@website.route('/tags')
def tags():
    tags = sorted(pages.get('tags/'), key=lambda tag: tag.meta['name'].lower())
    return render_template('tags.html', tags=tags)


@website.route('/tags/<tag>')
def tag(tag):
    tag = pages.get_or_404(request.path)

    tag_id = tag.path.split('/')[-1]
    projects = sorted((
        project for project in pages.get('projects/')
        if tag_id in project.meta.get('tags', list())
    ), key=lambda project: project.meta['period'][-1], reverse=True)

    tags = [pages.get('tags/' + tag)
            for tag in tag.meta.get('related', list())]

    jobs = sorted((
        job for job in pages.get('jobs/')
        if tag_id in job.meta.get('tags', list())
    ), key=lambda job: job.meta['period'], reverse=True)

    return render_template('tag.html', tag=tag, projects=projects, tags=tags,
                           jobs=jobs)
