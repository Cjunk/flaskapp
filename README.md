# **CRYPTO PORTFOLIO TRACKER** #
##### Designed, created and written by Jericho Sharman 



#### link [Crypto Portfolio Tracker](https://pure-stream-33801.herokuapp.com/)  
#### [Email]<jsharman@hotmail.com.au>  
#### Buy me a coffee <https://www.buymeacoffee.com/jerichosharman>
---

## Summary ##
An online crypto currency portfolio tracker with live coin price data.

---
## Instructions ##
Create and monitor your portfolio online with this fake money crypto portfolio tracker. 

Consolodate your holdings into one portfolio to provide a full oversite. Your holdings will be 
tracked against real live prices. A running transaction/order history will also be kept to prived
you with historical data.

1. Register a new account or Login  
2. Start buying crypto currency  

---
## Use Cases ##

- Mirror your real crypto holdings consolodated into the single portfolio  
- For practising your trading skills in a safe environment   
- Fun Fun Fun !!!
---
## Technical Details ##
| Package | version | Use | comment | version |  |
| :---: | :---: | :---: | :---: | :---: | :---: |
| postgres | 301 | SQL | Local database | 301 | 283 |
| gunicorn | 301 | Heroku | heroku | 301 | 283 |
| psycopg2 | 2.9.3 | Python | SQL conns | 301 | 283 |
| requests | 2.27.1 | HTTP | Internet/ APIs | 301 | 283 |
| python | 301 | Logic | code | 301 | 283 |
| flask | 1.1.1 | Html Server | Djangi | 1.1.1 | 283 |
| JSON |  | API Access | flask | 1.1.1 | 283 |

push the postgresql database to Heroku
```bash
heroku pg:reset 
heroku pg:push local_cryptodb DATABASE_URL’
```
## Available Functionality ##
- Session control
    - Register new user
    - Login
- postgresql
    - Users table: 
    - Portfolios table: Starting balance $50,000   ***No option to change***   
    - Transaction History: Every buy and sell filtered by portfolio ID
    - Heroku support
- Buy & Sell Crypto
- Display portfolio
- Display Transaction History
---
## Class Coinspot

```python
from coinspot import CoinSpot

SECRET_KEY = os.environ.get('SECRET_KEY','pretend secret key')

cryptoApi = CoinSpot("df",SECRET_KEY) 
allprices = cryptoApi.latestsall().json()
```

- Flask server
    - Server side
    - Django
- sessions
    - Remember user
- API
    - Provided by CoinSpot
  
---
## Languages used ##
- postgresql : Heroku suppor
- javascript
    - Client side
- html
- css
- python

---
## INSTALATION ##

 

## TODO ##
- Sound: clicks when hover over buttons
- Multiple portfolios
- Confirmation to sell crypto
- Summary and Confirmation when Buying crypto
- Remove user option
- Rename portfolio option
- Move the transaction history to the far right hand side and implement scroll bars.
- Factor in FEEs when BUYING or SELLING
- Reduce size of background video as it currently extends current page height
- Implement a ticker at the bottom of the page with crypto news, prices.
- Improve login. Use the email and not the username to login.
- Ticker along the bottom: BTC, ETH prices. 

## License
[MIT](https://choosealicense.com/licenses/mit/)