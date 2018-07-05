from places import restaurant_super
import re
class restaurant(restaurant_super):

    name = 'Bryggeriet'
    lunch_url = "http://www.kvartersmenyn.se/rest/9664"

    def __init__(self):
        restaurant_super.__init__(self, self.name, self.lunch_url)

    def build_menu(self, soup):
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
        for div in menu[0].children:
            if div.name == 'strong':
                today = div.string
                days[today] = []
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
                    days[today] = []
            elif div.name == None:
                self.menu_add_lunch_to_day(today, div.string)
        return self.menu