from models import Customer, User
from app import Session
import getpass

session = Session()

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
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    user = session.query(User).filter_by(username=username).first()

    if user and user.check_password(password) and user.has_role('admin'):
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
        else:
            print("Customer not found.")
    else:
        print("Permission denied.")

delete_customer(14)
    