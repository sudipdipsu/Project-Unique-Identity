from FormEntry import app, db
from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FormEntry.models import Pinfo, User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    citizenship = IntegerField('Citizenship No', validators=[DataRequired()])
    
    firstname = StringField('First Name', 
                            validators=[DataRequired(), Length(min=2, max=50) ])

    lastname = StringField('Last Name', 
                            validators=[DataRequired(), Length(min=2, max=50) ])

    sex = RadioField('Sex', choices=[('Male','Male'),('Female','Female'), ('Others','Others')])

    picture = FileField('Profile Picture',
                            validators=[DataRequired(), FileAllowed(['jpg','png'])])

    dob =   DateField('DoB', format='%Y-%m-%d')
    
    submit = SubmitField('Register Form')

    def validate_citizenship(self,citizenship):
        user_1 = Pinfo.query.filter_by(citizenship=citizenship.data).first()
        if user_1:
            raise ValidationError('Not a Valid Ctizenship No.')


class RegistrationAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length( min=2, max=50) ])

    email = StringField('Email', 
                            validators=[DataRequired(),Email()])

    password = PasswordField('Password', 
                                validators=[DataRequired(), Length(min=6)])

    confirm_password = PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken please take another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken please take another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(),Email()])

    password = PasswordField('Password', 
                                validators=[DataRequired(), Length(min=6)])

    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    citizenship = IntegerField('Citizenship No', validators=[DataRequired()])
    
    firstname = StringField('First Name', 
                            validators=[DataRequired(), Length(min=2, max=50) ])

    lastname = StringField('Last Name', 
                            validators=[DataRequired(), Length(min=2, max=50) ])

    sex = RadioField('Sex', choices=[('Male','Male'),('Female','Female'), ('Others','Others')])

    picture = FileField('Profile Picture',
                            validators=[DataRequired(), FileAllowed(['jpg','png'])])

    dob =   DateField('DoB', format='%Y-%m-%d')    
    
    submit = SubmitField('Register Form')

    def validate_citizenship(self,citizenship):
        id = current_user.id
        userinfo = Pinfo.query.filter_by(user_id=id).first()
        print(userinfo)
        if citizenship.data != userinfo.citizenship :
            user_1 = Pinfo.query.filter_by(citizenship=citizenship.data).first()
            if user_1:
                raise ValidationError('Not a Valid Ctizenship No.')