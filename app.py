from flask import Flask,render_template,request,make_response,session,redirect
from imports.cryptoFlaskFunctions import *
from imports.coinspot import CoinSpot
from imports.theConstants import *
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#   ----------------------------------------------------------------------------------------------------------------------------------------
# sha = hashlib.sha256()  # Do not delete this line as I feel it maybe used to 'randomize' sha256
cryptoApi = CoinSpot("df",SECRET_KEY)   
def getallprices():
    #   Function to gather all available coin prices from the API
    currentpricelist = {}
    allprices = cryptoApi.latestsall().json()
    for each in allprices['prices']:    #   Filter the list by removing redunant data
        currentpricelist[each]=allprices['prices'][each]['bid']
    return currentpricelist
     
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

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
            session['portfolioID']= get_portfolioID_fromuserID(userid) # ASSUMPTION of only one portfolio per person TODO Change this to accomodate multiple portfolios
            session['nick_name'] = username
            session['portfolios'] = getportfolio(userid) #Add the porfolio summary to the session
            session['showportfolio'] = 1 # variable to decide if we are displaying a portfolio or not
        else: #user does not exist or incorrect password or incorrect login
            pass # TODO Create an alert etc to advise the user that the user doesnt exist
        return redirect("/")

@app.route('/buy',methods=['GET'])
def buy():
    coin=request.args.get('coin').split(',')[0]     #   Get the COIN 
    price=request.args.get('coin').split(',')[1]    #   Get the coin price
    qty=request.args.get('qty')
    buycoin(coin,price,qty)
    session['portfolios'] = getportfolio(session['portfolioID']) #Add the porfolio summary to the session
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
    if request.method == 'POST':    #   Path taken when registering
        session['nick_name'] = request.form['nick_name'] 
        session['first_name'] = request.form['fname'] 
        session['last_name'] = request.form['lname'] 
        session['password'] = request.form['pword']
    else:
        if session.get("userid") :
            portfolioDetail = getportfolioDetail(session['portfolioID'],session['userid'])
            session['portfolios'] = getportfolio(session['portfolioID']) #Add the porfolio summary to the session
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
            return render_template(homepage,portfoliodetail="None")
    return render_template(homepage,portfoliodetail=getportfolioDetail(1,2))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        return redirect(homepage)

if __name__ == '__main__':
    app.run(debug=True)