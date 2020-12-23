import base64
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import login_required, SQL
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
db = SQL('sqlite:///database.sqlite3')

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_text(file):
    if file == "indexabout":
        with open('./text/index-about.txt', 'r') as f:
            return f.read()


@app.route('/')
def index():
    title = "Home"
    img = db.execute('SELECT * FROM images')
    event = db.execute('SELECT * FROM events')
    result = get_text("indexabout")
    return render_template("index.html", title=title, images=img, year=datetime.now().year, indexabout=result, events=event)


@app.route('/events', methods=["GET", "POST"])
def events():
    if request.method == "POST":
        print('event post')
    else:
        event = db.execute('SELECT * FROM events')
        return render_template('events.html', year=datetime.now().year, events=event)


@app.route('/resource', methods=["GET", "POST"])
def resource():
    return "TODO resources"


@app.route('/advance', methods=["GET", "POST"])
def advance():
    return "TODO advancement"


@app.route('/photos', methods=["GET", "POST"])
def photos():
    return "TODO photos"


@app.route('/docs', methods=["GET", "POST"])
def docs():
    return "TODO Docs"


@app.route('/eagle', methods=["GET", "POST"])
def eagle():
    return "TODO eagle"


@app.route('/presource', methods=["GET", "POST"])
def presource():
    return "TODO Planning resources"


@app.route('/contact', methods=["GET", "POST"])
def contact():
    return "TODO Contact us"


@app.route('/policy', methods=["GET", "POST"])
def policy():
    return "TODO Policy"


@app.route('/message', methods=["GET", "POST"])
def message():
    return "TODO messaging services"


@app.route('/about', methods=["GET", "POST"])
def about():
    return "TODO About Us"


@app.route('/news', methods=["GET", "POST"])
def news():
    return "TODO News"
    

@app.route('/webmaster', methods=["GET", "POST"])
def webhome():
    return render_template('webmaster.html', title="Webmaster", year=datetime.now().year)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if not request.form.get("username"):
            return "must provide username"

        elif not request.form.get("password"):
            return "must provide password"

        else:
            if request.form.get("username") == "webmaster":
                if request.form.get("password") == "youshalln'tpass":
                    session["user_id"] = 1
                else:
                    return "Incorrect information"

        return redirect("/webmaster")

    else:
        return render_template("login.html", title="Log In")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
            # return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": "9d4ed2d7a3d5758a3a3ad8d1aba2329d",
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)
            info = res.json()
            db.execute('INSERT INTO images (url) VALUES (:url)',
                       url=info["data"]["display_url"])
            return redirect('/webmaster')
        else:
            return "ERROR"
    return render_template('upload.html', year=datetime.now().year)


@app.route('/imgdel', methods=['GET', 'POST'])
@login_required
def imgdel():
    return "Delete Images"


@app.route('/editevent', methods=['GET', 'POST'])
@login_required
def editevent():
    return "Edit Events"


@app.route('/caledit', methods=['GET', 'POST'])
@login_required
def caledit():
    return "Edit Calender"


@app.route('/hra', methods=['GET', 'POST'])
@login_required
def hra():
    return "Add Honor Roll"


@app.route('/text', methods=['GET', 'POST'])
@login_required
def text():
    return "Edit Text"


if __name__ == "__main__":
    app.run(debug=True)
