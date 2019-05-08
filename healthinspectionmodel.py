import pymysql

class healthinspectionmodel():
    db = pymysql.connect("sutterlaird.com","sutterla_cst205","restaurant","sutterla_montereyrestaurants" )

    def getRestaurantPermitNum(self, restaurantName):
        with self.db.cursor() as cursor:
            sql = "SELECT `permit_no` FROM `restaurants` WHERE `name`LIKE %s"
            cursor.execute(sql, ("%" + restaurantName + "%"))
            # cursor.execute(sql, ("%DOMIN%"))
            result = cursor.fetchone()
            if result:
                print("permit num is " + str(result[0]))
            else:
                print("not found")