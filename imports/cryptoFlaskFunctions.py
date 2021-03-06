import os,psycopg2,hashlib
from flask import session
#   -------------------------------------------- CONSTANTS ---------------------------------------------------------------
OFF = False
ON = True
MASTER_DEBUG = OFF
BUY = 1
SELL = 2
if MASTER_DEBUG:
    SQL_DEBUG = OFF
    API_DEBUG = OFF
    REGISTER_NEW_USER = ON
else:
    SQL_DEBUG = OFF
    API_DEBUG = OFF
    REGISTER_NEW_USER = OFF
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
STARTING_CASH = 50000
#   ----------------------------------------------------------------------------------------------------------------------
def buycoin(coin,price,qty):
    #   TODO Update the transaction history table with the transaction
    if SQL_DEBUG:
        print("This is the coin",coin,"PORTFOLIO ID =",session['portfolioID'])
        print("THE AMOUNT PASSED IS = ",price)
        print("THE QTY PASSED IS = ",qty)
    else:
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()   
        cost = float(price) * float(qty)     
        postgres_insert_query = """INSERT INTO portfolio_detail (porfolio_id, coin, cost, quantity) VALUES (%s,%s,%s,%s)"""
        values_to_insert = [int(session['portfolioID']),coin.upper(),price,qty]  
        cur.execute(postgres_insert_query,values_to_insert)
        postgres_insert_query = """UPDATE portfolios SET current_balance = current_balance - %d WHERE id = %d""" %(float(cost),int(session['portfolioID']))
        cur.execute(postgres_insert_query)
        conn.commit()        
        cur.close()
        conn.close()
        addTransaction(coin.upper(),int(session['portfolioID']),BUY,qty,price)
def sellrow(rowId,amount):
    #   TODO Update the transaction history table with the transaction
    if SQL_DEBUG:
        print("This is the row id",rowId,"PORTFOLIO ID =",session['portfolioID'])
        print("THE AMOUNT PASSED IS = ",amount)
    else:
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()        
        postgres_insert_query = """DELETE FROM portfolio_detail WHERE id = %d""" %(int(rowId))
        cur.execute(postgres_insert_query)
        postgres_insert_query = """UPDATE portfolios SET current_balance = current_balance + %d WHERE id = %d""" %(float(amount),int(session['portfolioID']))
        cur.execute(postgres_insert_query)
        conn.commit()        
        cur.close()
        conn.close()
        addTransaction(rowId,int(session['portfolioID']),SELL,amount,int(rowId))
def getuserID (username):
    #   Used to retrieve the user id when registering a new user
        username = username.upper()
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        postgres_insert_query = """SELECT id FROM users WHERE UPPER(nickname) Like '%s'""" %(username)
        cur.execute(postgres_insert_query)
        id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return id
def registernewuser(nickname,firstname,lastname,password):
    # This function adds a new user to the crypto user database
    # TODO Check if the user exists already prior to adding
    # TODO if the user does exist already alert the user
    nickname = nickname.upper()
    firstname = firstname.upper()
    lastname = lastname.upper()
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    print("REGISTERING THE NEW USER INTO THE DATABASE")
    try:
        if REGISTER_NEW_USER:
            userid = 1  # Dummy user id.
            print("registernewuser() is set to DEBUG MODE: No updates to the database for the new user")
        else:
            conn=psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()            
            postgres_insert_query = """INSERT INTO users (nickname, fname, lname, hashed_password) VALUES (%s,%s,%s,%s)"""
            values_to_insert = [nickname,firstname,lastname,password]  
            cur.execute(postgres_insert_query,values_to_insert)
            conn.commit()
            userid = getuserID(nickname)  
        # Create the portfolio for this newly registered user
            try:
                postgres_insert_query = """INSERT INTO portfolios (customer_owner, title, starting_cash, current_balance) VALUES (%s,%s,%s,%s)"""
                values_to_insert = [userid,'default portfolio name',STARTING_CASH,STARTING_CASH]  
                cur.execute(postgres_insert_query,values_to_insert)
                conn.commit()
            except: # Failed to insert into datbase
                print("The new portfolio did not go in the database")
                pass
            cur.close()
            conn.close()  
        return userid
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into users table", error)
        return 0     
def loginuser(username,hashedpassword):
    #   Will check the database for valid hash and return the user ID otherwise will return 0 for not found
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        retval = 0
        username = str(username).upper()
        postgres_insert_query = """SELECT hashed_password,id FROM users WHERE UPPER(nickname) = %s"""
        values_to_insert = [username.upper()] 
        cur.execute(postgres_insert_query,values_to_insert)  # causing crash on HEROKU
        rows = cur.fetchone()
        if cur.rowcount > 0:
            usershashedPassword = rows[0] # retrieve the first result
            if usershashedPassword:
                if usershashedPassword == hashedpassword:# successfull login
                    retval = rows[1] # get the user id
                else:
                    pass
            else:   # If the user doesnt exist
                print("User doesnt exist")
                pass
        cur.close()
        conn.close()    
        return retval
def getportfolio(userid): # Gets the porftolios summary from the database for the user
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()  
    postgres_insert_query = """SELECT * FROM portfolios WHERE customer_owner = %s""" %(userid)    
    cur.execute(postgres_insert_query)
    if cur.rowcount > 0:
        results = cur.fetchall()
    else:
        results = None
    cur.close()
    conn.close() 
    return results
def getportfolioDetail(portid):
    # retrieves all the detail for a single portfolio from the database
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    postgres_insert_query = """SELECT * FROM portfolio_detail WHERE porfolio_id = %s ORDER BY coin""" %(portid)    
    cur.execute(postgres_insert_query)
    if cur.rowcount > 0:
        results = cur.fetchall()
    else:
        results = None
    cur.close()
    conn.close() 
    return results
def get_portfolioID_fromuserID(userid):
    # SELECT * FROM portfolios WHERE customer_owner = 1;
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    postgres_insert_query = """SELECT id FROM portfolios WHERE customer_owner = %d""" %(userid)    
    cur.execute(postgres_insert_query)
    if cur.rowcount > 0:
        results = cur.fetchone()[0] # Get the first one. TODO Change this if multiple portfolios allowed
    else:
        results = None
    cur.close()
    conn.close()
    return results
def addTransaction(coin,portfolio_id,transaction_type,quantity,price):
    # function to log a transaction in the transaction table
    if SQL_DEBUG:
        print("THE DETAILS PASSED = ",coin,portfolio_id,transaction_type,quantity,price)
    else:
        print("THE DETAILS PASSED = ",coin,portfolio_id,transaction_type,quantity,price)
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()        
        postgres_insert_query = """INSERT INTO transaction_history (coin, portfolio_id, tran_type, quantity, price) VALUES (%s,%s,%s,%s,%s)"""
        values_to_insert = [portfolio_id,int(session['portfolioID']),int(transaction_type),float(quantity),float(price)]  
        cur.execute(postgres_insert_query,values_to_insert)
        conn.commit()        
        cur.close()
        conn.close()
def getTransactionHistory():
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    retval = 0
    postgres_insert_query = """SELECT * FROM transaction_history WHERE portfolio_id = %s"""
    values_to_insert = [session['portfolioID']] 
    cur.execute(postgres_insert_query,values_to_insert)  # causing crash on HEROKU
    rows = cur.fetchall()
    if cur.rowcount > 0:
        retval = rows
    else:
        retval = 0
    cur.close()
    conn.close() 
    return retval