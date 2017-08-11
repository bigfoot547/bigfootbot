import bot

class Tell:
	def __init__(self, target, nick, harbinger, message):
		self.target = target
		self.nick = nick
		self.message = message
		self.harbinger = harbinger

class TellManager:
	def __init__(self, filename, client):
		self.client = client
		self.filename = filename
		self.tells = []
		self.current_tell_number = 0

		try:
			file = open(self.filename, 'r')
		except FileNotFoundError:
			print("[TellManager] Input file not found")
			return

		str = file.read().split('\n')
		for each in str:
			tab = each.split(' ', maxsplit=3)
			if len(tab) < 4:
				break

			self.tells.append(0)
			self.tells[self.current_tell_number] = Tell(tab[0], tab[1], tab[2], tab[3])
			self.current_tell_number += 1
		file.close()

	def save_tells(self):
		file = open(self.filename, 'w')

		for each in self.tells:
			file.write(each.target + ' ' + each.nick + ' ' + each.harbinger + ' ' + each.message + '\n')
		file.close()
		return 0

	def add_tell(self, target, nick, harbinger, message):
		#print("In function add_tell")
		if self.current_tell_number == len(self.tells):
			self.tells.append(0)
		#print("Appended")
		self.tells[self.current_tell_number] = Tell(target, nick, harbinger, message)
		#print("Tell added")
		self.current_tell_number += 1
		#print("Returning")
		return self.current_tell_number-1

	def remove_tell(self, number, activate=True):
		if number > len(self.tells)-1:
			return 1

		tell = self.tells[number]
		if len(self.tells) == 1:
			self.current_tell_number = 0
			self.tells = []
			if activate:
				self.client.notice(tell.target, "{}: <{}@{}> {}".format(tell.nick, tell.harbinger, tell.target, tell.message))
			return 0

		self.tells.pop(number)
		self.current_tell_number -= 1
		if activate:
			self.client.notice(tell.target, "<{}@{}> {}: {}".format(tell.harbinger, tell.target, tell.nick, tell.message))
		return 0
