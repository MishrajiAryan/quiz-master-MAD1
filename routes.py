from flask import Flask, render_template
from app import app

#the decorator @app.route is directing towards root dir '/'
@app.route('/')
def index():
    return render_template('index.html')