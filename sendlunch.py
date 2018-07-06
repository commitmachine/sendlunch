#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os, sys, time, re, json, requests, importlib, places, sqlite3, pprint, time
from threading import Thread
from flask import Flask, request, Response, render_template
from datetime import datetime, date, timedelta

pp = pprint.PrettyPrinter(indent=2)
dbname = 'sendlunch.sqlite'
lunch_places = []

def to_str(string):
    if sys.version_info < (3,0):
         return unicode(string)
    return str(string)

#dynamic import of restaurants
for i in places.__all__:
    __import__("places." + i)
    lunch_places.append(sys.modules["places."+i].restaurant())

#set up the sqlite db
def init_db():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS lunches(
      lunchdate text, restaurant text, food text, price text, hasbeer boolean, everyday boolean, lunchtimes text
    )"""
    conn.execute(sql)
    conn.commit()
    conn.close()

#initialize everything
def init():
    init_db()
    #start polling thread
    t = Thread(target=get_lunches,
                   name='get_lunches')
    t.setDaemon(True)
    t.start()

def get_lunches():
    while(True):
        for lunch_place in lunch_places:
            add_lunches(lunch_place.get_lunches())
        time.sleep(2000)

def get_week_dates():
    year,week, dow = datetime.now().isocalendar()
    d = date(year,1,1)
    d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return datetime.now().strftime("%Y-%m-%d"), (d + dlt + timedelta(days=4)).strftime("%Y-%m-%d")

def add_lunches(menu):
    conn = sqlite3.connect(dbname)
    for date in menu['lunches'].keys():
        for food_list in menu['lunches'][date]:
            conn.cursor().execute("""INSERT INTO lunches SELECT ?, ?, ?, ?, ?, ?, ?
                                     WHERE NOT EXISTS(SELECT 1 FROM lunches
                                        WHERE lunchdate = ? AND restaurant = ? AND food = ?);""",
            (date, menu['name'], food_list['food'], food_list['price'], menu['hasbeer'], food_list['everyday'], menu['lunchtimes'],
             date, menu['name'], food_list['food'],))
    conn.commit()
    conn.close()

init()

app = Flask(__name__)
@app.route('/')
def site():
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    fromd ate, todate = get_week_dates()
    cur.execute("""SELECT lunchdate, restaurant, food, price, hasbeer, everyday, lunchtimes FROM lunches
                   WHERE lunchdate >= ? AND lunchdate <= ? ORDER BY restaurant""",
                (fromdate, fromdate,))
    rows = cur.fetchall()
    conn.close()

    current_header = ''
    current_name = ''
    current_lunchtimes = ''
    out = []
    for row in rows:
        header = None
        name = None
        lunchtimes = None
        if current_header != row[0]:
            header = row[0]
            current_header = row[0]
        if current_name != row[1]:
            name = row[1]
            current_name = row[1]
        if current_lunchtimes != row[6]:
            lunchtimes = row[6]
            current_lunchtimes = row[6]
        out.append({'header':header, 'headername':name, 'lunchtimes': lunchtimes, 'name': row[1], 'line': row[2], 'price': row[3], 'everyday': row[5]})
    return render_template('list.html', rows = out)
