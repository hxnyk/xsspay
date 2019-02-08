from flask import app, render_template, request, send_from_directory
from flask import Flask

app = Flask(__name__)

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
    return send_from_directory("static/js", path)

@app.route("/css/<path:path>")
def load_css(path):
    return send_from_directory("static/css", path)

@app.route("/img/<path:path>")
def load_img(path):
    return send_from_directory("static/img", path)

# -----------------------------------------

@app.route("/")
def index():
    return render_template('auth.html')
