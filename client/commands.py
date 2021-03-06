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
					print "You awake and find yourself in {}".format(worldmap[loc['mapindex']]['title'])
				else:
					print "Login succeded."
				return
			else:
				print "Login failed. Probably a wrong password"
				loggedIn = False
def move(parameters):
	global loggedIn
	global worldmap
	if not loggedIn:
		print "Please use the >login command first."
		return
	if len(parameters) < 1:
		print "You need to specify a direction."
		return
	if parameters[0] in ['n', 'e', 's', 'w']:
		r = requests.post(baseURL+"/api/user/move/", json={'token': userToken, 'direction': parameters[0]})
		if 'result' not in r.json():
			print r.json()['error']
		else:
			if r.json()['result'] == "true":
				loc = r.json()['location']
				print "You travel {}".format(parameters[0])
				print " === New Location === "
				print worldmap[loc['mapindex']]['title']
				print worldmap[loc['mapindex']]['description']
				print "--------------------"
			else:
				print "You can't go this way."
				print r.json()['error']
				if "item" in r.json()['error']:
					print "You need a tool of the type: {}".format(worldmap[r.json()['location']['mapindex']]['requireditems'][0])
	else:
		print "Direction needs to be <n/e/s/w>."
def inventory(parameters):
	global loggedIn
	global items
	if not loggedIn:
		print "Please use the >login command first."
		return
	r = requests.post(baseURL+"/api/user/inventory/", json={'token': userToken})
	if 'items' not in r.json():
		print "Error: {}".format(r.json()['error'])
	else:
		if len(r.json()['items']) < 1:
			print "You don't seem to have anything on you."
			return
		# Create an array the same as the items
		myitems = [0] * len(items)
		# For each item found, add to the count
		for i in r.json()['items']:
			myitems[i['id']] += i['count']
		# Loop through the myitems
		print " ==== Inventory ==== "
		for i in range(len(myitems)):
			# if there's one, just print it
			if myitems[i] == 1:
				print items[i]['name']
				print items[i]['description']
				print "Damage: {}".format(items[i]['damage'])
				print "Type: {}".format(items[i]['type'])
				print "-----------------"
			elif myitems[i] > 1:
				# if there's multiple print the plural version
				print "{} {}".format(myitems[i], items[i]['plural'])
				print items[i]['description']
				print "Damage: {}".format(items[i]['damage'])
				print "-----------------"
def printHelp():
	print " ==== Help ==== "
	print " Welcome to Muddy Pyddle "
	print " <>   denotes optional values"
	print " []   denotes mandatory values"
	print " === Commands === "
	print "quit/exit/q - exit the program"
	print "help/? - this helpful information"
	print "login - login to your account"
	print "register - register a new account"
	print " === Requires Login === "
	print "inv/i - look at your inventory"
	print "stats - look at your stats"
	print "quests - list the quests available where you are"
	print "location/loc - where is your character"
	print "look/l <n/e/s/w> - take a look around"
	print "move/go [n/e/s/w] - move in a direction"
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
# Get the users stats
def stats():
	global loggedIn
	if not loggedIn:
		print "Please use the >login command first."
		return
	else:
		r = requests.post(baseURL+"/api/user/stats/", json={'token': userToken})
		if 'error' in r.json():
			print "Error: {}".format(r.json()['error'])
		else:
			print " ==== Stats ==== "
			print "Strength  -  {}".format(r.json()['strength'])
			print "Fortitude -  {}".format(r.json()['fortitude'])
			print "Charisma  -  {}".format(r.json()['charisma'])
			print "Wisdom    -  {}".format(r.json()['wisdom'])
			print "Dexterity -  {}".format(r.json()['dexterity'])
			print "-----------------"
# Get the location of the user from the server
def location():
	global userToken
	global loggedIn
	global worldmap
	if not loggedIn:
		print "Please use the >login command first."
		return
	else:
		loc = getLocation()
		if loc != None:
			# // FIX
			print " === Current Location === "
			print worldmap[loc['mapindex']]['title']
			print worldmap[loc['mapindex']]['description']
			print "--------------------"
		else:
			print "Couldn't locate your character."
# Get the location, returns an object with ['x'] and ['y'] fields
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
		print worldmap[loc['mapindex']]['here']
		return
	# If the parameters are correct
	if parameters[0] in ['n', 'e', 's', 'w']:
		print worldmap[loc['mapindex']][parameters[0]]
		return
	else:
		print "Direction must be <n/e/s/w>."
# Download the map and a list of items
def getStartData():
	global worldmap
	global worldheight
	global worldwidth
	global items
	try:
		r = requests.get(baseURL+"/api/world/map/")
		if 'worldmap' not in r.json():
			return False
		else:
			worldmap = r.json()['worldmap']
			worldheight = r.json()['height']
			worldwidth = r.json()['width']
		r = requests.get(baseURL+"/api/world/items/")
		if 'items' not in r.json():
			return False
		else:
			items = r.json()['items']
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
	if len(username) < 4 or len(password) < 6:
		print "Username must be greater than 4 characters and password must be greater than 6 characters."
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
