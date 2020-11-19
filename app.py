from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    title = "Home"
    return render_template("layout.html", title=title)

if __name__ == "__main__":
    app.run(debug=True)