### FastAPI Order Management Service ###

A lightweight, production‑ready FastAPI application that provides four core order management operations backed by a PostgreSQL database. This service is designed for simplicity, clarity, and easy deployment (e.g., via Railway).

### Features ###

This API exposes four user‑facing endpoints:

    # Function #        # Description #
    Create Order	    Accepts order details, calculates totals, and stores the order in PostgreSQL
    Get Order Status	Retrieves the current status of an order by ID
    Cancel Order	    Updates an existing order’s status to cancelled
    Get Order Itemized	Returns a full breakdown of items, tax, shipping, and totals

### Tech Stack ###

    FastAPI – high‑performance Python web framework
    PostgreSQL – persistent relational data storage
    psycopg2 – PostgreSQL database adapter for Python
    Uvicorn – ASGI server
    Railway – optional cloud hosting

### Installation ###

Clone the repository and install dependencies:

    pip install -r requirements.txt

Make sure your PostgreSQL connection string is set in your environment variables, typically:

    DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname

### Running the Application Locally ###

Start the FastAPI server:

    uvicorn main:app --reload

Local access:

    API root: http://127.0.0.1:800
    Interactive Swagger docs: http://127.0.0.1:8000/docs

### Hosted Deployment (Railway) ###

The product demo is currently deployed on Railway, the live API is available at:

    https://it499-stephenbrock-productdemo.up.railway.app

### API Endpoints ###

1. Create Order

POST /order

    Creates a new order with items, tax rate, and shipping cost.

    Sample Request Body (json):
{
  "shipping": 5.99,
  "tax_rate": 1.06,
  "items": {
    "012345678905": 1,
    "098765432112": 2,
    "123450987654": 1,
    "445566778899": 3,
    "556677889900": 1,
    "667788990011": 1,
    "778899001122": 2,
    "889900112233": 1,
    "990011223344": 2,
    "101112131415": 1,
    "121314151617": 1,
    "131415161718": 1,
    "141516171819": 2,
    "151617181920": 1,
    "161718192021": 1,
    "171819202122": 1,
    "181920212223": 2,
    "192021222324": 1,
    "202122232425": 1,
    "212223242526": 3
  }
}

2. Get Order Status

GET /order

    Returns the current status (e.g., Not Shipped, Fulfilled, Cancelled).

3. Cancel Order

POST /order/{order_id}

    Marks an order as cancelled if it has not already been processed.

4. Get Order Itemized

GET /order/{order_id}

    Returns a detailed breakdown including:

        Items and quantities and costs
        Tax
        Shipping
        Final total

### Testing ###

You can test all endpoints interactively using the demo deployment on Railway:

    https://it499-stephenbrock-productdemo.up.railway.app