**Why Crypto Portfolio:**   
## I have bought crypto currency from multiple sites and previously used Excel to try and givea  consolodated overview of all my holdings. It was natural for me to come up with this idea. ##
---

## The Process ##
Designed a bit on paper at first how I wanted it to look
In code I created the prototypes for the functions

## Database ##
Passwords are stored in Hashed format. When a user logs in their password is hashed and checked against the database matching their user name then the hashed password. Moving forward I will change this to be the email rather than the username so as to be more unique.

Five tables in all: ***3rd Normal Form (3NF)***
- users                 :   User names, passwords contained here.
- portfolios            :   Portfolio overviews documenting available funcds
- portfolio_detail      :   The specific holdings in each portfolio
- transaction_history   :   All transactions logged in this table.
- transaction_types     :   Two rows for BUY or SELL options. 

---
## Applications used to assit
- VSCODE
- PYCHARM
- MICROSOFT WORD
- MICROSOFT EXCEL
- CORAL PAINTSHOP PRO

#### **Used in this application** ####
HTML () , CSS (animation, style), JAVASCRIPT ()
Python : Flask, Class object (API control),
postgresql : Host own database server 

### **Back End:Functionality**
HTTP requests, API access, SQL database connection, Sessions, Hashed passwords, 

---
## Accomplishments ##
- Understanding and implementing the session control feature. At first I was working with cookies but 'stumbled' upon some session info while googling. I found this to be a much better solution than cookies in that is was easier to work with, encrypted on the client side. And readily available throughout the application. 

- Much cleaner separation of code with a base template and subsequent child pages. 


## Hurdles ##
- At some point the Heroku application would crash after logging in. I was able to identify that it was due to /login POST and not /login GET. A few hours of attempting troubleshooting lead me to move the return redirect ('/') line to the beginning of the login route, git add,commit and push to heroku, gradually moving the redirect line down , line by line, untill Heroku crashed. This process I was able to identify that it was due to a missing database. Which was odd as it hada database already for a few days and was working. So I am guessing something I had done had removed the database'. 
The solution was to restart the Heroku database and upload my local database to Heroku. Code is below
```bash
heroku pg:reset 
heroku pg:push local_cryptodb DATABASE_URL
```

- For no apprent reason the psql server was no longer operating. It turns out this was a simple solution of starting up the psql server

```
sudo service postgresql start
```

- Overall structure. I hit the road running, however after much coding I started to see the flaws in my overall structure and started to lose track of things. I learnt my lesson that many smaller functions should be made first rather than tackle big ones straight away. I scrapped the original app.py and redone a new one. 
---
## Learnings ##
- Document well before writing any code
    - Front End: Story boarding
    - Front ENd: Designing processes
    - Back End: Deciding file structure
    - Back End: Clear on packages required.
- Front End: Prototype via Excel more so for graphical user interface
- Get multiple users feedback on front page design and functionality
- Back End: More time and thought put into code design to help minimise redundant code. Makes it more efficient. Lower database calls.
- Always Document a learnings book (Microsoft Word) from the beginning
- SQL: Users database : Composite key from email and hashed password. To ensure unique entries.
