from places import restaurant_super

class restaurant(restaurant_super):

	name = 'Bryggeriet'
	lunch_url = "http://www.kvartersmenyn.se/rest/9664"

	def __init__(self):
		restaurant_super.__init__(self, self.name, self.lunch_url)

	def build_menu(self, soup):
		day = soup.find_all('div', {"class": "day"})
		menu = day[0].find_all('div', { "class": "meny" })
		days = {}
		for div in menu[0].children:
		    today = None
		    if div.name == 'strong':
		        today = div.string
		        days[today] = []
		        print "Day: " + div.string
