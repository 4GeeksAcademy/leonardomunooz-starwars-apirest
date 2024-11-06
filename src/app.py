"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
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


# POPULATION DATABASE SWAPI 
# https://www.swapi.tech/api/people?page=1&limit=5

@app.route("/people/population", methods = ["GET"])
def get_population():

    # resources = ['planets', 'people']
    # Del lado del backend, se piden los datos con la libreria requests
    response  = requests.get("https://www.swapi.tech/api/people?page=1&limit=10")
    # Se pasan los datos en un formato manipulable (se traducen el json para poder entender)
    response = response.json()
    # obtenemos  lo que necesitamos.
    response = response.get('results')
    

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get("result")

        print(result)
        # se crea el objeto que queremos agregar
        people = People()

        # Lo que esta en el resultado del detalla del personaje se le asigna a los registros de la bd
        people.height = result.get("properties").get("height")
        people.homeworld = result.get("properties").get("homeworld")
        people.url = result.get("properties").get("url")
        people.name = result.get("properties").get('name')
        people.birth = result.get("properties").get("birth_year")
        people.gender = result.get("properties").get("gender")
        people.skin_color = result.get("properties").get("skin_color")
        people.hair_color = result.get("properties").get("hair_color")
        people.eye_color = result.get("properties").get("eye_color")
        
        try: 
            db.session.add(people)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify("error"),500

    # print(response)
    return jsonify(["Data loaded"]), 200



@app.route("/planets/population", methods = ['GET'])
def get_planet_population():

    response = requests.get("https://www.swapi.tech/api/planets?page=1&limit=5")
    response = response.json()
    print(response)
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get('result')
        planet = Planet()
        planet.name = result.get('properties').get('name')
        planet.clima = result.get("properties").get('climate')

        try: 
            db.session.add(planet)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify("error"),500


    return jsonify(['data loaded']),200

@app.route("/people", methods =['GET'])
def get_people():
    # creamos un objeto people
    people = People()
    # dentro de este objeto, buscamos en la base de datos sus registros
    people = people.query.all()
    # le aplicamos el formato serialize
    people = list(map(lambda item : item.serialize(),people))
    # devuelve resultado en formato json 
    return jsonify(people), 200


@app.route("/planets", methods = ["GET"])
def get_planet():

    planet = Planet()
    planet = planet.query.all()
    planet = list(map(lambda planet : planet.serialize(),planet))
    return jsonify(planet),200




@app.route("/people/<int:theid>", methods = ["GET"])
def get_by_people_id(theid):
    if theid is not None :
        people  = People()
        people= people.query.get(theid)
        
        if people is None: 
            return jsonify(["Ohhh, people doenst exists"]), 404
        else :
            return jsonify(people.serialize()), 200

@app.route("/planet/<int:theid>",methods = ["GET"])
def get_by_planet_id(theid):

    if theid is not None:
        planet = Planet()
        planet = planet.query.get(theid)

        if planet is None: 
            return jsonify(["Ohh planet doesnt exists"]),404
        else:
            return jsonify(planet.serialize()),200

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
    # valida si hay un id en la url
    if theid is not None:
        user  = User()
        user = user.query.get(theid)
        # print(user)
        
       # cuando la base de data no consigue algo responde un null (None) (utilizando querys)
        if user is not None : 
            return jsonify(user.serialize()) , 200
        else : 
            return jsonify({
                "Message" : "User is not found!"
            }),404
    


@app.route("/users/favorites/<int:user_id>", methods = ["GET"])
def get_all_user_favorites(user_id = None):

    user = User()
    user = user.query.filter_by(id = user_id).first()
    print(user.serialize())

    return jsonify(user.serialize()),200

# agrega los planetas favoritos del usuario
@app.route("/favorite/planet/<int:planet_id>", methods = ["POST"])
def add_planet_favorite(planet_id):
    user_id = 1
    favorite = Favorite()
    fav_planet = favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()

    if fav_planet is not  None:
        return jsonify({"msg":"Este favorito ya existe"}) , 400
    
    favorite.user_id = user_id
    favorite.planet_id = planet_id

    db.session.add(favorite)
    try:
        db.session.commit()
        return jsonify("Se ha guardado el planeta en favoritos exitosamente"),201
    except Exception as error: 
        db.session.rollback()
        return jsonify("Algo ha ocurrido"),404   
    
@app.route("/favorite/planet/<int:planet_id>", methods = ["DELETE"])
def del_planet_favorite(planet_id):

    user_id = 1
    favorite = Favorite()
    # Filter_by( columnana = valor )
    favorite = favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()

    # print(favorite)
    if favorite is  None:
        return jsonify({"msg": "No existe el planeta"}), 404
    
    db.session.delete(favorite)
    try:
        db.session.commit()
        return jsonify("Se ha eliminado el planeta"), 200
    except Exception as error :
        db.session.rollback()
        return jsonify("Algo ha ocurrido"),404
    


 # ELIMINA UN FAVORITO DE PEOPLE 
@app.route("/favorite/people/<int:people_id>", methods = ['DELETE'])
def del_people_favorite(people_id):

    user_id = 2 
    favorite = Favorite()
    favorite = favorite.query.filter_by(user_id =  user_id, people_id = people_id).first()

    print(favorite)

    if favorite is None:
        return jsonify("No existe este people"), 404

    db.session.delete(favorite)
    try:
        db.session.commit()
        return jsonify("Se ha eliminado el people"), 200        
    except Exception as error :
        db.session.rollback()
        return jsonify("Algo ha ocurrido"),404
        


# Agrega los peoples favoritos del usuario
@app.route("/favorite/people/<int:people_id>", methods = ["POST"])
def add_people_favorite(people_id):

    user_id = 2
    favorite = Favorite()
    favorite.user_id = user_id
    favorite.people_id = people_id

    # guarda los datos en la tabla
    db.session.add(favorite)
    try:
        # commit compromete los datos para ser guardado
        db.session.commit()
        return jsonify("Se ha guardado people en favoritos exitosamente"),201
    except Exception as error :
        db.session.rollback()
        return jsonify("Algo ha ocurrido"),404
    


# ESTANDAR A SEGUIR PARA RESPPUESTAS CON POST

@app.route('/user', methods=['POST'])
def add_user():
    data  = request.json # recibe lo que el cliente (postman) envia
    if data.get("name") is None:   # valida si recibimos las propiedades concretas del cliente (postman)
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
