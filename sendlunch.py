#!/usr/bin/python
import os, sys, time, re, json, requests, importlib
import places

places_list = []

for i in places.__all__:
    __import__("places." + i)
    places_list.append(sys.modules["places."+i].restaurant().get_name())

print places_list
