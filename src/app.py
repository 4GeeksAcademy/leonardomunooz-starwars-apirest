"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods = ['GET'])
def get_users():
    users = User()
    # aqui va a la base de datos a buscar todos los usuarios
    users =  users.query.all()
    # aplica el metodo serializar para responder al cliente
    users = list(map(lambda item : item.serialize(), users))
    # el metodo jsonfiy convierte los datos en formato json
    return jsonify(users),200


@app.route('/user/<int:theid>', methods = ["GET"])
def get_by_user_id(theid=None):
    # valida si hay un id
    if theid is not None:
        user  = User()
        user = user.query.get(theid)
        print(user)
        
       # cuando la base de data no consigue algo responde un null (None) (utilizando querys)
        if user is not None : 
            return jsonify(user.serialize()) , 200
        else : 
            return jsonify({
                "Message" : "User is not found!"
            }), 200  
    
# ESTANDAR A SEGUIR PARA RESPPUESTAS CON POST

@app.route('/user', methods=['POST'])
def add_user():
    data  = request.json # recibe lo que el cliente (postman) envia
    if data.get("name") is None:   # valida si recibimos las propiedades concretas del postman
        return jsonify({"message": "user doenst exits"}), 400
    if data.get("email") is None: 
        return jsonify({"message": "user doenst exits"}), 400
    # validacion de si el usuario existe
    user = User()
    user_email = user.query.filter_by(email = data['email']).first()
    if user_email is None:
        # Creamos a el usuario
        user = User(name= data['name'], email = data["email"])
        # se prepara para guardar en base de datos
        db.session.add(user)
        try:
            # Lo guarda
            db.session.commit()
            return jsonify({"Message": "usuario guardado correctamente"}), 201
        except Exception as error:
            # echa para atras el proceso de guardar usuario (transaccion cancelada) si algun error ocurre
            db.session.rollback()
            return jsonify({"Message":"algo ha ocurrido "}), 404             
    else : 
        return jsonify({"Message": "El usuario existe"}), 400




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    # return jsonify(response_body), 200