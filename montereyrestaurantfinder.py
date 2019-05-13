from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import random

from yelpmodel import yelpmodel
from healthinspectionmodel import healthinspectionmodel

# Create the model for yelp queries
model = yelpmodel()

# ChooseCuisineForm is the class for the form that the user uses to select the cuisine for a random restaurant
class ChooseCuisineForm(FlaskForm):
    # SelectField forms a dropdown menu with the specified choices
    # The first value in each tuple is what will get passed to the code,
    # while the second value is what the user sees. So far it seems to pass
    # the second value to the code as well so I'm confused. SL
    cuisines = SelectField(
        'Select Cuisine',
        choices=[('american', 'American'), ('mexican', 'Mexican'), ('italian', 'Italian'), ('mediterranean', 'Mediterranean'),('random', 'Random')]
    )
    submit=SubmitField('Find me food!')
    

app = Flask(__name__)
bootstrap = Bootstrap(app)


# Render the homepage with the form for the genre selection
@app.route('/')
def home():
    form = ChooseCuisineForm()
    return render_template('home.html', form=form)


# Display the results of the cuisine form. So far, just a list of the names of the restaurants in the cuisine
# The next step will be to choose a random restaurant and generate a page with all of its information
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = ChooseCuisineForm()
    # Get the selected cuisine from the form
    cuisine=dict(form.cuisines.choices).get(form.cuisines.data)
    # While it is random, choose a random cuisine. This keeps Random from choosing Random
    while cuisine == "Random":
        randomCuisine = random.choice(form.cuisines.choices)
        cuisine = randomCuisine[1]
    # Use the Yelp model to get one random restaurant with the cuisine
    foundRestaurant = model.getRandomRestaurantByCuisine(cuisine)
    # Use the health inspection model to get the health inspection data
    healthModel = healthinspectionmodel()
    inspectionString = healthModel.getRestaurantInformation(foundRestaurant["name"].upper())
    return render_template('randomSelection.html', results=foundRestaurant, inspection=inspectionString)


# This is necessary for forms according to StackOverflow. Not sure why or what it does
app.config['SECRET_KEY'] = 'any secret string'

# Code to allow app to be run normally from command line
if __name__ == '__main__':
    app.run(debug=True)