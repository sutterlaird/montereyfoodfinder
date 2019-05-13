from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pymysql

# Code to Remove &amp;
# UPDATE `restaurants` SET `name`=REPLACE(`name`, "&amp;", "&")

class healthinspectionmodel():
    db = pymysql.connect("sutterlaird.com","sutterla_cst205","restaurant","sutterla_montereyrestaurants" )

    def getRestaurantPermitNum(self, restaurantName):
        # Open database cursor
        with self.db.cursor() as cursor:
            # Perform query using MySQL 'like' statement
            sql = "SELECT `permit_no` FROM `restaurants` WHERE `name`LIKE %s"
            cursor.execute(sql, ("%" + restaurantName + "%"))
            # Get the first result
            result = cursor.fetchone()
            if result:
                return str(result[0])
            # If no success, adjust the query and try again

            # Remove apostrophes
            noApostrophes = restaurantName.replace("'", "")
            sql = "SELECT `permit_no` FROM `restaurants` WHERE `name`LIKE %s"
            cursor.execute(sql, ("%" + noApostrophes + "%"))
            # Get the first result
            result = cursor.fetchone()
            if result:
                return str(result[0])

            # Try just first two words
            nameList = restaurantName.split()
            if len(nameList) > 1:
                sql = "SELECT `permit_no` FROM `restaurants` WHERE `name`LIKE %s"
                cursor.execute(sql, ("%" + nameList[0] + " " + nameList[1] + "%"))
                result = cursor.fetchone()
                if result:
                    return str(result[0])
            return "not found"

    def getRestaurantInformation(self, restaurantName):
        inspectionData = list()
        # Get permit number for the restaurant
        permit_num = self.getRestaurantPermitNum(restaurantName)
        # If not in DB, abort immediately
        if permit_num == "not found":
            inspectionData.append(False)
            return inspectionData
        # Otherwise, proceed with extracting data
        inspectionData.append(True)
        inspection_site = "http://www.decadeonline.com/insp.phtml?agency=mon&violsortfield=TB_CORE_INSPECTION_VIOL.VIOLATION_CODE&record_id=PR0"
        # Request headers
        req = Request(
            inspection_site + str(permit_num),
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        # Perform the request and then pass the results to BS
        resp = urlopen(req)
        soup = BeautifulSoup(resp.read(), 'lxml')
        # Find all <td> elements with class="inspectionTableHeading"
        inspections = soup.findAll("td", {"class": "inspectionTableHeading"})
        # outputString = "Most Recent Inspection"
        # The code for scraping the inspection page is ugly and hacky but it works
        # First process the column that shows the date and type of inspection
        typeList = str(inspections[0]).split("<")
        inspectionData.append(typeList[2][28:])
        # Then process the column that shows the inspection results
        inspectList = str(inspections[1]).split(">")
        inspectionData.append(inspectList[1][:-5])
        inspectionData.append(inspection_site + str(permit_num))
        return inspectionData


# TEST CODE PLEASE REMOVE
# healthmodel = healthinspectionmodel()
# print(healthmodel.getRestaurantInformation("Tacos California Grill Mexican Restaurant"))