from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required

from Forms.department_form import DepartmentForm
from Forms.job_form import AddJobForm
from Forms.login_form import LoginForm
from Forms.register_form import RegisterForm
from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.team_leader = form.team_leader.data
        job.user = current_user

        session = db_session.create_session()
        job = session.merge(job)
        session.add(job)
        session.commit()

        return redirect('')
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/users.sqlite")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        session = db_session.create_session()
        session.add(user)
        session.commit()
        return redirect('')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/сhange_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def сhange_job(job_id):
    form = AddJobForm()
    form.submit.label.text = 'Изменить данные'
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.team_leader.data = job.team_leader
        form.is_finished.data = job.is_finished

    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        if current_user.id == 1 or job.user.id == current_user.id and job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            job.team_leader = form.team_leader.data
            session.add(job)
            session.commit()
            return redirect('')
        else:
            return render_template('add_job.html', title='Редактирование работы', form=form, message="У Вас нет на это прав!")
    return render_template('add_job.html', title='Редактирование работы', form=form)


@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if current_user.id == 1 or job.user.id == current_user.id:
        session.delete(job)
        session.commit()
    return redirect('')


@app.route('/')
def jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    return render_template('jobs.html', jobs=jobs, users=users, title='Главная')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    departments = session.query(Department).all()
    users = session.query(User).all()
    return render_template('departments.html', departments=departments, users=users, title='Департаменты')


@app.route('/add_depart', methods=['GET', 'POST'])
@login_required
def add_depart():
    form = DepartmentForm()
    if form.validate_on_submit():
        depart = Department()
        depart.title = form.title.data
        depart.chief = form.chief.data
        depart.members = form.members.data
        depart.email = form.email.data

        session = db_session.create_session()
        session.add(depart)
        session.commit()

        return redirect('departments')
    return render_template('add_department.html', title='Добавление департамента', form=form)


@app.route('/сhange_depart/<int:department_id>', methods=['GET', 'POST'])
@login_required
def сhange_department(department_id):
    form = DepartmentForm()
    form.submit.label.text = 'Изменить данные'
    if request.method == "GET":
        session = db_session.create_session()
        depart = session.query(Department).filter(Department.id == department_id).first()
        form.title.data = depart.title
        form.chief.data = depart.chief
        form.members.data = depart.members
        form.email.data = depart.email

    if form.validate_on_submit():
        session = db_session.create_session()
        depart = session.query(Department).filter(Department.id == department_id).first()
        if current_user.id == 1 or depart.chief == current_user.id and depart:
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            session.add(depart)
            session.commit()
            return redirect('departments')
        else:
            return render_template('add_department.html', title='Редактирование департамента',
                                   form=form, message="У Вас нет на это прав!")
    return render_template('add_department.html', title='Редактирование департамента', form=form)


@app.route('/delete_depart/<int:department_id>', methods=['GET', 'POST'])
@login_required
def delete_depart(department_id):
    session = db_session.create_session()
    depart = session.query(Department).filter(Department.id == department_id).first()
    if current_user.id == 1 or depart.chief == current_user.id:
        session.delete(depart)
        session.commit()
    return redirect('departments')


def main():
    db_session.global_init("db/users.sqlite")
    app.run(port=7981, host='127.0.0.1')


if __name__ == '__main__':
    main()
