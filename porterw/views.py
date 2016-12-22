from porterw import app
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
    jobs = [ job for job in col.find() ]
    return "Jobs in DB %r" % jobs
