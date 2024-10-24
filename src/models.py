from flask_sqlalchemy import SQLAlchemy 



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email" : self.email
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False , unique = True)
    clima = db.Column(db.String(20), nullable = True)
    creacion_planeta = db.Column(db.String(50), nullable = True)


class People(db.Model): 
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    birth = db.Column(db.String(50), nullable = True)
    gender = db.Column(db.String(20), nullable = True)
    height = db.Column(db.Float, nullable = True)
    skin_color = db.Column(db.String(20),nullable = True)
    hair_color = db.Column(db.String(20), nullable = True)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key = True)
    people_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'), nullable = True)

# class User_Planet(db):
#     __tablename__ = 'usuario_planeta'
#     id = db.Column(Integer, primary_key = True)
#     user_id = db.Column(Integer,ForeignKey('usuario.id'))
#     user_id = db.Column(Integer, ForeignKey('planeta.id'))

#     # RELACIONES PARA LOS ENDPOINTS 
#     usuario = relationship('Usuario')
#     planeta = relationship('Planeta ')



# class Usuario_Personaje(db):
#     __tablename__ = 'usuario_personaje'
#     id = db.Column(Integer, primary_key = True)
#     usuario_id = db.Column(Integer, ForeignKey('usuario.id'))
#     personaje_id = db.Column(Integer, ForeignKey('personaje.id'))

#     # RELACIONES PARA LOS ENDPOINTS   
#     usuario = relationship('Usuario')
#     personaje = relationship('Personaje')