# Final_project_IS

The project follows a typical design pattern for building RESTful APIs with FastAPI. It separates the concerns into different modules:

1. main.py: This module defines the FastAPI application and handles the routing of API endpoints. It uses Pydantic models to define the request and response data structures for each endpoint.

2. crud.py: This module contains the CRUD (Create, Read, Update, Delete) functions for interacting with the SQLite database. It provides a set of helper functions that encapsulate the database operations for customers, items, and orders.

3. init_db.py This module is responsible for initializing the SQLite database and populating it with sample data from the 'example_orders.json' file. It uses SQLAlchemy to define the database models and relationships.

The project follows a relational database design, with three main entities: 'Customer', 'Item', and 'Order'. The relationships between these entities are defined as follows:

A 'Customer' can have multiple 'Order' instances.
An 'Order' can have multiple 'Item' instances (many-to-many relationship).
An 'Order is associated with a single 'Customer'.

The 'init_db.p' script sets up the database schema and enforces these relationships using foreign keys and an association table ('order_items') for the many-to-many relationship between 'Order' and 'Item'.

Implementation

1. main.py: This module imports the necessary dependencies and defines the Pydantic models for 'Customer', 'Item', and 'Order'. It also sets up the database connection using the 'get_db_connection' function and creates a dependency 'get_db' to manage the database connection lifecycle.

   The API endpoints are defined using FastAPI's routing decorators ('@app.get', '@app.post', '@app.put', '@app.delete'). Each endpoint calls the corresponding CRUD function from 'crud.py' and handles any exceptions that may arise.

2. crud.py: This module defines the CRUD functions for 'Customer', 'Item', and 'Order'. Each CRUD operation is implemented using SQL queries executed against the SQLite database.

   The module also imports the Pydantic models and the database connection utilities ('get_db_connection' and 'get_db'). It defines a FastAPI application and maps the CRUD functions to the corresponding API endpoints.

3. init_db.py: This module defines the SQLAlchemy models for 'Customer`, `Item', and 'Order', along with the association table 'order_items'. The 'create_database' function creates the SQLite database file ('db.sqlite') and initializes the database schema.

   The 'load_data' function reads the sample data from 'example_orders.json' and populates the database with customers, items, and orders. It ensures unique customers based on their name and phone number, and creates new items if they don't exist in the database.

The project follows best practices for building RESTful APIs, such as adhering to HTTP verbs (GET, POST, PUT, DELETE) and using appropriate status codes for error handling. It also leverages Pydantic for data validation and SQLAlchemy for database interactions, making the code more robust and maintainable.

--------------------------How to USE ---------------------------
First of all Create an virual environment 
conda create --name dosa-api python=3.9
source activate dosa-api

1. Install Dependencies:
   
pip install fastapi pydantic uvicorn sqlalchemy
  

3. Initialize the Database :

  Before running the application, you need to initialize the SQLite database with sample data. Run the ‘init_db.py’ script to create the ‘db.sqlite’ file and populate it with sample data from ‘example_orders.json’:

  
   python init_db.py


3. Start the Server:
   With the database initialized, you can now start the FastAPI server by running the following command:


   uvicorn main:app --reload


   This will start the server at http://localhost:8000. The --reload flag enables automatic server reload whenever you make changes to the code.

4. Access the API:
To access the API documentation and test the endpoints interactively, open your web browser and visit `http://localhost:8000/docs.


     

5. Perform CRUD Operations :
   The API provides the following endpoints for CRUD operations:

   Customers :
     POST /customers: Create a new customer
     GET /customers/{id}: Retrieve a customer by ID
     PUT /customers/{id}: Update a customer by ID
     DELETE /customers/{id}: Delete a customer by ID

   Items :

     POST /items: Create a new item
     GET /items/{id}: Retrieve an item by ID
     PUT /items/{id}: Update an item by ID
     DELETE /items/{id}: Delete an item by ID

   Orders :

    POST /orders: Create a new order
    GET /orders/{id}: Retrieve an order by ID
    PUT /orders/{id}: Update an order by ID
    DELETE /orders/{id}  : Delete an order by ID

To perform these operations, send HTTP requests to the corresponding endpoints with the appropriate method (GET, POST, PUT, DELETE) and data payload (for POST and PUT requests).

6. Stop the Server :
   When you're done using the API, you can stop the server by pressing `Ctrl+C` in the terminal where the server is running.

