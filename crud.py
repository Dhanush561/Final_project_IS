from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from typing import Optional

# CRUD functions
def get_customer(conn: sqlite3.Connection, customer_id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    else:
        return None

def create_customer(conn: sqlite3.Connection, customer: dict):
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE name = ? AND phone = ?", (customer['name'], customer['phone']))
    existing_customer = cur.fetchone()
    if existing_customer:
        return {"message": "Customer already exists", "id": existing_customer["id"]}
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer['name'], customer['phone']))
    conn.commit()
    return {"message": "Customer created successfully", "id": cur.lastrowid}

def update_customer(conn: sqlite3.Connection, customer_id: int, customer: dict):
    cur = conn.cursor()
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer['name'], customer['phone'], customer_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

def delete_customer(conn: sqlite3.Connection, customer_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

def get_item(conn: sqlite3.Connection, item_id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    else:
        return None

def create_item(conn: sqlite3.Connection, item: dict):
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE name = ? AND price = ?", (item['name'], item['price']))
    existing_item = cur.fetchone()
    if existing_item:
        return {"message": "Item already exists", "id": existing_item["id"]}
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item['name'], item['price']))
    conn.commit()
    return {"message": "Item created successfully", "id": cur.lastrowid}

def update_item(conn: sqlite3.Connection, item_id: int, item: dict):
    cur = conn.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item['name'], item['price'], item_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

def delete_item(conn: sqlite3.Connection, item_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

def get_order(conn: sqlite3.Connection, order_id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    else:
        return None

def create_order(conn: sqlite3.Connection, order: dict):
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
                (order['customer_id'], order['timestamp'], order['notes']))
    conn.commit()
    return {"message": "Order created successfully", "id": cur.lastrowid}

def update_order(conn: sqlite3.Connection, order_id: int, order: dict):
    cur = conn.cursor()
    cur.execute("UPDATE orders SET customer_id = ?, timestamp = ?, notes = ? WHERE id = ?",
                (order['customer_id'], order['timestamp'], order['notes'], order_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

def delete_order(conn: sqlite3.Connection, order_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

# Pydantic models
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    timestamp: int
    notes: str

# Database connection
def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Dependency
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

# FastAPI app
app = FastAPI()

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the dosa restaurant API!"}

# Customers endpoints
@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    customer = get_customer(conn, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers")
def create_customer_endpoint(customer: Customer, conn: sqlite3.Connection = Depends(get_db)):
    result = create_customer(conn, customer.dict())
    return result

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer_endpoint(customer_id: int, customer: Customer, conn: sqlite3.Connection = Depends(get_db)):
    update_customer(conn, customer_id, customer.dict())
    return {"id": customer_id, **customer.dict()}

@app.delete("/customers/{customer_id}")
def delete_customer_endpoint(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    delete_customer(conn, customer_id)
    return {"message": "Customer deleted successfully"}

# Items endpoints
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    item = get_item(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item_endpoint(item: Item, conn: sqlite3.Connection = Depends(get_db)):
    result = create_item(conn, item.dict())
    return result

@app.put("/items/{item_id}", response_model=Item)
def update_item_endpoint(item_id: int, item: Item, conn: sqlite3.Connection = Depends(get_db)):
    update_item(conn, item_id, item.dict())
    return {"id": item_id, **item.dict()}

@app.delete("/items/{item_id}")
def delete_item_endpoint(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    delete_item(conn, item_id)
    return {"message": "Item deleted successfully"}

# Orders endpoints
@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, conn: sqlite3.Connection = Depends(get_db)):
    order = get_order(conn, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders")
def create_order_endpoint(order: Order, conn: sqlite3.Connection = Depends(get_db)):
    result = create_order(conn, order.dict())
    return result

@app.put("/orders/{order_id}", response_model=Order)
def update_order_endpoint(order_id: int, order: Order, conn: sqlite3.Connection = Depends(get_db)):
    update_order(conn, order_id, order.dict())
    return {"id": order_id, **order.dict()}

@app.delete("/orders/{order_id}")
def delete_order_endpoint(order_id: int, conn: sqlite3.Connection = Depends(get_db)):
    delete_order(conn, order_id)
    return {"message": "Order deleted successfully"}
