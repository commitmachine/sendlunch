from bs4 import BeautifulSoup
import requests

class restaurant_super:

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

	def get_name(self):
		return self.name

	def download_menu(self):
		r = requests.get(self.lunch_url)
		return r.content

	def build_menu(self, soup):
		return None

	def get_lunches(self):
		menu_content = self.download_menu()
		soup = BeautifulSoup(menu_content, 'html.parser')
		return self.build_menu(soup)

	def menu_add_lunch_to_day(self, date, food, price = None, everyday = False):
		food_dict = {
						'food': food,
						'price': price,
						'everyday': everyday
					}

		if date not in self.menu['lunches'].keys():
			self.menu['lunches'][date] = [food_dict]
		else:
			self.menu['lunches'][date].append(food_dict)

	def menu_has_beer(self, hasbeer):
		self.menu['hasbeer'] = hasbeer
