from bs4 import BeautifulSoup
import requests
import re
import psycopg2

def collectStrings(text, tag, class_name): #returns an array with containing all strings of a certain tag and class
    items = text.find_all(tag, class_ = class_name)
    result = []

    for item in items:
        result.append(item.string)
    
    return result

''' Collect site data directly from the internet. Doesn't work because coinbase seems to block bots
url = "https://www.coinbase.com/explore"
response = request.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

else:
    print("Error retrieving site data")
'''

#open html from file
with open("coinbase.htm") as fp:
    soup = BeautifulSoup(fp, "html.parser")

#collect names of coins and how many there are
nameCount = 0
names = []
unfilteredNames = collectStrings(soup, 'h2', "cds-typographyResets-t1xhpuq2 cds-headline-htr1998 cds-foreground-f1yzxzgu cds-transition-txjiwsi cds-start-s1muvu8a")
for name in unfilteredNames[:-6]: #avoid collecting other useless headings that appear at the bottom of the page
    nameCount += 1
    names.append(name) #only append actual coin names to names array
    #print(name)


print("# of currency names: " + str(nameCount))
print("\n")

#collect prices of the above coins 
priceCount = 0
prices = []
unfilteredPrices = collectStrings(soup, 'div', "cds-flex-f1g67tkn cds-flex-end-f9tvb5a cds-column-ci8mx7v cds-flex-start-f1urtf06 cds-0_5-_5akrcb")
for price in unfilteredPrices:
    if (price != None) and (price[0] == '$') and not ('M' in price or 'B' in price or 'T' in price): #avoid collecting empty strings or market caps, which include M or T
        priceCount += 1
        prices.append(price) #only append actual coin prices to prices array
        #print(price)

print("# of prices: " + str(priceCount))

#use psycop to update data in postgresql database

#set up database connection
conn = psycopg2.connect(database="crypto_db",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

cursor = conn.cursor()

for i in range(0, len(names)): #simultaneously loop through both lists
    newName = names[i]
    newPrice = prices[i]

    #print("Name: " + newName + " | Price: " + str(newPrice) + "\n")
    cursor.execute("INSERT INTO coinbase_table (coin_name, coin_price) VALUES (%s, %s);", (newName, newPrice))

cursor.execute("SELECT * from coinbase_table;")
print(cursor.fetchall())

#conn.commit()


# Close communication with the database
cursor.close()
conn.close()
