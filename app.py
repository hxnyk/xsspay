from flask import app, request
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "yeet"
