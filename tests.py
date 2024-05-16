import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chocolate, Customer, Order, Base

# Create a new engine and sessionmaker
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

# Now you can use Session in your tests
def test_db():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
@pytest.fixture(scope='module')
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.close()

def test_create_chocolate(test_db):
    new_chocolate = Chocolate(name='Test Chocolate', price=10, inventory=100)
    test_db.add(new_chocolate)
    test_db.commit()
    chocolate_in_db = test_db.query(Chocolate).first()
    assert chocolate_in_db.name == 'Test Chocolate'
    assert chocolate_in_db.price == 10
    assert chocolate_in_db.inventory == 100

def test_create_customer(test_db):
    new_customer = Customer(first_name='John', last_name='D', email='johnnydoe@example.com', phone_number='+1234567810', address='123 Main St Brooklyn NY 11213')
    test_db.add(new_customer)
    test_db.commit()
    customer_in_db = test_db.query(Customer).first()
    assert customer_in_db.first_name == 'John'
    assert customer_in_db.last_name == 'D'
    assert customer_in_db.email == 'johnnydoe@example.com'
    assert customer_in_db.phone_number == '+1234567810'
    assert customer_in_db.address == '123 Main St Brooklyn NY 11213'

def test_create_order(test_db):
    existing_chocolate = test_db.query(Chocolate).filter_by(name='Test Chocolate').first()
    existing_customer = test_db.query(Customer).filter_by(phone_number='+1234567810').first()
    new_order = Order(customer=existing_customer, chocolates=[existing_chocolate], quantity=1)
    test_db.add(new_order)
    test_db.commit()
    order_in_db = test_db.query(Order).first()
    assert order_in_db.customer == existing_customer
    assert order_in_db.chocolates[0] == existing_chocolate

def test_update_chocolate(test_db):
    existing_chocolate = test_db.query(Chocolate).filter_by(name='Test Chocolate').first()
    existing_chocolate.price = 20
    test_db.commit()
    updated_chocolate = test_db.query(Chocolate).filter_by(name='Test Chocolate').first()
    assert updated_chocolate.price == 20

def test_delete_chocolate(test_db):
    existing_chocolate = test_db.query(Chocolate).filter_by(name='Test Chocolate').first()
    test_db.delete(existing_chocolate)
    test_db.commit()
    chocolate_in_db = test_db.query(Chocolate).filter_by(name='Test Chocolate').first()
    assert chocolate_in_db is None