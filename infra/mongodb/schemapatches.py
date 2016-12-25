import os
import  pymongo, json

# Keep a record for 90 days
record_expiration_time = 60*60*24*90

# Keep a record for 180 days
record_expiration_time_6month = 60*60*24*180

# Keep a cache record for 24 hours
record_cache_expiration_time = 60*60*24

# Long term collection ( keep for 2 years )
record_expiration_time_archive = 60*60*24*750

# Keep a testjob session for 7 days
jukebox_session_expiration_time = 60 * 60 * 24 * 7 

# Keep a CW user session for 22 hours
cwuser_session_expiration_time = 60 * 60 * 22

def connectdb():
    host='localhost'
    port=48084
    db='porter'
    client = pymongo.MongoClient(host, port)
    db = getattr(client, db)
    return db

#____________________________________________

def drop_collection(**kwargs):
    db = connectdb()
    collections = kwargs['collection']
    for collection in collections:
        try:
            col = pymongo.collection.Collection(db, collection, create=False)
            col.drop()
        except Exception as e:
            print "Error code: %r"  % e.code
            print "Error details: %r"  % e.details
            continue
#____________________________________________

def init_collection(**kwargs):
    db = connectdb()
    
    collection = kwargs['collection']

    col = pymongo.collection.Collection(db, collection, create=False)
    col.drop()

    db.create_collection(collection)

    indexes = kwargs.get('indexes', [])
    if len(indexes):
        for index in indexes:
            index_key = index.pop("index_key")
            index_key = [ (ikl[0], getattr(pymongo, ikl[1])) for ikl in index_key ]
            print "Index key: %r" % index_key
            print "Index: %r" % index
            col.create_index(index_key, **index)

    return col

#____________________________________________

def fill_collection_from_json_file(**kwargs):
    db = connectdb()
    collection = kwargs['collection']
    col = pymongo.collection.Collection(db, collection, create=False)

    json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), kwargs['json_file'])
    docs = json.load(open(json_file, 'r'))
    for doc in docs:
        try:
            insert_result = col.insert(doc, w=1)
            print("Insert  result: %r" % insert_result) 
        except pymongo.errors.DuplicateKeyError:
            continue
#____________________________________________

def obsolete_collection(**kwargs):
    collections = kwargs['collections']
    for collection in collections:
        try:
            col = pymongo.collection.Collection(db, collection, create=False)
            col.rename("obs.%s.obs" % collection)
        except Exception as e:
            print "Error code: %r"  % e.code
            print "Error details: %r"  % e.details
            continue
#____________________________________________


