import os
import services
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

sqlConnection = None

def runFlask(sqlConnectionInit):
    global sqlConnection
    sqlConnection = sqlConnectionInit
    sqlConnection.connect()
    app.run(host='0.0.0.0', debug=True)

@app.route('/api/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        data = {"test": "test2"}
        return jsonify(data)
    elif request.method == 'POST':
        requestData = request.get_json()
        resultData = {"receivedData": requestData}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405


@app.route('/api/createUserCode', methods=['POST'])
def createUserCode_API():
    if request.method == 'POST':
        requestData = request.get_json()
        userCode = services.createUser(requestData, sqlConnection)
        print(userCode)
        # TODO send email
        resultData = {"status": 1}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@app.route('/api/login', methods=['POST'])
def login_API():
    if request.method == 'POST':
        requestData = request.get_json()
        resultData = services.loginHandler(requestData, sqlConnection)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@app.route('/api/signup', methods=['POST'])
def signup_API():
    if request.method == 'POST':
        requestData = request.get_json()
        resultData = services.signupHandler(requestData, sqlConnection)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405