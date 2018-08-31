from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request

from flaskblog.forms import RegistrationForm, LoginForm 

from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

posts = [

    {
        'author':'Divesh Chandolia',
        'title': 'Blog1',
        'content':'post content 1',
        'date_posted':'28-08-2018'
    },
    {
        'author':'Sandeep Sharma',
        'title': 'Blog 2',
        'content':'post content 2',
        'date_posted':'29-08-2018'
    }


]

def hello_world():
    return "Hello World"


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title = 'Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # encript the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Account Created Sucessfully','success')
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Registration', form=form )

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('home'))

        flash('Login Unsuccessful, Please check Username and Password', 'danger')

    return render_template('login.html', title = 'Login', form=form )

@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():

    return render_template('account.html', title='Account')