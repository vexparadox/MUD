import requests
import base64
import os.path
userID = ""
loggedIn = False
def main():
	running = True
	userInput = ""
	while(running):
		# Split up the user input
		userInput = raw_input("> ").split()
		command = userInput[0] # Get the first word, or the command
		# If there's more than one word, take the parameter
		parameter = None
		if len(userInput) > 1:
			parameter = userInput[1] 
		switchCommands(command, parameter)


def switchCommands(command, parameter):
	if command == "quests":
		quests(parameter)
		return
	if command == "help":
		printHelp()
		return
	if command == "userid":
		if userID:
			print "UserID: {}".format(userID)
		else:
			print "No userID given, use the >login method"
		return
	if command == "exit" or command == "quit" or command == "q":
		running = False
		return
	if command == "login":
		login(parameter)
		return
	print "Unknown command, try using \"help\" or \"?\""

def printHelp():
	print "quit/exit/q - exit the program"
	print "login [userID] - verify your userID and store it for use later"
	print " === Requires Login === "
	print "quests - list the quests available on the server"
	print "userid - print your current userID"

# Get the quests, checks for login
def quests(parameter):
	global userID
	global loggedIn
	if not loggedIn or not userID:
		print "Please use the >login command first."
		return
	if not parameter:
		getQuests()
def getQuests():
	r = requests.post("http://localhost:5000/api/quests/", json= {'userID' : userID})
	if not r.json()['quests']:
		print "Error: {}".format(r.json()['error'])
	else:
		print " === Quests Available === "
		for quest in r.json()['quests']:
			print "Title > {}".format(quest['title']) 
			print "Description > {}".format(quest['description'])
			print "QuestID > {}".format(quest['questID'])
			print "--------------------"

# "Logs in" actually just checks the validity of the userID and stores it
def login(parameter):
	global userID
	global loggedIn
	while not loggedIn:
		if not parameter:
			userID = raw_input("Enter your userID > ")
		else:
			userID = parameter
		if userID:
			d = {'userID' : userID}
			r = requests.post("http://localhost:5000/api/logincheck/", json=d)
			if not r.json()['result']:
				print "Error: {}".format(r.json()['error'])
			else:
				if r.json()['result'] == "true":
					loggedIn = True
					saveLogin()
				else:
					print "Login failed. Try again with a valid userID."
					parameter = None
					loggedIn = False
	print "Login successfull."
def saveLogin():
	global userID
	userInput = raw_input("Do you want to save your userID? [y/n] > ")
	if userInput != "n" and userInput != "y":
		saveLogin()
	elif userInput == "y":
		# if the user wants to save their login
		file = open("userID.txt", "w")
		file.write(userID)
		file.close()
		print "userID saved"
try:
	main()
except KeyboardInterrupt:
	print ""
	print "Goodbye :)"
