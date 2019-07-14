#this is Logic server

from flask import Flask, request, jsonify, render_template
import json
import requests
import yaml

app = Flask(__name__)
list_of_dict = [{
    "fruit": "Apple",
    "size": "Large",
    "color": "Red"
}]



@app.route('/')
def hello_world():
    return 'Hello World!'

# step 2 - to receive JSON query from Front-End
@app.route('/logic/query_data', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        list_of_dict.append(data)
        data_yaml = yaml.dump(data) 		#JSON to YAML
        list_of_dict.append(data_yaml)
        res = requests.post('http://localhost:5003/query/yml_data',data=data_yaml)
    return data.status_code

# to check step 2 result
@app.route('/logic/list', methods=['GET'])
def returnAll():
    return render_template("index.html",
                           title='Home',
                           list_of_dict=list_of_dict)

#step 3 send Yaml query from Logic to Query Server 
#/query/yml_data
#@app.route('/logic/intraday')
#def test():
#    json_file = open("intraday.json")
#    intraday_query_json = json.load(json_file)
#    res = requests.post('http://localhost:5002/logic/query_data',json=intraday_query_json)
#    return res.status_cod

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

