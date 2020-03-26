from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Время работы в часах', validators=[DataRequired()])
    collaborators = StringField('Список id участников в формате "id1, id2, id3"', validators=[DataRequired()])
    team_leader = IntegerField('id лидера', validators=[DataRequired()])
    is_finished = BooleanField('Работа выполнена?')
    submit = SubmitField('Добавить работу')