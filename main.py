from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from Forms.job_form import AddJobForm
from Forms.login_form import LoginForm
from Forms.register_form import RegisterForm
from data import db_session
from data.jobs import Jobs
from data.users import User

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
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.team_leader = form.team_leader.data

        session = db_session.create_session()
        session.add(job)
        session.commit()

        return redirect('')
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/information.sqlite")
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


@app.route('/')
def jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    return render_template('jobs.html', jobs=jobs, users=users, title='Главная')


def main():
    db_session.global_init("db/users.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
