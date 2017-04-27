from flask import Flask, request, jsonify
import hashlib
import sys
import MySQLdb
import uuid
from worldmap import *
from items import *
from config import *
app = Flask(__name__)
cursor = db.cursor()

# Updates the token with the userID, used on login
# Returns true or false
def getMapIndex(x, y):
	global worldmap
	return y*worldmap['width']+x
def updateToken(userID, token):
	try:
		cursor.execute("UPDATE users SET token = %s WHERE userID = %s", (token, userID))
		db.commit()
		return True
	except:
		db.rollback()
		return False
# returns true or false
def checkToken(token):
	cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
	if not cursor.rowcount:
		return False
	else:
		return True
# Checks if the map location is marked as passable
def isMapPassable(location):
	global worldmap
	# Check the 1D map using x,y
	loc1D = getMapIndex(location['x'], location['y'])
	print loc1D
	if worldmap['worldmap'][loc1D]['passable'] == "true":
		return True
	else:
		return False
# Checks if the given inventory has the requirements for the location
def requiredMapItems(inventory, location):
	global worldmap
	global items
	loc1D = getMapIndex(location['x'], location['y'])
	required = worldmap['worldmap'][loc1D]['requireditems']
	# If there's no required items
	if len(required) < 1:
		return True
	else:
		invitems = []
		# Build an array of ids in the inventory
		for i in inventory:
			invitems.append(i['id'])
		# Loop over the required array
		for r in required:
			# Loop through the items
			for i in invitems:
				# If they match remove them from the list
				if r == items['items'][i]['type']:
					required.remove(r)
		# if the list is empty, return true
		# All the required items are met
		if len(required) == 0:
			return True
		else:
			return False
# Returns an inventory of a userID
# This is an array of a dictionary containing itemID's and quanities
def getInventory(userID):
	items = []
	cursor.execute("SELECT * FROM items WHERE userID = %s", (userID,))
	results = cursor.fetchall()
	for r in results:
		i = {
			'id' : r[1],
			'count': r[3]
		}
		items.append(i)
	return items
def movePlayer(currentLoc, direction):
	if direction in ['n', 'e', 's', 'w']:
		cols = currentLoc['x']
		rows = currentLoc['y']
		if direction == 'e':
			if cols+1 >= worldmap['width']:
				return None
			else:
				currentLoc['x'] += 1
				return currentLoc
		elif direction == 'w':
			if cols <= 0:
				return None
			else:
				currentLoc['x'] -= 1
				return currentLoc;
		elif direction == 'n':
			if rows <= 0:
				return None
			else:
				currentLoc['y'] -= 1
				return currentLoc
		elif direction == 's':
			if rows+1 >= worldmap['height']:
				return None
			else:
				currentLoc['y'] += 1
				return currentLoc
	else:
		return None
@app.route('/api/user/inventory/', methods=['POST'])
def inventory():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
			items = getInventory(cursor.fetchone()[0])
			return jsonify({'result': 'true', 'items': items})
		else:
			return jsonify({'error': "Invalid token."})
	else:
		return jsonify({'error': "Invalid data format."})

@app.route('/api/user/stats/', methods=['POST'])
def getStats():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
			result = cursor.fetchone()
			return jsonify({'strength': result[6], 'fortitude': result[7], 'charisma': result[8], 'wisdom': result[9], 'dexterity': result[10]})
		else:
			return jsonify({'error': "Invalid token."})
	else:
		return jsonify({'error': "Invalid data format."})
@app.route('/api/user/move/', methods=['POST'])
def move():
	global worldmap
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			if 'direction' in request.json:
				# Get the user ID
				cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
				result = cursor.fetchone()
				userID = result[0] # userID is the 1st
				oldLocation = {}
				oldLocation['x'] = result[4] # Location X is the 4th 
				oldLocation['y'] = result[5] # Location Y is the 5th 
				newLoc = movePlayer(oldLocation, request.json['direction'])
				# newLoc is a ['x'] and ['y'] object
				inventory = getInventory(userID)
				# movePlayer will return None if the move isn't allowed (aka outside of the map)
				if newLoc != None:
					# Get the 1d map index
					mapindex = getMapIndex(newLoc['x'], newLoc['y'])
					# make sure it's passable
					if not isMapPassable(newLoc):
						return jsonify({'error': "You can't pass through here.", 'result': 'false', 'location': {'x' : newLoc['x'], 'y': newLoc['y'], 'mapindex': mapindex}})
					# Check for required items
					if not requiredMapItems(inventory, newLoc):
						return jsonify({'error': "An item is required to go here.", 'result': 'false', 'location': {'x' : newLoc['x'], 'y': newLoc['y'], 'mapindex': mapindex}})
					# If all seems good, update the users location
					try:
						cursor.execute("UPDATE users SET locx = %s, locy = %s WHERE token = %s", (newLoc['x'], newLoc['y'], request.json['token']))
						db.commit()
						return jsonify({'result': 'true', 'location': {'x' : newLoc['x'], 'y': newLoc['y'], 'mapindex': mapindex} })
					except:
						db.rollback()
						return jsonify({'error': 'Database failed to write.'})
				else:
					return jsonify({'error': "You can't leave this earth... yet"})
			else:
				return jsonify({'error': "Incorrect data format, a direction is required."})
		else:
			return jsonify({'error': "Invalid token given, try logging in again to refresh."})
	else:
		return jsonify({'error': "Incorrect data format, a token is required."})
@app.route('/api/user/location/', methods=['POST'])
def location():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
			result = cursor.fetchone()
			mapindex = getMapIndex(result[4], result[5])
			return jsonify({'location': {'x' : result[4], 'y': result[5], 'mapindex': mapindex} })
		else:
			return jsonify({'error': "Invalid token."})
	else:
		return jsonify({'error': "Incorrect data format."})
@app.route('/api/world/map/', methods=['GET'])
def getMap():
	global worldmap
	return jsonify(worldmap)

@app.route('/api/world/items/', methods=['GET'])
def getItems():
	global items
	return jsonify(items)

@app.route('/api/user/register/', methods=['POST'])
def register():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'username' and 'password' and 'salt' in request.json:
		# add to the database
		try:
			cursor.execute("INSERT INTO users (username, password, salt, token, strength, fortitude, charisma, wisdom, dexterity) VALUES(%s, %s, %s, '', '1', '1', '1', '1', '1')", (request.json['username'], request.json['password'], request.json['salt']))
			cursor.execute("INSERT INTO items (itemID, userID) VALUES ('0', LAST_INSERT_ID())")
			db.commit()
			return jsonify({'result': 'true'})
		except:
			db.rollback()
			return jsonify({'error': "Database failed to write."})
	else:
		return jsonify({'error': "Incorrect data format."})


@app.route('/api/user/salt/', methods=['POST'])
def getSalt():
	if not request.json:
		return jsonify({'error': "No data detected."})
	cursor.execute("SELECT * FROM users WHERE username = %s", (request.json['username'],))
	if not cursor.rowcount:
		return jsonify({'error': "Username not found."})
	return jsonify({'salt': cursor.fetchone()[3]})



@app.route('/api/user/login/', methods=['POST'])
def loginCheck():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'username' and 'password' in request.json:
		# check the login
		cursor.execute("SELECT * FROM users WHERE `username` = %s AND `password` = %s", (request.json['username'], request.json['password']))
		# if there's no rows found
		if not cursor.rowcount:
			return jsonify({'result': 'false'})
		# Generate a new token
		token = uuid.uuid4().hex
		if updateToken(cursor.fetchone()[0], token):
			return jsonify({'result': 'true', 'token': token})
		else:
			return jsonify({'error': 'Token failed to generate.'})
	else:
		return jsonify({'error': 'Incorrect data format.'})

@app.route('/api/quests/', methods=['POST'])
def quests():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if checkToken(request.json['token']):
		quests = []
		cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
		result = cursor.fetchone()
		cursor.execute("SELECT * FROM quests WHERE locx = %s AND locy = %s", (result[4], result[5]))
		results = cursor.fetchall()
		for r in results:
			q = {
				'questID' : r[0],
				'title' : r[1],
				'description' : r[2]
			}
			quests.append(q)
		return jsonify({'quests': quests})
	else:
		return jsonify({'error': "Invalid token."})

if __name__ == "__main__":
	if len(sys.argv) > 1:
		IPAddress = sys.argv[1]
	app.run(host=IPAddress)
	db.close()
	cursor.close()