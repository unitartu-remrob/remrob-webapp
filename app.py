from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Message, Mail
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt, verify_jwt_in_request, decode_token
import bcrypt, os
from functools import wraps
from datetime import date, timedelta, timezone, datetime
from dotenv import load_dotenv, find_dotenv

##########################################
# git module imports
##########################################
import requests, json
# How do you even python module?
from communication import git_clone
from communication import git_commit_push
##########################################

app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

env_file = '.env.production' if (os.environ.get('FLASK_ENV') == 'production') else '.env'
load_dotenv(find_dotenv(env_file))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 100000
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


from models import *

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


def send_email(user):
    url = os.getenv("FRONTEND_BASE_URL") + "password_reset/"
    token = create_access_token(identity=user.id)
    msg = Message()
    msg.subject = "Password reset"
    msg.sender = os.getenv("MAIL_USERNAME")
    msg.recipients = [user.email]
    msg.html = render_template("reset_email.html", url=url+token)
    mail.send(msg)

def send_confirmation(email):
    msg = Message()
    msg.subject = "Register confirmation"
    msg.sender = os.getenv("MAIL_USERNAME")
    msg.recipients = [email]
    msg.html = render_template("confirmation_email.html")
    mail.send(msg)


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
    first_name = data["first_name"]
    last_name = data["last_name"]

    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400
    if not first_name:
        return "Missing firstname", 400
    if not last_name:
        return "Missing lastname", 400

    user = User.query.filter_by(email=email).first()
    
    if user:
        return "There already is a user with this email", 400
    else:
        user = User(email=email, first_name=first_name, last_name=last_name, password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), active=False, role="ROLE_LEARNER")
        db.session.add(user)
        db.session.commit()
        send_confirmation(email)
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

@app.route('/api/v1/password_reset', methods=['POST'])
def reset():
    data = request.json
    email = data['email']
    user = User.query.filter_by(email = email).first()

    if user:
        send_email(user)
        return "Email sent", 200
    return "No user found", 403

@app.route('/api/v1/password_reset_verified/<token>', methods=['POST'])
def reset_verified(token):
    user_id = decode_token(token)["sub"]
    user = User.query.get(user_id)
    if not user:
        return "No user found", 403

    password = request.json["password"]
    if password:
        user.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        db.session.commit()
        return "Password changed", 200

@app.route("/api/v1/slots", methods=["GET"])
@admin_required()
def all_slots():
    results = []
    slots = Bookings.query.all()
    for slot in slots: 
        slot_object = {
            "title": slot.project.title(),
            "start": slot.start_time,
            "end": slot.end_time,
            "id": slot.id,
            "extendedProps": {
                "admin": slot.admin
            }
        }
        results.append(slot_object)
    return jsonify({"bookings": results}), 200

@app.route('/api/v1/bookings', methods=["GET", "POST"])
@jwt_required()
def bookings():
    if request.method == "POST":
        data = request.json
        booking = Bookings(
            start_time=data["start"],
            end_time=data["end"],
            simulation=data["is_simulation"],
            project=data["project"],
            admin=data["admin"]
        )
        db.session.add(booking)
        db.session.commit()
        return "Booking slot created", 200
    elif request.method == "GET":
        results = []
        bookings = Bookings.query.filter_by(user_id=None).all()
        for booking in bookings: 
            if datetime.strptime(booking.start_time, "%Y-%m-%dT%H:%M") < datetime.now():
                color = "gray"
            else:
                color = "blue" 
            #inv = Inventory.query.get(booking.inventory_id)
            slot_object = {
                "title": booking.project.title(),
                "start": booking.start_time,
                "end": booking.end_time,
                "id": booking.id,
                "color": color,
                "extendedProps": {
                    "admin": booking.admin
                }
            }
            results.append(slot_object)
        return jsonify({"bookings": results}), 200

@app.route('/api/v1/bookings/bulk', methods=["POST"])
@admin_required()
def bookings_bulk():
    data = request.json
    date_format = "%Y-%m-%dT%H:%M"
    start_time = datetime.strptime(data["start"], date_format)
    end_time = datetime.strptime(data["end"], date_format)
    while start_time < end_time:
        end = start_time + timedelta(hours=int(data["interval"]))
        booking = Bookings(
            start_time=datetime.strftime(start_time, date_format),
            end_time=datetime.strftime(end, date_format),
            simulation=data["is_simulation"],
            project=data["project"],
            admin=data["admin"]
        )
        db.session.add(booking)
        db.session.commit()
        #print((datetime.strftime(start_time, date_format), datetime.strftime(end, date_format)))
        start_time = end
    return "Slots created", 200

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
                "color": "green",
                "extendedProps": {
                    "admin": booking.admin
                }
            }
            results.append(slot_object)
        return jsonify({"user_bookings": results}), 200
    else:
        return "Wrong user", 403

def overlaps(slot, booked_time_list):
    for times in booked_time_list:
        if slot[1] >= times[0] and times[1] > slot[0]:
            return True
    return False 

@app.route("/api/v1/bookings/book/<id>", methods=["POST"])
@jwt_required()
def book_slot(id):
    data = request.json
    current_user = get_jwt_identity()
    slot = Bookings.query.get(id)
    user_bookings = Bookings.query.filter_by(user_id = str(current_user))
    date_format = "%Y-%m-%dT%H:%M"
    user_booking_times = []
    for i in user_bookings:
        start = datetime.strptime(i.start_time, date_format)
        end = datetime.strptime(i.end_time, date_format)
        user_booking_times.append((start, end))

    if overlaps((datetime.strptime(slot.start_time, date_format), datetime.strptime(slot.end_time, date_format)), user_booking_times):
        return "Cannot book overlapping slots", 400

    is_simulations = False
    is_defaults = False
    for booking in user_bookings:
        if datetime.strptime(booking.start_time, date_format).date() == datetime.strptime(slot.start_time, date_format).date():
            if booking.simulation:
                is_simulations = True
            else:
                is_defaults = True

    if is_simulations and is_defaults:
        return "You have already booked both types for the day", 400
    if is_simulations and slot.simulation:
        return "Simulation already booked for the day", 400
    if is_defaults and not slot.simulation:
        return "Default booked already for the day", 400
    if int(data["userId"]) == current_user:
        if slot.user_id == None:
            slot.user_id = data["userId"]
            db.session.commit()
            return "Slot booked", 200
        else:
            return "Slot is already booked", 400
    else:
        return "Wrong user", 403

@app.route("/api/v1/bookings/delete/<id>", methods=["DELETE"])
@admin_required()
def delete_slot(id):
    slot = Bookings.query.get(id)
    db.session.delete(slot)
    db.session.commit()
    return "Slot deleted",200


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
        return "Wrong user", 403

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
@admin_required()
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
            "cell": inv.cell,
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
            cell = 0,
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
        if "status" in data and is_admin:
            if isinstance(data["status"], bool):             
                entry.status = data["status"]
            else:
                return "Expected boolean", 400
        if "project" in data and is_admin:
            entry.project = data["project"]
        if "cell" in data and is_admin:
            entry.cell = data["cell"]
        # else:
        #     return "Bad query", 400
        db.session.commit()
        return "Inventory successfully updated", 200

    elif is_admin and request.method == "DELETE":
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
                "first_name": user.first_name,
                "last_name": user.last_name,
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

@app.route("/api/v1/admins", methods=["GET"])
@admin_required()
def admins():
    admins = User.query.filter_by(role="ROLE_ADMIN")
    result = []
    for admin in admins:
        result.append(admin.first_name + " " + admin.last_name)
    return jsonify(result), 200

@app.route("/api/v1/cameras", methods=["POST"])
@admin_required()
def cameras():
    # Just an endpoint, so you don't have to manually fill the table
    if request.method == "POST":
        Cameras.query.delete()
        for i in range(8):
            cont = Cameras(
                cell = i+1,
            )
            db.session.add(cont)
        db.session.commit()
        return "Camera table filled", 201


############################################
##                  GIT                   ##
############################################

load_dotenv("communication/.env")
print(os.getenv("REPOS_ROOT"))
REPOS_ROOT = os.getenv("REPOS_ROOT")
CLONING_ROOT = os.getenv("CLONING_ROOT")
TOKEN_NAME = os.getenv("TOKEN_NAME")
TOKEN = os.getenv("TOKEN")


@app.route('/api/v1/check_user', methods=['GET'])
@jwt_required()
def api_check_user():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
    else:
        return 'error: no user specified'
    return check_project(user_name)

@app.route('/api/v1/commit_push', methods=['GET'])
def api_repo_commit_push():
    # This one is for committing from within the container
    if 'token' in request.args:
        session_token = request.args['token']
    else:
        return 'error: no session token provided'

    user = User.query.filter_by(git_token=session_token).first()

    if not user:
        return "No user found", 403
    else:
        user_name = user.user_repo

    path = os.path.join(REPOS_ROOT, user_name)

    return git_commit_push.commit_push(path)

@app.route('/api/v1/reclone', methods=['GET'])
def api_repo_reclone():
    # This one is for recloning from within the container
    """This function takes token as the request argument parses to get username after which it removes the repo and clones it again 

    Returns:
        _type_: _description_
    """

    if 'token' in request.args:
        session_token = request.args['token']
    else:
        return 'error: no session token provided'

    user = User.query.filter_by(git_token=session_token).first()

    if not user:
        return "No user found", 403
    else:
        user_name = user.user_repo

    path = os.path.join(REPOS_ROOT, user_name)

    force = False
    if 'force' in request.args:
        if 'true' == request.args['force'].lower():
            force = True  

    return git_clone.clone(CLONING_ROOT+user_name, TOKEN_NAME, TOKEN, REPOS_ROOT, force)
    

@app.route('/api/v1/clone_jwt', methods=['GET'])
@jwt_required()
def api_repo_clone_jwt():
    # @ user_name
    # @ [force]
    if 'user_name' in request.args:
        user_name = request.args['user_name']
    else:
        return 'error: no user specified'

    force = False
    if 'force' in request.args:
        if 'true' == request.args['force'].lower():
            force = True        

    return git_clone.clone(CLONING_ROOT+user_name, TOKEN_NAME, TOKEN, REPOS_ROOT, force)

@app.route('/api/v1/commit_push_jwt', methods=['GET'])
@jwt_required()
def api_repo_commit_push_jwt():
    # This one is for committing from the web
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    path = os.path.join(REPOS_ROOT, user.user_repo)
    
    return git_commit_push.commit_push(path)

def check_project(project_name: str):
    """Checks if repo exists, if not then creating it

    Args:
        project_name (str): user name

    Returns:
        str: status
    """
    url = "https://gitlab.ut.ee/api/v4/projects"
    project_path = project_name
    description = f"Project of the user: {project_name}"

    payload = json.dumps({
        "name": project_name,
        "description": description,
        "path": project_path,
        "initialize_with_readme": "true"
    })
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())

    if isinstance(response.json(), dict):
        resp = 'User exists' if response.json().get('message', 0) else 'User repo was created'
    else:
        resp = 'User exists'

    return resp

## Git end
############################################

if __name__ == '__main__':
    app.run(host="0.0.0.0")