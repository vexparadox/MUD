import requests
import base64
import os.path
import uuid
import hashlib
userToken = ""
loggedIn = False
running = True
def main():
	global running
	userInput = ""
	while(running):
		# Split up the user input
		userInput = raw_input("> ").split()
		if userInput != []:
			command = userInput[0] # Get the first word, or the command
			# If there's more than one word, take the parameter
			parameter = None
			if len(userInput) > 1:
				parameter = userInput[1] 
			switchCommands(command, parameter)


def switchCommands(command, parameter):
	global running
	if command == "quests":
		quests(parameter)
		return
	if command == "help":
		printHelp()
		return
	if command == "exit" or command == "quit" or command == "q":
		running = False
		return
	if command == "login":
		login()
		return
	if command == "register":
		register()
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
	global userToken
	global loggedIn
	if not loggedIn or not userToken:
		print "Please use the >login command first."
		return
	if not parameter:
		getQuests()
	# take quests
def getQuests():
	r = requests.post("http://localhost:5000/api/quests/", json= {'token' : userToken})
	if 'quests' not in r.json():
		print "Error: {}".format(r.json()['error'])
	else:
		print " === Quests Available === "
		for quest in r.json()['quests']:
			print "Title > {}".format(quest['title']) 
			print "Description > {}".format(quest['description'])
			print "QuestID > {}".format(quest['questID'])
			print "--------------------"

# "Logs in" actually just checks the validity of the userID and stores it
def login():
	global userToken
	global loggedIn
	username = raw_input("Enter your username > ")
	password = raw_input("Enter your password > ")
	if username and password:
		salt = getSalt(username)
		if not salt:
			print "Failed to retieve salt."
			return
		password = hashlib.sha256(password+salt).hexdigest()
		r = requests.post("http://localhost:5000/api/users/login/", json={'username': username, 'password': password})
		if not r.json()['result']:
			print "Error: {}".format(r.json()['error'])
		else:
			if r.json()['result'] == "true": 
				userToken = r.json()['token']
				loggedIn = True
				print "Login successfull."
				return
			else:
				print "Login failed. Probably a wrong password"
				loggedIn = False

def getSalt(username):
	r = requests.post("http://localhost:5000/api/users/salt/", json={'username': username})
	if not r.json()['salt']:
		print "Error: {}".format(r.json()['error'])
		return None
	else:
		return r.json()['salt']

def register():
	username = raw_input("Enter a username > ")
	password = raw_input("Enter a password > ")
	password2 = raw_input("Enter the password again > ")
	if password != password2:
		print "Passwords don't match, try again."
		return
	salt = uuid.uuid4().hex
	password = hashlib.sha256(password+salt).hexdigest()
	r = requests.post("http://localhost:5000/api/users/register/", json={'username' : username, 'password': password, 'salt': salt})
	if not r.json()['result']:
		print "Error: {}".format(r.json()['error'])
	else:
		if r.json()['result'] == "true":
			print "Account registered! You can now >login"
try:
	main()
except KeyboardInterrupt:
	print ""
	print "Goodbye :)"
