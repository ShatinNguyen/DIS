from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "fucker \n")
    name2 = request.args.get("2", '3')

    s = 'test'
    return f'Hello, {escape(name)} {escape(s)}!'