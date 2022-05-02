from flask import Flask,render_template,request,make_response,session,redirect
import requests
from cryptoFlaskFunctions import *
import os,psycopg2,bcrypt,json
from coinspot import CoinSpot
COOKIELABEL=['userID','customerNumber']
homepage= 'home.html'
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
STATUSS = ["not logged in","logged in"]
SESSION_STATUS = STATUSS[0]
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
sha = hashlib.sha256()
cryptoApi = CoinSpot("df",SECRET_KEY)
response = cryptoApi.latestPrice("xrp")
print(">>>>>>>>>>>>>>>>>>>>> ",response)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def getportfoliodetail(portid,userid):
    print(session['portfolios'])    
    pass

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # Check if the user exists.
        # if the user exists setup the session
        username = request.values.get('uname')
        password = hashlib.sha256(str(request.values.get('pword')).encode('utf-8')).hexdigest()
        userid = loginuser(username,password)  
        if(userid>0): #  user and password correct so log them in One time action
            session['userid'] = userid
            session['nick_name'] = username
            session['portfolios'] = getportfolio(userid) #Add the porfolio summary to the session
            session['showportfolio'] = 1 # variable to decide if we are displaying a portfolio or not
            #get the porfolio detail and pass through to the render_template.
            try:
                print("The user name = ", username,userid,session['portfolios'][session['showportfolio']])  
            except:
                pass
            # get the portfolio detail  
            portfolioDetails = getportfolioDetail(session['showportfolio'],userid)  
            print(portfolioDetails)
        else: #user does not exist or incorrect password or incorrect login
            pass
        return redirect("/")


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nick_name'] = request.form['nick_name'] 
        session['first_name'] = request.form['fname'] 
        session['last_name'] = request.form['lname'] 
        session['password'] = request.form['pword']
    else:
        if session.get("userid") :
            print("Home page no params, however user already logged in")
            try:
                print(session['portfolios'][0])
            except:
                pass
            print(getportfolioDetail(1,session['userid']))
            return render_template(homepage,portfoliodetail=getportfolioDetail(1,session['userid']))
        else:
            print("Home page no params, however no user")
            return render_template(homepage,portfoliodetail="None")
        pass
    return render_template(homepage,portfoliodetail=getportfolioDetail(1,2))

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def registerLand():
    return redirect("home.html")

@app.route("/showportfolio", methods=['GET'])
def showportfolio():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)