#!/usr/bin/python
import os, sys, time, re, json, requests, importlib
import places
import pprint

pp = pprint.PrettyPrinter(indent=4)

places_list = []

for i in places.__all__:
    __import__("places." + i)
    places_list.append(sys.modules["places."+i].restaurant().get_lunches())

for p in places_list:
    pp.pprint(p)

