def command(*command_list):
	def add_attribute(function):
		function.command_list = command_list
		return function

	return add_attribute

