from flask import Flask
from flask import render_template
from flask import request
import requests
import json
import yaml

# from Front to Logic /logic/query_data
# from Logic to Query /query/yml_data
# from Query to Logic /logic/yml_data

app = Flask(__name__)

list_of_datas = []

#api_url = "https://api.worldtradingdata.com/api/v1/stock?symbol=AAPL,MSFT,GM,AMSE&api_token=KFzAzKDWU88IAG2uQHp3i3kBa9RCkd3JAWJulicwGNHssxEwq0wElClEUACM"

def get_data_from_remote_api(api_url):
    res = requests.get(api_url)
    # decoded_response = res.decode("UTF-8")
    data = res.json()
    yml_data = yaml.dump(data)
   # print(yml_data)
    return yml_data
    #print(res.status_code)


@app.route("/")
def hello():
    return "Hello world!"

@app.route('/logic/query_data', methods=['POST'])
def post_json_data():
    income_data = request.get_data()
    print("TYPE of data: " + str(type(income_data)))
    print(request.is_json)
    print(income_data)
    json_string = json.loads(income_data)
    print(str(type(json_string)))
    yaml_string = yaml.dump(json_string)
    #print(json_string)
    #list_of_datas.append(json_string)
    #string_of_datas = ';'.join(str(i) for i in list_of_datas)
#    print(yaml_string)
#    return render_template( 'genlist.html', name='api', list=string_of_datas)
    #post_req = requests.post('http://127.0.0.1:5005/query/yml_data', data=yaml_string) 
    query_resp = get_data_from_remote_api(api_url) 
    #print(test)
    query_resp_yaml = yaml.safe_load(query_resp)
    query_resp_json = json.dumps(query_resp_yaml)
    return query_resp_json
    #return query_resp_json

def json_to_dict(thin):
    pass

def yaml_to_dict(thin):
    pass

def dict_to_yaml(thin):
    pass

def dict_to_json(thin):
    pass

def logic_realtime(dict1):
    pass

def logic_intraday(dict1):
    pass

def query_realtime(dict_from_json):
    pass

if __name__ == "__name__":
    app.run(host='0.0.0.0', port=5002)

