from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True, nullable=False)
    last_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__= "planets"
    id = db.Column(db.Integer, primary_key = True)
    name_planet = db.Column(db.String(200), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship(User)

    def serialize(self):
        return {
            "id": self.id,
            "name_planet": self.name_planet,
        }

class People(db.Model):
    __tablename__= "people"
    id = db.Column(db.Integer, primary_key = True)
    name_people = db.Column(db.String(200), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    users = db.relationship(User)

    def serialize(self):
        return {
            "id": self.id,
            "name_people": self.name_people,
        }