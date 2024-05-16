import re
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Index
from sqlalchemy.orm import relationship, validates, declarative_base
import bcrypt

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
    __table_args__ = (Index('idx_username', 'username'),)

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def has_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Chocolate(Base):
    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)

    orders = relationship("Order", secondary=association_table, back_populates="chocolates")

class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = (Index('idx_email', 'email'), Index('idx_phone_number', 'phone_number'),)

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(15), nullable=False, unique=True)
    address = Column(String(200), nullable=False)

    orders = relationship("Order", back_populates="customer")
    
    @validates('first_name', 'last_name', 'email', 'phone_number', 'address')
    def validate_fields(self, key, value):
        if key in ['first_name', 'last_name', 'address'] and not value:
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be empty")
        if key == 'email' and not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value):
            raise ValueError("Invalid email format")
        if key == 'phone_number' and not re.match(r'^\+?1?\d{9,15}$', value):
            raise ValueError("Invalid phone number")
        return value

class Order(Base):
    __tablename__ = 'orders'
 
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    quantity = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    chocolates = relationship("Chocolate", secondary=association_table, back_populates="orders")
