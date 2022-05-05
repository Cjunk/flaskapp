 SELECT * from portfolio_detail JOIN portfolios ON portfolio_detail.porfolio_id = portfolios.id;
--  Only shows portfolio detail where there is detail
  id | porfolio_id | coin | cost  | quantity | id | customer_owner |  title  | starting_cash | current_balance 
----+-------------+------+-------+----------+----+----------------+---------+---------------+-----------------
  1 |           1 | BTC  | 56000 |     0.12 |  1 |              1 | savings |         50000 |           50000
  2 |           1 | ETH  |  2900 |     0.25 |  1 |              1 | savings |         50000 |           50000
  3 |           1 | XRP  |  0.78 |     1000 |  1 |              1 | savings |         50000 |           50000
  4 |           2 | BTC  | 56000 |     0.12 |  2 |              1 | new one |         50000 |           50000



-- return the customer ID for a portfolio id
SELECT customer_owner FROM portfolios WHERE id=3;

-- #Get the portfolio ID from the customer : ASSUMPTION is only one portfolio per user
SELECT * FROM portfolios WHERE customer_owner = 1;