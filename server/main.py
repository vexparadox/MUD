from flask import Flask, request, jsonify
import hashlib
import sys
import MySQLdb
import uuid
from worldmap import *
from config import *
app = Flask(__name__)
cursor = db.cursor()

# Updates the token with the userID, used on login
# Returns true or false
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
def movePlayer(currentLoc, direction):
	if direction in ['n', 'e', 's', 'w']:
		cols = currentLoc%(worldmap['width']+1) # +1 because 2%2 is 0 but the col is 2
		rows = ((currentLoc-cols)/worldmap['width'])+1
		print "column: ",cols
		print "row: ",rows
		if direction == 'e':
			if cols+1 > worldmap['width']:
				return None
			else:
				return currentLoc+1
		elif direction == 'w':
			if cols-1 < 1:
				return None
			else:
				return currentLoc-1;
		elif direction == 'n':
			if rows-1 < 1:
				return None
			else:
				return currentLoc-worldmap['width']
		elif direction == 's':
			if rows+1 > worldmap['height']:
				return None
			else:
				return currentLoc+worldmap['width']
	else:
		return None
@app.route('/api/user/move/', methods=['POST'])
def move():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			if 'direction' in request.json:
				cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
				newLoc = movePlayer(cursor.fetchone()[4], request.json['direction'])
				if newLoc != None:
					try:
						cursor.execute("UPDATE users SET location = %s WHERE token = %s", (newLoc, request.json['token']))
						db.commit()
						return jsonify({'result': 'true', 'location': newLoc})
					except:
						db.rollback()
						return jsonify({'error': 'Database failed to write.'})
				else:
					return jsonify({'error': "Invalid move."})
			else:
				return jsonify({'error': "Incorrect data format."})
		else:
			return jsonify({'error': "Invalid token."})
	else:
		return jsonify({'error': "Incorrect data format."})
@app.route('/api/user/location/', methods=['POST'])
def location():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'token' in request.json:
		if checkToken(request.json['token']):
			cursor.execute("SELECT * FROM users WHERE token = %s", (request.json['token'],))
			return jsonify({'location': cursor.fetchone()[4]})
		else:
			return jsonify({'error': "Invalid token."})
	else:
		return jsonify({'error': "Incorrect data format."})
@app.route('/api/world/map/', methods=['GET'])
def getMap():
	global worldmap
	return jsonify(worldmap)

@app.route('/api/user/register/', methods=['POST'])
def register():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'username' and 'password' and 'salt' in request.json:
		# add to the database
		try:
			cursor.execute("INSERT INTO users (username, password, salt, location, token) VALUES(%s, %s, %s, '1', '')", (request.json['username'], request.json['password'], request.json['salt']))
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
	print request.json['username']
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
		cursor.execute("SELECT * FROM quests WHERE location = %s", (cursor.fetchone()[4],))
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