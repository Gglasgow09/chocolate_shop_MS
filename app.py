from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Chocolate, Customer, Order


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
def add_customer(first_name, last_name, email):
    customer = Customer(frst_name=first_name, last_name=last_name, email=email)
    session.add(customer)
    session.commit()

def add_new_customer(first_name, last_name, email):
    existing_customer = session.query(Customer).filter_by(email=email).first()
    if existing_customer is None:
        new_customer = Customer(first_name=first_name, last_name=last_name, email=email)
        session.add(new_customer)
        session.commit()
    else:
        print(f"A customer with the email {email} already exists.")

def update_customer_name(name_id, new_name):
    customer = session.query(Customer).filter_by(id=name_id).first()
    if customer:
        customer.id = new_name
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

# some simple queries for SQL
# 1. Get all customers
customers = session.query(Customer).all()
for customer in customers:
    print(customer.first_name, customer.last_name, customer.email)
