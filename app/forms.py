from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Adding Items
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    keywords = StringField('Keywords')
    location = StringField('Location', validators=[DataRequired()])
    notes = StringField('Notes')
    submit = SubmitField('Add Item')

# Searching Items
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

# User Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    security_question = StringField('Security Question', validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    submit = SubmitField('Register')

# User Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Resetting Passwords
class ResetPasswordForm(FlaskForm):
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

# Security Questions
class SecurityQuestionForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Admin to reset user passwords
class AdminResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')
