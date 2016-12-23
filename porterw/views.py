from flask import render_template
from porterw import app
from porterw.forms import LoginForm
import pymongo

HOST='porter-mongodb'
PORT=48084
DB='porter'

# _______________________________________

def connectdb():
    client = pymongo.MongoClient(HOST, PORT)
    return getattr(client, DB)

# _______________________________________

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    db = connectdb()
    collection = 'jobs'
    col = pymongo.collection.Collection(db, collection, create=False)
#    jobs = [ job for job in col.find() ]
#    return "Jobs in DB %r" % jobs
    user = { 'nickname' : "Bobo" }
    return render_template('index.html', title='Home', user = user)
# _______________________________________

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
