from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt, verify_jwt_in_request
import bcrypt
from functools import wraps
from datetime import timezone, datetime

app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/remrob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 100000

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

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
    simulation = db.Column(db.Boolean)
    project = db.Column('project', db.String(100))
    start_time = db.Column('start_time', db.String(100))
    end_time = db.Column('end_time', db.String(100))

class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key = True)
    robot_id = db.Column('robot_id', db.Integer)
    slug = db.Column('slug', db.String(100))
    project = db.Column('project', db.String(100))
    status = db.Column(db.Boolean)

    expires = db.Column('end_time', db.String(100))
    user_id = db.Column('user', db.Integer)
    vnc_uri = db.Column('vnc_uri', db.String(255))
    issue = db.Column('issue', db.Boolean)

class Simtainers(db.Model):
    __tablename__ = "simulation_containers"
    id = db.Column(db.Integer, primary_key = True)
    container_id = db.Column('container_id', db.Integer)
    slug = db.Column('slug', db.String(100))

    expires = db.Column('end_time', db.String(100))
    user_id = db.Column('user', db.Integer)
    vnc_uri = db.Column('vnc_uri', db.String(255))


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

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
        if user.role == "ROLE_ADMIN":
            access_token = create_access_token(identity=user.id, additional_claims={"is_administrator": True})
        else:
            access_token = create_access_token(identity=user.id, additional_claims={"is_administrator": False})
        return jsonify(access_token=access_token, user_id=user.id, role=user.role), 200
    else:
        return "User not active or wrong credentials", 400

@app.route("/api/v1/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")

@app.route('/api/v1/bookings', methods=["GET", "POST"])
@jwt_required()
def bookings():
    if request.method == "POST":
        data = request.json
        booking = Bookings(
            start_time=data["start"],
            end_time=data["end"],
            simulation=data["is_simulation"],
            project=data["project"]
        )
        db.session.add(booking)
        db.session.commit()
        return "Booking slot created", 200
    elif request.method == "GET":
        results = []
        bookings = Bookings.query.filter_by(user_id=None).all()
        for booking in bookings: 
            #inv = Inventory.query.get(booking.inventory_id)
            slot_object = {
                "title": booking.project.title(),
                "start": booking.start_time,
                "end": booking.end_time,
                "id": booking.id
            }
            results.append(slot_object)
        return jsonify({"bookings": results}), 200

@app.route('/api/v1/bookings/<user_id>', methods=["GET"])
@jwt_required()
def user_bookings(user_id):
    current_user = get_jwt_identity()
    _filter = request.args.get('booking')
    if current_user == int(user_id):
        results = []
        if _filter:
            bookings = Bookings.query.filter_by(user_id=user_id, id=_filter).all()
            if len(bookings) == 0:
                return "No such booking", 400
        else:
            bookings = Bookings.query.filter_by(user_id=user_id).all()
        
        for booking in bookings: 
            #inv = Inventory.query.get(booking.inventory_id)
            slot_object = {
                "title": booking.project.title(),
                "start": booking.start_time,
                "end": booking.end_time,
                "id": booking.id,
                "is_simulation": booking.simulation,
                "project": booking.project,
                "color": "green"
            }
            results.append(slot_object)
        return jsonify({"user_bookings": results}), 200
    else:
        return "Wrong user", 403

@app.route("/api/v1/bookings/book/<id>", methods=["POST"])
@jwt_required()
def book_slot(id):
    data = request.json
    current_user = get_jwt_identity()
    if int(data["userId"]) == current_user:
        slot = Bookings.query.get(id)
        slot.user_id = data["userId"]
        db.session.commit()
        return "Slot booked", 200
    else:
        return "Wrong user", 400

@app.route("/api/v1/bookings/unbook/<user_id>/<slot_id>", methods=["DELETE"])
@jwt_required()
def unbook(user_id, slot_id):
    current_user = get_jwt_identity()
    if int(user_id) == current_user:
        slot = Bookings.query.get(slot_id)
        # Check if a container assignment might also need to be unset
        inv = Simtainers if slot.simulation else Inventory
        claimed_container = inv.query.filter_by(user_id=slot.user_id).first()

        if claimed_container:
            claimed_container.user_id = None
            claimed_container.expires = None
        slot.user_id = None
        db.session.commit()

        return "Booking deleted", 200
    else:
        return "Wrong user", 400

@app.route("/api/v1/simtainers", methods=["POST", "GET"])
@admin_required()
def new_simtainer():
    # Just an endpoint, so you don't have to manually fill the table
    # Currently a single server can handle max 9 containers, will have to adjust this table with a multi-server setup
    if request.method == "POST":
        Simtainers.query.delete()
        for i in range(9):
            cont = Simtainers(
                container_id = i+1,
                slug = f"robosim-{i+1}",
            )
            db.session.add(cont)
        db.session.commit()
        return "Simtainer table filled", 201

    elif request.method == "GET":
        sims = Simtainers.query.all()
        results = [
            {   
                "id": sim.id,
                "container_id": sim.container_id,
                "slug": sim.slug,
                "title": f"ROBOSIM-{sim.container_id}",
                "vnc_uri": sim.vnc_uri
            } for sim in sims
        ]
        sorted_inv = sorted(results, key=lambda x : x['container_id'])
        return jsonify(sorted_inv), 200

@app.route("/api/v1/inventory", methods=["GET"])
@jwt_required()
def inventory():
    inventory = Inventory.query.all()
    results = [
        {   
            "id": inv.id,
            "robot_id": inv.robot_id,
            "slug": inv.slug,
            "title": f"Robotont-{inv.robot_id}",
            "status": inv.status,
            "project": inv.project,
            "vnc_uri": inv.vnc_uri
        } for inv in inventory
    ]
    sorted_inv = sorted(results, key=lambda x : x['robot_id'])
    return jsonify(sorted_inv), 200

@app.route("/api/v1/inventory", methods=["POST"])
@admin_required()
def new_inventory():
    data = request.json
    if "robot_id" in data:
        id = data["robot_id"]
        if id == None:
            return "Empty id", 400
    else:
        return "Bad query", 400

    entry = Inventory.query.filter(Inventory.robot_id == id).first()
    if entry == None:
        inventory = Inventory(
            robot_id = id,
            slug = f"robo-{id}",
            project = 'default',
            status = True
        )
        db.session.add(inventory)
        db.session.commit()
        return "Inventory entry created successfully", 201
    else:
        return "Item already in inventory", 400

@app.route("/api/v1/inventory/<inv_id>", methods=["DELETE", "PUT"])
@jwt_required()
def update_inventory(inv_id):
    is_admin = get_jwt()["is_administrator"]
    current_user = get_jwt_identity()
    if request.method == "PUT":
        data = request.json
        entry = Inventory.query.filter_by(slug=inv_id).first()
        if entry == None:
            return "Requested item does not exist", 400
        # Check if the user has ownership of the item
        if entry.user_id != current_user and not is_admin:
            return "Unauthorized item", 403
        # Check between different update targets
        if "issue" in data:
            entry.issue = data["issue"]
        elif "status" in data and is_admin:
            if isinstance(data["status"], bool):             
                entry.status = data["status"]
            else:
                return "Expected boolean", 400
        elif "project" in data and is_admin:
            entry.project = data["project"]
        else:
            return "Bad query", 400
        db.session.commit()
        return "Inventory successfully updated", 200

    elif request.method == "DELETE":
        Inventory.query.filter(Inventory.slug == inv_id).delete()
        db.session.commit()
        return "Record deleted successfully", 200


@app.route("/api/v1/users", methods=["GET", "PUT"])
@admin_required()
def users():
    if request.method == "GET":
        users = User.query.all()
        results = [
            {
                "id": user.id,
                "email": user.email,
                "active": user.active,
                "role": user.role
            } for user in users
        ]
        return jsonify(results), 200

    elif request.method == "PUT":
        data = request.json
        for u in data:
            user = User.query.get(u["id"])
            user.active = u["active"]
            user.role = u["role"]
            db.session.commit()
        return "Users updated", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)