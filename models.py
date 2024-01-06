"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, DateTime

db = SQLAlchemy(session_options={"expire_on_commit": False})

class Cupcake(db.Model):
    __tablename__ = "cupcakes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float(2), nullable=False)
    image = db.Column(db.String(), nullable=False, default="https://tinyurl.com/demo-cupcake")

    def serialize(self):
        """Serialize a cupcake SQLAlchemy obj to dictionary"""
        return {
            "id":self.id,
            "flavor":self.flavor,
            "size":self.size,
            "rating":self.rating,
            "image":self.image
        }

############## CONNECT DB ##############

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()