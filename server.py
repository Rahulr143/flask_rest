from flask import Flask,Response,request
from flask_restful import Resource, Api
import pymongo
import json
from bson.objectid import ObjectId


app = Flask(__name__)
api = Api(app)

try:
    mongo = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo["Login"]
    mycol = mydb["customers"]
except :
    print("Database not connected")

class User(Resource):


    def post(self,id):
        try:
            mydict = {"name": request.form['name'], "address":request.form['address']}
            x = mydb.mycol.insert_one(mydict)
            print(str(x.inserted_id))

            return  Response(
                response= json.dumps({"message":"User created","id":f"{x.inserted_id}"}),
                status=200,
                mimetype='application/json'

            )


        except Exception as ex:

                print(ex)
    def put(self,id):
        try:

         dbres =mydb.mycol.update_one(
                    {"_id":ObjectId(id)},
                    { "$set": { "name": request.form['name']}}
                     )
         for attr in dir(dbres):
             print(attr)

         if dbres.modified_count ==1:

             return  Response(
                response=json.dumps({"message":"User updated"}),
                 status=200,
                 mimetype='application/json'
             )
         else:
             return Response(
                 response=json.dumps({"message": "Nothing to updated"}),
                 status=200,
                 mimetype='application/json'
             )

        except Exception as ex:
            pass
    def delete(self,id):
        try:
            dres=mydb.mycol.delete_one({"_id":ObjectId(id)})
            return Response(
            response=json.dumps({"message": "User Delete"}),
            status=200,
            mimetype='application/json'
            )
        except Exception as ex:
            pass

class GetUser(Resource):
    def get(self):
        try:
            data = list(mydb.mycol.find())
            print(str(data))
            for user in data:
                user["_id"] = str(user["_id"])
            if data:
                return Response(
                    response=json.dumps(data),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message":"User is Empty"}),
                    status=200,
                    mimetype='application/json'
                )

        except Exception as ex:
            pass


api.add_resource(GetUser,'/user')
api.add_resource(User,'/user/<id>')

if __name__ == '__main__':
    app.run(debug=True)
