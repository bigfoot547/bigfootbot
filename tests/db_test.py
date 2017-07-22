#!/usr/bin/env python3
# Imports
import os
import sys
# By default the bot is one directory up.
sys.path.append("../")
import db

# Test the DB.
try:
	print("TESTING: Writing to the database.")
	g = db.puretext_db(os.getcwd())
	g.add("karma", "lennart", "-1000")
	print("TESTING: Reading from the database.")
	print("Result: {}".format(g.get("karma", "lennart", "-1000")))
except:
	print("FAILURE: Database.")
