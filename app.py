from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_restful import Resource ,Api

from bson.objectid import ObjectId

from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash


app =Flask(__name__)
api=Api(app)
app.secret_key ='secretkey'
app.config['MONGO_URI'] ="mongodb://localhost:27017/Users"

mongo =PyMongo(app)

class Add(Resource):

    def post(self,name):
        json =request.json
        name =json['name']
        email =json ['email']
        password = json ['pwd']




        if name and email and password and request.method == 'POST':
                hashed =generate_password_hash(password)
            
                x=mongo.db.user.insert_one({'name':name,'email':email,'pwd':hashed})
                print(x)


                return {"message":"user created"}

                resp.status_code =200
        return {'Message':'User is not added in database'},404

    def delete(self,name):
        user = mongo.db.user.delete_many({'name':name})
        resp = dumps(user)
        return {"message":"deleted"}



class Res(Resource):
    def get(self):
        user =mongo.db.user.find()
        resp =dumps(user)
        return {"resp":resp}



api.add_resource(Add,'/add/<string:name>')
api.add_resource(Res,'/res')
if __name__ == '__main__':
    app.run(port=5000,debug=True)

