import os
homepage= 'home.html'
COOKIELABEL=['userID','customerNumber']
DATABASE_URL = os.environ.get('DATABASE_URL','dbname=cryptodb') # dbname is the name of the local database
SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')
STATUSS = ["not logged in","logged in"]
SESSION_STATUS = STATUSS[0]
# PORTFOLIO DETAILS
PORTFOLIO_DETAIL_ID = 0
PORTFOLIO_DETAIL_PARENT_PORTFOLIO = 1
PORTFOLIO_DETAIL_COIN = 2
PORTFOLIO_DETAIL_PRICE = 3
PORTFOLIO_DETAIL_QTY = 4
