import bot

class Ban:
	def __init__(self, target, mask):
                self.target = target
                self.mask = mask

	def set_ban(self, client):
		client.rawmsg("MODE", self.target, '+b', self.mask)

	def remove_ban(self, client):
		client.rawmsg("MODE", self.target, '-b', self.mask)

class BanManager:

	def __init__(self, filename, client):
		self.bans = []
		self.current_ban_number = 0
		self.filename = filename
		self.client = client
		try:
			file = open(self.filename, 'r')
		except FileNotFoundError:
			print("[BanManager] Input file not found.")
			return
		string = file.read().split('\n')
		for each in string:
			tab = each.split(' ')
			if len(tab) < 2:
				break
			self.bans.append(0)
			self.bans[self.current_ban_number] = Ban(tab[0], tab[1])
			#self.bans[self.current_ban_number].set_ban(self.client)
			self.current_ban_number += 1
		file.close()

	def save_bans(self):
		file = open(self.filename, 'w')

		for each in self.bans:
			file.write(each.target + ' ' + each.mask + '\n')
		file.close()
		return 0

	def add_ban(self, target, hostmask):
		if self.current_ban_number == len(self.bans):
			self.bans.append(0)
		#print("In function add_ban {} {}".format(len(self.bans), self.current_ban_number))
		self.bans[self.current_ban_number] = Ban(target, hostmask)
		#print("Ban object created")
		self.bans[self.current_ban_number].set_ban(self.client)
		#print("Ban set")
		self.current_ban_number += 1
		return self.current_ban_number-1

	def remove_ban(self, number):
		#print("In function remove_ban")
		if number > len(self.bans)-1:
			return 1

		mask = self.bans[number]
		#print("Mask = ", type(mask))
		#print("bans = ", self.bans)
		if len(self.bans) == 1:
			#print("Only one ban. ", number)
			mask.remove_ban(self.client)
			self.current_ban_number = 0
			self.bans = []
			return 0

		self.bans.pop(number)
		mask.remove_ban(self.client)
		self.current_ban_number -= 1
		return 0
