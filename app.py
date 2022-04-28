from flask import Flask
import os

DATABASE_URL = os.environ.get('DATABASE_URL','dbname=project2db') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')

app = Flask(__name__)
app.config['SECRET_KEY']= SECRET_KEY

@app.route('/')
def index():
    return "Hello, World"

if __name__ == '__main__':
    app.run(debug=True)