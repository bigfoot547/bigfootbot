#!/usr/bin/env python3
# Imports
import argparse
import os
import bot
import config
import plugins
import socket
import sys
import exceptions
import path

# Parse arguments
parser = argparse.ArgumentParser(description='None')
parser.add_argument('--config', help='Sets where we get our config from.', required=False)
args = parser.parse_args() # Parse the arguments and set 'args' to be a reference to it.

# Handle arguments.
if args.config:
	config_dir = args.config
else:
	path_obj = path.path()
	path_obj.fromstr(os.getcwd())
	path_obj.add(".pybot")
	config_dir = path_obj.tostr()

# Initialize the config system, and read the config.
config_obj = config.config()
config_obj.config_dir = config_dir
config_obj.read_config("main.conf")

# Initialize the plugin system, and load plugins.
plugin_obj = plugins.plugin_manager(config_obj)
plugin_obj.load_plugins()

# Initialize the bot.
try:
	client = bot.Bot(nickname = config_obj.nick, realname = config_obj.name)
	# Pass on our plugin_manager instance, config instance, and the channel list.
	client.plugin = plugin_obj
	client.channel_list = config_obj.channels
	client.config = config_obj
	# Connect the bot.
	client.sasl_password = config_obj.sasl_password
	client.sasl_username = config_obj.sasl_username
	client.connect(config_obj.server, config_obj.port, tls = config_obj.ssl)
	# Go into a infinite event loop. (This never returns unless an exception is thrown.)
	client.handle_forever()
except KeyboardInterrupt:
	# Exit on CTRL+C
	try:
		bot.error("Recieved KeyboardInterrupt, Exiting.")
		client.quit(message = "Recieved KeyboardInterrupt.")
	except BaseException as e:
		# Catch exceptions from pydle.
		bot.error("Failed to disconnect, probably haven't connected yet. {} {}".format(str(e), type(e)))

	sys.exit(2)
except (ConnectionRefusedError, socket.timeout):
	# Handle connection errors.
	bot.error("Error connecting to {}:{}, Exception: {} {}".format(config_obj.server, config_obj.port, sys.exc_info()[0], sys.exc_info()[1]), fatal = True)
except:
	# Handle random exceptions.
	# It's safer to exit on unknown exceptions, than to keep going.
	bot.error("Caught unhandled exception: {} {}".format(str(sys.exc_info()[0]), sys.exc_info()[1]), fatal = True)


