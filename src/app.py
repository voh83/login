from flask import Flask, request
from flask_pymongo import PyMongo
import json

app=Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://sliwmsmaster:YIb40Rl0axhmKDug@cluster0-u8jcj.mongodb.net/sliwms_db?retryWrites=true&w=majority"
mongo=PyMongo(app)

@app.route('/', methods=['GET'])
def jelo_worl():
    #print(request)

    return {"message":"Hello World!"}, 200

@app.route('/register', methods=['POST'])
def register_users():

    js_rqt=request.json

    email=js_rqt['email']
    psw=js_rqt['password']

    if empty_required_fields(email, psw):
        return ("",204)
    
    if mongo.db.users.find_one({'email':email}) is not None:
        return {'message':'Usuario ya existe'}, 409

    _id=mongo.db.users.insert_one({
        "email":email,
        "password":psw
    })

    return {'message':f'Usuario {email} Creado'}, 201

@app.route('/login', methods=['POST'])
def login():

    js_rqt=request.json
    email=js_rqt['email']
    psw=js_rqt['password']

    if empty_required_fields(email, psw):
        return ("",204)

    res=mongo.db.users.find_one({
        "email":email
    })
    #comprueba si el usuario existe
    if res is None:
        return {"message":"Usuario o Password Incorrecto"}, 404

    if res["password"] != psw:
        return({"message":"Usuario/Constraseña Incorrectos"},404)
        
    return({"message":"Usuario Loggeado exitosamente"},200)

def empty_required_fields(email:str,psw:str):
    if not email or not psw:
        return True
        

if __name__=="__main__":
    app.run(debug=True)


