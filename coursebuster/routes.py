from flask import render_template, flash, redirect, url_for, session, \
    logging, request
from coursebuster import app, db
from coursebuster.models import Course, User
from coursebuster.forms import AddCourseForm, RegistrationForm, LoginForm, \
    UpdateAccountForm
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash = pbkdf2_sha256.hash(form.password.data)
        user = User(
            username=form.username.data, email=form.email.data, password=hash)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            flash('You have successfully logged in!')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Login information did not match!')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!')
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(request.form)
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'account.html', title='Account', image_file=image_file, form=form)

