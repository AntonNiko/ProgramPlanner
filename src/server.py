import flask
from flask import request
import os 

templateDir = os.path.abspath('../www/templates')
app = flask.Flask(__name__, template_folder=templateDir)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Yo</h1>"