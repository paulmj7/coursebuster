from wtforms import Form, StringField, SelectField, TextAreaField, \
    PasswordField, BooleanField, validators, ValidationError
from coursebuster.models import Course, User
from flask_login import current_user


class AddCourseForm(Form):
    name = StringField('Course Name', [
        validators.Length(min=1, max=120), validators.InputRequired()])
    author = StringField('Author', [
        validators.Length(min=2, max=80), validators.InputRequired()])
    category = SelectField('Category', choices=[('tech', 'Technology'), (
        'help', 'Self-Help'), ('money', 'Finances')])
    description = TextAreaField('Course Description', [
        validators.InputRequired(), validators.Length(min=20, max=750)])


class RegistrationForm(Form):
    username = StringField('Username', validators=[
        validators.Length(min=5, max=20), validators.InputRequired()])
    email = StringField('Email', validators=[
        validators.Length(min=7, max=120), validators.InputRequired()])
    password = PasswordField('Password', [
        validators.InputRequired(), validators.Length(min=8, max=20), ])
    confirm_password = PasswordField('Confirm Password', [
        validators.InputRequired(), validators.EqualTo(
            'password', message='Passwords must match')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


class LoginForm(Form):
    email = StringField('Email', validators=[
        validators.Length(min=7, max=120), validators.InputRequired()])
    password = PasswordField('Password', [
        validators.InputRequired(), validators.Length(min=8, max=120), ])
    remember = BooleanField('Remember Me')


class UpdateAccountForm(Form):
    username = StringField('Username', validators=[
        validators.Length(min=5, max=20), validators.InputRequired()])
    email = StringField('Email', validators=[
        validators.Length(min=7, max=120), validators.InputRequired()])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already in use')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')
