import requests
import base64
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
	if command == "help":
		printHelp()
	if command == "userid":
		if userID:
			print "UserID: {}".format(userID)
		else:
			print "No userID given, use the >login method"
	if command == "exit" or command == "quit" or command == "q":
		running = False
	if command == "login":
		login()

def printHelp():
	print "quit/exit/q - exit the program"
	print "login - verify your userID and store it for use later"
	print " === Requires Login === "
	print "quests - list the quests available on the server"

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
			print "--------------------"

# "Logs in" actually just checks the validity of the userID and stores it
def login():
	global userID
	global loggedIn
	while not loggedIn:
		userID = raw_input("Enter your userID > ")
		if userID:
			d = {'userID' : userID}
			r = requests.post("http://localhost:5000/api/logincheck/", json=d)
			if not r.json()['result']:
				print "Error: {}".format(r.json()['error'])
			else:
				if r.json()['result'] == "true":
					loggedIn = True
				else:
					print "Login failed. Try again with a valid userID."
					loggedIn = False
	print "Login successfull."
try:
	main()
except KeyboardInterrupt:
	print ""
	print "Goodbye :)"
