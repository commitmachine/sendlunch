#!/usr/bin/python
# -*- coding: utf-8 -*-
from places import restaurant_super
import re, datetime
class restaurant(restaurant_super):
    name = 'Pompeij'
    lunch_url = "http://www.restaurangpompei.se/index.php/dagens-lunch"

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
        #if not day.encode('utf-8') in days.keys():
        if not day.encode('utf-8') in days.keys():
            return None

        x = days[day.encode('utf-8')]
        date = first_day_of_week + datetime.timedelta(days=x)

        return date

    def build_menu(self, soup):
        self.menu_has_beer(True)

        panels = soup.find_all('div', { "class": "sppb-panel-modern" })
        dish = None
        dishes = {}
        all_dates = {}

        for panel in panels:
            header = panel.find_all('div', { "class": "sppb-panel-heading" })
            title = header[0].find_all('span', { "class": "sppb-panel-title" })
            today = title[0].string

            table = panel.find_all('table')
            tds = panel.find_all('td')
            for td in tds:
                h3 = td.find_all('h3')
                if len(h3) > 0:
                    name = h3[0].string.strip()
                    if len(name) > 3:
                        y = self.date_from_weekday(27, today)
                        if not y == None:
                            all_dates[y] = True
                        dishes[name] = { "name": name, "date": y }
                x = td.string
                if len(name) > 0 and not td.string == None:
                    s = td.string.strip().replace(':-', '')
                    if s.isdigit():
                        dishes[name]['price'] = s
                    else:
                        dishes[name]['name'] += ' ' + td.string
        for d in dishes.keys():
            key = dishes[d]
            if not key['date'] == None:
                self.menu_add_lunch_to_day(key['date'].strftime('%Y-%m-%d'), key['name'], int(key['price']))
            else:
                for date in all_dates:
                    self.menu_add_lunch_to_day(date.strftime('%Y-%m-%d'), key['name'], int(key['price']))

        return self.menu