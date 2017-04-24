from flask import Flask, request, jsonify
import MySQLdb
import uuid
app = Flask(__name__)
db = MySQLdb.connect("localhost","root","","flask")
cursor = db.cursor()
def checkLogin(userID):
	q = "SELECT * FROM users WHERE userID = '{}'".format(userID);
	cursor.execute(q)
	if not cursor.rowcount:
		return False
	else:
		return True


@app.route("/")
def root():
    return "No api in root."

@app.route('/api/register/<string:username>', methods=['GET'])
def register(username):
	userID = uuid.uuid4().hex
	query = """INSERT INTO users (userID, invID, username, XP) VALUES ('{}', 0, '{}', 0)""".format(userID, username)
	try:
		cursor.execute(query)
		db.commit()
		d = {"userID": userID}
		return jsonify(d)
	except:
		db.rollback()
		return jsonify({"error": "Database failed to write."})

@app.route('/api/logincheck/', methods=['POST'])
def loginCheck():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if checkLogin(request.json['userID']):
		return jsonify({'result': 'true'})
	else:
		return jsonify({'result': 'false'})

@app.route('/api/quests/', methods=['POST'])
def quests():
	if not request.json:
		return jsonify({'error': "No data detected."})
	if checkLogin(request.json['userID']):
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
		return jsonify({'error': "Invalid userID."})

@app.route('/api/quests/<int:quest_id>', methods=['GET'])
def get_task(quest_id):
    quest = [quest for quest in quests if quests['id'] == quest_id]
    if len(quest) == 0:
        abort(404)
    return jsonify({'quest': quests[0]})

if __name__ == "__main__":
    app.run()
    db.close()