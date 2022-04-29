import hashlib,psycopg2,os,json
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
def deletecookies(r,c):
    # This funcion will delete all the cookies passed to it
    # USAGE deletecookies(the response,[An array of cookie labels]])
    for each in c:
        r.delete_cookie(each)
    return
def addcookies(r,c,l):
    count = 0
    for each in c:
        print("ffffffffffffffffffffffffffffffffffff",each,count,l)
        r.set_cookie(each,l[count])
        count = count + 1
    return
def getuserID (username):
        username = username.upper()
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        postgres_insert_query = """SELECT id FROM users WHERE UPPER(nickname) Like '%s'""" %(username)
        cur.execute(postgres_insert_query)
        cur.close()
        conn.close()
def registernewuser(nickname,firstname,lastname,password):
    # This function adds a new user to the crypto user database
    # TODO Check if the user exists already prior to adding
    # TODO if the user does exist already alert the user
    nickname = nickname.upper()
    firstname = firstname.upper()
    lastname = lastname.upper()
    
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    try:
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        postgres_insert_query = """INSERT INTO users (nickname, fname, lname, hashed_password) VALUES (%s,%s,%s,%s)"""
        values_to_insert = [nickname,firstname,lastname,password]  
        cur.execute(postgres_insert_query,values_to_insert)
        conn.commit()
        userid = getuserID(nickname,password)  
        cur.close()
        conn.close()  
        return 1
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into users table", error)
        return 0
        
def loginuser(username,hashedpassword):
    #   Will check the database for valid hash and return the user ID otherwise will return 0 for not found
        conn=psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        retval = 0
        print(hashedpassword)
        username = str(username).upper()
        postgres_insert_query = """SELECT hashed_password,id FROM users WHERE UPPER(nickname) Like '%s'""" %(username)
        cur.execute(postgres_insert_query)
        rows = cur.fetchone()
        print("HASHED PASSWORD ##",rows[0])
        if cur.rowcount > 0:
            print("------------------------------ cur.rowcount > 0 ---------------------------")
            usershashedPassword = rows[0] # retrieve the first result
            print("---------------Users hashed password",usershashedPassword)
            if usershashedPassword:
                if usershashedPassword == hashedpassword:# successfull login
                    #print("CORRECT PASSWORD ENTERED")
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", username,rows,cur.rowcount,cur.fetchall())
                    retval = rows[1] # get the user id
                else:
                    #print("INCORRECT PASSWORD")
                    pass
            else:   # If the user doesnt exist
                print("User doesnt exist")
        cur.close()
        conn.close()    
        return retval
def getportfolio(userid): # Gets the porftolio from the dataabase for the user
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()  
    postgres_insert_query = """SELECT * FROM portfolios WHERE customer_owner = %s""" %(userid)    
    cur.execute(postgres_insert_query)
    print("search for portfolios")
    if cur.rowcount > 0:
        results = cur.fetchall()
    else:
        results = None
    cur.close()
    conn.close() 
    return results
def getuserid_byusername(username):
    conn=psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    postgres_insert_query = """SELECT id FROM users WHERE customer_owner = %s""" %(username)    
    cur.execute(postgres_insert_query) 
    cur.close()
    conn.close() 
