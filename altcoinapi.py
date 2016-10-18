from flask import Flask
from flask import json
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    
    return "Hello World"

@app.route('api/sdc')
def BTC_SDC():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    
    #Print value to user and assign to variable
    print(r)
    data = r.json()
    #Print value to user and assign to variable
    print(b)
    bittrex = b.json()
    print(bittrex)
    for key in data.keys():
        print(key)
    
    print(data['BTC_SDC']['highestBid'])

    #Prints the bittrex api data for coin 134 aka sdc
    print(bittrex['result'][134])
    
    
    # In this section highBid and lowAsk are unicode
    poloHighBid  =  data['BTC_SDC']['highestBid']
    poloLowAsk = data['BTC_SDC']['lowestAsk']
    
    # In order to sum the values and not all the values for the list we need to convert the vars to floats
    # Float allows us to add the decimal numbers together with precision
    poloLast = float(data['BTC_SDC']['last'])
    
    # Get bittrex data for current market
    bittrexLast = float(bittrex['result'][134]['Last'])
    pricesList = [poloLast, bittrexLast]
    # Calc avg between 3 markets
    avgPrice = sum(pricesList) / float(len(pricesList))


    # Fill JSON with lowAsk highBid price avgBid 
    providedJson = {"poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk,"poloHighBid": poloHighBid}

    # data['BTC_SDC']
    return json.dumps(providedJson)
    # end function

@app.route('api/eth')
def BTC_ETH():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    
    #Print value to user and assign to variable
    print(r)
    data = r.json()
    #Print value to user and assign to variable
    print(b)
    bittrex = b.json()
    print(bittrex)
    for key in data.keys():
        print(key)
    
    print(data['BTC_ETH']['highestBid'])

    #Prints the bittrex api data for coin 61 aka ETH
    print(bittrex['result'][61])
    
    
    # In this section highBid and lowAsk are unicode
    poloHighBid  =  data['BTC_ETH']['highestBid']
    poloLowAsk = data['BTC_ETH']['lowestAsk']
    
    # In order to sum the values and not all the values for the list we need to convert the vars to floats
    # Float allows us to add the decimal numbers together with precision
    poloLast = float(data['BTC_ETH']['last'])
    
    # Get bittrex data for current market
    bittrexLast = float(bittrex['result'][61]['Last'])


    pricesList = [poloLast, bittrexLast]
    # Calc avg between 3 markets
    avgPrice = sum(pricesList) / float(len(pricesList))

    marketName = bittrex['result'][61]['MarketName']
    # Fill JSON with lowAsk highBid price avgBid 
    providedJson = {"Market Name": marketName, "poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk,"poloHighBid": poloHighBid}

    # data['BTC_SDC']
    return json.dumps(providedJson)
    # end function

@app.route('api/xmr')
def BTC_XMR():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    
    #Print value to user and assign to variable
    print(r)
    data = r.json()
    #Print value to user and assign to variable
    print(b)
    bittrex = b.json()
    print(bittrex)
    for key in data.keys():
        print(key)
    
    print(data['BTC_XMR']['highestBid'])

    #Prints the bittrex api data for coin 193 aka XMR
    print(bittrex['result'][193])
    
    
    # In this section highBid and lowAsk are unicode
    poloHighBid  =  data['BTC_XMR']['highestBid']
    poloLowAsk = data['BTC_XMR']['lowestAsk']
    
    # In order to sum the values and not all the values for the list we need to convert the vars to floats
    # Float allows us to add the decimal numbers together with precision
    poloLast = float(data['BTC_XMR']['last'])
    
    # Get bittrex data for current market
    bittrexLast = float(bittrex['result'][193]['Last'])


    pricesList = [poloLast, bittrexLast]
    # Calc avg between 3 markets
    avgPrice = sum(pricesList) / float(len(pricesList))

    marketName = bittrex['result'][193]['MarketName']
    # Fill JSON with lowAsk highBid price avgBid 
    providedJson = {"Market Name": marketName, "poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk,"poloHighBid": poloHighBid}

    # data['BTC_SDC']
    return json.dumps(providedJson)
    # end function

app.run()