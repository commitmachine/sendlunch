#!/usr/bin/python
# -*- coding: utf-8 -*-
from places import restaurant_super
import re, datetime
class restaurant(restaurant_super):

    name = 'Bryggeriet'
    lunch_url = "http://www.kvartersmenyn.se/rest/9664"

    def __init__(self):
        restaurant_super.__init__(self, self.name, self.lunch_url)

    def date_from_week_number(self, week_number):
        year = datetime.datetime.now().year
        d = str(year) + "-W" + str(week_number)
        r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")

        return r

    def add_lunch(self, date, str, everyday = False):
        regex = r"(\D+)?((\d+):-)?"
        x = re.search(regex, str, re.IGNORECASE)
        name = x.group(1).strip()
        price = x.group(3)
        if price == None:
            price = self.lunch_price

        self.menu_add_lunch_to_day(date, name, int(price), everyday)

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
        if not day.encode('utf-8') in days.keys():
            return None

        x = days[day.encode('utf-8')]
        date = first_day_of_week + datetime.timedelta(days=x)

        return date

    def parse_price(self, soup):
        divider = soup.find_all('div', { "class": "divider-full" })
        for d in divider[0].children:
            if d.name == 'p' and not d.string == None:
                regex = r"^Pris (\d+):-$"
                x = re.search(regex, d.string, re.IGNORECASE)
                if not x == None:
                    return x.group(1)

    def parse_week_number(self, soup):
        divider = soup.find_all('div', { "class": "divider-full" })
        for d in divider[0].children:
            if d.name == 'p' and not d.string == None:
                regex = r"^VECKA (\d+), (\d+)"
                x = re.search(regex, d.string, re.IGNORECASE)
                if not x == None:
                    week = int(x.group(1))
                    year = int(x.group(2))

                    return [week, year]

    def build_menu(self, soup):
        self.menu_set_lunchtimes('12-15')
        w = self.parse_week_number(soup)
        week_number = w[0]
        year = w[1]
        self.lunch_price = self.parse_price(soup)

        self.menu_has_beer(True)
        all_days = []

        day = soup.find_all('div', { "class": "day" })
        menu = day[0].find_all('div', { "class": "meny" })
        opening_hours = {}
        for element in menu[1].children:
            if element.name == 'i' and not element.string == None:
                regex = '(\d+\.\d+)\s+-\s+(\d+\.\d+)'
                x = re.search(regex, element.string, re.IGNORECASE)
                #if not x == None:
                    #print(x.groups())
        days = {}
        today = None
        date = None
        for div in menu[0].children:
            if div.name == 'strong':
                today = div.string
                days[today] = []
                date = self.date_from_weekday(week_number, today)
                all_days.append(date)
            elif div.name == 'b':
                txt = None
                if div.string == None:
                    for x in div.children:
                        if not x.string == None:
                            txt = x.string
                else:
                    txt = div.string
                if txt == 'Hela veckan':
                    today = 'Week'
            elif div.name == None:
                date = self.date_from_weekday(week_number, today)
                if not date == None:
                    self.add_lunch(date.strftime('%Y-%m-%d'), div.string)
                else:
                    for day in all_days:
                        self.add_lunch(day.strftime('%Y-%m-%d'), div.string, True)
        return self.menu