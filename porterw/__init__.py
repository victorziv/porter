from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
from pymongo import MongoClient
dbclient = MongoClient(app.config['DBHOST'], app.config['DBPORT'])
db = getattr(dbclient, app.config['DBNAME'])

from porterw import views
