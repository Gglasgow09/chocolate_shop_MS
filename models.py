from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Chocolate(Base):
    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    chocolate_id = Column(Integer, ForeignKey('chocolates.id'))
    quantity = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    chocolate = relationship("Chocolate", back_populates="orders")

Chocolate.orders = relationship("Order", back_populates="chocolate")
Customer.orders = relationship("Order", back_populates="customer")

engine = create_engine('sqlite:///chocolate_shop.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
