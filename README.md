# Monterey Food Finder

## What it Does
This Flask app helps users decide where to eat in the Monterey Bay Area. Users select a cuisine, and the app will display a random restaurant that serves that cuisine and is currently open. It also pulls health inspection data for that restaurant from Monterey County, as well as displaying ratings, prices, and a Google Map of the restaurant.

## Who Built It
Built as the Final Project for Wes Modes' CST205 Multimedia Programming at California State University, Monterey Bay. The development team included Hector Lopez, Yazmin Carrillo, Edgar Licup, and Sutter Laird.

## Usage
This program is very user-friendly and intuitive. Upon launching the web app, users are presented with a drop-down menu of cuisines. Users can select the cuisine they desire to eat, or choose the Random option to have the app choose a random cuisine for them. Users then click the “Find me Food!” button. When the button is clicked, the app queries the Yelp and Google APIs and our custom interface for Monterey County’s health inspection data and presents the user with information on the selected restaurant. An embedded Google Map allows the user to locate the restaurant, while a link to Yelp allows the user to read guests’ reviews.

## Installation Instructions
1. Download contents of this repository to local system
2. Ensure all modules included in `requirements.txt` are installed
3. Execute `montereyfoodfinder.py` in Python 3
4. Navigate to `http://127.0.0.1:500` in your web browser
5. Find somewhere to eat!

