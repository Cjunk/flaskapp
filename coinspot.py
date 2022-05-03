#from time import time
import requests
class CoinSpot(object):
    # The endpoint for the API
    # API_ENDPOINT = "https://www.coinspot.com.au:443/api/"
    API_ENDPOINT_PUBLIC = "https://www.coinspot.com.au/pubapi/v2/"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret.encode()
    def latestPrice(self,coin):
        # Return the latest public price from Coinpot
        response =  requests.get(self.API_ENDPOINT_PUBLIC +"latest/"+coin).json()['prices']['bid']
        return response

    @staticmethod
    def latest(cointype): # returns the latest price
        s = requests.get("https://www.coinspot.com.au/pubapi/v2/latest/"+cointype).json()
        return s

    # def orders(self, cointype):
    #     return self._request("orders", {
    #         "cointype": cointype
    #     })

 
    # def orders_history(self, cointype):
    #     return self._request("orders/history", {
    #         "cointype": cointype
    #     })

 
    # def my_balances(self):
    #     return self._request("my/balances")


    # def spot(self):
    #     return self._request("spot")
    # def my_orders(self):
    #     return self._request("my/orders")

    # def my_buy(self, cointype, amount, rate):
    #     return self._request("my/buy", {
    #         "cointype": cointype,
    #         "amount": amount,
    #         "rate": rate
    #     })

 
    # def my_buy_cancel(self, _id):
    #     return self._request("my/buy/cancel", {
    #         "id": _id
    #     })

 
    # def my_sell(self, cointype, amount, rate):
    #     return self._request("my/sell", {
    #         "cointype": cointype,
    #         "amount": amount,
    #         "rate": rate
    #     })

   
    # def my_sell_cancel(self, _id):
    #     return self._request("my/sell/cancel", {
    #         "id": _id
    #     })


    # def public_latest(self):
    #     return self._request("pubapi/latest")

    # def my_coin_deposit(self, cointype):
    #     return self._request("my/coin/deposit", {
    #         "cointype": cointype
    #     })

  
    # def my_coin_send(self, cointype, address, amount):
    #     return self._request("my/coin/send", {
    #         "cointype": cointype,
    #         "address": address,
    #         "amount": amount
    #     })


    # def quote_buy(self, cointype):
    #     return self._request_pub("buyprice/" + cointype)

    # def quote_mybuy(self, cointype,amount):
    #     return self._request_pub("quote/buy", {
    #         "cointype": cointype,
    #         "amount": amount
    #     })


    # def quote_mysell(self, cointype,amount):
    #     return self._request("quote/sell", {
    #         "cointype": cointype,
    #         "amount": amount
    #     })
    # def quote_sell(self, cointype):
    #     dd = self._request_pub("sellprice/" + cointype, {
    #         "cointype": cointype
    #     })
    #     return dd

