#!/usr/bin/python
import os, sys, pymongo, json
from bson import ObjectId
project = 'porter'
import schemapatches
DB = schemapatches.connectdb()

#________________________________________

def apply_patch(patch):

    patch_collection = 'config.schemapatch' 
    col = pymongo.collection.Collection(DB, patch_collection, create=False)

    try:
        patchid = col.insert(patch, w=1)
        print 'Patch ID: %r' % patchid

    except pymongo.errors.DuplicateKeyError:
        print "Patch %s(%s) already applied - skipping" % (patch['_id'], patch['name'])
        return True

    else:

        try:
            print "Applying patch: %s(%s)" % (patch['_id'], patch['name'])
            pfunc = getattr(schemapatches, patch['name'])
            pfunc(**patch['kwargs'])

        except Exception as e:
            print "Exception: %s" % str(e)
            print "Patch %s(%s) failed - removing from patch registry" % (patch['_id'], patch['name'])
            remove_result = col.remove({'_id':patchid})
            print "Removed: %r" % remove_result
            return False 

    return True
#________________________________________

def set_patch_ids(patchf):
    pf = open(patchf, 'r')
    patchlist = json.load(pf)
    pf.close

    print "Loaded patchlist: %r" % patchlist 

    for p in patchlist:
        if not p.has_key('_id'):
            p['_id'] = str(ObjectId())

    pfw = open(patchf, 'w')
    json.dump(patchlist, pfw, indent=4)
    pfw.close()
#________________________________________

def patch_schema():

    patch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patchlist.json')
    set_patch_ids(patch_path)
    patch_list_file = open(patch_path, 'r')
    patchlist = json.load(patch_list_file)
    patch_list_file.close()

    print "Patch list: %r" % patchlist
    
    results = []
    for p in patchlist:
        results.append(apply_patch(p))

    return results

#____________________________________________

def main():

    results = patch_schema()

    if all(results):
        rc = 0
    else:
        rc = 1

    sys.exit(rc)
#________________________________________

if __name__ == '__main__':
    main()

