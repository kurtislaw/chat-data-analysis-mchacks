from flaskr import app
from flask import render_template
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
