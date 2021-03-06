from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm

from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

import os
from PIL import Image

# posts = [

#     {
#         'author':'Divesh Chandolia',
#         'title': 'Blog1',
#         'content':'post content 1',
#         'date_posted':'28-08-2018'
#     },
#     {
#         'author':'Sandeep Sharma',
#         'title': 'Blog 2',
#         'content':'post content 2',
#         'date_posted':'29-08-2018'
#     }


# ]

def hello_world():
    return "Hello World"


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
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


def save_picture(form_picture):
    randon_hex = os.urandom(8).encode('hex')
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = randon_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # resize before saving
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)


    return picture_fn


@app.route('/account', methods=['GET', 'POST'] )
@login_required
def account():

    form = UpdateAccountForm()

    # if POST
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # update db
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file )
    return render_template('account.html', title='Account', image_file=image_file, form=form )

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():

        post = Post(title=form.title.data, content = form.content.data, author=current_user  )
        db.session.add(post)
        db.session.commit()

        flash('Posted Successfully','success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form , legend='Create Post')


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post )    


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()
        flash('Your post has been updated','success')
        return redirect(url_for('post',post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title=post.title, form=form, legend = 'Update Post' )   

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted','success')
    return redirect(url_for('home'))