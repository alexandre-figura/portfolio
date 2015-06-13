from flask import Blueprint, render_template

website = Blueprint('website', __name__)


@website.route('/')
def home():
    return render_template('home.html')


@website.route('/skills')
def skills():
    return render_template('skills.html')


@website.route('/realizations')
def realizations():
    return render_template('realizations.html')


@website.route('/experiences')
def experiences():
    return render_template('experiences.html')
