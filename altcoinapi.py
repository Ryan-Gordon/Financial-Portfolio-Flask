from flask import Flask
from flask import json
import requests

@app.route('/')
def hello_world():
    
    return "Hello World"


app.run(debug=False)