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
    def latestsall(self):
        return requests.get("https://www.coinspot.com.au/pubapi/v2/latest")
