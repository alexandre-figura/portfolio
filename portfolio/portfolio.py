from flask import Flask, Response, render_template, request

app = Flask(__name__)
app.config['THEME_ASSETS'] = 'assets'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/skills/index.html')
def skills():
    return "Skills"


@app.route('/realizations/index.html')
def realizations():
    return "Realizations"


@app.route('/experiences/index.html')
def experiences():
    return "Experiences"
