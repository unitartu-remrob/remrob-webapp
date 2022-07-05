from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import bcrypt


app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/remrob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #first_name = db.Column(db.String(100))
    #last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    role = db.Column(db.String(100))

class Bookings(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.String(100), nullable=True)
    inventory_id = db.Column('inventory_id', db.Integer)
    start_time = db.Column('start_time', db.String(100))
    end_time = db.Column('end_time', db.String(100))

class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key = True)
    server_container_id = db.Column('server_container_id', db.Integer)
    robot_id = db.Column('robot_id', db.Integer)


@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route("/api/v1/register", methods=["POST"])
def register():
    data = request.json

    email = data["email"]
    password = data["password"]
    #first_name = data["first_name"]
    #last_name = data["last_name"]

    user = User(email=email, password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), active=True, role="ROLE_ADMIN")
    db.session.add(user)
    db.session.commit()
    return "User created", 200


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400
    user = User.query.filter_by(email=email).first()

    if not user:
        return "User not found", 400

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")) and user.active == True:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user_id=user.id, role=user.role), 200

@app.route('/api/v1/bookings', methods=["GET", "POST"])
@jwt_required()
def bookings():
    if request.method == "POST":
        data = request.json
        booking = Bookings(start_time=data["start"], end_time=data["end"], inventory_id=data["inventoryId"])
        db.session.add(booking)
        db.session.commit()
        return "Booking slot created", 200
    elif request.method == "GET":
        bookings = Bookings.query.filter_by(user_id=None).all()
        results = [
            {
                "title": "Robot + Server",
                "start": booking.start_time,
                "end": booking.end_time,
                "id": booking.id
            } for booking in bookings
        ]
        return jsonify({"bookings": results}), 200

@app.route('/api/v1/bookings/<user_id>', methods=["GET"])
@jwt_required()
def user_bookings(user_id):
    bookings = Bookings.query.filter_by(user_id=user_id).all()
    results = [
        {
            "title": "Robot + Server",
            "start": booking.start_time,
            "end": booking.end_time,
            "id": booking.id,
            "color": "green"
        } for booking in bookings
    ]
    return jsonify({"user_bookings": results}), 200

@app.route("/api/v1/bookings/book/<id>", methods=["POST", "DELETE"])
@jwt_required()
def book_slot(id):
    if request.method == "POST":
        data = request.json
        slot = Bookings.query.get(id)
        slot.user_id = data["userId"]
        db.session.commit()
        return "Slot booked", 200
    elif request.method == "DELETE":
        slot = Bookings.query.get(id)
        slot.user_id = None
        db.session.commit()
        return "Booking deleted", 200

@app.route("/api/v1/inventory", methods=["POST", "GET"])
@jwt_required()
def inventory():
    if request.method =="POST":
        data = request.json
        inventory = Inventory(server_container_id = data["server_container_id"], robot_id = data["robot_id"])
        db.session.add(inventory)
        db.session.commit()
        return "Inventory created successfully", 200
    elif request.method == "GET":
        inventory = Inventory.query.all()
        results = [
            {
                "title": "Robot " + inv.robot_id + "+" "Server " + inv.server_container_id,
                "robot_id": inv.robot_id,
                "server_container_id": inv.server_container_id,
            } for inv in inventory
        ]
        return jsonify(results), 200
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")