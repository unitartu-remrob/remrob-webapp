import json

from datetime import timedelta, timezone, datetime, date
from functools import wraps

from flask import Flask, request, jsonify, render_template
from sqlalchemy import func, text, cast, Date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Message, Mail
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager, \
    get_jwt, verify_jwt_in_request, decode_token, set_refresh_cookies, unset_refresh_cookies
import bcrypt, os
from dotenv import load_dotenv, find_dotenv

from logs.top import get_system_usage


app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

is_prod = os.environ.get('FLASK_ENV') == 'production'
env_file = '.env.production' if (is_prod) else '.env'
load_dotenv(find_dotenv(env_file))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5000)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

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
    msg.html = render_template("reset_email.html", user_name=f"{user.first_name} {user.last_name}", url=url + token)
    mail.send(msg)


def send_confirmation(email, name):
    msg = Message()
    msg.subject = "Registration confirmation"
    msg.sender = os.getenv("MAIL_USERNAME")
    msg.recipients = [email]
    msg.html = render_template("confirmation_email.html", user_name=name)
    mail.send(msg)


def send_activation_email(email, name):
    msg = Message()
    msg.subject = "Your Remrob account is now active! 🤖"
    msg.sender = os.getenv("MAIL_USERNAME")
    msg.recipients = [email]
    msg.html = render_template("activation_email.html", user_name=name)
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

    # Capitalize first letter of first and last name
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()

    user = User.query.filter(func.lower(User.email)==email.lower()).first()

    if user:
        return "There already is a user with this email", 400
    else:
        user = User(email=email, first_name=first_name, last_name=last_name, password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), active=False, role="ROLE_LEARNER")
        db.session.add(user)
        db.session.commit()
        send_confirmation(email, f"{first_name} {last_name}")
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
    user = User.query.filter(func.lower(User.email)==email.lower()).first()

    if not user:
        return "User not found", 400

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        if user.active:
            additional_claims = {"is_administrator": user.role == "ROLE_ADMIN"}

            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)

            response = jsonify(access_token=access_token, user_id=user.id, role=user.role)
            set_refresh_cookies(response, refresh_token)
            return response, 200
        else:
            return "Your account has not been activated yet", 403
    else:
        return "Invalid password", 400


@app.route("/api/v1/refresh-token", methods=["POST"])
@jwt_required(refresh=True, locations="cookies")
def refresh():
    jwt = get_jwt()
    user_id = jwt["sub"]
    user = User.query.filter_by(id=user_id).first()
    is_administrator = user.role == "ROLE_ADMIN"
    access_token = create_access_token(identity=user_id, additional_claims={"is_administrator": is_administrator})
    return jsonify(access_token=access_token, user_id=user_id, role=user.role)


@app.route("/api/v1/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    res = jsonify(msg="JWT revoked")
    unset_refresh_cookies(res)
    return res


@app.route('/api/v1/password_reset', methods=['POST'])
def reset():
    data = request.json
    email = data['email']
    user = User.query.filter(func.lower(User.email)==email.lower()).first()

    if user:
        try:
            send_email(user)
            return "Email sent", 200
        except:
            return f"Email could not be delivered to {email}", 400
    return f"No user found for email {email}", 403


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
    else:
        return "Missing password", 400


@app.route("/api/v1/owncloud_link", methods=["GET"])
@jwt_required()
def user_owncloud():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=str(current_user)).first()
    if user.owncloud_id == None:
        return "User does not have an owncloud folder created", 404
    else:
        link = os.getenv("OWNCLOUD_VIEW_URL") + user.owncloud_id
        return link, 200

@app.route("/api/v1/newsboard", methods=["GET", "POST", "DELETE", "PUT"])
@jwt_required()
def newsboard():
    if request.method == "GET":
        latest = request.args.get("latest")
        print(latest)
        if latest == "true":
            news = Newsboard.query.filter_by(active=True)
        else:
            news = Newsboard.query.all()
            print(news)
        if news:
            results = [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "active": item.active
                } for item in news
            ]
            return jsonify(results), 200
        else:
            return "No newsboard found", 404

    elif request.method == "POST" and get_jwt()["is_administrator"]:
        data = request.json
        content = data["content"]
        title = data["title"]
        news = Newsboard(content=content, title=title, active=False)
        db.session.add(news)
        db.session.commit()
        return "Newsboard post created", 200

@app.route("/api/v1/newsboard/<post_id>", methods=["DELETE", "PUT"])
@admin_required()
def newsboard_update(post_id):
    if request.method == "PUT":
        data = request.json
        post = Newsboard.query.filter_by(id=post_id).first()
        if post:
            if "content" in data: post.content = data["content"]
            if "title" in data: post.title = data["title"]
            if "active" in data:
                # Set the previous one to inactive
                Newsboard.query.filter_by(active=True).update({"active": False})
                # Activate latest
                post.active = data["active"]
            db.session.commit()
            return "Newsboard item updated", 200
        else:
            return "Requested item not found", 404
    
    elif request.method == "DELETE":
        post = Newsboard.query.filter_by(id=post_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return "Newsboard post deleted", 200
        else:
            return "Requested item not found", 404

    else:
        return "Unauthorized", 403

@app.route("/api/v1/slots", methods=["GET"])
@admin_required()
def all_slots():
    results = []
    slots = Bookings.query.all()
    color = ""
    user_name = ""
    for slot in slots:
        if datetime.strptime(slot.end_time, "%Y-%m-%dT%H:%M").date() < date.today():
            # Do not send slots that are more than a week old
            continue

        if slot.user_id != None:
            color = "green"
            user = User.query.get(slot.user_id)
            if user:
                if user.first_name == None:
                    user.first_name = ""
                if user.last_name == None:
                    user.last_name = ""
                user_name = user.first_name + " " + user.last_name
        else:
            user_name = ""
            color = "blue"
        if slot.simulation:
            title = "Simulation"
        else:
            title = "Robot"
        slot_object = {
            "title": title,
            "start": slot.start_time,
            "end": slot.end_time,
            "id": slot.id,
            "color": color,
            "extendedProps": {
                "admin": slot.admin,
                "user": user_name
            }
        }
        results.append(slot_object)
    return jsonify({"bookings": results}), 200


@app.route('/api/v1/bookings', methods=["GET", "POST"])
@jwt_required()
def bookings():
    if request.method == "POST" and get_jwt()["is_administrator"]:
        data = request.json
        booking = Bookings(
            start_time=data["start"],
            end_time=data["end"],
            simulation=data["is_simulation"],
            project=data["project"],
            admin=data["admin"],
            activated=False
        )
        db.session.add(booking)
        db.session.commit()
        return "Booking slot created", 200
    elif request.method == "GET":
        results = []
        bookings = Bookings.query.filter_by(user_id=None).all()
        for booking in bookings:
            if datetime.strptime(booking.end_time, "%Y-%m-%dT%H:%M").date() < date.today():
                # Do not send slots that are more than a week old
                continue
            if datetime.strptime(booking.end_time, "%Y-%m-%dT%H:%M") < datetime.now():
                color = "gray"
            else:
                color = "blue"
            # inv = Inventory.query.get(booking.inventory_id)

            if booking.simulation:
                title = "Simulation"
            else:
                title = "Robot"
            slot_object = {
                "title": title,
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
        end = start_time + timedelta(minutes=int(data["interval"]))
        # if end > end_time:
        #     end = end_time
        for _ in range(int(data["nr_of_slots"])):
            booking = Bookings(
                start_time=datetime.strftime(start_time, date_format),
                end_time=datetime.strftime(end, date_format),
                simulation=data["is_simulation"],
                project=data["project"],
                admin=data["admin"]
            )
            # print("adding slot", data["nr_of_slots"])
            db.session.add(booking)
        db.session.commit()
        # print((datetime.strftime(start_time, date_format), datetime.strftime(end, date_format)))
        start_time = end + timedelta(minutes=int(data["downtime"]))
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
            if booking.simulation:
                title = "Simulation"
            else:
                title = "Robot"
            # inv = Inventory.query.get(booking.inventory_id)
            slot_object = {
                "title": title,
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
    user_bookings = Bookings.query.filter_by(user_id=str(current_user))
    date_format = "%Y-%m-%dT%H:%M"
    user_booking_times = []
    upcoming_bookings = 0
    for i in user_bookings:
        start = datetime.strptime(i.start_time, date_format)
        end = datetime.strptime(i.end_time, date_format)
        user_booking_times.append((start, end))

    if overlaps((datetime.strptime(slot.start_time, date_format), datetime.strptime(slot.end_time, date_format)),
                user_booking_times):
        return "Cannot book overlapping slots", 400

    for booking in user_bookings:
        if datetime.now() < datetime.strptime(booking.start_time, date_format):
            upcoming_bookings += 1

    if upcoming_bookings < 2:
        if int(data["userId"]) == current_user:
            if slot.user_id == None:
                slot.user_id = data["userId"]
                db.session.commit()
                return "Slot booked", 200
            else:
                return "Slot is already booked", 400
        else:
            return "Wrong user", 403
    else:
        return "Limit of active bookings reached", 400

@app.route("/api/v1/bookings/delete", methods=["DELETE"])
@admin_required()
def delete_date():
    data = request.get_json()
    selected_day = data.get("selected_day")
    # create a condition that checks if the start time has the same date as the selected day
    bookings_to_delete = Bookings.query.filter(
        cast(Bookings.start_time, Date) == selected_day
    ).all()
    for booking in bookings_to_delete:
        db.session.delete(booking)
    # deleted_count = Bookings.query.filter(cast(Bookings.start_time, Date) == selected_day).delete()
    db.session.commit()
    return "Day cleared", 200

@app.route("/api/v1/bookings/delete/<id>", methods=["DELETE"])
@admin_required()
def delete_slot(id):
    slot = Bookings.query.get(id)
    db.session.delete(slot)
    db.session.commit()
    return "Slot deleted", 200


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
    args = request.args
    if request.method == "POST":
        Simtainers.query.delete()
        for i in range(9):
            cont = Simtainers(
                container_id=i + 1,
                slug=f"robosim-{i + 1}",
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
                "vnc_uri": sim.vnc_uri,
                "user": sim.user_id
            } for sim in sims
        ]
        if args.get('user') == "true":
            results = [sim for sim in results if sim["user"] != None]
        sorted_inv = sorted(results, key=lambda x: x['container_id'])
        return jsonify(sorted_inv), 200


@app.route("/api/v1/inventory", methods=["GET"])
@admin_required()
def inventory():
    args = request.args
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
            "vnc_uri": inv.vnc_uri,
            "user": inv.user_id,
        } for inv in inventory
    ]
    if args.get('user') == "true":
        results = [item for item in results if item["user"] != None]
    sorted_inv = sorted(results, key=lambda x: x['robot_id'])
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
            robot_id=id,
            slug=f"robo-{id}",
            project='default',
            cell=0,
            status=False
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
        return "Item deleted successfully", 200


@app.route("/api/v1/users", methods=["GET", "PUT"])
@admin_required()
def users():
    if request.method == "GET":
        args = request.args
        users = User.query.order_by(User.id.desc()).all()
        results = [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "active": user.active,
                "role": user.role,
                "user_repo": user.user_repo,
                "owncloud_id": user.owncloud_id
            } for user in users
        ]
        if args.get('active') == "false":
            results = [user for user in results if not user["active"]]
        return jsonify(results), 200

    elif request.method == "PUT":
        data = request.json
        if "active" in data:
            user = User.query.get(data["id"])
            user_name = f"{user.first_name} {user.last_name}"
            # If user is not activated, but the request is to activate, send an activation email
            if not user.active and data["active"]:
                try:
                    send_activation_email(user.email, user_name)
                except Exception as e:
                    print(e)
                    print(f"Activation email failed to send for {user_name}, but account will still be activated")
            # Change the status, if the account gets disabled, no email is sent
            user.active = data["active"]
            db.session.commit()
            if user.active:
                return f"{user_name} account activated", 200
            else:
                return f"{user_name} account deactivated", 200
        if "role" in data:
            user = User.query.get(data["id"])
            user.role = data["role"]
            db.session.commit()
            return f"{user.first_name} {user.last_name} role updated to ${data['role']}", 200


@app.route("/api/v1/users/<id>", methods=["DELETE"])
@admin_required()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return f"User {user.first_name} {user.last_name} has been removed", 200


@app.route("/api/v1/admins", methods=["GET"])
@admin_required()
def admins():
    admins = User.query.filter_by(role="ROLE_ADMIN")
    result = []
    for admin in admins:
        if admin.first_name == None:
            admin.first_name = ""
        if admin.last_name == None:
            admin.last_name = ""
        result.append(admin.first_name + " " + admin.last_name)
    return jsonify(result), 200


@app.route('/fps', methods=['POST'])
def fps_measure():
    data = request.json

    if 'fps' not in data:
        return {"error": "No fps value provided"}, 400

    if 'source' not in data:
        return {"error": "No source provided"}, 400

    cpu_usage, ram_usage, gpu_usage, gpu_util = get_system_usage()

    # Add metrics to data dictionary
    data['cpu_usage'] = cpu_usage
    data['ram_usage'] = ram_usage
    data['gpu_usage'] = gpu_usage
    data['gpu_util'] = gpu_util

    with open('logs/fps_data.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')

    return {"message": "FPS data logged successfully"}, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0")
