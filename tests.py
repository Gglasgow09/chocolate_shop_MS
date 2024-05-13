import pytest
from models import Chocolate, Customer, Order, Session, Base, create_engine

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
    new_customer = Customer(first_name='John', last_name='Doe', email='johndoe@example.com')
    test_db.add(new_customer)
    test_db.commit()
    customer_in_db = test_db.query(Customer).first()
    assert customer_in_db.first_name == 'John'
    assert customer_in_db.last_name == 'Doe'
    assert customer_in_db.email == 'johndoe@example.com'

def test_create_order(test_db):
    new_chocolate = Chocolate(name='Test Chocolate', price=10, inventory=100)
    new_customer = Customer(first_name='John', last_name='Doe', email='johndoe@example.com')
    new_order = Order(customer=new_customer, chocolates=[new_chocolate], quantity=1)
    test_db.add(new_order)
    test_db.commit()
    order_in_db = test_db.query(Order).first()
    assert order_in_db.customer == new_customer
    assert order_in_db.chocolates[0] == new_chocolate
    assert order_in_db.quantity == 1