import requests
class CoinSpot(object):
    # The endpoint for the API
    API_ENDPOINT_PUBLIC = "https://www.coinspot.com.au/pubapi/v2/"
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret.encode()
    def latestPrice(self,coin):
        # Return the latest public price from Coinpot
        return requests.get(self.API_ENDPOINT_PUBLIC +"latest/"+coin).json()['prices']['bid']
        
    @staticmethod
    def latest(cointype): # returns the latest price
        return requests.get("https://www.coinspot.com.au/pubapi/v2/latest/"+cointype).json()
    def latestsall(self):
        return requests.get("https://www.coinspot.com.au/pubapi/v2/latest")
