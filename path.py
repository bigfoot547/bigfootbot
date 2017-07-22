import os

class path():
	""" Library to astract paths. """

	def __init__(self):
		""" Initilizes the class. """
		self.rawpath = list()
		# And what we use to seperate the path.
		self.pathsep = os.path.sep
		# What the path starts with.
		self.pathstart = os.path.abspath(os.sep)

	def delete(self, section):
		""" Deletes a section from the path. """
		index = self.rawpath.index(section)
		self.rawpath.pop(index)

	def add(self, section, before = None):
		""" Adds a section into the path. """
		if before == None:
			# Add it to the end.
			self.rawpath.append(section)
		else:
			# Add it before before.
			index = self.rawpath.index(before)
			self.rawpath.insert(index, section)

	def get(self, section):
		""" Gets a section from the path. """
		index = self.rawpath.index(section)
		return self.rawpath[index]

	def tostr(self):
		""" Converts a path object to a filesystem string. """
		return_string = self.pathstart

		# Put together the string.
		for section in self.rawpath:
			return_string = return_string + section + os.path.sep

		# Strip the leading path seperator.
		return_string = return_string.rstrip(os.path.sep)

		# Return it.
		return return_string

	def fromstr(self, string):
		""" Converts a filesystem string to a path object. """
		split_string = string.split(os.path.sep)

		# Add each chunk.
		for each in split_string:
			if each == "":
				continue
			self.add(each)
