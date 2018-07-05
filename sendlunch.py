#!/usr/bin/python

import os, sys, time, re, json, requests, importlib
from places.mclarens import Mclarens

mc = Mclarens()

print mc.get_lunches()