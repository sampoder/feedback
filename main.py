from typing import Collection
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify, make_response
from dotenv import load_dotenv
import os
import pytz
from flask_cors import CORS
load_dotenv()

path = "" if os.getenv("LOCAL_DEV") else "https://" + os.getenv("DETA_PATH")
host = ".deta.app" if os.getenv("DETA_SPACE_APP") else "" if os.getenv(
    "LOCAL_DEV") else ".deta.dev"

app = Flask(__name__)

CORS(app)

utc = pytz.utc

@app.route('/', methods=["GET"])
def index():
    r = make_response(render_template('index.html'))
    r.headers.set('cache-control', 'no-store')
    return r

@app.route('/updates', methods=["GET"])
def updates():
    r = make_response(render_template('updates.html'))
    r.headers.set('cache-control', 'no-store')
    return r

@app.route('/post', methods=["GET"])
def post():
    r = make_response(render_template('post.html'))
    r.headers.set('cache-control', 'no-store')
    return r


if __name__ == "__main__":
    app.run(debug=True)
