from __future__ import unicode_literals, print_function

#!/usr/bin/python
# -*- coding: utf-8 -*-
from places import restaurant_super
import re, datetime

class restaurant(restaurant_super):
    name = 'Underbar'
    lunch_url = "http://restaurangunderbar.se/lunch/"

    def __init__(self):
        restaurant_super.__init__(self, self.name, self.lunch_url)

    def date_from_week_number(self, week_number):
        year = datetime.datetime.now().year
        d = str(year) + "-W" + str(week_number)
        r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")

        return r

    def build_menu(self, soup):
        self.menu_set_lunchtimes('11-14:30')
        panels = soup.find_all('section', { "class": "page__content" })
        lunchrows = []

        for panel in panels:
            divs = panel.find_all('div')
            for div in divs:
                #find the first half of the menu
                ps = div.find_all('p')
                #for p in ps:
                #    lunchrows += (unicode(p).replace("<p>", "").replace("</p>", "").split("<br/>"))
                #get the rest
                lunchrows += (unicode(div).replace("<p>", "").replace('<div class="">', "").replace("</p>", "").split("<br/>"))

        for lunchrow in lunchrows:
            regex = '(.+) (\d*):-'
            x = re.search(regex, lunchrow, re.IGNORECASE)
            if x and x.group(1):
                self.menu_add_lunch_to_day(datetime.datetime.now().strftime('%Y-%m-%d'), x.group(1), x.group(2))


        return self.menu