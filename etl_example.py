import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="newuser",
  password="Daniela+1992"
)

print(mydb)