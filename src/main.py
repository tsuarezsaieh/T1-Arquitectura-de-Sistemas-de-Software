# Flask Libs
from flask import Flask
from flask import request, Response, send_from_directory, render_template, request, redirect
from flask_cors import CORS, cross_origin
# System libs
import json
# Other libs
from .db import DB

app = Flask(__name__)
CORS(app)

# FIX GET ip address
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

@app.route("/", methods = ["GET", "POST", "PUT"])
def ruta():
    # Para evitar problemas con Chrome
    if request.method == "GET":
        page = request.args.get('p') or 1
        page = int(page)
        db = DB()
        result = { 'messages' : db.get_queries(page), "next_url" : "{}?p={}".format(request.base_url, page+1), "previous_url": '/#'}
        if page > 1:
            result["previous_url"] = "{}?p={}".format(request.base_url, page-1)
        status = 200

        return render_template('messages.html', data=result)

    elif request.method == "POST":
        print(request.form['message'])
        try:
            db = DB()
            result = db.new_message(request)
            status = 201
        except Exception as e:
            status = 400
            result = {'message': 'No message found, send a json with "message" key', 'error': str(e)}
    
    if request.headers['content-type'] and request.headers['content-type'] == 'application/json':
        resp = Response(json.dumps(result), status=status, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return redirect('/')

