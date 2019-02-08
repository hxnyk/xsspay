from flask import app, render_template, request, send_from_directory
from flask import Flask

app = Flask(__name__, static_url_path="static")

'''
app.py
static
-- js
-- -- script.js
-- css
-- -- style.css
-- img
-- -- icon.png
templates
-- index.html
'''

@app.route("/js/<path:path>")
def load_js(path):
    return send_from_directory("js", path)

@app.route("/css/<path:path>")
def load_css(path):
    return send_from_directory("css", path)

@app.route("/img/<path:path>")
def load_img(path):
    return send_from_directory("img", path)

# -----------------------------------------

@app.route("/")
def index():
    return render_template('index.html')
