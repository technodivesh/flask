from datetime import datetime
from flaskblog import db
from flaskblog import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Models
class User(db.Model, UserMixin):
    
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

