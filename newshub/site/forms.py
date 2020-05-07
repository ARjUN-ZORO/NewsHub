from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, RadioField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Email,Length, NumberRange, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Enter your Email',validators=[InputRequired(),Email(),Length(min=5,max=25)])
    password = PasswordField('Enter your Password',validators=[InputRequired(),Length(min=6,max=80)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField('Full Name',validators=[InputRequired(),Length(min=2,max=20)])
    # dob = DateField('Date of Birth',format="%Y-%m-%d",validators=[InputRequired()])
    email = StringField('Enter your Email',validators=[InputRequired(),Email(),Length(min=5,max=25)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=80)])
    repassword = PasswordField('Conform Password',validators=[InputRequired(),EqualTo('password')])
    address = TextAreaField('Address')
    submit = SubmitField("Register")

class UpdateAccountForm(FlaskForm):
    name = StringField('Full Name',validators=[InputRequired(),Length(min=2,max=20)])
    # dob = DateField('Date of Birth',format="%Y-%m-%d",validators=[InputRequired()])
    email = StringField('Enter your Email',validators=[InputRequired(),Email(),Length(min=5,max=25)])
    address = TextAreaField('Address')
    submit = SubmitField("Update")
