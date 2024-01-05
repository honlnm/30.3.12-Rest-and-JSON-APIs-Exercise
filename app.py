import os
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('secret_key')

############## CONNECT DB ##############

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

############## ROUTES ##############

@app.route('/api/cupcakes', methods=["GET", "POST"])
def list_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def single_cupcake_data(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())
