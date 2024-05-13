from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

association_table = Table('order_chocolates', Base.metadata,
                          Column('order_id', Integer, ForeignKey('orders.id')),
                          Column('chocolate_id', Integer, ForeignKey('chocolates.id'))
                          )

class Chocolate(Base):
    __tablename__ = 'chocolates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False)

    orders = relationship("Order", secondary=association_table, back_populates="chocolates")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    orders = relationship("Order", back_populates="customer")

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
