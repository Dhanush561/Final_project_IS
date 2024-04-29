import json
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

Base = declarative_base()

# Association table for the many-to-many relationship between Orders and Items
order_items = Table(
    'order_items',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('item_id', ForeignKey('items.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    orders = relationship('Order', back_populates='customer')

    __table_args__ = (UniqueConstraint('name', 'phone', name='unique_name_phone'),)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    orders = relationship('Order', secondary=order_items, back_populates='items')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    notes = Column(String)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')
    items = relationship('Item', secondary=order_items, back_populates='orders')

def create_database(uri='sqlite:///db.sqlite'):
    engine = create_engine(uri, echo=True)
    Base.metadata.create_all(engine)
    return engine

def load_data(engine, filename='example_orders.json'):
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    with open(filename) as f:
        data = json.load(f)

    for order_data in data:
        # Ensure unique customer based on name and phone
        customer = session.query(Customer).filter_by(name=order_data['name'], phone=order_data['phone']).first()
        if not customer:
            customer = Customer(name=order_data['name'], phone=order_data['phone'])
            session.add(customer)
            session.commit()  # Commit immediately to ensure it's written to the database

        # Create a new order each time
        order = Order(timestamp=order_data['timestamp'], notes=order_data['notes'], customer=customer)
        session.add(order)

        for item_data in order_data['items']:
            item_key = (item_data['name'], item_data['price'])
            item = session.query(Item).filter_by(name=item_data['name'], price=item_data['price']).first()
            if not item:
                item = Item(name=item_data['name'], price=item_data['price'])
                session.add(item)
                session.commit()  # Ensure the item is added to the database

            if not session.query(order_items).filter_by(order_id=order.id, item_id=item.id).first():
                order.items.append(item)

        session.commit()

    session.close()

if __name__ == "__main__":
    engine = create_database()
    load_data(engine)

