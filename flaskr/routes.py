from flaskr import app
from flask import render_template, request, redirect, url_for
import json
from .individual import Conversation
from .individual import find_all_names
import plotly
import os
from werkzeug.utils import secure_filename
import zipfile

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
            zip_ref.extractall(UPLOAD_FOLDER)
            zip_ref.close()
            return filename


@app.route('/successful')
def successful():
    names = list(find_all_names())
    return render_template('successful.html', names=names)


@app.route('/results', methods=['POST', 'GET'])
def results():
    selected = request.form.get('select-names')
    dir = find_all_names()[selected]
    df = Conversation(dir)
    fig1 = df.message_over_time('flask')
    graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('results.html', graphJSON=graphJSON)
