import re
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, validates, declarative_base


Base = declarative_base()

# many to many relationship between orders and chocolates
association_table = Table('order_chocolates', Base.metadata,
                          Column('order_id', Integer, ForeignKey('orders.id')),
                          Column('chocolate_id', Integer, ForeignKey('chocolates.id'))
                          )
# many to many relationship between users and roles
user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('role_id', Integer, ForeignKey('roles.id'))
                   )

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name= Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Chocolate(Base):
    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)

    orders = relationship("Order", secondary=association_table, back_populates="chocolates")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)

    orders = relationship("Order", back_populates="customer")
    
    @validates('first_name', 'last_name', 'email', 'phone_number','address')
    def validate_fields(self, key, value):
        if key == 'first_name':
            assert value != '', "First name cannot be empty"
        elif key == 'last_name':
            assert value != '', "Last name cannot be empty"
        elif key == 'email':
            assert re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value), "Invalid email format"
        elif key == 'phone_number':
            assert re.match(r'^\+?1?\d{9,15}$', value), "Invalid phone number"
        elif key == 'address':
            assert value != '', "Address cannot be empty"
        return value
class Order(Base):
    __tablename__ = 'orders'
 
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    quantity = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    chocolates = relationship("Chocolate", secondary=association_table, back_populates="orders")

