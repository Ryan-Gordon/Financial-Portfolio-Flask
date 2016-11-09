from flask import Flask
from flask import render_template, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
import requests
import datetime
from decimal import *
# Create app
mail = Mail()
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_TLS = False
MAIL_USE_SSL= True
MAIL_USERNAME = 'ryantest216@gmail.com'
MAIL_PASSWORD = '99Google99'
app = Flask(__name__)
app.config.from_object(__name__)
mail.init_app(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SECURITY_REGISTERABLE'] = True

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

users_currencies = db.Table('users_currencies',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('amount', db.Integer()),
        db.Column('ticker', db.String(255)),
        db.Column('last', db.Float()),
        db.Column('bid', db.Float()),
        db.Column('ask', db.Float())
        
        )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    

class Currency(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(255), unique=True)
    last = db.Column(db.String(255))
    ask = db.Column(db.String(255))
    bid = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())

class UserCurrency(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float())
    ticker = db.Column(db.String(255), unique=True)
    last = db.Column(db.String(255))
    ask = db.Column(db.String(255))
    bid = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())



# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Currency)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
       if db is None:
        db.create_all()
        user_datastore.create_user(email='ryan@gordon.com', password='password',confirmed_at=datetime.datetime.now())
        db.session.commit()

@app.route('/')
def landing_page():
    db.create_all()
    
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    
    #Print value to user and assign to variable
    print(r)
    data = r.json()
    #Print value to user and assign to variable
    print(b)
    bittrex = b.json()
   
    for key in data.keys():
        print(key)
        print(data[key]['last'])
        
        print(float(data[key]['lowestAsk']))
        print(Decimal(data[key]['lowestAsk']))
       
        print(type(data[key]['lowestAsk']))
       
        u = Currency(ticker=key,last=data[key]['last'], ask=data[key]['lowestAsk'],bid=data[key]['highestBid'], timestamp=datetime.datetime.now())
        db.session.add(u)

    db.session.commit()
    return render_template("homepage.html")

@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/logout')
def logout():
    logout_user(self)

@app.route('/addCurrency')
def addCurrency():
    peter = Currency.query.filter_by(ticker='BTC_XMR').first()
    me = UserCurrency(amount='100', ticker=peter.ticker,last=peter.last, bid=peter.bid, ask=peter.last,timestamp=datetime.datetime.now())
    print(me)
    db.session.add(me)
    db.session.commit()
    return render_template("index.html")

# To DO:
# Add list of most used routes
# Add page that can add coins


### This starts the API section

@app.route('/api/sdc')
@login_required
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

@app.route('/api/eth')
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

@app.route('/api/xmr')
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

app.run(host='0.0.0.0')