from typing import Collection
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify, make_response
from dotenv import load_dotenv
import os
import pytz
from flask_cors import CORS
from pyairtable import Table
from flaskext.markdown import Markdown

load_dotenv()

api_key = os.getenv("AIRTABLE_API_KEY")
path = "" if os.getenv("LOCAL_DEV") else "https://" + os.getenv("DETA_PATH")
host = ".deta.app" if os.getenv("DETA_SPACE_APP") else "" if os.getenv(
    "LOCAL_DEV") else ".deta.dev"
updatesTable = Table(api_key, 'appuc2zlKlrEX6OSv', 'Updates')
feedbackTable = Table(api_key, 'appuc2zlKlrEX6OSv', 'Feedback')

app = Flask(__name__)

Markdown(app)

CORS(app)

utc = pytz.utc

@app.route('/', methods=["GET", "POST"])
def index():
    submitted = False
    if request.method == 'POST':
        feedbackTable.create({'Status': 'To Be Read', "Subject": request.form['subject'], "Message": request.form['message']})
        submitted = True
    updates = updatesTable.all(sort=["-Publish Date"])
    r = make_response(render_template('index.html', updates=updates, submitted=submitted))
    r.headers.set('cache-control', 'no-store')
    return r

@app.route('/updates', methods=["GET"])
def updates():
    updates = updatesTable.all(sort=["-Publish Date"])
    r = make_response(render_template('updates.html', updates=updates))
    r.headers.set('cache-control', 'no-store')
    return r

@app.route('/post/<id>', methods=["GET"])
def post(id):
    post = updatesTable.get(id)
    updates = updatesTable.all(sort=["-Publish Date"])
    r = make_response(render_template('post.html', post=post, updates=updates))
    r.headers.set('cache-control', 'no-store')
    return r

if __name__ == "__main__":
    app.run(debug=True)
