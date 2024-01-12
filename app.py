from flask import Flask, jsonify, request, render_template
from models import Cupcake, db, connect_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.debug = True

connect_db(app)

@app.route('/')
def root():
  return render_template('index.html')

# Route to list cupcakes
@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
  cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

  return jsonify(cupcakes=cupcakes)


# Route to get a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)

  return jsonify(cupcake=cupcake.serialize())

# Route to create a cupcake
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
  data = request.json
  
  new_cupcake = Cupcake(flavor=data['flavor'], size=data['size'], rating=data['rating'], image=data['image'])

  db.session.add(new_cupcake)
  db.session.commit()

  return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  data = request.json

  cupcake.flavor = data['flavor']
  cupcake.size = data['size']
  cupcake.rating = data['rating']
  cupcake.image = data['image']
  
  db.session.add(cupcake)
  db.session.commit()

  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  db.session.delete(cupcake)
  db.session.commit()

  return jsonify(message='Deleted'), 200

if __name__ == '__main__':
  app.run()
