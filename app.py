from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Chocolate, Customer, Order

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

def delete_chocolate(chocolate_id):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        session.delete(chocolate)
        session.commit()


# customer
def add_new_customer(first_name, last_name, email):
    if not first_name or not last_name or not email:
        print("First name, last name, and email are required.")
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


engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# add_new_customer('Sally', 'Johnson', 'sallyj@example.com')
# update_customer_name(5, 'Sandra', 'Johnson')

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

# intermediate queries

# top selling chocolate
top_selling_chocolate = session.query(
    Chocolate.name, 
    func.sum(Order.quantity).label('total')
).join(
    Order.chocolates
).group_by(
    Chocolate.name
).order_by(
    desc('total')
).first()

print(f"The top selling chocolate is {top_selling_chocolate.name}.")

# customer with the most orders
customer_most_orders = session.query(
    Customer.first_name, 
    Customer.last_name, 
    func.count(Order.id).label('total')
).join(
    Order.customer
).group_by(
    Customer.id
).order_by(
    desc('total')
).first()

print(f"The customer with the most orders is {customer_most_orders.first_name} {customer_most_orders.last_name}.")

# total revenue
total_revenue = session.query(
    func.sum(Chocolate.price * Order.quantity)
).join(
    Order.chocolates
).first()

print(f"The total revenue is ${total_revenue[0]}.")






