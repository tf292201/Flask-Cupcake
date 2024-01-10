from flask import Flask, jsonify, request
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.debug = True

connect_db(app)
# Create the application context
with app.app_context():
  db.create_all()
# Route to list cupcakes
@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
  cupcakes = Cupcake.query.all()
  cupcakes_data = []

  for cupcake in cupcakes:
    cupcakes_data.append({
      'id': cupcake.id,
      'flavor': cupcake.flavor,
      'size': cupcake.size,
      'rating': cupcake.rating
    })

  return jsonify(cupcakes_data)

# Route to get a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)

  return jsonify({
    'id': cupcake.id,
    'flavor': cupcake.flavor,
    'size': cupcake.size,
    'rating': cupcake.rating,
    'image': cupcake.image
  })

# Route to create a cupcake
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
  flavor = request.json['flavor']
  size = request.json['size']
  rating = request.json['rating']
  image = request.json['image']

  new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

  db.session.add(new_cupcake)
  db.session.commit()

  return jsonify({
    'id': new_cupcake.id,
    'flavor': new_cupcake.flavor,
    'size': new_cupcake.size,
    'rating': new_cupcake.rating,
    'image': new_cupcake.image
  })

if __name__ == '__main__':
  app.run()
