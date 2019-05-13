from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pymysql

db = pymysql.connect("sutterlaird.com","sutterla_cst205","restaurant","sutterla_montereyrestaurants" )
cursor = db.cursor()

root_url = "http://www.decadeonline.com/insp.phtml?agency=mon&violsortfield=TB_CORE_INSPECTION_VIOL.VIOLATION_CODE&record_id=PR0"

id = 600000
# id = 612513

while id < 640000:
    # Request headers
    req = Request(
        root_url + str(id),
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    # Perform the request and then pass the results to BS
    resp = urlopen(req)
    soup = BeautifulSoup(resp.read(), 'lxml')

    # Find all items inside <b> tags
    for boldText in soup.find_all('b'):
        # Check for 939 (first three of the zip code of every Monterey County city) to verify that you're in the block with the restaurant name
        if "939" in str(boldText):
            # Remove the tag brackets
            nameList = str(boldText).split("<")
            nameList[1] = nameList[1].replace("'", "''")
            restaurantName = nameList[1][4:]
            # Print the permit number and the name with the <b> removed
            print(str(id) + ": " + restaurantName)
            sql = "SELECT * FROM `restaurants` WHERE `permit_no`=%d"
            cursor.execute(sql % id)
            result = cursor.fetchone()
            if result:
                print("Duplicate")
            else:
                # Insert the permit number and the restaurant name into the database
                sql = "INSERT INTO restaurants(permit_no, \
                name) \
                VALUES ('%d', '%s')" % \
                (id, restaurantName)
                try:
                    # Execute the SQL command
                    cursor.execute(sql)
                    # Commit your changes in the database
                    db.commit()
                except pymysql.InternalError as error:
                    print("Failed to add to DB" + error)
                    # Rollback in case there is any error
                    db.rollback()
    id += 1


# disconnect from server
db.close()


# print(soup)