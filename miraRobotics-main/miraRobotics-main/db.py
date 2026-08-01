import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sksahir$4",
    database="AImodel"
)

cursor = conn.cursor(dictionary=True)