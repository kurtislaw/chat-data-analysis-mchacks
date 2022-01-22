from flaskr import app
from flask import render_template, request, redirect, url_for
import json
from .individual import Conversation
from .individual import find_all_names
import plotly

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))


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
    return render_template('test.html', graphJSON=graphJSON)
