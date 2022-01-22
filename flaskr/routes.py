from distutils.command.upload import upload
from flaskr import app
from flask import Flask, render_template, request, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('templates/index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        upload_file.save(uploaded_file.filename)
    return redirect(url_for('index'))
