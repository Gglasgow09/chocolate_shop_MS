from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chocolate, Customer, Order, Base

engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


chocolates_data = [
    {'name': 'Dark Chocolate', 'price': 3.99, 'inventory': 100},
    {'name': 'Milk Chocolate', 'price': 2.99, 'inventory': 150},
    {'name': 'White Chocolate', 'price': 6.99, 'inventory': 150},
    {'name': 'Blonde Chocolate', 'price': 5.99, 'inventory': 150},
    {'name': 'Ruby Chocolate', 'price': 9.99, 'inventory': 150},
    {'name': 'Raw Chocolate', 'price': 10.99, 'inventory': 150},
    {'name': 'Gianduja Chocolate', 'price': 8.99, 'inventory': 150},
    {'name': 'Vegan Chocolate', 'price': 2.99, 'inventory': 150},
]


customers_data = [
    {'first_name': 'John', 'last_name':'Doe', 'email': 'john@example.com'},
    {'first_name': 'Jane', 'last_name':'Doe', 'email': 'jane@example.com'},
    {'first_name': 'Will', 'last_name':'Smith', 'email': 'will@example.com'},
    {'first_name': 'Johnny', 'last_name':'Depp', 'email': 'johnny@example.com'},
    
]


orders_data = [
    {'customer_id': 1, 'quantity': 5, 'chocolates': [1, 2]},
    {'customer_id': 2, 'quantity': 3, 'chocolates': [2]},
    {'customer_id': 3, 'quantity': 2, 'chocolates': [3, 4]},
    {'customer_id': 4, 'quantity': 1, 'chocolates': [1]},
    {'customer_id': 1, 'quantity': 4, 'chocolates': [5, 6]},
    {'customer_id': 2, 'quantity': 3, 'chocolates': [7]},
    {'customer_id': 3, 'quantity': 2, 'chocolates': [2, 3]},
    {'customer_id': 4, 'quantity': 1, 'chocolates': [4, 5]},
]

# Insert chocolates
for data in chocolates_data:
    chocolate = Chocolate(**data)
    session.add(chocolate)

# Insert customers
for data in customers_data:
    customer = Customer(**data)
    session.add(customer)

# Insert orders
for data in orders_data:
    order = Order(customer_id=data['customer_id'], quantity=data['quantity'])
    for chocolate_id in data['chocolates']:
        order.chocolates.append(session.query(Chocolate).get(chocolate_id))
    session.add(order)

session.commit()
