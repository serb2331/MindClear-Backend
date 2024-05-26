import os
import time

import services
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

sqlConnector = None
conversations = None

def runFlask(sqlConnectionInit):
    global sqlConnector
    global conversations
    sqlConnector = sqlConnectionInit
    sqlConnector.connect()
    conversations = {}
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
        userCode = services.createUser(requestData, sqlConnector)
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
        resultData = services.loginHandler(requestData, sqlConnector)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@app.route('/api/signup', methods=['POST'])
def signup_API():
    if request.method == 'POST':
        requestData = request.get_json()
        resultData = services.signupHandler(requestData, sqlConnector)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@app.route('/api/getAddedEmployees', methods=['POST'])
def getAddedEmployees_API():
    if request.method == 'POST':
        requestData = request.get_json()
        resultData = services.getAddedEmployees(requestData, sqlConnector)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@app.route('/api/getEmployeesStressLevel', methods=['POST'])
def getEmployeesStressLevel_API():
    if request.method == 'POST':
        requestData = request.get_json()
        resultData = services.getEmployeesStressLevel(requestData, sqlConnector)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405


@app.route('/api/startConversation', methods=['GET'])
def startConversation_API():
    if request.method == 'GET':
        conversation_id = session.get('conversation_id', None)
        if not conversation_id:
            conversation_id = 'conv_' + str(int(time.time()))
            session['conversation_id'] = conversation_id

        resultData = services.createConversation(sqlConnector, conversations, conversation_id)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405


@app.route('/api/getNextMessage', methods=['POST'])
def getNextMessage_API():
    if request.method == 'POST':
        requestData = request.get_json()

        conversation_id = session.get('conversation_id', None)
        if not conversation_id:
            conversation_id = 'conv_' + str(int(time.time()))
            session['conversation_id'] = conversation_id

        resultData = services.getNextMessage(requestData, sqlConnector, conversations, conversation_id)
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405