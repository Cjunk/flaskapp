from flask import Flask,render_template
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')

app = Flask(__name__)
app.config['SECRET_KEY']= SECRET_KEY

@app.route('/')
def index():
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute ('SELECT 1',[])
    conn.close()
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)