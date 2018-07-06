#!/usr/bin/python
# -*- coding: utf-8 -*-
from places import restaurant_super
import re
from datetime import datetime, timedelta
class restaurant(restaurant_super):
    name = 'Hemma'
    lunch_url = "https://www.hemmavasastan.se/kopia-pa-boka-bord-1"
    def __init__(self):
        restaurant_super.__init__(self, self.name, self.lunch_url)

    def date_from_week_number(self, week_number):
        year = datetime.now().year
        d = str(year) + "-W" + str(week_number)
        r = datetime.strptime(d + '-1', "%Y-W%W-%w")

        return r

    def date_from_weekday(self, week_number, day):
        first_day_of_week = self.date_from_week_number(week_number)
        days = {
            'MÅNDAG': 0,
            'TISDAG': 1,
            'ONSDAG': 2,
            'TORSDAG': 3,
            'FREDAG': 4,
            'LÖRDAG': 5,
            'SÖNDAG': 6
        }
        #if not day.encode('utf-8') in days.keys():
        if not day.encode('utf-8') in days.keys():
            return None

        x = days[day.encode('utf-8')]
        date = first_day_of_week + timedelta(days=x)

        return date.strftime("%Y-%m-%d")

    def build_menu(self, soup):

        self.menu_has_beer(True)

        nonBreakSpace = u'\xa0'

        #print days.encode('utf-8')

        regex_week = '^Vecka\s(\d+)'
        regex_price = '^\s*Pris\s(\d+)'
        regex_days = '^(M\xc5NDAG|TISDAG|ONSDAG|TORSDAG|FREDAG|L\xd6RDAG|S\xd6NDAG)'
        regex_everyday = '^(Veckan|Alltid)'
        regex_dish_price = '(\d+):-'

        menu_item = soup.find_all('div', {"id": "comp-ivmtbgj3inlineContent"})
        header_item = menu_item[0].find_all('div', {"id": "comp-ivmua05y"})
        lunch_item = menu_item[0].find_all('div', {"id": "comp-ivmud3bc"})

        # Get price and week
        for i in header_item[0].children:
            i_str = i.string.replace(nonBreakSpace, ' ')

            x0 = re.search(regex_week, i_str)
            if x0:
                week = x0.group(1)

            x1 = re.search(regex_price, i_str)
            if x1:
                price = x1.group(1)

        # Get lunches
        for i in lunch_item[0].children:
            i_str = i.string
            if i_str:
                #print i_str
                x2 = re.search(regex_days, i.string)
                if x2:
                    day = x2.group(1)
                    #print day
            else:
                dish_item = i.find_all('p', {"class": "font_8"})
                for dish in dish_item:
                    dish_price = None
                    everyday = False

                    prefix = dish.contents[0].string.strip()
                    description = dish.contents[1].string.strip()

                    x3 = re.search(regex_dish_price, prefix)
                    if x3:
                        dish_price = x3.group(1)
                    else:
                        dish_price = price
                    
                    x4 = re.search(regex_everyday, prefix)
                    if x4:
                        everyday = True

                    date = self.date_from_weekday(week, day)

                    self.menu_add_lunch_to_day(date, description, dish_price, everyday)

                    #print(date, description, dish_price, everyday)

        return self.menu

