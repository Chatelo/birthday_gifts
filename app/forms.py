from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DecimalField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange

class UserForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Continue')

class MessageForm(FlaskForm):
    content = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')

class ContributionForm(FlaskForm):
    amount = DecimalField('Amount (KES)', validators=[
        DataRequired(),
        NumberRange(min=10, message='Minimum contribution is KES 10')
    ])
    phone = StringField('M-PESA Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Contribute')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    event_date = StringField('Event Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Save Event')