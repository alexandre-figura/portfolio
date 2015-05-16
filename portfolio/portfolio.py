from flask import Flask, render_template
from flask_flatpages import FlatPages

# Initialize Flask application.
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('portfolio.default_settings')
app.config.from_pyfile('portfolio.cfg', silent=True)

# Instantiate Flask extensions.
pages = FlatPages(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')


@app.route('/realizations')
def realizations():
    return render_template('realizations.html')


@app.route('/experiences')
def experiences():
    return render_template('experiences.html')
