import os
from flask import Flask , request , jsonify , render_template
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


client=MongoClient(os.getenv("MONGO_URI"))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app=Flask(__name__)


db=client["LBM"]
items=db["items"]




from flask import redirect, url_for

@app.route("/", methods=["GET"])
def hello():
    return redirect(url_for("view_items"))




@app.route("/view-items", methods=["GET"])
def view_items():
    print("🔍 Trying to fetch data from MongoDB...")

    try:
        docs = []
        for doc in items.find():
            doc["_id"] = str(doc["_id"])
            print("📄 Document:", doc)
            docs.append(doc)

        print("✅ Total docs fetched:", len(docs))
        return render_template("table.html", items=docs)
    
    except Exception as e:
        print("❌ ERROR:", e)
        return f"<h3 style='color:red;'>Error loading data: {e}</h3>"



@app.route("/items",methods=["POST"])
def create():
    data=request.get_json()

    result=items.insert_one(data)
    return jsonify({"_id":str(result.inserted_id)}),201


@app.route("/items",methods=["GET"])
def getall():
    docs=list()
    for doc in items.find():
        doc["_id"]=str(doc["_id"])
        docs.append(doc)
    return jsonify(docs),200

@app.route("/items/<id>",methods=["GET"])
def getspecific(id):
    doc=items.find_one({"_id":ObjectId(id)})
    doc["_id"]=str(doc["_id"])
    return jsonify(doc),200

@app.route("/items/<id>",methods=["PUT"])
def updatestudent(id):
    data=request.get_json()

    result=items.update_one({"_id":ObjectId(id)},{"$set":data})
    return jsonify({"Book updated successfully":result.modified_count}),200

@app.route("/items/<id>",methods=["DELETE"])
def deletestudent(id):
    result=items.delete_one({"_id":ObjectId(id)})
    return jsonify({"Book deleted successfully":True})




if __name__=="__main__":
    app.run(debug=True)