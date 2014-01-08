#!/usr/bin/env python
from flask import Flask
import pyfiglet
app = Flask(__name__)

@app.route('/')
@app.route('/<text>')
def hello_world(text=None):
    text = text or "Hello World!"
    fig = pyfiglet.Figlet()
    return fig.renderText(text)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
