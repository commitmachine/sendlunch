from bs4 import BeautifulSoup
import requests

class restaurant:

	lunch_url = None
	soup = None
	name = None
	menu = None

	def __init__(self, name, lunch_url):
		self.lunch_url = lunch_url
		self.name = name
		self.menu = {
			'name': self.name,
			'hasbeer': None,
			'lunches': {}
		}

	def download_menu(self):
		r = requests.get(self.lunch_url)
		return r.content

	def parse_menu_content(self, soup):
		return None

	def get_lunches(self):
		menu_content = self.download_menu()
		soup = BeautifulSoup(menu_content, 'html.parser')
		return self.parse_menu_content(soup)


	def menu_add_lunch_to_day(self, date, name, price, everyday):
		food_dict = {
						'food': name,
						'price': price,
						'everyday': everyday
					}

		if date not in menu['lunches'].keys():
			menu['lunches'][date] = [food_dict]
		else:
			menu['lunches'][date].append(food_dict)

	def menu_set_has_beer(self, hasbeer):
		menu['hasbeer'] = hasbeer
