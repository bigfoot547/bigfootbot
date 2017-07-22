import plugin
import pydle

commands = {"test": "test"}

@plugin.command("test")
def test():
	#print(command_list, flush = True)
	print("Hello world from test.py!", flush = True)
	return
