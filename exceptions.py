class InternalVariableOverride(Exception):
	""" An exception raised when something tries to override a internal variable with set_extra() """

	def  __init__(self, message = None, name = None, value = None):
		""" Sets what was trying to be set with set_extra() """
		self.name = name
		self.value = value
		# ew hack!
		self.args = [message]
