# Chocolate Shop Management System

This is a Python application that uses SQLAlchemy to manage a chocolate shop. It allows you to manage users, roles, customers, chocolates, and orders.

## Models

The application has the following models:

- `User`: Represents a user in the system. Each user has a first name, last name, username, password, and a list of roles.
- `Role`: Represents a role in the system. Each role has a name and a list of users.
- `Chocolate`: Represents a chocolate in the shop. Each chocolate has a name, description, and price.
- `Customer`: Represents a person that places chocolate orders. Each Customer has a first name, last name, email, phone number and address
- `Order`: Represents an order in the system. Each order has a customer, a list of chocolates, and a total price.

## Relationships

The application has the following relationships:

- A many-to-many relationship between `User` and `Role` models. This means that a user can have multiple roles and a role can be assigned to multiple users.
- A many-to-many relationship between `Order` and `Chocolate` models. This means that an order can contain multiple chocolates and a chocolate can be included in multiple orders.
- A one-to-many Relationship between `Customers` and `Orders`. This means that one customer can place many orders.
- A  one-to-many Relationship bwtween `Role` and `Users`. A role can be assigned to multiple users

## Setup

To set up the application, you need to create a database and update the `create_engine` call in `app.py` with your database URL. Then, you can run `app.py` to create the tables and `seed.py` to populate the tables with seed data.

## Usage

You can interact with the application through the Python shell. Here are some examples:

- To create a new user:

  ```python
  from models import User
  user = User(first_name='John', last_name='Doe', username='johndoe', password='password')
  session.add(user)
  session.commit()