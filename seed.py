from app import create_app
from models import db, connect_db, Cupcake

app = create_app("cupcakes", testing=False)
connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

with app.app_context():
    db.session.add_all([c1, c2])
    db.session.commit()