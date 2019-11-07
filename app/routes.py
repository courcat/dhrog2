from flask import render_template, url_for, flash, redirect, request
from app import app,db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/form', methods=['GET', 'POST'])
# def hash():
#     form = HashForm()
#     if form.validate_on_submit():
#         flash('Getting diff from builds {} to {}'.format(
#             form.base_hash.data, form.target_hash.data))
#         return redirect(url_for('submitted'))
#     return render_template('hash.html', title='L10n Diff Process', form=form)

# @app.route('/submitted')
# def submitted():
#     return render_template('submitted.html', title='submitted')

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if the user navigates to the login page
    #current user is the one who made the request
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #if the user was redirected here, send them back to the page
        # they came from
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User successfuly registered")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/test', methods=["POST"])
def test():
    with open("app/templates/test.json","r") as f:
        file = f.read()
    return file, 400