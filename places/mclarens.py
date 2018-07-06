from places import restaurant_super
from random import choice
import re
from datetime import datetime, timedelta
class restaurant(restaurant_super):
	name = 'McLarens'
	lunch_url = "https://mclarens.gastrogate.com/lunch/"
	def __init__(self):
		restaurant_super.__init__(self, self.name, self.lunch_url)
	def build_menu(self, soup):
		self.menu_set_lunchtimes('10:30-14')
		self.menu_has_beer(True)
		menu_item = soup.find_all('tr', {"class": "lunch-menu-item"})

		lunches = []

		regex_price = '^(\d+)\s(?:kr|:-)$'
		regex_desc_with_price = '^(?:-\s*)?(\D+)\s+(\d+)\s*(?::-|kr)$'
		regex_desc_without_price = '^(?:-\s*)?(\D+)$'
		for m in menu_item:
			description_tag = m.find_all('td', {"class": "td_title"})
			price_tag = m.find_all('strong', {"class": "price-tag"})
			if len(price_tag) > 0:
				x = re.search(regex_price, price_tag[0].string)
				price = x.group(1)
			else:
				price = None
			# If we have a price tag, all children is part of the same lunch
			if price:
				desc_part = ""
				for c in description_tag[0].children:
					if c.name == None:
						#print c.string.strip()
						desc_part = desc_part + c.string.strip() + " "
				desc_part = desc_part.strip()
				x = re.search(regex_desc_without_price, desc_part)
				description = x.group(1)
				lunches.append([description, price])
			# If we dont have a price tag, children can be their own lunches
			else:
				for c in description_tag[0].children:
					if c.name == None:
						#print c.string.strip()
						x = re.search(regex_desc_with_price, c.string.strip())
						if x:
							description = x.group(1)
							price = x.group(2)
							lunches.append([description, price])
		today = datetime.today()
		dow = today.weekday() # 0 = monday, 6 = sunday
		monday = today - timedelta(days=dow)
		# Menu is valid the whole week, thus create menus for Monday to Sunday
		for i in range(0,7):
			day = monday + timedelta(days=i)
			date = day.strftime("%Y-%m-%d")
			for lunch in lunches:
				food = lunch[0]
				price = lunch[1]
				self.menu_add_lunch_to_day(date, food, price, not choice(['yes', 'maybe', 'no']) == 'no')
		return self.menu