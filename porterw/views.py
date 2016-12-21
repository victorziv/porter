from porterw import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return "Hello Bla! Don't you want to give in?"
