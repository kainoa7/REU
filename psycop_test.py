import psycopg2

#set up database connection
conn = psycopg2.connect(database="coinbasedb",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

cursor = conn.cursor()

newName = 'alsharifcoin'
newPrice = '30.00'

cursor.execute("INSERT INTO coin_table (coin_name, coin_price) VALUES (%s, %s);", (newName, newPrice))

cursor.execute("SELECT * from coin_table;")
print(cursor.fetchall())

#Make the changes to the database persistent
#conn.commit()

# Close communication with the database
cursor.close()
conn.close()