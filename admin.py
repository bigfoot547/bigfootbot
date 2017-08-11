import bot

class Admin:
	def __init__(self, target, nick):
		self.target = target
		self.nick =  nick

class AdminManager:
	def __init__(self, filename, client):
		self.admins = []
		self.client = client
		self.current_admin_number = 0
		self.filename = filename

		try:
			file = open(filename, 'r')
		except FileNotFoundError:
			print("[AdminManager] Input file not found.")
			return

		string = file.read().split('\n')
		for each in string:
			tab = each.split(' ')
			if len(tab) < 2:
				break
			self.admins.append(0)
			self.admins[self.current_admin_number] = Admin(tab[0], tab[1])
			self.current_admin_number += 1
		file.close()

	def save_admins(self):
		file = open(self.filename, 'w')

		for each in self.admins:
			file.write(each.target + ' ' + each.nick + '\n')
		file.close()
		return 0

	def add_admin(self, target, nick):
		#print("In add_admin")
		if self.current_admin_number == len(self.admins):
			self.admins.append(0)
		#print("Adding to list")
		self.admins[self.current_admin_number] = Admin(target, nick)
		#print("Returning")
		self.current_admin_number += 1
		return self.current_admin_number-1

	def remove_admin(self, number):
		if number > len(self.admins)-1:
			return 1

		if len(self.admins) == 1:
			self.current_admin_number = 0
			self.admins = []
			return 0

		self.admins.pop(number)
		self.current_admin_number -= 1
		return 0
