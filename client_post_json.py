import requests
import sys
import json

# get file name
try:
    input_file = sys.argv[1]
except IndexError:
    print("Provide a file with json as a firts script argument and second arg as remote server address:")
    print("Example: ")
    print( str(sys.argv[0]) + " file-json.txt" + " http://localhost:5000/api")
    exit(2)

# get server address
try:
    dest_server = sys.argv[2]
except IndexError:
    print("Provide server address with file name")
    print("Example: ")
    print( str(sys.argv[0]) + " file-json.txt" + " http://localhost:5000/api")
    exit(2)

# read file
with open(input_file) as file:
    # create json data dict
    data_loaded = json.load(file)

# sent data to remote server
try:
    post_req = requests.post(dest_server, json=data_loaded)
    print( "HTTP code: " + str(post_req.status_code))
    print("Was sent:")
    print(data_loaded)
    print("Response")
    print(str(type(post_req.json())))
   # print(post_req.json())
    result_json = json.dumps(post_req.json())
    print(result_json)
except:
    print("Some error happened")
    exit(2)
