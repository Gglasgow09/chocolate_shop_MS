from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chocolate, Customer, Order, Base
from faker import Faker
# from random import randint, sample

fake = Faker()
engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


chocolates_data = [
    {'name': 'Dark Chocolate', 'price': 3.99, 'inventory': 150},
    {'name': 'Milk Chocolate', 'price': 2.99, 'inventory': 150},
    {'name': 'White Chocolate', 'price': 6.99, 'inventory': 150},
    {'name': 'Blonde Chocolate', 'price': 5.99, 'inventory': 150},
    {'name': 'Ruby Chocolate', 'price': 9.99, 'inventory': 150},
    {'name': 'Raw Chocolate', 'price': 10.99, 'inventory': 150},
    {'name': 'Gianduja Chocolate', 'price': 8.99, 'inventory': 150},
    {'name': 'Vegan Chocolate', 'price': 2.99, 'inventory': 150},
]


customers_data = [
    {'first_name': 'John', 'last_name':'Doe', 'email': 'john@example.com', 'phone_number': '+1234567890', 'address': '123 Main St Brooklyn NY 11212'},
    {'first_name': 'Jane', 'last_name':'Doe', 'email': 'jane@example.com', 'phone_number': '+1234567891', 'address': '124 Main St New York, NY 10012'},
    {'first_name': 'Will', 'last_name':'Smith', 'email': 'will@example.com', 'phone_number': '+1234567892', 'address': '125 Main St Jamaica NY 11433'},
    {'first_name': 'Johnny', 'last_name':'Depp', 'email': 'johnny@example.com','phone_number': '+1234567893', 'address': '126 Main St New York 10001'},
    
]


orders_data = [
    {'customer_id': 1, 'quantity': 5, 'chocolates': [1, 2]},
    {'customer_id': 2, 'quantity': 3, 'chocolates': [2]},
    {'customer_id': 3, 'quantity': 2, 'chocolates': [3, 4]},
    {'customer_id': 4, 'quantity': 1, 'chocolates': [1]},
    {'customer_id': 1, 'quantity': 4, 'chocolates': [5, 6]},
    {'customer_id': 2, 'quantity': 3, 'chocolates': [7]},
    {'customer_id': 3, 'quantity': 2, 'chocolates': [2, 3]},
    {'customer_id': 14, 'quantity': 3, 'chocolates': [8, 5]},
    {'customer_id': 8, 'quantity': 1, 'chocolates': [6, 5]},
    {'customer_id': 4, 'quantity': 10, 'chocolates': [6, 5]},
    {'customer_id': 10, 'quantity': 8, 'chocolates': [3, 5]},
    {'customer_id': 14, 'quantity': 9, 'chocolates': [2, 2]},
    {'customer_id': 10, 'quantity': 7, 'chocolates': [7, 5]},
    {'customer_id': 8, 'quantity': 15, 'chocolates': [7, 4]}

]


session.commit()
# Insert chocolates
for data in chocolates_data:
    chocolate = Chocolate(**data)
    session.add(chocolate)
session.commit()  

# Insert customers
for data in customers_data:
    customer = Customer(**data)
    session.add(customer)
session.commit()  

# Insert orders
for data in orders_data:
    order = Order(customer_id=data['customer_id'], quantity=data['quantity'])
    session.add(order) 
    session.commit()  
    for chocolate_id in data['chocolates']:
        chocolate = session.get(Chocolate, chocolate_id)
        order.chocolates.append(chocolate)
    session.commit()

# Add 10 customers using faker
highest_id = session.query(Customer).order_by(Customer.id.desc()).first().id

for _ in range(10):
    highest_id += 1
    customer_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone_number': '+1' + fake.numerify(text='##########'),  
        'address': fake.address().replace('\n', ', ')
    }
    customer = Customer(**customer_data)
    session.add(customer)
    session.commit()  

# # add 10 orders
# highest_id = session.query(Order).order_by(Order.id.desc()).first().id
# for _ in range(10):
#     highest_id += 1
#     order_data = {
#         'customer_id': randint(1, 10),
#         'quantity': randint(1, 10),
#         'chocolates': sample(range(1, 8))
#     }
#     order = Order(customer_id=order_data['customer_id'], quantity=order_data['quantity'])
#     session.add(order)
#     session.commit()
#     for chocolate_id in order_data['chocolates']:
#         chocolate = session.get(Chocolate, chocolate_id)
#         order.chocolates.append(chocolate)
#     session.commit()