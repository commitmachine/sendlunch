#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from places import restaurant_super
import re, datetime

class restaurant(restaurant_super):
    name = 'Restaurang Westman'
    lunch_url = "http://westmanska.se/restaurang/"

    def __init__(self):
        restaurant_super.__init__(self, self.name, self.lunch_url)

    def date_from_week_number(self, week_number):
        year = datetime.datetime.now().year
        d = str(year) + "-W" + str(week_number)
        r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")

        return r

    def date_from_weekday(self, week_number, day):
        first_day_of_week = self.date_from_week_number(week_number)
        days = {
            'Måndag': 0,
            'Tisdag': 1,
            'Onsdag': 2,
            'Torsdag': 3,
            'Fredag': 4,
            'Lördag': 5,
            'Söndag': 6
        }
        if not unicode(day) in days.keys():
            return None

        x = days[unicode(day)]
        date = first_day_of_week + datetime.timedelta(days=x)

        return unicode(date)[:10]

    def build_menu(self, soup):
        self.menu_set_lunchtimes('11-14:30')
        panel = soup.find('div', { "class": "tab-content" })
        week = panel.find('h4').find('strong').text.replace("Vecka ", "")

        lunchrows = []
        rows = panel.find_all('p')
        date = None
        regex = '(.+) (\d*):-'

        for row in rows:
            day = row.find('strong')
            if day:
                date = self.date_from_weekday(week, unicode(day.text))
                all_food = unicode(row).replace(unicode(day), '').replace('Salladsbuffé från vår salladsbar 95 kr inkl. kaffe, te, efterrätt', '').split('<br/>')
                for food in all_food:
                    if '<' not in food:
                        final_dish = food.replace('(G)', '').replace('(L)', '').replace('(G, L)', '').replace('(G,L)', '').replace('&amp;', ' och ')
                        self.menu_add_lunch_to_day(date, final_dish, 95)
        return self.menu