from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    email = EmailField("What's your email", validators=[DataRequired()])
    color = StringField("What's your favorite color")
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')
