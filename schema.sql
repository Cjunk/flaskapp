-- psql ccryptodb < schema.sql
DROP TABLE IF EXISTS users,portfolios,portfolio_detail,transaction_history,users_authentication,transaction_types;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nickname TEXT,
    fname TEXT,
    lname TEXT,
    hashed_password TEXT
);
CREATE TABLE transaction_types(
    type_id INTEGER PRIMARY KEY,
    tran_type TEXT
);
CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    customer_owner INTEGER REFERENCES users(id),
    title TEXT,
    starting_cash INTEGER,
    current_balance FLOAT
);
CREATE TABLE portfolio_detail(
    porfolio_id INTEGER REFERENCES portfolios(id) NOT NULL,
    coin TEXT,
    cost FLOAT,
    quantity FLOAT
);

CREATE TABLE transaction_history (
    tranid SERIAL PRIMARY KEY,
    tran_date DATE,
    coin TEXT,
    portfolio_id INTEGER REFERENCES portfolios(id),
    tran_type INTEGER REFERENCES transaction_types(type_id),
    quantity FLOAT,
    price FLOAT

);
CREATE TABLE users_authentication (
    customer_ID INTEGER,
    hashed_pw TEXT

);

INSERT INTO transaction_types(type_id,tran_type) VALUES(1,'BUY');
INSERT INTO transaction_types(type_id,tran_type) VALUES(2,'SELL');

INSERT INTO users(nickname,fname,lname,hashed_password) VALUES('Jericho','Jericho','Sharman','e191990b4d37a42f37453cb67edbb16d4c5782e2df3c78bcba21ececdb73056f');
INSERT INTO users(nickname,fname,lname,hashed_password) VALUES('Sharon','Sharon','Roddis','e191990b4d37a42f37453cb67edbb16d4c5782e2df3c78bcba21ececdb73056f');
INSERT INTO portfolios(customer_owner,title,starting_cash,current_balance) VALUES(1,'savings',5000000,5000000);
INSERT INTO portfolios(customer_owner,title,starting_cash,current_balance) VALUES(1,'new one',5000000,5000000);

INSERT INTO portfolio_detail(porfolio_id,coin,cost,quantity) VALUES(1,'BTC',56000,.12);
INSERT INTO portfolio_detail(porfolio_id,coin,cost,quantity) VALUES(1,'ETH',2900,.25);
INSERT INTO portfolio_detail(porfolio_id,coin,cost,quantity) VALUES(1,'XRP',1000,.86);

INSERT INTO portfolio_detail(porfolio_id,coin,cost,quantity) VALUES(2,'BTC',56000,.12);