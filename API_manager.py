import os

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
