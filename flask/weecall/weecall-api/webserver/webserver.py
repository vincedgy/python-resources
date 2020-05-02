import os
import datetime
from flask import Flask, redirect, render_template
import colorama
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

posts = [
    {
        'author': 'Vincent',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': '2020/04/27'
    },
    {
        'author': 'Jeanne',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': '2020/04/30'
    }
]

current_datetime = datetime.datetime.now()

def render(template, **kwargs):
    kwargs['current_year']=current_datetime.year
    return render_template(template, **kwargs)

@app.route('/welcome')
def get_welcome():
    return render('welcome.html')

@app.route('/posts')
def get_posts():
    return render('posts.html', posts=posts, title="Posts")


@app.route('/about')
def get_about():
    return render('about.html', title="About")


@app.route('/')
def default():
    return redirect("/welcome", code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 888))
    app.run(host='0.0.0.0', port=port, debug=True)