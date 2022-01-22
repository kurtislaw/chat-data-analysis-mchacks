from flaskr import app

@app.route('/')
@app.route('/index')
def index():
    return "bro u a loser fr"
