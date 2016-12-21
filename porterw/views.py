from porterw import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return "Hello once again! You gave in eventuall, ha?"
