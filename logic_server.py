from flask import Flask, request, jsonify, render_template
import requests
import json
import yaml
import sys
#import argparse

app = Flask(__name__)

req_timeout = 60
print(len(sys.argv))
if len(sys.argv) != 1 :
    app_run_address = sys.argv[1]
    app_run_port = sys.argv[2]
    app_query_url = sys.argv[3]
else:
    app_run_address = '127.0.0.1'
    app_run_port = '5002'
    app_query_url = 'http://127.0.0.1:5003/query/yml_data'

list_of_datas = []
realtime_response_filter = ['symbol', 'price', 'price_open','day_high', 'day_low',  'market_cap', 'volume']

## construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser(usage='%(prog)s -i xxx-openstack-vps-id-1-yyy,xxx-openstack-vps-id-2-yyy\nor use without arguments:\n%(prog)s ',
#                                description='This script counts bandwidth usage for VPS in OpenStack cloud. VPS will be suspended if it exhausted month limit. Read comments inside script for more information.',
#                                epilog="Check file 'vps-statistics' in the directory with this script for stored results. Script needs credentials to OpenStack API, be shure that file with name 'clouds.yaml' is exist in folder with script.")
#ap.add_argument("-i", "--ignore", type=str, required=False, help="List of vps IDs which will NOT be suspended regardless of bandwidth limit. Use ',' to separate IDs")
#ap.add_argument("-I", "--ignore-projects", type=str, required=False, help="List of OpenStack projects. VPS inside projects will not be suspended regardless of bandwidth limit. Use ',' to separate IDs")
#ap.add_argument("-l", "--limit", type=int, default=10240, help="Set monthly bandwidth limit for VPS in GBytes. Default is %(default)s GB" )
#args = vars(ap.parse_args())


def logic_realtime(dict_data):
    """ Take data-results from Query API and parse needed values for 'realtime' query type.
    Function accepts only dictionary obejcts. """
    filtered_data = { "data" : [] , "querytype": "realtime" }
    for item in dict_data.get("data"):
         item_dict = {}
         for filtes in realtime_response_filter:
             item_dict[filtes] = item[filtes]
         filtered_data["data"].append(item_dict)
    return filtered_data


def logic_intraday(dict1):
    # need to be finished
    pass

def query_realtime(dict_from_json):
    """ Send request with type "realtime" to "query" API and convert reply to dictionary.
    Function accepts only dictionary obejcts. """
    income_data_yaml = yaml.dump(dict_from_json)
    try: 
        request_to_query = requests.post(app_query_url, data=income_data_yaml, timeout=req_timeout)
    except:
        print(request_to_query)
        return 'error'
    dict_from_query = yaml.safe_load(request_to_query.text)
    return dict_from_query


def query_intraday(dict_from_json):
    """ Send request with type "intraday" to "query" API and convert reply to dictionary.
    Function accepts only dictionary obejcts. """
    data_yaml = yaml.dump(dict_from_json)
    res = requests.post(app_query_url, data=data_yaml, timeout=req_timeout)
    dict_from_query = yaml.safe_load(res.text)
    return dict_from_query

@app.route("/")
def hello():
    return "The root uri '/' doesn't configured. Use '/logic/query_data' instead."

@app.route('/logic/query_data', methods=['POST'])
def post_json_data():
    """ Main endpoint of logic server API """
    income_data = request.get_data()
    income_data_dict = json.loads(income_data.decode('utf-8'))
    if income_data_dict["query_type"] == "realtime":
	# process 'realtime' request to query API
        query_req =  query_realtime(income_data_dict)
        if query_req == 'error':
            err_mesage = "ERROR: Problems in connection to Query API: '" + app_query_url + "'."
            print(err_mesage)
            return(err_mesage)
        result_dict = logic_realtime(query_req)
    elif income_data_dict["query_type"] == "intraday":
	# process 'intraday' request to query API
        result_dict =  query_intraday(income_data_dict)
    else:
        print("Unknown query type: " + income_data_dict["query_type"])
        return "Unknown query type"

    result_json = json.dumps(result_dict)
    return result_json


if __name__ == "__main__":
    app.run(host=app_run_address, port=app_run_port)

