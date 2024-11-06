from flask_sqlalchemy import SQLAlchemy 



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    favorite = db.relationship('Favorite', backref = 'user', uselist = True)
    


    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email" : self.email,
            "favorites": list(map(lambda item : item.serialize(), self.favorite))
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False , unique = True)
    clima = db.Column(db.String(20), nullable = True)
    creacion_planeta = db.Column(db.String(50), nullable = True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clima": self.clima,
            "creacion_planeta" : self.creacion_planeta
        }


class People(db.Model): 
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key = True)
    height = db.Column(db.Float, nullable = False)
    homeworld = db.Column(db.String(255), nullable = False)
    url = db.Column(db.String(255), nullable = False )
    name = db.Column(db.String(20), nullable = False)
    birth = db.Column(db.String(50), nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    skin_color = db.Column(db.String(20),nullable = False)
    hair_color = db.Column(db.String(20), nullable = False) 
    eye_color = db.Column(db.String(20), nullable = False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender" : self.gender,
            "birth" : self.birth
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'), nullable = True)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'), nullable = True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id" :self.people_id,
            "planet_id" : self.planet_id
        }