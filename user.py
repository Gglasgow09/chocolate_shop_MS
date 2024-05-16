from models import User, Role
from app import Session, app
from flask import request, jsonify, g
from functools import wraps

session = Session()

# Roles
def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.has_role(role_name):
                return jsonify({"error": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function


def add_role_to_user(user_id, role_name):
    user = session.get(User, user_id)
    role = session.query(Role).filter_by(name=role_name).first()
    if user and role:
        user.roles.append(role)
        session.commit()
    else:
        print("User or role not found.")

    existing_role = session.query(Role).filter_by(name=role_name).first()

    if existing_role and existing_role.users:
        print(f"A user with the role {role_name} already exists.")
        return

def remove_role_from_user(user_id, role_name):
    user = session.get(User, user_id)
    role = session.query(Role).filter_by(name=role_name).first()
    if user and role:
        user.roles.remove(role)
        session.commit()
    else:
        print("User or role not found.")

def setup_roles():
    admin_role = session.query(Role).filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        session.add(admin_role)

    user_role = session.query(Role).filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user')
        session.add(user_role)

    session.commit()

with app.app_context():
    setup_roles()


# USER 
def get_current_user():
    user_id = request.headers.get('user_id')
    if user_id:
        user = session.get(User, user_id)
        return user
    return None

# Add a user
def add_new_user(first_name, last_name, username, password):
    if not first_name or not last_name or not username or not password:
        print("First name, last name, username and password are required.")
        return
    
    existing_user = session.query(User).filter_by(username=username).first()

    if existing_user:
        print(f"A user with the username {username} already exists.")
        return

    # Create a new user
    user = User(first_name=first_name, last_name=last_name, username=username)
    user.set_password(password)

    session.add(user)
    session.commit()

    print("User added successfully.")

def update_user_password(user_id, new_password):
    user = session.get(User, user_id)
    if user:
        user.set_password(new_password)
        session.commit()
    else:
        print("User not found.")


add_new_user('John', 'Doe', 'johndoe', 'password')
add_new_user('Marlon', 'Myers', 'mmyers', 'password')

add_role_to_user(1, 'admin')
add_role_to_user(2, 'user')
add_role_to_user(3, 'admin')