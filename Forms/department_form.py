from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = StringField('id начальника', validators=[DataRequired()])
    members = StringField('Список id участников в формате "id1, id2, id3"', validators=[DataRequired()])
    email = EmailField('Почта департамента', validators=[DataRequired()])
    submit = SubmitField('Создать департамент')
