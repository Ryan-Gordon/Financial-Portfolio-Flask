from flask import Flask
from flask import json
import requests

@app.route('/')
def hello_world():
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    print(r)
    data = r.json()
    

    # print("The response is" +str(data['BTC_SDC']))
    print(data['BTC_SDC'])
    return "Hello World"


app.run(debug=False)