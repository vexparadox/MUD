from flask import Flask, request, jsonify
import hashlib
import MySQLdb
import uuid
app = Flask(__name__)
db = MySQLdb.connect("localhost","root","","flask")
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
@app.route("/")
def root():
    return "No api in root."

@app.route('/api/users/register/', methods=['POST'])
def register():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if 'username' and 'password' and 'salt' in request.json:
		# add to the database
		try:
			cursor.execute("INSERT INTO users (username, password, salt, location, token) VALUES(%s, %s, %s, '0', '')", (request.json['username'], request.json['password'], request.json['salt']))
			db.commit()
			return jsonify({'result': 'true'})
		except:
			db.rollback()
			return jsonify({'error': "Database failed to write."})
	else:
		return jsonify({'error': "Incorrect data format."})


@app.route('/api/users/salt/', methods=['POST'])
def getSalt():
	if not request.json:
		return jsonify({'error': "No data detected."})
	print request.json['username']
	cursor.execute("SELECT * FROM users WHERE username = %s", (request.json['username'],))
	if not cursor.rowcount:
		return jsonify({'error': "Username not found."})
	return jsonify({'salt': cursor.fetchone()[3]})


@app.route('/api/users/login/', methods=['POST'])
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
		cursor.execute("SELECT * FROM quests")
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

@app.route('/api/quests/<int:quest_id>', methods=['GET'])
def get_task(quest_id):
    quest = [quest for quest in quests if quests['id'] == quest_id]
    if len(quest) == 0:
        abort(404)
    return jsonify({'quest': quests[0]})

if __name__ == "__main__":
    app.run()
    db.close()
    cursor.close()