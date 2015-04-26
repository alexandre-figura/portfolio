import flask

app = flask.Flask(__name__)


@app.route('/')
def home():
    return "Alexandre Figura - Portfolio"


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
