import commands
import sys
from globals import *
def main():
	global running
	if not commands.getMap():
		print "Map failed to download, server seems to be down."
		return
	userInput = ""
	print "Welcome to MUD, type \"help\" for a list of commands."
	while(running):
		# Split up the user input
		userInput = raw_input("> ").split()
		if userInput != []:
			command = userInput[0] # Get the first word, or the command
			parameters = userInput[1:] # Get the rest of the words
			switchCommands(command, parameters)

# Switches on the command and passes in parameters
# command is a single word
# parameters is an array of parameters
def switchCommands(command, parameters):
	global running
	if command == "quests":
		commands.quests(parameters)
		return
	if command == "help" or command == "?":
		commands.printHelp()
		return
	if command == "exit" or command == "quit" or command == "q":
		running = False
		return
	if command == "login":
		commands.login()
		return
	if command == "move" or command == "go":
		commands.move(parameters)
		return
	if command == "register":
		commands.register()
		return
	if command == "stats":
		commands.stats()
		return
	if command == "inv":
		commands.inventory(parameters)
		return
	if command == "look":
		commands.look(parameters)
		return
	if command == "location" or command == "loc":
		commands.location()
		return
	print "Unknown command, try using \"help\" or \"?\""
if __name__ == '__main__':
	if len(sys.argv) > 1:
		baseURL = sys.argv[1]
	try:
		main()
		print "Thanks for playing, all your data has been saved."
	except KeyboardInterrupt:
		print ""
		print "Goodbye :)"
