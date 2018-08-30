# first.py

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm 
from datetime import datetime
app = Flask(__name__)



app.config['SECRET_KEY'] = 'f18967deeee433fb67a0d6f7422067d7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
#Models
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self):

        return "User(%s,%s,%s)" % (self.username,self.email,self.image_file)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post(%s,%s,%s)" % (self.title,self.date_posted,self.content)

# # Queries
# from flaskblog import db
# db.create_all()

# from flaskblog import User, Post
# user_1 = User(username='Divesh',email='divesh@gmail.com',password='password')
# user_2 = User(username='Sandeep',email='Sandeep@gmail.com',password='password')
# db.session.add(user_1)
# db.session.add(user_2)
# db.session.commit()

# post_1 = Post(title='Blog 1', content='First Post Comment!', user_id=user_1.id)
# post_2 = Post(title='Blog 2', content='Second Post Comment!', user_id=user_1.id)
# db.session.add(post_1,post_2)
# db.session.commit()

# post_1.date_posted

# post = Post.query.first()
# posts = Post.query.all()
# post.author

# User.query.filter_by(username='Divesh').first()
# User.query.filter_by(username='Divesh').all()
# User.query.get(1) # get first row



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

@app.route('/')
def hello_world():
    return "Hello World"

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

if __name__ == "__main__":
    app.debug = True
    app.run()

