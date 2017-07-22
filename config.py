import configparser
import bot
import sys

class config(configparser.RawConfigParser):
	plugin_warning = 0

	def get(self, section, option, raw = False, vars = None, fallback = None):
		""" Get's a config value with exception handling. """
		try:
			return super().get(section, option)
		except (configparser.NoOptionError, configparser.NoSectionError) as e:
			# If it's something to do with plugins, then just warn the user and go on.
			if e.args[0] == "plugin_dir" or e.args[0] == "plugins":
				# We don't want to repeat the same error more then once.
				if self.plugin_warning == 1:
					self.plugin_warning = 0
					return ""

				# If this is the first error flag it.
				self.plugin_warning = 1

				# Warn the user and return.
				bot.warning("This bot isn't going to be useful without any plugins.")
				return ""

			# If we don't have any channels to join, just return a blank string.
			if e.args[0] == "channels":
				return ""

			# If it's something to do with SSL, then guess it by the port.
			# If we can't guess it by the port then default to False.
			if e.args[0] == "ssl":
				bot.warning("Missing SSL option in the config file, guessing based on port.")
				if self.port == 6697:
					return "True"
				elif self.port == 6667:
					return "True"
				else:
					bot.warning("We couldn't guess based on port, defaulting to False.")
					return "False"

			# Allow admin-less bot's.
			if e.args[0] == "hostnames" or e.args[0] == "nicknames":
				return ""

			# If it's any other section/option, then just make a fatal error.
			reason = str(e)
			bot.error("Invalid or empty config file. Exception: {}".format(reason), fatal = True)

	def getboolean(self, section, option):
		""" Gets a config value, converting it into a boolean value.
		True = Yes, yes, 1, True, true
		False = No, no, 0, False, false """
		value = self.get(section, option)
		if value == "Yes" or value == "yes" or value == "1" or value == "True" or value == "true":
			return True
		elif value == "No" or value == "no" or value == "0" or value == "False" or value == "false":
			return False

	def getint(self, section, option):
		""" Gets a config value, converting it into a interger. """
		value = self.get(section, option)
		# Before converting to a interger, check to see if it's a NoneType object.
		# If so, just return it.
		if value == None:
			return value

		return int(value)

	def getlist(self, section, option):
		""" Get's a list from a CSV value. """
		# Get the csv from the config.
		value = self.get(section, option)
		return_object = list()
		# If plugins isn't in the config file then return a blank list.
		if value == "" or not value:
			return return_object
		for each in value.split(','):
			# Strip the trailing space if any.
			each = each.strip(' ')
			# Add it to the list
			return_object.append(each)
		# Return the list.
		return return_object

	def read_config(self, file):
		""" Function to automate reading a config file. """
		# Read the config.
		result = self.read(file)
		# Set the values.
		self.server = self.get('main', 'server')
		self.port = self.getint('main', 'port')
		self.nick = self.get('main', 'nick')
		self.name = self.get('main', 'name')
		self.ssl = self.getboolean('main', 'ssl')
		self.channels = self.getlist('main', 'channels')
		self.plugins = self.getlist('main', 'plugins')
		self.plugin_dir = self.get('main', 'plugin_dir')
		self.sasl_password = self.get('main', 'sasl_password')
		self.sasl_username = self.get('main', 'sasl_username')
		self.admin_nicks = self.getlist('admins', 'nicknames')
		self.admin_hosts = self.getlist('admins', 'hostnames')
