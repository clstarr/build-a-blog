from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    new_blog = db.Column(db.String(750))
    completed = db.Column(db.Boolean)
    
    def __init__(self, title, new_blog):
        self.title = title
        self.new_blog = new_blog
        self.completed = False

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog-listings.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('add-post.html')

    title_error = ""
    new_blog_error = ""

    if request.method == 'POST':
        title = request.form['title']
        new_blog = request.form['new_blog']

    if not title:
        title_error = "Please enter a valid title"

    if not new_blog:
        new_blog_error = "Please enter a valid blog entry"

    if not title_error and not new_blog_error:
        blog = Blog(title, new_blog)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))

    return render_template('add-post.html', title_err=title_error, new_blog_err=new_blog_error)

@app.route('/blog', methods=['GET'])
def blog_listings():

    if request.args:
        id = request.args.get("id")
        blog = Blog.query.get(id)
        return render_template('blog-post.html', title="Build a blog", blog=blog)
    else:
        blogs = Blog.query.all()
        
        return render_template('blog-listings.html', blogs=blogs)

if __name__ == '__main__':
    app.run()