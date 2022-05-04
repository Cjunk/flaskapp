from flask import Flask,render_template,request,make_response,session,redirect
from cryptoFlaskFunctions import *
from coinspot import CoinSpot
from theConstants import *
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#   ----------------------------------------------------------------------------------------------------------------------------------------
sha = hashlib.sha256()  # Do not delete this line as I feel it maybe used to 'randomize' sha256
cryptoApi = CoinSpot("df",SECRET_KEY)       #
#response = cryptoApi.latestPrice("xrp")     #   These can be deleted, just used to ensure the coinspot class is working and communicating
#print(">>>>>>>>>>>>>>>>>>>>> ",response)    #
#print("USER ID = ",getuserid_from_portfolioID(2)[0])
#print("Portfolio id = " ,get_portfolioID_fromuserID(1))


def getallprices():
    currentpricelist = {}
    allprices = cryptoApi.latestsall().json()
    for each in allprices['prices']:
        currentpricelist[each]=allprices['prices'][each]['bid']
    return currentpricelist
    
getallprices()
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
        return redirect("/")
        if(userid>0): #  user and password correct so log them in One time action
            session['userid'] = userid
            session['portfolioID']= get_portfolioID_fromuserID(userid) # ASSUMPTION of only one portfolio per person TODO Change this to accomodate multiple portfolios
            session['nick_name'] = username
            session['portfolios'] = getportfolio(userid) #Add the porfolio summary to the session
            session['showportfolio'] = 1 # variable to decide if we are displaying a portfolio or not
        else: #user does not exist or incorrect password or incorrect login
            pass
        return redirect("/")

def getcryptovalue():
    pass
@app.route('/buy',methods=['GET'])
def buy():
    coin=request.args.get('coin').split(',')[0]
    price=request.args.get('coin').split(',')[1]
    qty=request.args.get('qty')
    buycoin(coin,price,qty)
    return redirect("/")

@app.route('/sell',methods=['GET'])
def sell():
    rowid=request.args.get('rowId')
    amount=request.args.get('amount')
    sellrow(rowid,amount)
    session['portfolios'] = getportfolio(session['portfolioID']) #Add the porfolio summary to the session
    return redirect("/")


@app.route('/',methods=['GET', 'POST'])
def index():
    currentpricelist = getallprices()       # update from coinpot the latest prices. passed to the html
    print("THE SESSION VALUE = ",session)
    if request.method == 'POST':
        session['nick_name'] = request.form['nick_name'] 
        session['first_name'] = request.form['fname'] 
        session['last_name'] = request.form['lname'] 
        session['password'] = request.form['pword']
    else:
        if session.get("userid") :
            portfolioDetail = getportfolioDetail(session['portfolioID'],session['userid'])
            session['portfolios'] = getportfolio(session['portfolioID']) #Add the porfolio summary to the session
            print("PORFOLIO ID: route('/')  index() Line 72 : ",portfolioDetail)
            response = []
            totalcosts = []
            if(portfolioDetail):
                for each in portfolioDetail:
                    response.append(float(cryptoApi.latestPrice(each[2])) * float(each[PORTFOLIO_DETAIL_QTY]))
                    totalcosts.append(each[PORTFOLIO_DETAIL_PRICE] * each[PORTFOLIO_DETAIL_QTY])
                totalcosts.append(sum(totalcosts))
                response.append(sum(response))
            return render_template(homepage,portfoliodetail=portfolioDetail,response=response,totalcosts=totalcosts,currentpricelist=currentpricelist)
        else:
            #print("Home page no params, however no user")
            return render_template(homepage,portfoliodetail="None")
    return render_template(homepage,portfoliodetail=getportfolioDetail(1,2))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        return redirect("home.html")


# Not used in project. This is where the user can have mutliple portfolios
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