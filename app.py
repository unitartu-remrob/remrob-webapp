from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/remrob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    return ""

@app.route('/api/v1/bookings', methods=["GET", "POST"])
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

@app.route("/api/v1/bookings/book/<id>", methods=["POST"])
def book_slot(id):
    data = request.json
    slot = Bookings.query.get(id)
    slot.user_id = data["userId"]
    db.session.commit()
    return "Slot booked", 200
    
if __name__ == '__main__':
    app.run()