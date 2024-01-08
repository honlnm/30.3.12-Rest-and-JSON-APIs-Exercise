import os
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from dotenv import load_dotenv

def create_app(db_name, testing=False):

    ############## CONFIG ##############

    app = Flask(__name__)

    load_dotenv()
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('secret_key')

    ############## ROUTES ##############

    @app.route('/')
    def home():
        cupcakes = Cupcake.query.all()
        return render_template('index.html', cupcakes=cupcakes)
    
    
    @app.route('/api/cupcakes')
    def list_cupcakes():
        cupcakes = Cupcake.query.all()
        serialized = [c.serialize() for c in cupcakes]
        return jsonify(cupcakes=serialized)

    @app.route('/api/cupcakes/<int:id>')
    def single_cupcake_data(id):
        cupcake = Cupcake.query.get_or_404(id)
        return jsonify(cupcake=cupcake.serialize())

    @app.route('/api/cupcakes', methods=["POST"])
    def create_cupcake():
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]

        if request.json["image"] != "":
            image = request.json["image"]
            new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        else:
            new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating)

        db.session.add(new_cupcake)
        db.session.commit()

        return (jsonify(cupcake=new_cupcake.serialize()), 201)

    @app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
    def update_cupcake_data(id):
        cupcake = Cupcake.query.get_or_404(id)
        db.session.query(Cupcake).filter_by(id=id).update(request.json)
        db.session.commit()
        return jsonify(cupcake=cupcake.serialize())

    @app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
    def delete_cupcake_data(id):
        cupcake = Cupcake.query.get_or_404(id)
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message="deleted")

    return app

############## CREATE APP/CONNECT DB ##############

if __name__ == '__main__':
    app = create_app('cupcakes')
    connect_db(app)
    app.run(debug=True)