from app import db

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
    cell = db.Column('cell', db.Integer)
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

class Cameras(db.Model):
    __tablename__ = "cameras"
    id = db.Column(db.Integer, primary_key = True)

    cell = db.Column('cell', db.Integer)
    ip = db.Column('camera_ip', db.String(100))