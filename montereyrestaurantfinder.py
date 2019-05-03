from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

from yelpmodel import yelpmodel

model = yelpmodel()
# restaurantList = model.findRestaurantByCuisine("Mexican")
# results = list()
# for restaurant in restaurantList:
#     results.append(model.get_business(model.API_KEY, restaurant['id']))
# print(results[0])
# model.findRestaurantByCuisine("Mexican")

# ChooseCuisineForm is the class for the form that the user uses to select the genre for a random restaurant
class ChooseCuisineForm(FlaskForm):
    # SelectField forms a dropdown menu with the specified choices
    # The first value in each tuple is what will get passed to the code,
    # while the second value is what the user sees. So far it seems to pass
    # the second value to the code as well so I'm confused. SL
    cuisines = SelectField(
        'Select Cuisine',
        choices=[('american', 'American'), ('mexican', 'Mexican'), ('italian', 'Italian'), ('mediterranean', 'Mediterranean')]
    )
    submit=SubmitField("GO!")
    

app = Flask(__name__)
bootstrap = Bootstrap(app)





# Render the homepage with the form for the genre selection
@app.route('/')
def home():
    form = ChooseCuisineForm()
    return render_template('home.html', form=form)





# Display the results of the genre form. So far, just shows the genre very large
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = ChooseCuisineForm()
    results = list()
    cuisine=dict(form.cuisines.choices).get(form.cuisines.data)
    restaurantList = model.findRestaurantByCuisine(cuisine)
    for restaurant in restaurantList:
        results.append(model.get_business(model.API_KEY, restaurant['id']))
    # print(results)
    return render_template('randomSelection.html', results=results)





# This is necessary for forms according to StackOverflow. Not sure why or what it does
app.config['SECRET_KEY'] = 'any secret string'

# Code to allow app to be run normally from command line
if __name__ == '__main__':
    app.run(debug=True)