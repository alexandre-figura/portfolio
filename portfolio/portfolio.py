from flask import Flask, Response, render_template, request

app = Flask(__name__)
app.config['THEME_ASSETS'] = 'assets'


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
