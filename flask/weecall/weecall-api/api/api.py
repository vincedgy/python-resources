import os
from flask import Flask, redirect
import colorama
from flask_cors import CORS
from services import list_s3_buckets, list_versions

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/about')
@app.route('/api/home')
@app.route('/api')
def get_greetings():
    return {
        'message': "Welcome to my REST Flask API",
        'versions': get_version()
    }


@app.route('/')
def default():
    return redirect("/api", code=302)


@app.route('/api/versions')
def get_version():
    return {'versions': list_versions()}


@app.route('/api/buckets')
def get_buckets():
    return {"data": list_s3_buckets()}


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)