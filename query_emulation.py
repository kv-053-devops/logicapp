#this is a Query server
# it is Emulation of Intraday response

from flask import Flask, request, jsonify, render_template
import json
import requests
import yaml

app = Flask(__name__)
list_of_dict = [{
}]



@app.route('/')
def hello_world():
    return 'Hello World!'

# TEST to obtain YAML request from Logic server step 3
# Send YAML reqest with intraday data to logic server  using data from https://intraday.worldtradingdata.com/api/v1/intraday?symbol=AAPL&range=1&interval=1&api_token=demo
# local life "intraday_data.yml"
@app.route('/query/yml_data', methods=['POST'])
def add():
    if request.method == 'POST':
        data1 = request.data
        list_of_dict.append(data1)
    return data1.status_code

@app.route('/query/list', methods=['GET'])
def returnAll():
    return render_template("index.html",
                           title='Home',
                           list_of_dict=list_of_dict)

@app.route('/query/test')
def test():
    yaml_file = open("intraday_data.yml")
    intraday_data_yaml = yaml.load(yaml_file)
    res = requests.post('http://localhost:5002/logic/query_data2',data=intraday_data_yaml)
    return res.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

