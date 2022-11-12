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
from models import db, User, Planets, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#-------------
# User
#-------------
@app.route("/user/list_user", methods=["GET"])
def listar_Usuarios():
    users = User.query.all()
    result = []

    for user in users:
        result.append(user.serialize())

    return jsonify(result)

@app.route("/user", methods=["POST"])
def crear_Usuario():
    
    body = request.get_json()
    if body is None:
        return "Error! Envie la información correcta"

    name = body.get("name")
    last_name = body.get("last_name")
    email = body.get("email")
    password = body.get("password")
    if name is None or last_name is None or email is None or password is None:
        return "La entrada es incorrecta! Revise los campos a ingresar(name,last_name,email,password)"

    user= User(
        name = name,
        last_name = last_name,
        email = email,
        password = password,
        is_active = True
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/user/<id>", methods=["GET"])
def obtener_user(id):
    user = User.query.get(id)
    if user is None:
        return "No existe el usuario con el id: " + str(id)
    return jsonify(user.serialize())

@app.route("/user/<id>/favoritos", methods=["GET"])
def obtener_favoritos(id):
    user = User.query.get(id)
    if user is None:
        return "No existe el usuario con el id: " + str(id)

    favorito_planet = Planets.query.filter_by(user_id=id).all()
    favorito_people = People.query.filter_by(user_id=id).all()
    result = []
    for fav1 in favorito_planet:
        result.append(fav1.serialize())
    for fav2 in favorito_people:
        result.append(fav2.serialize())    

    return jsonify(result)

@app.route("/user/<id1>/favoritos/planet/<id2>", methods=["DELETE"])
def eliminar_planetas_favoritos(id1,id2):
    user = User.query.get(id1)
    if user is None:
        return "No existe el usuario con el id: " + str(id1)
    
    favorito_planet = Planets.query.filter_by(user_id=id1).all()
    result = []
    for fav in favorito_planet:
        result.append(fav.serialize())
    obj = Planets.query.get(id2)
    if obj is None:
        return "No existe el planeta a eliminar con el id: " + str(id2)
    else:
        db.session.delete(obj)
        db.session.commit()
        return "El Planeta favorito con el id "+ str(id2) + " ha sido eliminado!"   

@app.route("/user/<id1>/favoritos/people/<id2>", methods=["DELETE"])
def eliminar_people_favoritos(id1,id2):
    user = User.query.get(id1)
    if user is None:
        return "No existe el usuario con el id: " + str(id1)

    favorito_people = People.query.filter_by(user_id=id1).all()
    result = []
    for fav in favorito_people:
        result.append(fav.serialize())
    obj = People.query.get(id2)
    if obj is None:
        return "No existe el people a eliminar con el id: " + str(id2)
    else:
        db.session.delete(obj)
        db.session.commit()
        return "El People favorito con el id "+ str(id2) + " ha sido eliminado!"     

#-------------
# People
#-------------    

@app.route("/people/list_people", methods=["GET"])
def listar_People():
    peoples = People.query.all()
    result = []

    for people in peoples:
        result.append(people.serialize())

    return jsonify(result)

@app.route("/people", methods=["POST"])
def crear_People():
    body = request.get_json()
    if body is None:
        return "Error! Envie la información correcta"

    name_people = body.get("name_people")
    user_id = body.get("user_id")
    if name_people is None:
        return "La entrada NAME_PEOPLE es incorrecta!"

    people= People(
        name_people = name_people,
        user_id = user_id
        )

    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize())

@app.route("/people/<id>", methods=["PUT"])
def modificar_people(id):
    people = People.query.get(id)
    if people is None:
        return "No existe el Personaje con id: " + str(id)
    
    body = request.get_json()
    people.name_people = body.get('name_people')
    db.session.commit()
    return jsonify(people.serialize())

@app.route("/people/<id>", methods=["DELETE"])
def eliminar_people(id):
    people = People.query.get(id)
    if people is None:
        return "No existe el Personaje con id: " + str(id)

    db.session.delete(people)
    db.session.commit()
    return "El Personaje con el id "+ str(id) + " ha sido eliminado!"    

#-------------
# Planets
#-------------   

@app.route("/planets/list_planets", methods=["GET"])
def listar_Planets():
    planets = Planets.query.all()
    result = []

    for planet in planets:
        result.append(planet.serialize())

    return jsonify(result)

@app.route("/planets", methods=["POST"])
def crear_Planet():
    body = request.get_json()
    if body is None:
        return "Error! Envie la información correcta"

    name_planet = body.get("name_planet")
    user_id = body.get("user_id")
    if name_planet is None:
        return "La entrada NAME_PLANET es incorrecta!"    

    planets = Planets(
        user_id = user_id,
        name_planet = name_planet,
        )  

    if name_planet is None:
        return "La entrada NAME_PLANET es incorrecta!"      

    db.session.add(planets)
    db.session.commit()
    return jsonify(planets.serialize())

@app.route("/planets/<id>", methods=["PUT"])
def modificar_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        return "No existe el planeta con id: " + str(id)
    
    body = request.get_json()
    planet.name_planet = body.get('name_planet')
    db.session.commit()
    return jsonify(planet.serialize())

@app.route("/planets/<id>", methods=["DELETE"])
def eliminar_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        return "No existe el planeta con id: " + str(id)

    db.session.delete(planet)
    db.session.commit()
    return "El planeta con el id "+ str(id) + " ha sido eliminado!"      
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
