from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def INDEX():
    return render_template('/INDEX.html')


if __name__ == '__main__':
    app.run()
