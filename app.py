import base64
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, send_file
from flask_session import Session
from helpers import login_required, SQL
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
import sqlalchemy
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
    

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
    with open(f'./text/{file}.txt', 'r') as f:
        return f.read()

def edit_file(file, text):
    f = open(f'./text/{file}.txt', 'w')
    f.writelines(text)
    fi = open(f'./text/{file}.txt')
    content = fi.read()
    fi.close()
    return content


@app.route('/')
def index():
    title = "Home"
    img = db.execute('SELECT * FROM images')
    event = db.execute("SELECT *, substr(date, 6,2) || '-' || substr(date, 9, 2)|| '-' || substr(date, 1, 4) AS new_date FROM events WHERE date >= date('now') ORDER BY new_date ASC LIMIT 4;")
    result = get_text("index-about")
    return render_template("index.html", title=title, images=img, year=datetime.now().year, indexabout=result, events=event)


@app.route('/events', methods=["GET", "POST"])
def events():
    event = db.execute("SELECT *, substr(date, 6,2) || '-' || substr(date, 9, 2)|| '-' || substr(date, 1, 4) AS new_date FROM events WHERE date >= date('now') ORDER BY new_date ASC;")
    return render_template('events.html', year=datetime.now().year, events=event, title="Events")


@app.route('/useful', methods=["GET", "POST"])
def useful():
    return render_template("useful.html", year=datetime.now().year, title="Useful Stuff")


@app.route('/advance', methods=["GET", "POST"])
def advance():      
    return redirect('./pdf/advancement.pdf')


@app.route('/photos', methods=["GET", "POST"])
def photos():
    img = db.execute('SELECT * FROM images')
    return render_template("photos.html", year=datetime.now().year, title="Photos", images=img)


@app.route('/docs', methods=["GET", "POST"])
def docs():
    return render_template('docs.html', year=datetime.now().year, title="Docs and Forms")


@app.route('/eagle', methods=["GET", "POST"])
def eagle():
    name = db.execute("SELECT *, substr(date, 6,2) || '-' || substr(date, 9, 2)|| '-' || substr(date, 1, 4) AS new_date FROM eagle ORDER BY new_date DESC")
    return render_template("eagle.html", year=datetime.now().year, title="Eagle Honor Roll", names=name)


@app.route('/presource', methods=["GET", "POST"])
def presource():
    return render_template("presource.html", year=datetime.now().year, title="Planning Resources")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    return redirect('mailto:scoutmaster@troop305.net')


@app.route('/policy', methods=["GET", "POST"])
def policy():
    return render_template("policy.html", year=datetime.now().year, title="Policy")


@app.route('/message', methods=["GET", "POST"])
def message():
    result = get_text('remind')
    return render_template("message.html", year=datetime.now().year, title="Messaging Services", code=result)


@app.route('/news', methods=["GET", "POST"])
def news():
    result = db.execute("SELECT * FROM news ORDER BY id DESC")
    return render_template("news.html", year=datetime.now().year, title="News", news=result)
    

@app.route('/pdf/<string:id>')
def pdf(id):
    return send_file(f'./pdf/{id}')


@app.route('/video/<id>')
def video(id):
    if id == "HOW TO BUILD A SNOW SHELTER - YouTube [360p].mp4":
        return redirect('https://youtu.be/pbQ6N0Kd6NY')
    elif id == "OKPIK.m4v":
        return redirect("https://youtu.be/_Skeve1gctA")


@app.route('/webmaster', methods=["GET", "POST"])
@login_required 
def webhome():
    return render_template('webmaster.html', title="Webmaster", year=datetime.now().year, home=True)


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
    if request.method == "POST":
        if request.form.get("sure") == "no":
            flash("Cancelled")
            return redirect('/webmaster')
        else:
            try:
                db.execute("DELETE FROM images WHERE id=:number", number=int(request.form.get("id")))
                flash("Done!")
                return redirect("/webmaster")
            except RuntimeError:
                flash("Invaild ID")
                return redirect("/webmaster")
    else:
        img = db.execute("SELECT * FROM images")
        return render_template('imgdel.html', title="Delete Images", year=datetime.now().year, home=True, images=img)


@app.route('/editevent', methods=['GET', 'POST'])
@login_required
def editevent():
    if request.method == "POST":
        if request.form.get("sure") == "no":
                flash("Cancelled")
                return redirect('/webmaster')
        else: 
            if request.form.get("submit") == "Delete":
                try:
                    db.execute("DELETE FROM events WHERE id=:number", number=int(request.form.get("id")))
                    flash("Done!")
                    return redirect("/webmaster")
                except RuntimeError:
                    flash("Invaild ID")
                    return redirect("/webmaster")
            else:
                db.execute("INSERT INTO events (event, date, desc, time) VALUES (:event, :date, :desc, :time)", event=request.form.get("event"), date=request.form.get("date"), desc=request.form.get("desc"), time=request.form.get("time"))
                flash("Done!")
                return redirect("/webmaster")
    else:
        event = db.execute("SELECT *, substr(date, 6,2) || '-' || substr(date, 9, 2)|| '-' || substr(date, 1, 4) AS new_date FROM events ORDER BY new_date ASC;")
        return render_template('editevent.html', title="Edit events", year=datetime.now().year, home=True, events=event)


@app.route('/newsedit', methods=["GET", "POST"])
@login_required
def newsedit():
    return render_template('webmaster.html', title="Webmaster", year=datetime.now().year, home=True)


@app.route('/hra', methods=['GET', 'POST'])
@login_required
def hra():
    if request.method == "POST":
        if request.form.get("sure") == "no":
                flash("Cancelled")
                return redirect('/webmaster')
        else:
            if request.form.get("submit") == "Add":
                try:
                    db.execute("INSERT INTO eagle (name, date) VALUES (:name, :date)", name=request.form.get("name"), date=request.form.get("date"))
                    flash("Done!")
                    return redirect("/webmaster")
                except RuntimeError:
                    flash("Error, please try again")
                    return redirect("/hra")
            else:
                try:
                    db.execute("DELETE FROM eagle WHERE name=:name", name=request.form.get("name"))
                    flash("Done!")
                    return redirect("/webmaster")
                except RuntimeError:
                    flash("Invaild ID")
                    return redirect("/webmaster")
    else:
        return render_template('hra.html', title="Add Honor Roll", year=datetime.now().year, home=True)


@app.route('/text', methods=['GET', 'POST'])
@login_required
def text():
    if request.method == "POST":
        if request.form.get("sure") == "no":
                flash("Cancelled")
                return redirect('/webmaster')
        else:
            if request.form.get("file") == "Front Page":
                x = "index-about"
            else:
                x = "remind"
            try:
                edit_file(x, request.form.get("desc"))
                flash("Done!")
                return redirect("/webmaster")
            except Exception:
                flash("Error, please try again")
                return redirect("/text")
    else:
        return render_template('text.html', title="Edit Text", year=datetime.now().year, home=True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html", name=e.name, code=e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == "__main__":
    app.run(debug=True)
