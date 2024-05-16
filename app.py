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
        user = session.query(User).get(user_id)
        return user
    return None

def add_role_to_user(user_id, role_name):
    user = session.query(User).get(user_id)
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

# # Get a user from the database
# user = session.get(User, 2) 
# delete_chocolate(1, user)
    
# chocolate
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



# customer
def add_new_customer(first_name, last_name, email, phone_number, address):
    if not first_name or not last_name or not email or not phone_number or not address:
        print("First name, last name, email, and phone number and address are required.")
        return

    existing_customer = session.query(Customer).filter_by(email=email).first()
    if existing_customer is None:
        new_customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address)
        session.add(new_customer)
        session.commit()
    else:
        print(f"A customer with the email {email} already exists.")

def add_customer(first_name, last_name, email):
    customer = Customer(frst_name=first_name, last_name=last_name, email=email)
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
  

def upadate_customer_phone_number(customer_id, new_phone_number):
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


# order
#advanced feature implementation of transactions
def add_order(quantity, customer_id, chocolate_ids):
    try:
        # Start a transaction
        order = Order(quantity=quantity, customer_id=customer_id)
        for chocolate_id in chocolate_ids:
            chocolate = session.query(Chocolate).get(chocolate_id)
            if chocolate.inventory < quantity:
                raise Exception(f"Not enough inventory for chocolate id {chocolate_id}")
            chocolate.inventory -= quantity
            order.chocolates.append(chocolate)
        session.add(order)
        # Commits the transaction
        session.commit()
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


# add_new_customer('Sally', 'Johnson', 'sallyj@example.com', '+17185237072', '110 Main Street Brookly NY, 11212' )
# update_customer_first_name(15, 'Sandra')
# update_customer_last_name(15, 'John')
# update_customer_email(15, 'sandrajohn@gmail.com')


# beginner simple queries for SQL
# 1. Get all customers
# customers = session.query(Customer).all()
# for customer in customers:
#     print(customer.first_name, customer.last_name, customer.email)

# # 2. where clause
# used the filter() method to create a query with a WHERE clause. The filter() method takes a column and a value to filter the results.
# customer = session.query(Customer).filter_by(first_name='John').first()
# print(customer.first_name, customer.last_name, customer.email)

# # 3. order by
# customers = session.query(Customer).order_by(Customer.first_name).all()
# for customer in customers:
#     print(customer.first_name, customer.last_name, customer.email)

# # 4. order by chocolates
# chocolates = session.query(Chocolate).order_by(Chocolate.price).all()
# for chocolate in chocolates:
#     print(chocolate.name, chocolate.price, chocolate.inventory)

# # intermediate queries

# # top selling chocolate
# top_selling_chocolate = session.query(
#     Chocolate.name, 
#     func.sum(Order.quantity).label('total')
# ).join(
#     Order.chocolates
# ).group_by(
#     Chocolate.name
# ).order_by(
#     desc('total')
# ).first()
# print(f"The top selling chocolate is {top_selling_chocolate.name}.")



# # customer with the most orders
# customer_most_orders = session.query(
#     Customer.first_name, 
#     Customer.last_name, 
#     func.count(Order.id).label('total')
# ).join(
#     Order.customer
# ).group_by(
#     Customer.id
# ).order_by(
#     desc('total')
# ).first()

# print(f"The customer with the most orders is {customer_most_orders.first_name} {customer_most_orders.last_name}.")

# # total revenue
# total_revenue = session.query(
#     func.sum(Chocolate.price * Order.quantity)
# ).join(
#     Order.chocolates
# ).first()

# print(f"The total revenue is ${total_revenue[0]}.")

# advanced queries
# 1. Get the top 3 customers with the most orders
# top_customers = session.query(
#     Order.customer_id,
#     Customer.first_name,
#     Customer.last_name,
#     func.count(Order.id).label('order_count')
# ).join(
#     Order
# ).group_by(
#     Customer.id
# ).order_by(
#     func.count(Order.id).desc()
# ).limit(3).all()

# for customer in top_customers:
#     print(f"{customer.first_name} {customer.last_name} has {customer.order_count} orders.")







