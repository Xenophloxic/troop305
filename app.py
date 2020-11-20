from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/login', methods=['GET', 'POST'])
def login():
  return "test"

@app.route('/')
def index():
    title = "Home"
    return render_template("index.html", title=title)

@app.route('/webmaster')
def webhome():
  return "test"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/webmaster')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/