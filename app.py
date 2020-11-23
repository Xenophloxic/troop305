import base64

import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import login_required, SQL
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
db = SQL('sqlite:///database.sqlite3')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['GET', 'POST'])
def login():
    return "test"


@app.route('/')
def index():
    title = "Home"
    img = db.execute('SELECT * FROM images')
    return render_template("index.html", title=title, image=img)


@app.route('/webmaster')
def webhome():
    return "test"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": "9d4ed2d7a3d5758a3a3ad8d1aba2329d",
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)
            info = res.json()
            cap = request.form.get('Caption')
            print(cap)
            db.execute('INSERT INTO images (url, caption) VALUES (:url, :caption)',
                       url=info["data"]["display_url"], caption=cap)
            # return redirect('/webmaster')
        else:
            return "ERROR"
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)  # host='0.0.0.0'

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
