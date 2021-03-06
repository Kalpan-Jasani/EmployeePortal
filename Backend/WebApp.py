from flask import Flask, render_template, url_for, request
from flask import jsonify
from flask.ext.elastic import Elastic
import json

app = Flask('WebApp', template_folder="../Frontend/templates")
es = Elastic(app)

@app.route("/")
def index():
    #response = make_response(render_template("index.html"))
    #response.headers["X-UName"] = "Swalters97"
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "WebApp ready!"

@app.route("/deleteusers", methods=["GET"])
def deleteusers():
    es.indices.delete(index="user")
    es.indices.create(index="user")
    return "Deleted users"

@app.route("/deletetables", methods=["GET"])
def deletetables():
    es.indices.delete(index="table")
    es.indices.create(index="table")
    return "Deleted tables"
    
    

@app.route("/createschedule/<_uName>", methods=["GET"])
def createSchedule(_uName):
    data = {}
    data["esID"] = ""
    for i in range(168): 
        tmp = str(i)
        data[tmp] = []
        
    json_data = json.dumps(data)
    res = es.index(index="table", doc_type="doc", body=json_data);
    _id = res["_id"]
    data["esID"] = _id
    json_data = json.dumps(data)
    print json_data
    res = es.index(index="table", doc_type="doc", id=_id, body=json_data);
    user = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName":_uName}}})
    print user
    userId = user["hits"]["hits"][0]["_id"]
    user = user["hits"]["hits"][0]["_source"]
    print len(user["codes"])
    array = [_id]
    print user["codes"]
    print array
    user["codes"] = user["codes"] + array
    res2 = es.index(index="user", doc_type="doc", id=userId, body=user)
    return _id

@app.route("/updateschedule/<_esId>", methods=["PUT"])
def updateSchedule(_esId):
    print request.data
    res = es.index(index="table", doc_type="doc", id=_esId, body=request.data)
    return jsonify(res)

@app.route("/getschedule/<_id>", methods=["GET"])
def getSchedule(_id):
    res = es.search(index="table", doc_type="doc", body={"query": { "terms": {"_id":
    [_id]}}})
    print res
    table = res["hits"]["hits"][0]["_source"]
    print table
    return jsonify(table)

@app.route("/allusers", methods=["GET"])
def allUsers():
    res = es.search(index="user", doc_type="doc", body={"query": { "match_all": {}}})
    return jsonify(res)

@app.route("/getuser/<_uName>", methods=["GET"])
def getUser(_uName):
    res = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName":_uName}}})
    user = res["hits"]["hits"][0]["_source"]
    return jsonify(user)

@app.route("/updateuser/", methods=["PUT"])
def updateUser():
    _uName = json.loads(request.data)["uName"]
    _id = json.loads(request.data)["esId"]
    user = es.search(index="user", doc_type="doc", body={"query": { "match": {"uName":_uName}}})
    print user
    userId = user["hits"]["hits"][0]["_id"]
    user = user["hits"]["hits"][0]["_source"]
    print len(user["codes"])
    array = [_id]
    print user["codes"]
    print array
    user["codes"] = user["codes"] + array
    res2 = es.index(index="user", doc_type="doc", id=userId, body=user)
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
    num = len(user["hits"]["hits"])
    print retStatus
    print num
    if (num > 0):
        print user
        user = user["hits"]["hits"][0]["_source"]
        print user["uName"]
        print user["pWord"]
        if (uname == user["uName"] and pwd == user["pWord"]):
            retStatus = "success"
        else:
            retStatus = "failed"
    print retStatus
    return retStatus

@app.route("/home/<_uName>", methods=["GET"])
def homePage(_uName):
    return render_template("home.html", uName=_uName)

@app.route("/schedule/<_uName>/<_esId>", methods=["GET"])
def schedulePage(_uName, _esId):
    return render_template("schedule.html", uName=_uName, esId=_esId)

app.run(host="0.0.0.0", port=5000, threaded=True)
