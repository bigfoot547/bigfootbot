import importlib.machinery
import bot
import plugin
import sys
import os

class plugin_manager():
	def __init__(self, config):
		""" Initilizes the class. """
		self.plugins = dict()
		self.plugin_commands = list()
		self.config = config

	def load_plugins(self):
		""" Loads all plugins. """
		# Check to see if we have plugins to load.
		if self.config.plugins == "" or not self.config.plugins:
			bot.warning("Trying to load plugins but we can't find any.")
			return

		for plugin in self.config.plugins:
			# Load the plugin.
			module = self.load_plugin(plugin, self.config.plugin_dir + os.path.sep + "{}.py".format(plugin))
			# If we failed to load a plugin, go on to the other ones.
			if module == None:
				continue

			# Get the commands for said plugin.
			for each in module.commands:
				# Example, version:version_command:version_plugin.
				value = "{}:{}:{}".format(each, module.commands[each], module.__name__)
				self.plugin_commands.append(value)
			new_dict = {module.__name__: module}
			self.plugins.update(new_dict)

	def load_plugin(self, name, path):
		""" Loads plugin name from the plugins directory
		Returns: A module object, or None if it failed. """
		try:
			# Plugins are just python modules.
			loader = importlib.machinery.SourceFileLoader(name, path)
			module = loader.load_module()
			return module
		except:
			# Upon error, alert the user and return None.
			bot.error("Failure loading plugin: {}, Exception: {} {}".format(name, sys.exc_info()[0].__name__, sys.exc_info()[1]), fatal = True)
			return None

