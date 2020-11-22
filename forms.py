from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')