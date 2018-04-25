from flask import Flask, render_template, url_for, request
from flask import jsonify
from flask.ext.elastic import Elastic
import json

app = Flask('WebApp', static_folder="static")
es = Elastic(app)

@app.route("/")
def index():
    #response = make_response(render_template("index.html"))
    #response.headers["X-UName"] = "Swalters97"
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "WebApp ready!"

@app.route("/deleteuserindex", methods=["GET"])
def deleteUsers():
    res = es.indices.delete(index="user")
    res = es.indices.create(index="user")
    return "Deleted All Users"

@app.route("/allusers", methods=["GET"])
def allUsers():
    res = es.search(index="user", doc_type="doc", body={"query": { "match_all": {}}})
    return jsonify(res)

@app.route("/getuser/<_uName>", methods=["GET"])
def getUser(_uName):
    res = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName":_uName}}})
    user = res["hits"]["hits"][0]["_source"]
    return jsonify(user)
    
@app.route("/adduser", methods=["POST"])
def addUser():
    print json.loads(request.data)
    uname = json.loads(request.data)["uName"]
    user = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName":
    uname}}})
    if (len(user["hits"]["hits"]) > 0): 
        return "User Exists"
    res = es.index(index="user", doc_type="doc", body=request.data)
    print res
    retId = res["_id"]
    return "User Added"

@app.route("/checkuser", methods=["POST"])
def checkUser():
    uname = json.loads(request.data)["uName"]
    pwd = json.loads(request.data)["pWord"]
    print uname
    print pwd
    user = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName": uname}}})
    retStatus = "failed"
    print user["hits"]["hits"]
    print len(user["hits"]["hits"])
    if (len(user["hits"]["hits"]) > 0):
        user = user["hits"]["hits"][0]["_source"]
        print user["uName"]
        print user["pWord"]
        if (uname == user["uName"] and pwd == user["pWord"]):
            retStatus = "success"
        else:
            retStatus = "failed"
    return retStatus

@app.route("/home/<_uName>", methods=["GET"])
def homePage(_uName):
    return render_template("home.html", uName=_uName)

@app.route("/schedule", methods=["GET"])
def schedulePage():
    return render_template("schedule.html")

app.run(host="0.0.0.0", port=5000, threaded=True)
