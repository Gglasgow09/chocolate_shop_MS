from sqlalchemy import func, desc
from models import  Customer, Order, Chocolate, User, Role
from app import Session
from customer import add_new_customer
from order import add_order

session = Session()


# # Examples for adding customers and orders
# add_new_customer('Sally', 'Johnson', 'sallyj@example.com', '+17185237072', '110 Main Street Brooklyn NY, 11212')
# add_order(5, 1, [1, 2])  # This example shows customer with id 1 exists and chocolates with ids 1 and 2 exist

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

# advanced queries
# 1. Get the top 3 customers with the most orders
top_customers = session.query(
    Order.customer_id,
    Customer.first_name,
    Customer.last_name,
    func.count(Order.id).label('order_count')
).join(
    Order
).group_by(
    Customer.id
).order_by(
    func.count(Order.id).desc()
).limit(3).all()
for customer in top_customers:
    print(f"{customer.first_name} {customer.last_name} has {customer.order_count} orders.")

# Get all users with admin role
admin_users = session.query(User).filter(User.roles.any(Role.name == 'admin')).all()
for user in admin_users:
    print(f"{user.first_name} {user.last_name} {user.username} has admin privelages.")

