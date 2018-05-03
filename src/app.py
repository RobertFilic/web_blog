from src.common.database import Database
from src.models import user
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

__author__ = 'robee'

from flask import Flask, render_template, request, session, make_response

# initiate the app
app = Flask(__name__)  # '__name__' containes '__main__'
app.secret_key = "jose"


# define an endpoint
@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')  # endpoint is www.mywebsite.com/api/
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialze()

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email'] # Flast asks to obtain 'email' data from front-end
    password = request.form['password']

    # validate if user is registered
    if User.login_valid(email, password):
        User.login(email) # return session

    else:
        session['email'] = None # if user is not valid enter empty session

    return render_template("profile.html", email=session['email'])# passing the email variable in the template, so it knows which session is


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password) # it sets the session as well, so no need to do it again here

    return render_template("profile.html", email=session['email'])

# DISPLAYING ALL BLOG POSTS FROM THE AUTHOR
@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id) # find the user with submitted id
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs() # get user's blogs

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_post()
    print(posts)

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog_id)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('/new_blog.html')
    else:
        title = request.form['title']
        print(title)
        description = request.form['description']
        print(description)
        user = User.get_by_email(session['email'])
        print(user)

        new_blog = Blog(user.email, title, description, user._id)
        print(new_blog)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('/new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

# Requirement to run the app:
if __name__ == '__main__':
    app.run(port=4996) # we can change the port by entering exmp: port=4995

