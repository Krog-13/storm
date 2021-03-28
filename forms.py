from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):

    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):

    name = StringField("Name: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Invalid email")])
    old = IntegerField('Old', default=18)
    city = StringField('City', validators=[Length(min=3, max=20, message="required name is  City min 3 max 10")])
    psw = PasswordField("Password: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    psw2 = PasswordField("Reaped password: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])

    submit = SubmitField("Register")
