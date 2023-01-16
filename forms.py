from flask_wtf import Form
from wtforms import StringField,RadioField,TextAreaField,IntegerField,SelectField,SubmitField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired,Email

class ContactForm(Form):
   name = StringField("Name Of Student",[validators.DataRequired("Please enter your name.")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")
   
   email = StringField("Email",[validators.DataRequired("Please enter your email address."),
      Email("Please enter your email address.")])
   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), 
      ('py', 'Python')])
   submit = SubmitField("Send")