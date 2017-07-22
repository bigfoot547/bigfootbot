import os
import path

class puretext_db():
	def __init__(self, database_dir):
		self.database_dir = database_dir

	def add(self, section, name, value):
		# Where are we going to store the database file.
		path_obj = path.path()
		path_obj.fromstr(self.database_dir)
		path_obj.add(section)
		path_obj.add(name)
		# The database file itself.
		entry = path.path()
		entry.fromstr(path_obj.tostr())
		entry.add("data")

		# Make the directoies.
		os.makedirs(path_obj.tostr(), exist_ok = True)

		# And write the value.
		with open(entry.tostr(), 'w') as file:
			file.write(value)

	def get(self, section, name, value):
		# Where are we going to store the database file.
		path_obj = path.path()
		path_obj.fromstr(self.database_dir)
		path_obj.add(section)
		path_obj.add(name)
		# The database file itself.
		entry = path.path()
		entry.fromstr(path_obj.tostr())
		entry.add("data")

		# Return the data.
		with open(entry.tostr(), 'r') as file:
			return file.read()

