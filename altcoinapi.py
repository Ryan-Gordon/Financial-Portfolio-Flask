from flask import Flask
from flask import json
import requests

@app.route('/')
def hello_world():
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    print(r)
    data = r.json()
    
    test = [{key} for key in data.keys()]

    # print("The response is" +str(data['BTC_SDC']))
    print(data['BTC_SDC'])
    return "Hello World"

@app.route('/sdc')
def BTC_SDC():
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    
    print(r)
    data = r.json()

    
    
    for key in data.keys():
        print(key)
    
    # print("The response is" +str(data['BTC_SDC']))
    print(data['BTC_SDC']['highestBid'])

    #Prints the bittrex api data for coin 134 aka sdc
    print(bittrex['result'][134])
    
    
    
    
    # We could just print avgBid but to have a string also we will need to convert to str
    print("This is the btc sdc highest bid "+ highBid)
    print("This is the btc sdc lowest bid "+ lowAsk)
    print("This is the btc sdc avg bid "+ str(avgBid))


    
    return json.dumps(data['BTC_SDC'])


app.run(debug=False)