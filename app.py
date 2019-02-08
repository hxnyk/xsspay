import web

from flask import app, render_template, request, send_from_directory
from flask import Flask

app = Flask(__name__)
web.app = app

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

@web.register("/js/<path:path>")
def load_js(path):
    return send_from_directory("static/js", path)

@web.register("/css/<path:path>")
def load_css(path):
    return send_from_directory("static/css", path)

@web.register("/img/<path:path>")
def load_img(path):
    return send_from_directory("static/img", path)

# -----------------------------------------

@web.register("/")
def index():
    return render_template('index.html')
