#this is Logic server

from flask import Flask, request, jsonify, render_template
import json
import requests
import yaml

app = Flask(__name__)
list_of_dict = [{
}]

list_of_dict2 = [{
}]

@app.route('/')
def hello_world():
    return 'Hello World!'

# step 2 - to receive JSON query from Front-End
# step 3 send Yaml query from Logic to Query Server
@app.route('/logic/query_data', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        list_of_dict.append(data)
        data_yaml = yaml.dump(data) 		#JSON to YAML
        list_of_dict.append(data_yaml)
        res = requests.post('http://localhost:5003/query/yml_data',data=data_yaml,timeout=1.5)
    return res.status_code

# to check step 2 result
@app.route('/logic/list', methods=['GET'])
def returnAll():
    return render_template("index.html",
                           title='Home',
                           list_of_dict=list_of_dict)

# test step 4 Receiving Interday YAML data from Query server to Logic Server 
#@app.route('/logic/query_data2', methods=['POST'])
#def add():
#    if request.method == 'POST':
#        data2 = request.data
#        list_of_dict2.append(data2)
#    return 200

#@app.route('/logic/list2', methods=['GET'])
#def returnAll():
#    return render_template("index.html",
#                           title='Home',
#                           list_of_dict2=list_of_dict2)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

