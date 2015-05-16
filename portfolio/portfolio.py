from flask import Flask, render_template

app = Flask(__name__)


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
