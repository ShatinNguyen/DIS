from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('web.html')


# def hello():
#     name = request.args.get("name", "fucker \n")
#     title = name.center()
#     return f'Hello, {escape(title)}!'


