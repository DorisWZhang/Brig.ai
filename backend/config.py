from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>hello</h1>"

#render_template allows you to return an html file instead of a
# the html code as a string
