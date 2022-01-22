from flaskr import app
from flask import render_template, request, redirect, url_for
import json
from .individual import Conversation
from .individual import find_all_names
import plotly
import os
from werkzeug.utils import secure_filename
import zipfile
from .overall import History

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

@app.route('/overall-results')
def overall():
    df = History('../inbox')

    fig1 = df.message_over_time('flask')
    message_over_time_graph = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    fig2 = df.popular_hours('flask')
    popular_hours_graph = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    top_names = list(df.individual_messages_count())[1:4]
    top_words = list(df.common_words())[1:4]

    return render_template(
        'overall.html',
        message_over_time_graph=message_over_time_graph,
        popular_hours_graph=popular_hours_graph,
        days_since=df.days_since_beginning(),
        total_messages=df.total_message_count(),
        top1=top_names[0],
        top2=top_names[1],
        top3=top_names[2],
        top_words=f'{top_words[0]}, {top_words[1]} and {top_words[2]}'
        )

@app.route('/individual-results', methods=['POST', 'GET'])
def individual_results():
    selected = request.form.get('select-names')
    dir = find_all_names()[selected]
    df = Conversation(dir)

    fig1 = df.message_over_time('flask')
    message_over_time_graph = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    fig2 = df.popular_hours('flask')
    popular_hours_graph = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    ppl = list(df.individual_messages_count())
    amt = list(df.individual_messages_count().values())

    if len(ppl) <= 1:
        p2 = 'you'
    else:
        p2 = ppl[1]

    if len(amt) <= 1:
        p2_amt = 'literally nothing back'
    else:
        p2_amt = amt[1]
    return render_template('individual-results.html',
                           message_over_time_graph=message_over_time_graph, 
                           popular_hours_graph=popular_hours_graph,
                           people=df.people(),
                           days_since=df.days_since_beginning(),
                           total_messages=df.total_message_count(),
                           p1=ppl[0],
                           p2=p2,
                           p1_amt=amt[0],
                           p2_amt=p2_amt,
                           first_texter=df.texted_first(),
                           first_content=df.first_text(),
                           first_day=df.first_day()
                           )
