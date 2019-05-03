from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)



# ChooseGenreForm is the class for the form that the user uses to select the genre for a random restaurant
class ChooseGenreForm(FlaskForm):
    # SelectField forms a dropdown menu with the specified choices
    # The first value in each tuple is what will get passed to the code,
    # while the second value is what the user sees. So far it seems to pass
    # the second value to the code as well so I'm confused. SL
    genres = SelectField(
        'Select Genre',
        choices=[('american', 'American'), ('mexican', 'Mexican'), ('italian', 'Italian'), ('mediterranean', 'Mediterranean')]
    )
    submit=SubmitField('Find me food!')
    

app = Flask(__name__)
bootstrap = Bootstrap(app)


# Render the homepage with the form for the genre selection
@app.route('/')
def home():
    form = ChooseGenreForm()
    return render_template('home.html', form=form)


# Display the results of the genre form. So far, just shows the genre very large
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = ChooseGenreForm()
    return render_template('randomSelection.html', genre=dict(form.genres.choices).get(form.genres.data))


# This is necessary according to StackOverflow. Not sure why or what it does
app.config['SECRET_KEY'] = 'any secret string'

# Code to allow app to be run normally from command line
if __name__ == '__main__':
    app.run(debug=True)