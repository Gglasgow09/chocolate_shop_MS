from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Chocolate, Customer, Order
import re


# chocolate
def add_chocolate(name, price, inventory):
    chocolate = Chocolate(name=name, price=price, inventory=inventory)
    session.add(chocolate)
    session.commit()

def update_chocolate_price(chocolate_id, new_price):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        chocolate.price = new_price
        session.commit()

def delete_chocolate(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        session.delete(chocolate)
        session.commit()


# customer
def is_valid_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email) is not None

def add_new_customer(first_name, last_name, email):
    if not first_name or not last_name or not email:
        print("First name, last name, and email are required.")
        return

    if not is_valid_email(email):
        print("Invalid email format.")
        return

    existing_customer = session.query(Customer).filter_by(email=email).first()
    if existing_customer is None:
        new_customer = Customer(first_name=first_name, last_name=last_name, email=email)
        session.add(new_customer)
        session.commit()
    else:
        print(f"A customer with the email {email} already exists.")

def add_customer(first_name, last_name, email):
    customer = Customer(frst_name=first_name, last_name=last_name, email=email)
    session.add(customer)
    session.commit()


def update_customer_name(customer_id, new_first_name, new_last_name):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.first_name = new_first_name
        customer.last_name = new_last_name
        session.commit()

def delete_customer(customer_id):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        session.delete(customer)
        session.commit()

def update_customer_email(customer_id, new_email):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if customer:
        customer.email = new_email
        session.commit()

# order
def add_order(quantity):
    order = Order(quantity=quantity)
    session.add(order)
    session.commit()

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


engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

add_new_customer('Sally', 'Johnson', 'sallyj@example.com')
update_customer_name(5, 'Sandra', 'Johnson')

# beginner simple queries for SQL
# 1. Get all customers
customers = session.query(Customer).all()
for customer in customers:
    print(customer.first_name, customer.last_name, customer.email)

# 2. where clause
customer = session.query(Customer).filter_by(first_name='John').first()
print(customer.first_name, customer.last_name, customer.email)

# 3. order by
customers = session.query(Customer).order_by(Customer.first_name).all()
for customer in customers:
    print(customer.first_name, customer.last_name, customer.email)

# 4. order by chocolates
chocolates = session.query(Chocolate).order_by(Chocolate.price).all()
for chocolate in chocolates:
    print(chocolate.name, chocolate.price, chocolate.inventory)
