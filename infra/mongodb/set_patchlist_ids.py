import json
from bson import ObjectId

pf = open('patchlist.json', 'r')
patchlist = json.load(pf)
pf.close

print "Loaded patchlist: %r" % patchlist 

for p in patchlist:
    if not p.has_key('_id'):
        p['_id'] = str(ObjectId())


pfw = open('patchlist.json', 'w')
json.dump(patchlist, pfw, indent=4)
pfw.close()
