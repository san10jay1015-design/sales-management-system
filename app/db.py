import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sanjay@10",   
        database="sales_db"
    )
    return conn