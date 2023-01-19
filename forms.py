from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,TextAreaField,IntegerField,SelectField,SubmitField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired,Email

class ContactForm(FlaskForm):
   name = StringField("Name Of Student",validators=[validators.DataRequired("Name is required")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")
   
   email = StringField("Email", validators=[validators.DataRequired("email required"),validators.Email("Bad email")])
   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), 
      ('py', 'Python')])
   submit = SubmitField("Send")