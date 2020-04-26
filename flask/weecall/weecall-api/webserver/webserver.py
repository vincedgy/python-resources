import os
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

@app.route('/home')
def get_home():
    return render_template('welcome.html', posts=posts)


@app.route('/about')
def get_about():
    return render_template('about.html')


@app.route('/')
def default():
    return redirect("/home", code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 888))
    app.run(host='0.0.0.0', port=port, debug=True)