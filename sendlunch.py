import os, sys, time, re, json, requests, importlib
from collections import OrderedDict, defaultdict
from flask import Flask, request, Response, render_template

from restaurants import mclarens

mc = mclarens.Mclarens()

mc.get_lunches()