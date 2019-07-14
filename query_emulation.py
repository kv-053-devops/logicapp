from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)
list_of_dict = [{
    "fruit": "Apple",
    "size": "Large",
    "color": "Red"
}]


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/add', methods=['POST'])
def add():

    try:
        if request.method == 'POST':
            # data =request.json()
            data = request.get_json()
            print(request)
        list_of_dict.append(data)
        print(list_of_dict)
    except:
        print("This didn't work.")
    return ""


@app.route('/api/list', methods=['GET'])
def returnAll():
    return render_template("index.html",
                           title='Home',
                           list_of_dict=list_of_dict)


# @app.route('/')
# @app.route('/index')
# def returnAll1():
#     # return jsonify(list_of_dict)
#     # user = { 'nickname': 'Miguel' } 
#     return render_template("index.html",
#         title = 'Home',
#         list_of_dict = list_of_dict)
#     # return '''
#     # <html>
#     #   <head>
#     #     <title>Home Page</title>
#     #   </head>
#     #   <body>
#     #     <h1>Hello, ''' + list_of_dict + '''</h1>
#     #   </body>
#     # </html>
#     # '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

