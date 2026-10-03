from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app import db
from app.models import User
import sqlalchemy

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()] )
    password2 = PasswordField("Repeat password",validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField("Registration")

    def validate__username(self,username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Input other username")


    def validate__username(self,email):
           user = db.session.scalar(sa.select(User).where(User.email == email.data))
           if user is not None:
               raise ValidationError("Input other email")