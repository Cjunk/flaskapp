from flask import Flask,render_template,request,make_response
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

@app.route('/')
def index():
    user = request.cookies.get(COOKIELABEL[0]) # Look for previous cookie  
    #currentuserID = int(request.cookies.get(COOKIELABEL[1])) # Look for previous cookie 
    opt_param = request.args.get("status")
    print(opt_param)
    sess=STATUSS[1]
    if opt_param is None:
        if not user: # If there is no previous cookie then make user = ''
            user = ""
            sess=STATUSS[0]
        else:
            currentuserID = int(request.cookies.get(COOKIELABEL[1])) # Look for previous cookie
            portfolios = getportfolio(currentuserID)
            resp = make_response(render_template(homepage,user=user,SESSION_STATUS=sess,portfolios=portfolios))
            return resp
    else:
        resp = make_response(render_template(homepage,user = '',SESSION_STATUS=STATUSS[0]))         
        deletecookies(resp,COOKIELABEL)
        return resp    
    return render_template(homepage,user=user,SESSION_STATUS=sess)

@app.route('/', methods = ['POST'])
def addnewuser():  # Registering a new user
    #   Gather the paramaters
    nickname = request.form['nick_name']
    fname = request.form['fname']
    lname = request.form['lname']
    password =request.form['pword']
    resp = make_response(render_template(homepage,user='',SESSION_STATUS=STATUSS[0]))
    userid = registernewuser(nickname,fname,lname,password)  # returns 1 if registing new user successfull
    if userid>0:
        resp = make_response(render_template(homepage,user=nickname,SESSION_STATUS=STATUSS[1])) 
        paramsList = []
        paramsList.append(nickname)
        paramsList.append(userid)
        addcookies(resp,COOKIELABEL,paramsList) 
    else: # returns 0 :  New user was not registered successfully.
        #TODO alert user when the user was not registered.
        pass  
    return resp

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('uname')
        password = hashlib.sha256(str(request.values.get('pword')).encode('utf-8')).hexdigest()
        userid = loginuser(username,password)
        if(userid>0):
           
            portfolios = getportfolio(userid)   # Gets all the row data for each portfolio
            print("PORTFOLIOS",portfolios)            
            resp = make_response(render_template(homepage,user=username,SESSION_STATUS=STATUSS[1],portfolios=portfolios)) 
            paramsList = []
            paramsList.append(username)
            paramsList.append(str(userid))
            addcookies(resp,COOKIELABEL,paramsList)            
            return resp
        else: #user not in database
            return render_template(homepage,user='',SESSION_STATUS=STATUSS[0])
    else: # method is GET
        return render_template("login.html")
    pass
if __name__ == '__main__':
    app.run(debug=True)