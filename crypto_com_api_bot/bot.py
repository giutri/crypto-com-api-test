import hmac
import hashlib
import json
import requests
import time

class CryptoBot():

    API_BASE_URL = 'https://api.crypto.com/v2/'
    API_KEY = ''
    SECRET_KEY = ''

    def __init__(self):

        with open('keys.json') as keyFile:
            keys = json.load(keyFile)
            self.API_KEY = keys['api_key']
            self.SECRET_KEY = keys['secret_key']

    ########## GET PUBLIC REQUEST HELPER #################
        
    def performPublicRequest(self, routeURI):

        endpointURL = self.API_BASE_URL+routeURI
        res = requests.get(endpointURL)


        if (res.status_code == 200):
            data = json.loads(res.text)#['result']['data']
            return data
        
        else:
            raise ValueError('Bad Request')

    ########## POST PRIVATE REQUEST HELPER #################

    def performAuthRequest(self, routeURI, params):

        req = {
            "id": 12,
            "method": routeURI,
            "api_key": self.API_KEY,
            "params": params,
            "nonce": int(time.time() * 1000)
        }

        # First ensure the params are alphabetically sorted by key
        paramString = ""

        if "params" in req:
            for key in sorted(req['params']):
                paramString += key
                paramString += str(req['params'][key])

            sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])

            req['sig'] = hmac.new(
                bytes(str(self.SECRET_KEY), 'utf-8'),
                msg=bytes(sigPayload, 'utf-8'),
                digestmod=hashlib.sha256
                ).hexdigest()

            res = requests.post(
                self.API_BASE_URL+routeURI,
                json=req,
                headers={'Content-Type':'application/json'}
            )

            if (res.status_code == 200):
                data = json.loads(res.text)
                return data
            
            else:
                raise ValueError('Bad Request')

    ########## ACCOUNT REQUESTS #################

    def getOrderHistory(self):

        routeURI = "private/get-order-history"
        params = {}

        try:

            data = self.performAuthRequest(routeURI, params)

            orderList = data['result']['order_list']

            if orderList is None:
                raise ValueError('No orderList data found')
            else :
                return orderList

        except ValueError as err:
            raise ValueError(err.args)


    def getAccountSummary(self):

        routeURI = "private/get-account-summary"
        params = {}

        try:

            data = self.performAuthRequest(routeURI, params)

            accountSummary = data['result']['accounts']

            if accountSummary is None:
                raise ValueError('No accountSummary data found')
            else :
                return accountSummary

        except ValueError as err:
            raise ValueError(err.args)


    ############# TRADE EXEC ENDPOINTS ############

    def createOrder(self):

        routeURI = "private/create-order"
        params =  {
            "instrument_name": "ETH_CRO",
            "side": "BUY",
            "type": "LIMIT",
            "price": 100.12,
            "quantity": 1.2,
            "client_oid": "my_order_0002",
            "time_in_force": "GOOD_TILL_CANCEL",
            "exec_inst": "POST_ONLY"
        }

        try:

            data = self.performAuthRequest(routeURI, params)

            orderResult = data['result']

            if orderResult is None:
                raise ValueError('No orderResult data found')
            else :
                return orderResult

        except ValueError as err:
            raise ValueError(err.args)

    ############# PRICE INFO ENDPOINTS ##################

    def getCandlesticks(self, instrumentName, period):

        routeURI = 'public/get-candlestick?instrument_name='+instrumentName+'&timeframe='+period

        try:

            data = self.performPublicRequest(routeURI)

            candleSticks = data['result']['data']

            if candleSticks is None:
                raise ValueError('no candlestick data found')
            else :
                return candleSticks
            

        except ValueError as err:
            raise ValueError(err.args)
           
#bot = CryptoBot()
#candleSticks = bot.getCandlesticks('ddsf', '1D')