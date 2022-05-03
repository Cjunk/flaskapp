from flask import Flask,render_template,request,make_response,session,redirect
from cryptoFlaskFunctions import *
import os,hashlib
from coinspot import CoinSpot
COOKIELABEL=['userID','customerNumber']
homepage= 'home.html'
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
STATUSS = ["not logged in","logged in"]
SESSION_STATUS = STATUSS[0]
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#   ----------------------------------------------------------------------------------------------------------------------------------------
sha = hashlib.sha256()  # Do not delete this line as I feel it maybe used to 'randomize' sha256
cryptoApi = CoinSpot("df",SECRET_KEY)       #
response = cryptoApi.latestPrice("xrp")     #   These can be deleted, just used to ensure the coinspot class is working and communicating
print(">>>>>>>>>>>>>>>>>>>>> ",response)    #

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def getportfoliodetail(portid,userid):
    print(session['portfolios'])  
    # TODO determine Return data   
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
            # try:
            #     print("The user name = ", username,userid,session['portfolios'][session['showportfolio']])  
            # except:
            #     pass
            # get the portfolio detail  
            #portfolioDetails = getportfolioDetail(session['showportfolio'],userid)  
            #print(portfolioDetails)
        else: #user does not exist or incorrect password or incorrect login
            pass
        return redirect("/")

def getcryptovalue():
    pass

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nick_name'] = request.form['nick_name'] 
        session['first_name'] = request.form['fname'] 
        session['last_name'] = request.form['lname'] 
        session['password'] = request.form['pword']
    else:
        if session.get("userid") :
            #print("Home page no params, however user already logged in")
            try:
                print("session['portfolios'][0]",session['portfolios'][0])  # print the console the session stored portfolio detail
            except:
                pass
            portfolioDetail = getportfolioDetail(1,session['userid'])
            response = []
            totalcosts = []
            for each in portfolioDetail:
                response.append(float(cryptoApi.latestPrice(each[1])) * float(each[3]))
                totalcosts.append(each[2] * each[3])
            totalcosts.append(sum(totalcosts))
            response.append(sum(response))
            # Generate the current crypto values from coinspot
            return render_template(homepage,portfoliodetail=portfolioDetail,response=response,totalcosts=totalcosts)
        else:
            #print("Home page no params, however no user")
            return render_template(homepage,portfoliodetail="None")
    return render_template(homepage,portfoliodetail=getportfolioDetail(1,2))

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def registerLand():
    return redirect("home.html")

@app.route("/showportfolio", methods=['GET'])
def showportfolio():
    portid = request.args.get('portid')
    portfolioDetail=getportfolioDetail(int(portid),session['userid'])
    response = []
    totalcosts = []    
    if(portfolioDetail):

        for each in portfolioDetail:
            response.append(float(cryptoApi.latestPrice(each[1])) * float(each[3]))
            totalcosts.append(each[2] * each[3])
        totalcosts.append(sum(totalcosts))
        response.append(sum(response))
    resp = render_template("home.html",portfoliodetail=portfolioDetail,response=response,totalcosts=totalcosts)
    return resp
if __name__ == '__main__':
    app.run(debug=True)