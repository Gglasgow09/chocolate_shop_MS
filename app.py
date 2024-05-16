from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Chocolate, Customer, Order, User, Role
from flask import Flask, request, jsonify, g
from functools import wraps

app = Flask(__name__)

engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()

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

def get_current_user():
    user_id = request.headers.get('user_id')
    if user_id:
        user = session.get(User, user_id)
        return user
    return None

def add_role_to_user(user_id, role_name):
    user = session.get(User, user_id)
    role = session.query(Role).filter_by(name=role_name).first()
    if user and role:
        user.roles.append(role)
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



add_new_user('John', 'Doe', 'johndoe', 'password')

# add_role_to_user(1, 'admin')

# Chocolate
def add_chocolate(name, price, inventory):
    if not name:
        print("Name is required.")
        return

    if not isinstance(price, (int, float)) or price <= 0:
        print("Price must be a positive number.")
        return

    if not isinstance(inventory, int) or inventory < 0:
        print("Inventory must be a non-negative integer.")
        return

    existing_chocolate = session.query(Chocolate).filter_by(name=name).first()
    if existing_chocolate is None:
        chocolate = Chocolate(name=name, price=price, inventory=inventory)
        session.add(chocolate)
        session.commit()
    else:
        print(f"A chocolate with the name {name} already exists.")

def update_chocolate_price(chocolate_id, new_price):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        chocolate.price = new_price
        session.commit()

def update_chocolate_inventory(chocolate_id, new_inventory):
    if not isinstance(new_inventory, int) or new_inventory < 0:
        print("Inventory must be a non-negative integer.")
        return

    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        chocolate.inventory = new_inventory
        session.commit()
    else:
        print(f"No chocolate found with the id {chocolate_id}.")

def purchase_chocolate(chocolate_id, quantity):
    if not isinstance(quantity, int) or quantity < 0:
        print("Quantity must be a non-negative integer.")
        return

    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()

    if chocolate:
        if chocolate.inventory < quantity:
            print("Not enough inventory.")
            return

        chocolate.inventory -= quantity
        session.commit()
    else:
        print(f"No chocolate found with the id {chocolate_id}.")

def delete_chocolate(chocolate_id, user):
    if user and user.has_role('admin'):
        chocolate = session.query(Chocolate).get(chocolate_id)
        if chocolate:
            session.delete(chocolate)
            session.commit()
        else:
            print("Chocolate not found.")
    else:
        print("Permission denied.")

# Customer
def add_new_customer(first_name, last_name, email, phone_number, address):
    if not first_name or not last_name or not email or not phone_number or not address:
        print("First name, last name, email, phone number, and address are required.")
        return

    existing_customer = session.query(Customer).filter_by(email=email).first()
    if existing_customer is None:
        new_customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address)
        session.add(new_customer)
        session.commit()
    else:
        print(f"A customer with the email {email} already exists.")

def add_customer(first_name, last_name, email):
    customer = Customer(first_name=first_name, last_name=last_name, email=email)
    session.add(customer)
    session.commit()

def update_customer_first_name(customer_id, new_first_name):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.first_name = new_first_name
        session.commit()

def update_customer_last_name(customer_id, new_last_name):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.last_name = new_last_name
        session.commit()

def update_customer_email(customer_id, new_email):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.email = new_email
        session.commit()

def update_customer_phone_number(customer_id, new_phone_number):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.phone_number = new_phone_number
        session.commit()

def update_customer_address(customer_id, new_address):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.address = new_address
        session.commit()

def delete_customer(customer_id):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()

# Order
def add_order(quantity, customer_id, chocolate_ids):
    try:
        # Start a transaction
        order = Order(quantity=quantity, customer_id=customer_id)
        session.add(order)
        session.flush()  # Ensure the order ID is generated

        for chocolate_id in chocolate_ids:
            chocolate = session.query(Chocolate).get(chocolate_id)
            if chocolate.inventory < quantity:
                raise Exception(f"Not enough inventory for chocolate id {chocolate_id}")
            chocolate.inventory -= quantity
            order.chocolates.append(chocolate)
            print(f"Updated inventory for chocolate id {chocolate_id}: {chocolate.inventory}")

        session.commit()
        print(f"Order {order.id} added successfully.")
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"Failed to add order: {e}")
    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"Failed to add order: {e}")

def update_order(order_id, new_order):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        order.id = new_order
        session.commit()

def delete_order(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        session.delete(order)
        session.commit()
