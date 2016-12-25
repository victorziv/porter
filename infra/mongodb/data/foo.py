#!/usr/bin/python

import json

countries = []

data = json.load(open('countries_list.json'))

for d in data:
    cl = {}
    for k in d.keys():
        cl[k.lower()] = d[k]

    countries.append(cl)


f = open('countries.json', 'w')
json.dump(countries, f)
