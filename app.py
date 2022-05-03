from flask import Flask,render_template,request,make_response,session,redirect
from cryptoFlaskFunctions import *
import os
from coinspot import CoinSpot
from theConstants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#   ----------------------------------------------------------------------------------------------------------------------------------------
sha = hashlib.sha256()  # Do not delete this line as I feel it maybe used to 'randomize' sha256
cryptoApi = CoinSpot("df",SECRET_KEY)       #
#response = cryptoApi.latestPrice("xrp")     #   These can be deleted, just used to ensure the coinspot class is working and communicating
#print(">>>>>>>>>>>>>>>>>>>>> ",response)    #

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
@app.route('/sell',methods=['GET'])
def sell():
    rowid=request.args.get('rowId')
    sellrow(rowid)
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
            #print("Home page no params, however user already logged in")
            portfolioDetail = getportfolioDetail(1,session['userid'])
            print(portfolioDetail)
            response = []
            totalcosts = []
            for each in portfolioDetail:
                response.append(float(cryptoApi.latestPrice(each[2])) * float(each[PORTFOLIO_DETAIL_QTY]))
                totalcosts.append(each[PORTFOLIO_DETAIL_PRICE] * each[PORTFOLIO_DETAIL_QTY])
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
            response.append(float(cryptoApi.latestPrice(each[2])) * float(each[4]))
            totalcosts.append(each[3] * each[4])
        totalcosts.append(sum(totalcosts))
        response.append(sum(response))
    resp = render_template("home.html",portfoliodetail=portfolioDetail,response=response,totalcosts=totalcosts)
    return resp
if __name__ == '__main__':
    app.run(debug=True)