from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from typing import Optional
import crud

app = FastAPI()

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

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the dosa restaurant API!"}

# Customers endpoints
@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    customer = crud.get_customer(conn, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer, conn: sqlite3.Connection = Depends(get_db)):
    customer_id = crud.create_customer(conn, customer.dict())
    return {"id": customer_id, **customer.dict()}

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: Customer, conn: sqlite3.Connection = Depends(get_db)):
    crud.update_customer(conn, customer_id, customer.dict())
    return {"id": customer_id, **customer.dict()}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, conn: sqlite3.Connection = Depends(get_db)):
    crud.delete_customer(conn, customer_id)
    return {"message": "Customer deleted successfully"}

# Items endpoints
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    item = crud.get_item(conn, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
def create_item(item: Item, conn: sqlite3.Connection = Depends(get_db)):
    item_id = crud.create_item(conn, item.dict())
    return {"id": item_id, **item.dict()}

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, conn: sqlite3.Connection = Depends(get_db)):
    crud.update_item(conn, item_id, item.dict())
    return {"id": item_id, **item.dict()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, conn: sqlite3.Connection = Depends(get_db)):
    crud.delete_item(conn, item_id)
    return {"message": "Item deleted successfully"}

# Orders endpoints
@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, conn: sqlite3.Connection = Depends(get_db)):
    order = crud.get_order(conn, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders", response_model=Order)
def create_order(order: Order, conn: sqlite3.Connection = Depends(get_db)):
    order_id = crud.create_order(conn, order.dict())
    return {"id": order_id, **order.dict()}

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order, conn: sqlite3.Connection = Depends(get_db)):
    crud.update_order(conn, order_id, order.dict())
    return {"id": order_id, **order.dict()}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, conn: sqlite3.Connection = Depends(get_db)):
    crud.delete_order(conn, order_id)
    return {"message": "Order deleted successfully"}
