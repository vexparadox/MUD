import requests
import uuid
import getpass
import hashlib
import base64
from globals import *
# Logs in using a username and password
# The password is appended with a salt retrieved from the server and hashed
def login():
	global userToken
	global loggedIn
	global baseURL
	username = raw_input("Enter your username > ")
	password = getpass.getpass("Enter your password > ")
	if username and password:
		salt = getSalt(username)
		if not salt:
			print "Failed to retieve salt."
			return
		password = hashlib.sha256(password+salt).hexdigest()
		r = requests.post(baseURL+"/api/user/login/", json={'username': username, 'password': password})
		if 'result' not in r.json():
			print "Error: {}".format(r.json()['error'])
		else:
			if r.json()['result'] == "true": 
				userToken = r.json()['token']
				loggedIn = True
				loc = getLocation()
				if loc != None:
					print "You awake and find yourself in {}".format(worldmap[loc]['title'])
				else:
					print "Login succeded."
				return
			else:
				print "Login failed. Probably a wrong password"
				loggedIn = False

def printHelp():
	print " ==== Help ==== "
	print "quit/exit/q - exit the program"
	print "help/? - this helpful information"
	print "login - login to your account"
	print "register - register a new account"
	print " === Requires Login === "
	print "quests - list the quests available on the server"
	print "location/loc - where is your character in the world"
	print "look <n/e/s/w>- take a look around"
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
# Retireves and prints the quests from the server
def getQuests():
	global baseURL
	r = requests.post(baseURL+"/api/quests/", json= {'token' : userToken})
	if 'quests' not in r.json():
		print "Error: {}".format(r.json()['error'])
	else:
		print " === Quests Available === "
		for quest in r.json()['quests']:
			print "Title > {}".format(quest['title']) 
			print "Description > {}".format(quest['description'])
			print "QuestID > {}".format(quest['questID'])
			print "--------------------"

# Get the location of the user from the server
def location():
	global userToken
	global loggedIn
	global worldmap
	if loggedIn:
		loc = getLocation()
		if loc != None:
			print " === Current Location === "
			print worldmap[loc]['title']
			print worldmap[loc]['description']
			print "--------------------"
		else:
			print "Couldn't locate your character."
	else:
		print "Please use >login first."
def getLocation():
	global userToken
	try:
		r = requests.post(baseURL+"/api/user/location/", json={'token': userToken})
		if 'location' not in r.json():
			print "Error: {}".format(r.json()['error'])
			return None
		else:
			return r.json()['location']
	except requests.ConnectionError:
		print "Couldn't connect to the server."
		return None

def look(parameters):
	global loggedIn
	# If they're not logged in
	if not loggedIn:
		print "Please use the >login command first."
		return
	# get the location of the character
	loc = getLocation()
	# check the location
	if loc == None:
		print "Location couldn't be retrieved."
		return
	# If there's no parameters given
	if len(parameters) < 1:
		print worldmap[loc]['here']
		return
	# If the parameters are correct
	if parameters[0] in ['n', 'e', 's', 'w']:
		print worldmap[loc][parameters[0]]
		return
	else:
		print "Direction must be <n/e/s/w>."
def getMap():
	global worldmap
	try:
		r = requests.get(baseURL+"/api/world/map/")
		if 'worldmap' not in r.json():
			return False
		else:
			worldmap = r.json()['worldmap']
			return True
	except requests.ConnectionError:
		print "Couldn't connect to the server."
		return False

# Retrieves and returns the salt of a given username
def getSalt(username):
	try:
		r = requests.post(baseURL+"/api/user/salt/", json={'username': username})
		if 'salt' not in r.json():
			print "Error: {}".format(r.json()['error'])
			return None
		else:
			return r.json()['salt']
	except requests.ConnectionError:
		print "Couldn't connect to the server."
		return None
# Registers a new user, will generate a salt and send a hashed password+salt to the server
# Does not login.
def register():
	username = raw_input("Enter a username > ")
	password = getpass.getpass("Enter a password > ")
	password2 = getpass.getpass("Enter the password again > ")
	if password != password2:
		print "Passwords don't match, try again."
		return
	if len(username) < 6 or len(password) < 6:
		print "Username and password must be greater than 6 characters."
		return
	salt = uuid.uuid4().hex
	password = hashlib.sha256(password+salt).hexdigest()
	try:
		r = requests.post(baseURL+"/api/user/register/", json={'username' : username, 'password': password, 'salt': salt})
		if 'result' not in r.json():
			print "Error: {}".format(r.json()['error'])
		else:
			if r.json()['result'] == "true":
				print "Account registered! You can now >login"
	except requests.ConnectionError:
		print "Couldn't connect to the server."