import re
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Index, UniqueConstraint 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates


Base = declarative_base()

association_table = Table('order_chocolates', Base.metadata,
                          Column('order_id', Integer, ForeignKey('orders.id')),
                          Column('chocolate_id', Integer, ForeignKey('chocolates.id'))
                          )

class Chocolate(Base):
    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)

# the difference between __table_args__ and unique=True
    '''
    __table_args__ are used to define table-level options that are not specific to a single column.
    you can use __table_args__ to define indexes, unique constraints, and other table-level options. 
    you also have the option to name the index or unique constraint. This can be helpful when you need 
    to reference the index or unique constraint later on. It is useful for db admin purposes. It allows
    you to easily identify the index or unique constraint in the database.
    where as unique =true is used to define a unique constraint on a single column. SQLAlchemy will automatically
    create a unique constraint on the column. This is useful when you want to ensure that no two rows in the table
    have the same value for a specific column.
    '''

    orders = relationship("Order", secondary=association_table, back_populates="chocolates")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)

# example of unique constraint
    # __table_args__ = (
    #     # makes sure no two customers can have the same email
    #     UniqueConstraint('email', name='uix_email'),
    #     # makes sure no two customers can have the same phone number
    #     UniqueConstraint('phone_number', name='uix_phone_number'),
    # )

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


engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
