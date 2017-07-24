import pydle
import subprocess
import sys
import exceptions
from time import sleep

# Set our name and version.
name = "Python3Bot"
version = "0.1-dev"
cmd = "!"

def error(error, fatal = False):
	""" Prints error to stdout, flusing the output, and exiting if it's a fatal error. """
	if not fatal:
		print("ERROR: {}".format(error), flush = True)
	else:
		print("FATAL ERROR: {}".format(error), flush = True)
		raise SystemExit(1)

def warning(warning):
	""" Prints warning to stdout, flusing the output. """
	print("WARNING: {}".format(warning), flush = True)

def debug(debug):
	""" Prints debug to stdout, flushing the output. """
	print("DEBUG: {}".format(debug), flush = True)

def is_yes(s):
	""" Returns whether the string means True or False """
	s = s.lower()
	
	if s == "true" or s == "yes" or s == "y":
		return True
	else:
		return False

class Bot(pydle.Client):
	""" The main bot class. Handles events, and the raw IRC connection."""

	def quit(self, message=None):
		""" Quits network. """
		# I'm gonna implement something here.
		# But for now just return the super call.
		debug("Quitting. Reason: {}".format(message))
		return super().quit(message)

	def on_connect(self):
		""" Join configured channels on connect """
		
		# Call the superclass.
		super().on_connect()
		# Join channels.
		for channel in self.channel_list:
			self.join(channel)

	def is_admin(self, string, type):
		if type == "nick":
			# Return True if we find the current nick in the admin nicks list.
			for each in self.config.admin_nicks:
				if each == string:
					return True
		elif type == "host":
			# Return True if we find the current hostmaks in the admin hostmasks list.
			for each in self.config.admin_hosts:
				if each == string:
					return True

		# This is reached when no admin privliges we're detected.
		return False


	@pydle.coroutine
	def __handle_internal(self, target, source, message):
		""" Handles commands for internal plugin(s). """
		if message == cmd+"version":
			# Handler for !version.
			self.message(target, "{}: {}, Version: {}. {}".format(source, name, version, target))

		if message == cmd+"quit":
			# Handler for !quit.
			# Check for admin privs.
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				self.quit("Recieved a quit command.")
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message == cmd+"next":
			self.__respond(target, source, "Another satisfied customer. NEXT!")
		
		if message.startswith(cmd+"remove"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=2)
				pmsg = ""
				if len(args) == 2:
					pmsg = "Removed by {}".format(source)
				elif len(args) == 3 and args[2] != "":
					pmsg = "Removed by {} (".format(source) + args[2] + ")"
				else:
					self.message(target, "{}: Invalid command invocation.".format(source))
					return
				
				if args[1] == self.config.nick:
					self.message(target, "{}: I refuse to remove myself.".format(source))
					return
				
				self.rawmsg("REMOVE", target, args[1], pmsg)
				self.message(target, "{}: Removed {}.".format(source, args[1]))
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"ban"): # syntax !ban <hostmask> [<remove> <nick> reason>]
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=4)
				remove = False
				reason = ""
				#self.message(target, "Ban command invoked")
				if len(args) == 2:
					#self.message(target, "Banning without removing")
					self.rawmsg("MODE", target, '+b', args[1])
				elif len(args) > 2:
					#self.message(target, "Banning with 2nd argument")
					remove = is_yes(args[2])
					
					if len(args) == 4:
						reason = "Banned by {}".format(source)
					elif len(args) == 5:
						reason = "Banned by {} ({})".format(source, args[4])
					else:
						self.__respond(target, source, "{}: Invalid command invocation.".format(source))
						return
					#self.message(target, "Remove reason {}".format(reason))
					self.rawmsg("MODE", target, '+b', args[1])
					if remove:
						#self.message(target, "Removing")
						self.rawmsg("REMOVE", target, args[3], reason)
				else:
					self.__respond(target, source, "{}: Invalid command invocation.".format(source))
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"unban"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '-b', args[1])
				else:
					self.__respond(target, source, "{}: Invalid command invocation.".format(source))
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"quiet"): # syntax !quiet <hostmask>
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=2)
				if len(args) == 2:
					self.rawmsg("MODE", target, '+q', args[1])
				else:
					
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"unquiet"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '-q', args[1])
				else:
					self.__respond(target, source, "{}: Invalid command invocation.".format(source))
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))

		if message.startswith(cmd+"op"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '+o', args[1])
				else:
					self.rawmsg("MODE", target, '+o', source)
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"deop"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					if args[1] == self.config.nick:
						self.__respond(target, source, "{}: I refuse to deop myself.".format(source))
						return
					
					self.rawmsg("MODE", target, '-o', args[1])
				else:
					self.rawmsg("MODE", target, '-o', source)
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))

		if message.startswith(cmd+"voice"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '+v', args[1])
				else:
					self.rawmsg("MODE", target, '+v', source)
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"devoice"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '-v', args[1])
				else:
					self.rawmsg("MODE", target, '-v', source)
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"exempt"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '+e', args[1])
				else:
					self.rawmsg("MODE", target, '+e', "*!*@" + host['hostname'])
					return
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message.startswith(cmd+"unexempt"):
			host = yield self.whois(source)
			if self.is_admin(source, "nick") or self.is_admin(host['hostname'], "host"):
				args = message.split(' ', maxsplit=1)
				if len(args) == 2:
					self.rawmsg("MODE", target, '-e', args[1])
				else:
					self.rawmsg("MODE", target, '-e', "*!*@" + host['hostname'])
			else:
				self.__respond(target, source, "{}: You need admin privs to execute that command.".format(source))
		
		if message == cmd+"help":
			# Please leave this here.
			"""helptext = "" \
			"Command list:\n" \
			"  <name>  | <arguments>                       |  <description>\n" \
			"!version  |                                   | Displays the version information of the bot.\n" \
			"!quit     |                                   | Kills the bot (Requires admin privs)\n" \
			"!next     |                                   | NEXT!\n" \
			"!remove   | <nick> [reason]                   | Removes <nick> from channel with optional [reason].\n" \
			"!ban      | <mask> [<remove> <nick> [reason]] | Bans the mask <mask> and can remove <nick> with optional [reason] if <remove> is true.\n" \
			"!unban    | <mask>                            | Unbans the specified <mask>.\n" \
			"!quiet    | <mask>                            | Sets quiet on <mask>.\n" \
			"!unquiet  | <mask>                            | Removes quiet on <mask>.\n" \
			"!op       | [nick]                            | Ops [nick]. If not specified, ops you.\n" \
			"!deop     | [nick]                            | Deops [nick]. If not specified, deops you.\n" \
			"!voice    | [nick]                            | Gives voice to [nick]. If not specified, voices you.\n" \
			"!devoice  | [nick]                            | Takes voice from [nick. If not specified, devoices you.\n" \
			"!exempt   | [hostmask]                        | Sets ban exempt status on [hostmask]. If not specified, uses your hostmask.\n" \
			"!unexempt | [hostmask]                        | Removes ban exempt status from [hostmask]. If not specified, uses your hostmask.\n" \
			"!help     |                                   | Sends this help message\n" \
			"End of help." """
			
			self.message(target, "{}: I have PM'd you the help link.".format(source))
			self.message(source, "Help link: http://ix.io/yDJ")

	def __respond(self, target, source, message):
		""" Responds to a command. """
		if self.is_channel(target):
			self.message(target, message)
		else:
			self.message(source, message)

	def on_message(self, target, source, message):
		""" Debugging function to print messages to stdout """
		# Call the superclass.
		super().on_message(target, source, message)

		# Handle internal command(s).
		self.__handle_internal(target, source, message)

		# Trigger plugins.
		for each in self.plugin.plugin_commands:
			value = each.split(":")
			if message.startswith("!{}".format(value[0])):
				module_obj = self.plugin.plugins[value[2]]
				function_obj = getattr(module_obj, value[1])
				warning("Plugin returned: {}".format(function_obj()))

		# Print message.
		debug("Target: {}, Source: {}, Message: {}".format(target, source, message))

	def on_kick(self, channel, target, by, reason=None):
		""" Called when a person is kicked from the channel """
		# Call the superclass.
		super().on_kick(channel, target, by, reason)

		# Rejoin the channel
		if target == self.config.nick:
			self.join(channel)

	def on_part(self, channel, user, message=None):
		""" Called when a person parts from the channel """
		# Call the superclass.
		super().on_kick(channel, user, message)

		# Rejoin the channel
		if user == self.config.nick:
			self.join(channel)

	def on_raw(self, data):
		""" Debugging function to print all raw data to stdout """
		# Call the superclass.
		super().on_raw(data)

		# Convert data to a string.
		data = str(data)

		# Strip newlines from the data.
		data = data.strip('\n')

		# And output it.
		debug(data)

	def on_unknown(self, message):
		""" Unknown command. """
		warning("Recieved an unknown command: {}".format(message))

	def on_data_error(self, exception):
		""" Handle's socket errors. """
		error("Caught a socket exception. {} {}".format(exception.__name__, str(e)), fatal = True)
