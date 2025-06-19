from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, FileField
from wtforms.validators import DataRequired


class ThemeForm(FlaskForm):
    train_class = SelectField('Учебный класс', validators=[DataRequired()],
                              choices=[('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')])

    theme = FileField('Файл', validators=[DataRequired(), FileAllowed(['docx'])])

    def to_dict(self):
        return {
            'title': self.train_class.data,
            'price': self.theme.data,
        }
