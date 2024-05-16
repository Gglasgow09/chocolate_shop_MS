from models import Order, Chocolate
from sqlalchemy.exc import SQLAlchemyError
from app import session

# Order
def add_order(quantity, customer_id, chocolate_ids):
    try:
        # Start a transaction
        order = Order(quantity=quantity, customer_id=customer_id)
        session.add(order)
        session.flush()  # Ensure the order ID is generated

        for chocolate_id in chocolate_ids:
            chocolate = session.query(Chocolate).get(chocolate_id)
            if chocolate.inventory < quantity:
                raise Exception(f"Not enough inventory for chocolate id {chocolate_id}")
            chocolate.inventory -= quantity
            order.chocolates.append(chocolate)
            print(f"Updated inventory for chocolate id {chocolate_id}: {chocolate.inventory}")

        session.commit()
        print(f"Order {order.id} added successfully.")
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"Failed to add order: {e}")
    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"Failed to add order: {e}")

def update_order(order_id, new_order):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        order.id = new_order
        session.commit()

def delete_order(order_id):
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        session.delete(order)
        session.commit()
