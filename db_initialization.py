import os
import psycopg2
from dotenv import load_dotenv
import logging

log = logging.getLogger("Activity Log")
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("activity.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s","%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

load_dotenv()

def db_connect():
    DATABASE_URL = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    return cur, conn

def db_disconnect(cur, conn):
    cur.close() 
    conn.close()

def db_init():
    schema_sql = """CREATE EXTENSION IF NOT EXISTS pgcrypto;
                        CREATE TABLE customers (
                            customerID int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            first_name varchar(30) NOT NULL,
                            last_name varchar(30) NOT NULL,
                            phone varchar(20),
                            email varchar(254) UNIQUE NOT NULL,
                            address varchar(255) NOT NULL
                        );

                        CREATE TABLE payment_methods (
                            paymentID int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            payment_details BYTEA,
                            customerID int REFERENCES customers(customerID)
                        );

                        CREATE TABLE orders (
                            orderID int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            order_number bigint GENERATED ALWAYS AS IDENTITY (START WITH 1000000000 INCREMENT BY 1),
                            order_date date NOT NULL,
                            order_time time NOT NULL,
                            order_shipping decimal(10,2) NOT NULL,
                            tax_rate decimal(3,2) NOT NULL,
                            pre_total decimal(10,2) NOT NULL,
                            tax_value decimal(10,2) NOT NULL,
                            order_total decimal(10,2) NOT NULL,
                            order_status varchar(15) NOT NULL,
                            customerID int REFERENCES customers(customerID),
                            paymentID int REFERENCES payment_methods(paymentID)
                        );

                        CREATE TABLE products (
                            productID int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            product_name varchar(100) NOT NULL,
                            upc_number varchar(20) UNIQUE NOT NULL,
                            price decimal(10,2) NOT NULL
                        );

                        CREATE TABLE order_itemization (
                            orderID int REFERENCES orders(orderID),
                            productID int REFERENCES products(productID),
                            quantity int NOT NULL
                        );"""
    
    table_seed_sql = """INSERT INTO products (product_name, upc_number, price)
                        VALUES ('WIRELESS MOUSE', '012345678905', 19.99),
                        ('MECHANICAL KEYBOARD', '098765432112', 89.50),
                        ('USB-C CHARGING CABLE', '123450987654', 12.99),
                        ('27" LED MONITOR', '445566778899', 179.00),
                        ('BLUETOOTH HEADPHONES', '556677889900', 59.95),
                        ('EXTERNAL HARD DRIVE 1TB', '667788990011', 74.99),
                        ('LAPTOP STAND', '778899001122', 29.50),
                        ('PORTABLE POWER BANK 10,000MAH', '889900112233', 24.99),
                        ('HDMI 2.1 CABLE', '990011223344', 14.49),
                        ('SMART DESK LAMP', '101112131415', 39.99),
                        ('WIRELESS EARBUDS', '121314151617', 49.99),
                        ('GAMING CONTROLLER', '131415161718', 64.99),
                        ('500GB SSD', '141516171819', 52.00),
                        ('OFFICE CHAIR CUSHION', '151617181920', 22.95),
                        ('NOISE-CANCELING HEADSET', '161718192021', 129.99),
                        ('WEB CAMERA 1080P', '171819202122', 34.99),
                        ('MINI BLUETOOTH SPEAKER', '181920212223', 27.49),
                        ('SURGE PROTECTOR 6-OUTLET', '192021222324', 18.75),
                        ('WIRELESS KEYBOARD', '202122232425', 32.99),
                        ('ADJUSTABLE PHONE STAND', '212223242526', 9.99);

                        INSERT INTO customers (first_name, last_name, phone, email, address)
                        VALUES ('JOHN', 'CARTER', '555-214-8890', 'john.carter@example.com', '102 Maple Ridge Dr, Austin, TX 78721'),
                        ('MARIA', 'SANCHEZ', '555-771-0042', 'maria.sanchez@example.com', '88 Willow Bend Ln, Phoenix, AZ 85016'),
                        ('DAVID', 'NGUYEN', '555-903-1128', 'david.nguyen@example.com', '450 Sunset Park Blvd, Denver, CO 80205'),
                        ('EMILY', 'ROBERTS', '555-642-7781', 'emily.roberts@example.com', '12 Brookside Terrace, Portland, OR 97206'),
                        ('MICHAEL', 'THOMPSON', '555-330-9922', 'michael.thompson@example.com', '760 Lakeview Ct, Chicago, IL 60614'),
                        ('SARAH', 'PATEL', '555-118-4477', 'sarah.patel@example.com', '55 Orchard Hill Rd, Atlanta, GA 30309'),
                        ('KEVIN', 'WILSON', '555-889-2204', 'kevin.wilson@example.com', '901 Cedar Grove St, Columbus, OH 43215'),
                        ('LINDA', 'MARTIN', '555-447-6610', 'linda.martin@example.com', '33 Pine Hollow Ave, Tampa, FL 33611'),
                        ('ROBERT', 'HARRIS', '555-702-5533', 'robert.harris@example.com', '284 Oak Meadow Dr, Nashville, TN 37211'),
                        ('JESSICA', 'LEE', '555-990-7744', 'jessica.lee@example.com', '19 Evergreen Crest, Seattle, WA 98115');

                        INSERT INTO payment_methods (payment_details, customerid)
                        VALUES (pgp_sym_encrypt('30569309025904', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 1),
                        (pgp_sym_encrypt('4539148803436467', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 2),
                        (pgp_sym_encrypt('4716321012345678', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 3),
                        (pgp_sym_encrypt('5424180012345678', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 4),
                        (pgp_sym_encrypt('5555341234567890', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 5),
                        (pgp_sym_encrypt('371449635398431', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 6),
                        (pgp_sym_encrypt('378282246310005', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 7),
                        (pgp_sym_encrypt('6011601160116611', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 8),
                        (pgp_sym_encrypt('6011000990139424', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 9),
                        (pgp_sym_encrypt('3566002020360505', '3f92b1e7c4a8d0f6e1b3c9d2a7f4e0c1'), 10);
                        """
    role_management_sql = """REVOKE ALL ON SCHEMA public FROM PUBLIC;
                        REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

                        CREATE ROLE "ordermanager" LOGIN PASSWORD 'ordermng';
                        GRANT USAGE ON SCHEMA public TO "ordermanager";
                        GRANT SELECT, INSERT, UPDATE ON customers, order_itemization, orders, payment_methods, products TO "ordermanager";
                        """
    create_function_sql = """CREATE OR REPLACE FUNCTION CreateNewOrder(customer_id int, orderdate date, ordertime time, ordershipping decimal, taxrate decimal)
                        RETURNS TABLE(orderid int, order_number bigint, order_date date, order_time time, order_shipping decimal, tax_value decimal, order_total decimal, order_status varchar)
                        LANGUAGE plpgsql
                        AS $$
                        DECLARE
                            v_paymentid int;
                            v_orderid int;
                        BEGIN
                            SELECT paymentid INTO v_paymentid FROM payment_methods WHERE customerid = customer_id;
                            
                            INSERT INTO orders (order_date, order_time, order_shipping, tax_rate, pre_total, tax_value, order_total, order_status, customerid, paymentid)
                            VALUES (orderdate, ordertime, ordershipping, taxrate, 0.00, 0.00, 0.00, 'Not Shipped', customer_id, v_paymentid)
                            RETURNING orders.orderid INTO v_orderid;

                            RETURN QUERY
                            SELECT o.orderid, o.order_number, o.order_date, o.order_time, o.order_shipping, o.tax_value, o.order_total, o.order_status
                            FROM orders AS o
                            WHERE o.orderid = v_orderid;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION CreateOrderItem(order_id int, upc varchar, quantity_count int)
                        RETURNS TABLE(productid int, product_name varchar, price decimal, quantity int)
                        LANGUAGE plpgsql
                        AS $$
                        DECLARE
                            v_productid int;
                        BEGIN
                            SELECT p.productid INTO v_productid FROM products AS p WHERE upc_number = upc;
                            
                            INSERT INTO order_itemization (orderid, productid, quantity)
                            VALUES (order_id, v_productid, quantity_count);
                            
                            RETURN QUERY
                            SELECT p.productid, p.product_name, p.price, o.quantity
                            FROM products p JOIN order_itemization o ON p.productid = o.productid
                            WHERE p.productid = v_productid
                            AND o.orderid = order_id;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION CalculateOrderPreTotal(order_id int)
                        RETURNS decimal
                        LANGUAGE plpgsql
                        AS $$
                        DECLARE
                            v_pre_total decimal;
                        BEGIN
                            SELECT SUM(p.price * o.quantity) INTO v_pre_total
                            FROM products p JOIN order_itemization o ON p.productid = o.productid
                            WHERE o.orderid = order_id;

                            RETURN v_pre_total;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION UpdateOrderTotals(order_id int, pretotal decimal, taxvalue decimal, ordertotal decimal)
                        RETURNS TABLE(orderid int, order_number bigint, order_shipping decimal, pre_total decimal, tax_value decimal, order_total decimal, order_status varchar)
                        LANGUAGE plpgsql
                        AS $$
                        BEGIN
                            UPDATE orders o
                            SET pre_total = pretotal, tax_value = taxvalue, order_total = ordertotal
                            WHERE o.orderid = order_id;
                            
                            RETURN QUERY
                            SELECT o.orderid, o.order_number, o.order_shipping, o.pre_total, o.tax_value, o.order_total, o.order_status
                            FROM orders o
                            WHERE o.orderid = order_id;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION GetOrderStatus(user_id int, order_id int)
                        RETURNS TABLE(orderid int, order_number bigint, order_date date, order_time time, order_shipping decimal, tax_value decimal, order_status varchar, order_total decimal, customerid int)
                        LANGUAGE plpgsql
                        AS $$
                        BEGIN
                            RETURN QUERY
                            SELECT o.orderid, o.order_number, o.order_date, o.order_time, o. order_shipping, o.tax_value, o.order_status, o.order_total, o.customerid
                            FROM orders o
                            WHERE o.orderid = order_id
                            AND o.customerid = user_id;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION CancelCustomerOrder(user_id int, order_id int)
                        RETURNS TABLE(orderid int, order_number bigint, order_date date, order_time time, order_status varchar, order_total decimal)
                        LANGUAGE plpgsql
                        AS $$
                        BEGIN
                            UPDATE orders o 
                            SET order_status = 'Cancelled'
                            WHERE o.orderid = order_id AND o.order_status NOT IN ('Fulfilled', 'Cancelled')
                            AND o.customerid = user_id;
                            
                            RETURN QUERY
                            SELECT o.orderid, o.order_number, o.order_date, o.order_time, o.order_status, o.order_total
                            FROM orders o
                            WHERE o.orderid = order_id
                            AND o.customerid = user_id;
                        END;
                        $$;

                        CREATE OR REPLACE FUNCTION GetOrderItemization(user_id int, order_id int)
                        RETURNS TABLE(productid int, product_name varchar, upc_number varchar, price decimal, quantity int, item_total decimal, customerid int)
                        LANGUAGE plpgsql
                        AS $$
                        BEGIN
                            RETURN QUERY
                            SELECT p.productid, p.product_name, p.upc_number, p.price, o.quantity, (p.price * o.quantity) AS item_total, c.customerid
                            FROM products p JOIN order_itemization o ON p.productid = o.productid
                            JOIN orders c ON o.orderid = c.orderid
                            WHERE o.orderid = order_id
                            AND c.customerid = user_id;
                        END;
                        $$;
                        """

    cur, conn = db_connect()
    try:
        cur.execute(schema_sql)
        cur.execute(table_seed_sql)
        cur.execute(role_management_sql)
        cur.execute(create_function_sql)
        conn.commit()

    except Exception as e:
        log.error(e)
        return {"Error initializing database"}
    finally:
        db_disconnect(cur, conn)
