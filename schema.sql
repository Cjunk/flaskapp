DROP TABLE IF EXISTS customers,portfolios,portfolio_detail,transaction_history,users_authentication,transaction_types;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    date_joined DATE
);
CREATE TABLE transaction_types(
    type_id INTEGER PRIMARY KEY,
    tran_type TEXT
);
CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    customer_owner INTEGER REFERENCES customers(id),
    starting_cash INTEGER
);
CREATE TABLE portfolio_detail(
    porfolio_id INTEGER NOT NULL,
    coin TEXT,
    cost FLOAT,
    quantity FLOAT
);

CREATE TABLE transaction_history (
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