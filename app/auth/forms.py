from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email Address", validators=[
        DataRequired(),
        Length(max=100),
        Regexp(r"^[\w\.-]+@[\w\.-]+\.\w+$", message="Please enter a valid email address.")
    ])
    role = SelectField("Account Role", choices=[("USER", "Standard User"), ("ADMIN", "Administrator")], default="USER")
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Create Account")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.strip()).first():
            raise ValidationError("This username is already taken. Please choose another.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError("This email is already registered. Please login instead.")

class LoginForm(FlaskForm):
    username = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember My Session")
    submit = SubmitField("Secure Login")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Update Password")

class FaceEnrollmentForm(FlaskForm):
    consent = BooleanField("I voluntarily consent to biometric facial template generation for secondary identity verification.", validators=[DataRequired()])
    face_image = FileField("Upload Clear Frontal Face Photo (PNG/JPG)", validators=[DataRequired()])
    submit = SubmitField("Enroll Biometric Profile")
