from models import Chocolate, Order
from app import Session

session = Session()

def add_chocolate(name, price, inventory):
    if not name:
        print("Name is required.")
        return

    if not isinstance(price, (int, float)) or price <= 0:
        print("Price must be a positive number.")
        return

    if not isinstance(inventory, int) or inventory < 0:
        print("Inventory must be a non-negative integer.")
        return

    existing_chocolate = session.query(Chocolate).filter_by(name=name).first()
    if existing_chocolate is None:
        chocolate = Chocolate(name=name, price=price, inventory=inventory)
        session.add(chocolate)
        session.commit()
    else:
        print(f"A chocolate with the name {name} already exists.")

def update_chocolate_price(chocolate_id, new_price):
    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        chocolate.price = new_price
        session.commit()

def update_chocolate_inventory(chocolate_id, new_inventory):
    if not isinstance(new_inventory, int) or new_inventory < 0:
        print("Inventory must be a non-negative integer.")
        return

    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()
    if chocolate:
        chocolate.inventory = new_inventory
        session.commit()
    else:
        print(f"No chocolate found with the id {chocolate_id}.")

def purchase_chocolate(chocolate_id, quantity, customer_id):
    if not isinstance(quantity, int) or quantity < 0:
        print("Quantity must be a non-negative integer.")
        return

    chocolate = session.query(Chocolate).filter_by(id=chocolate_id).first()

    if chocolate:
        if chocolate.inventory < quantity:
            print("Not enough inventory.")
            return

        chocolate.inventory -= quantity

        # Create a new order
        order = Order(quantity=quantity, customer_id=customer_id)
        order.chocolates.append(chocolate)
        session.add(order)

        session.commit()
    else:
        print(f"No chocolate found with the id {chocolate_id}.")

purchase_chocolate(2, 20, 3)
print("Updated inventory for chocolate")

def delete_chocolate(chocolate_id, user):
    if user and user.has_role('admin'):
        chocolate = session.query(Chocolate).get(chocolate_id)
        if chocolate:
            session.delete(chocolate)
            session.commit()
        else:
            print("Chocolate not found.")
    else:
        print("Permission denied.")

