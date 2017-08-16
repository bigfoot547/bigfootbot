import bot

class Channel:
	def __init__(self, name):
		self.name = name

class ChannelManager:
	def __init__(self, filename, client):
		self.filename = filename
		self.client = client
		self.channels = []
		self.current_channel = 0

		try:
			file = open(self.filename, 'r')
		except FileNotFoundError:
			print("[ChannelManager] Input file not found.")
			return
		str = file.read().split('\n')
		print(str)
		for each in str:
			if len(each) <= 0:
				break
			self.channels.append(0)
			self.channels[self.current_channel] = Channel(each)
			self.client.join(each)
			self.current_channel += 1
		file.close()

	def save_chans(self):
		file = open(self.filename, 'w')

		for each in self.channels:
			file.write(each.name + '\n')
		file.close()
		return 0

	def join_chan(self, target):
		if self.current_channel > len(self.channels)-1:
			self.channels.append(0)
		self.channels[self.current_channel] = Channel(target)
		self.current_channel += 1
		self.client.join(target)

	def part_chan(self, number, source):
		if number > len(self.channels)-1:
			return 1

		if len(self.channels) == 1:
			self.client.rawmsg('PART', self.channels[number].name, "Bot deactivated by {}.".format(source))
			self.channels = []
			self.current_channel = 0
			return 0

		channel = self.channels[number]
		self.channels.pop(number)
		self.current_channel -= 1
		self.client.rawmsg('PART', channel.name, "Bot deactivated by {}.".format(source))
		return 0
