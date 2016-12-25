#!/usr/bin/python
import pymongo


HOST='localhost'
PORT=48084
DB='porter'

# _______________________________________

def connectdb():
    client = pymongo.MongoClient(HOST, PORT)
    return getattr(client, DB)

# _______________________________________

def main():

    db = connectdb()
    collection = 'config.schemapatch' 

    col = getattr(db, collection )
    col.drop()
    db.create_collection(collection)
# _______________________________________

if __name__ == '__main__':
    main()
