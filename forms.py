from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

choices = ['✅', '❌']

class Search(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Search")

class Add(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Maps Link", validators=[DataRequired(), URL()])
    img_url = StringField("Image Link", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets', choices=choices, validators=[DataRequired()])
    has_toilet = SelectField('Has Toilet', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi', choices=choices, validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls', choices=choices, validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffe Price", validators=[DataRequired()])
    submit = SubmitField("Add")
    cancel = SubmitField('Cancel')

class Update(FlaskForm):
    img_url = StringField("Image Link", validators=[DataRequired(), URL()])
    has_sockets = SelectField('Has Sockets', choices=choices, validators=[DataRequired()])
    has_toilet = SelectField('Has Toilet', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi', choices=choices, validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls', choices=choices, validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffe Price", validators=[DataRequired()])
    submit = SubmitField("Confirm")
    cancel = SubmitField('Cancel')