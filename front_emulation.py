#this is Fron-End Emolation server
# It send request in JSON (json.example) intraday query to Logic server 

from flask import Flask, request, jsonify, render_template
import json
import requests


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


#  STEP 1 here we send JSON data from Logic to Front
@app.route('/front/intraday')
def test():
    json_file = open("intraday.json")
    intraday_query_json = json.load(json_file)
    res = requests.post('http://localhost:5002/logic/query_data',json=intraday_query_json)
    return res.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

print("Just to check")
