from flaskr import app
from flask import render_template, request, redirect, url_for
import json
from .individual import Conversation
import plotly

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    df = Conversation('/Users/kurtis/Documents/Personal/Coding/mchack-chats/inbox/agnesyau_4napxth37a')
    fig1 = df.message_over_time('flask')
    graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('test.html', graphJSON=graphJSON)


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))
