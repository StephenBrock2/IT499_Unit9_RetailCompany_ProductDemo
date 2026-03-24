from order_repo import OrderRepository
import os
import psycopg2
from dotenv import load_dotenv
import time
import logging

load_dotenv()

def db_connect():
    DATABASE = os.getenv("DATABASE")
    USERNAME = os.getenv("USERNAME")
    PWD = os.getenv("PWD")
    conn = psycopg2.connect(f'dbname={DATABASE} user={USERNAME} password={PWD}')
    cur = conn.cursor()
    return cur, conn

def db_disconnect(cur, conn):
    conn.commit() 
    cur.close() 
    conn.close()

class DBOrderRepository(OrderRepository):

    def create_order():
        cur, conn = db_connect()



        db_disconnect(cur, conn)
        return

    def get_order_status():
        cur, conn = db_connect()



        db_disconnect(cur, conn)
        return

    def cancel_order():
        cur, conn = db_connect()



        db_disconnect(cur, conn)
        return

    def get_order_itemized():
        cur, conn = db_connect()



        db_disconnect(cur, conn)
        return



'''
EXAMPLE

    def row_count(self, tbl):
        tbl = VALID_TABLES[tbl]
        with psycopg.connect(f'dbname={self.database} user={self.cred_decrypt(self.__user)} password={self.cred_decrypt(self.__password)}') as conn:
            with conn.cursor() as cur:
                if tbl == 'in450a':
                    cur.execute(f'SELECT GetRowsTableA();')
                elif tbl == 'in450c':
                    cur.execute(f'SELECT GetRowsTableC();')
                query = cur.fetchall()
                query = query.pop()
                query = query[0]
            return query
            
            
            '''