from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect

from flaskblog.forms import RegistrationForm, LoginForm 

from flaskblog import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account Created Sucessfully','success')
        return redirect(url_for('home'))

    return render_template('register.html', title = 'Registration', form=form )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been sucessfully Loged In','success')
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful, Please check Username and Password', 'danger')

    return render_template('login.html', title = 'Login', form=form )