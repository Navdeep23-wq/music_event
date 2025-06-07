from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime

class CreateEventForm(FlaskForm):
    name = StringField('Event Name', validators=[
        DataRequired(message="Event name is required"),
        Length(min=3, max=100, message="Event name must be between 3 and 100 characters")
    ])
    
    genre_id = SelectField('Genre', coerce=int, validators=[
        DataRequired(message="Please select a genre")
    ])
    
    date = DateTimeField('Date & Time', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired(message="Please select a date and time")
    ])
    
    location = StringField('Location', validators=[
        DataRequired(message="Location is required"),
        Length(min=5, max=200, message="Location must be between 5 and 200 characters")
    ])
    
    price = DecimalField('Ticket Price', places=2, validators=[
        DataRequired(message="Price is required"),
        NumberRange(min=0, max=1000, message="Price must be between $0 and $1000")
    ])
    
    capacity = IntegerField('Ticket Capacity', validators=[
        DataRequired(message="Capacity is required"),
        NumberRange(min=1, max=10000, message="Capacity must be between 1 and 10,000")
    ])
    
    description = TextAreaField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(min=20, max=2000, message="Description must be between 20 and 2000 characters")
    ])
    
    image = FileField('Event Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files (jpg, png, gif) are allowed')
    ])
    
    terms = BooleanField('Agree to Terms', validators=[
        DataRequired(message="You must agree to the terms")
    ])
    
    def validate_date(form, field):
        if field.data < datetime.now():
            raise ValidationError("Event date must be in the future")