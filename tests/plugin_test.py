#!/usr/bin/env python3
# Imports
import sys
# By default the bot is one directory up.
sys.path.append("../")
import plugins
import config

# Config file.
config_file = "../main.conf"

# Failures
fails = 0

# Read the config file.
try:
	print("TESTING: Config.")
	c = config.config()
	c.read_config(config_file)
except:
	print("FAILURE: Loading config.")
	fails = fails + 1

# Load the plugin manager.
try:
	print("TESTING: Plugins")
	p = plugins.plugin_manager(c)
	p.load_plugins()
except:
	print("FAILURE: Loading plugins.")

# Final essesment.
print("Failures: {}".format(fails))
