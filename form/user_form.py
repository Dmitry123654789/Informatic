from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = EmailField('Ваш e-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
