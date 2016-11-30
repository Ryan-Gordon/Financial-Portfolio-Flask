import os
from flask import Flask, session, g
from flask import render_template, json, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.indexable import index_property
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import UserMixin, RoleMixin, login_required, current_user
import requests
import datetime
from decimal import *
from flask import session, g
# Setup flask_mail. This is used to email users
# Can send a welcome email on registration or forgotten password link
mail = Mail()
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'ryantest216@gmail.com'
MAIL_PASSWORD = '99Google99'
app = Flask(__name__)  # Setup flask app
app.config.from_object(__name__)  # Setup app config
mail.init_app(app)  # Initialise flask_mail with this app
# @Config settings
app.config['DEBUG'] = True  # Disable this when ready for production
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SECURITY_REGISTERABLE'] = True  # This enables the register option for flask_security
app.config['SECURITY_RECOVERABLE'] = True  # This enables the forgot password option for flask_security
app.config['SECURITY_POST_LOGIN_VIEW'] = 'dashboard'
app.config['SECURITY_POST_REGISTER_VIEW'] = 'dashboard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)  # Create database connection object with SQLAlchemy

# Define models for db
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
# This class is used to model the table which will hold Users
# Contains a backreference to the Role class for User/Admin role possiblities


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# This class is used to model the table which will hold Users
# Contains a backreference to the Role class for User/Admin role possiblities


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
# This class is used to model the table which will hold the currencies themselves
# Information acquired via the /GET/ method of a publicly available REST API


class Currency(db.Model, UserMixin):
    __tablename__ = "Currency"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(255), unique=True)
    last = db.Column(db.String(255))
    ask = db.Column(db.String(255))
    bid = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())


# This class is used to model the table which will hold each users currency
# Contains id as a foreign key from User


class UserCurrency(db.Model, UserMixin):
    __tablename__ = "users_cur"
    trans_id = db.Column(db.Integer, primary_key=True, index=True)
    id = db.Column(db.Integer)

    amount = db.Column(db.Numeric())
    ticker = db.Column(db.String(255))
    priceInBTC = db.Column(db.Numeric())
    priceInUSD = db.Column(db.Numeric())
    priceInEUR = db.Column(db.Numeric())
    priceInCHY = db.Column(db.Numeric())
    last = db.Column(db.String(255))
    ask = db.Column(db.String(255))
    bid = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())
    index = index_property('id', 'index')


class Stock(db.Model, UserMixin):
    __tablename__ = "Stocks"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(255), unique=True)
    last = db.Column(db.String(255))
    market = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())


# This class is used to model the table which will hold each users stock investments
# Contains id as a foreign key from User


class UserStocks(db.Model, UserMixin):
    __tablename__ = "users_stocks"
    trans_id = db.Column(db.Integer, primary_key=True, index=True)
    id = db.Column(db.Integer)

    amount = db.Column(db.Numeric())
    ticker = db.Column(db.String(255))
    market = db.Column(db.String(255))
    priceInBTC = db.Column(db.Numeric())
    priceInUSD = db.Column(db.Numeric())
    priceInEUR = db.Column(db.Numeric())
    priceInCHY = db.Column(db.Numeric())
    last = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())
    index = index_property('id', 'index')

# Setup user_datastore and sqlalchemy for flask_security to use
user_datastore = SQLAlchemyUserDatastore(db, User, Currency)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    # Possible implementation
    # Query db for users by email
    # if dummy user does not exist, create him and attempt to fill the database
    # if not perhaps check the db and if no currencies are there fill that up too.
    if db is None or User.query.first() is None:
        print("No Users found, creating test user")
        db.create_all()
        user_datastore.create_user(email='ryan@gordon.com', password='password', confirmed_at=datetime.datetime.now())
        r = requests.get('https://poloniex.com/public?command=returnTicker')
        # Pull JSON market data from Bittrex
        b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
        # Print value to user and assign to variable
        data = r.json()
        # Print value to user and assign to variable
        bittrex = b.json()

        for key in data.keys():
            u = Currency(ticker=key, last=data[key]['last'], ask=data[key]['lowestAsk'], bid=data[key]['highestBid'], timestamp=datetime.datetime.now())
            db.session.add(u)

        db.session.commit()
    else:
        print("Found Users in DB")
# The default route. Provides a landing page with info about the app and options to login/register


@app.route('/')
def landing_page():
    db.create_all()
    return render_template("homepage.html")
# This route provides a basic UI view of the app with no content. Will be removed in production


@app.route('/index')
@login_required
def index():
    return render_template("index.html")
# All this does is log out the user if any and 


@app.route('/logout')
def logout():
    logout_user(self)

# This route provides shows all the currencies for the user if any.


@app.route('/currencies')
@login_required
def currencies():
    Currencies = UserCurrency.query.filter_by(id=current_user.id).all()
    print(Currencies)
    return render_template("currencies.html", Currencies=Currencies)

# This route is the main starter view of the app and contains info from the other sections


@app.route('/stocks')
@login_required
def stocks():
    # We want the price of 5+ stocks
    # http://finance.google.com/finance/info?client=ig&q=NASDAQ%3AAAPL,GOOG,MSFT,AMZN,TWTR
    # Use this to access the stock prices or perhaps use a better one if one exists
    # this should ebe the same crack as it was with the Poloniex and Bittrex API
    if Stock.query.first() is None:
        print("No stock data found in DB")
        request = requests.get('http://finance.google.com/finance/info?client=ig&q=NASDAQ%3AAAPL,GOOG,MSFT,AMZN,TWTR')
        request.encoding = 'utf-8'  # We need to change encoding as this API uses ISO and i use utf-8 everywhere else
        o = request.text[4:]  # The response object contains some characters at start that we cant parse. Trim these off
        result = json.loads(o)  # After we trim the characters, turn back into JSON
        for i in result:
            u = Stock(ticker=i['t'], last=i['l'], market=i['e'], timestamp=datetime.datetime.now())
            db.session.add(u)

        db.session.commit()
    else:
        print("Found stock data in DB")
        # do something
    # query db for stocks
    Stocks = UserStocks.query.filter_by(id=current_user.id).all()

    # pass into html using render_template
    return render_template("stocks.html", Stocks=Stocks)


@app.route('/addNewStock', methods=['POST'])
def addNewStock():
    amount = request.form['Amount']  # Amount taken from posted form
    ticker = request.form['Ticker'].upper()  # Ticker taken from posted form
    queriedStock = Stock.query.filter_by(ticker=ticker).first()  # query the db for currency
    fiat = requests.get('http://api.fixer.io/latest?base=USD')  # Fiat is a term for financials i.e Euro, Dollar
    usd2fiat = fiat.json()
    queriedCur = UserStocks.query.filter_by(ticker=ticker, id=current_user.id).first()

    if queriedStock is not None:
        if queriedCur is not None:
            queriedCur.amount += Decimal(amount)
            queriedCur.timestamp = datetime.datetime.now()
            # queriedCur.priceInEUR = queriedCur.priceInUSD * usd2fiat['rates']['EUR']
            # queriedCur.priceInCHY = queriedCur.priceInUSD * usd2fiat['rates']['CNY']
            print("Currency amount updated in DB")
        else:
            me = UserStocks(amount=float(amount), id=current_user.id, ticker=queriedStock.ticker, market=queriedStock.market, last=queriedStock.last, timestamp=datetime.datetime.now(), priceInUSD=((float(queriedStock.last)*float(amount))), priceInEUR=(((float(queriedStock.last)*float(amount))*float(usd2fiat['rates']['EUR']))), priceInCHY=(((float(queriedStock.last)*float(amount)) * float(usd2fiat['rates']['CNY']))))

            db.session.add(me)
            print("Currency added to DB")
        db.session.commit()
    else:
        flash('Unrecognised Ticker. Please select one of the supported tickers')
    return redirect(url_for('stocks'))
# This route is the main starter view of the app and contains info from the other sections


@app.route('/dashboard')
@login_required
def dash():
    return render_template("dashboard.html")
# This route provides an about me page for me the creator.


@app.route('/about')
@login_required
def about():
    return render_template("about.html")
# This route provides contact links. Not much going on here.


@app.route('/contact')
@login_required
def contact():
    return render_template("contact.html")

# This route is used when a user adds a new currency. Info is submitted to server via POST.
# Removed Get method. Design Principle from John Healy. Use only what you need.


@app.route('/addNewCurrency', methods=['POST'])
def addNewCurrency():
    amount = request.form['Amount']  # Amount taken from posted form
    ticker = request.form['Ticker'].upper()  # Ticker taken from posted form
    currency = Currency.query.filter_by(ticker='BTC_'+ticker).first()  # query the db for currency
    usd2btc = Currency.query.filter_by(ticker='USDT_BTC').first()
    fiat = requests.get('http://api.fixer.io/latest?base=USD')
    usd2fiat = fiat.json()
    queriedCur = UserCurrency.query.filter_by(ticker='BTC_'+ticker, id=current_user.id).first()
    if currency is not None:
        if queriedCur is not None:
            queriedCur.amount += Decimal(amount)
            queriedCur.timestamp = datetime.datetime.now()
            queriedCur.priceInBTC = (float(currency.last)*float(queriedCur.amount))
            queriedCur.priceInUSD = (queriedCur.priceInBTC * float(usd2btc.last))
            queriedCur.priceInEUR = queriedCur.priceInUSD * usd2fiat['rates']['EUR']
            queriedCur.priceInCHY = queriedCur.priceInUSD * usd2fiat['rates']['CNY']
            print("Currency amount updated in DB")
        else:
            me = UserCurrency(amount=float(amount), id=current_user.id, ticker=currency.ticker, last=currency.last, bid=currency.bid, ask=currency.last, timestamp=datetime.datetime.now(), priceInBTC=(float(currency.last)*float(amount)), priceInUSD=(float(usd2btc.last)*(float(currency.last)*float(amount))), priceInEUR=((float(usd2btc.last)*(float(currency.last)*float(amount))*float(usd2fiat['rates']['EUR']))), priceInCHY=((float(usd2btc.last)*(float(currency.last)*float(amount)) * float(usd2fiat['rates']['CNY']))))

            db.session.add(me)
            print("Currency added to DB")
        db.session.commit()
    else:
        flash('Unrecognised Ticker. Please select one of the supported tickers')
    return redirect(url_for('currencies'))


# This route is triggered via the currency route
# Db is queried for provided currency and if user has stock it removes from db and commits change
# If nothing there it prints this to console and redirects


@app.route('/currencies/delete/<ticker>')
def deleteentry(ticker):
    queriedCur = UserCurrency.query.filter_by(ticker=ticker, id=current_user.id).first()
    if queriedCur is not None:
        UserCurrency.query.filter_by(ticker=ticker, id=current_user.id).delete()
        print("Deleted Currency")
    else:
        print("Could not delete. Redirecting")

    db.session.commit()
    return redirect(url_for('currencies'))

# This route is triggered via the stocks route
# Db is queried for provided stock and if user has stock it removes from db and commits change
# If nothing there it prints this to console and redirects


@app.route('/stocks/delete/<ticker>')
def deletestock(ticker):
    queriedCur = UserStocks.query.filter_by(ticker=ticker, id=current_user.id).first()
    if queriedCur is not None:
        UserStocks.query.filter_by(ticker=ticker, id=current_user.id).delete()
        print("Deleted Currency")
    else:
        print("Could not delete. Redirecting")

    db.session.commit()
    return redirect(url_for('stocks'))

# Charts view allows for visual represententation of the users assets 
# I leveraged the skills I learned in my Graphics Programming module 
# and utilised chart js. This is the only part of my project that uses JS apart from the menu toggle


@app.route("/charts")
def chart():
    labels = []
    valuesAmount = []
    valuesInEur = []
    # valuesInGBP = []
    valuesInUSD = []
    valuesInCNY = []

    Currencies = UserCurrency.query.filter_by(id=current_user.id).all()
    for row in Currencies:
        labels.append(row.ticker)
        valuesAmount.append(row.amount)
        valuesInEur.append(row.priceInEUR)
        # valuesInGBP.append(row.priceInGBP)
        valuesInUSD.append(row.priceInUSD)
        valuesInCNY.append(row.priceInCHY)

    print(len(valuesAmount))
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC"]
    return render_template('charts.html', set=list(zip(valuesAmount, valuesInEur, valuesInUSD, valuesInCNY, labels, colors)))

# This starts the API section. I initially set out on this project as I noticed there was no API
# for averaged data for crypto currencies. In my api I have set up averaged prices for a number of top
# cryptocurrencies. It is my hope after this project it may be improved by the open source community.


@app.route('/api/sdc')
@login_required
def BTC_SDC():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    data = r.json()
    # Print value to user and assign to variable
    bittrex = b.json()
    # In this section highBid and lowAsk are unicode
    poloHighBid = data['BTC_SDC']['highestBid']
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
    providedJson = {"poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk, "poloHighBid": poloHighBid}

    # data['BTC_SDC']
    return json.dumps(providedJson)
    # end function


@app.route('/api/eth')
def BTC_ETH():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    # Print value to user and assign to variable
    data = r.json()
    # Print value to user and assign to variable
    bittrex = b.json()
    # In this section highBid and lowAsk are unicode
    poloHighBid = data['BTC_ETH']['highestBid']
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
    providedJson = {"Market Name": marketName, "poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk, "poloHighBid": poloHighBid}

    # data['BTC_SDC']
    return json.dumps(providedJson)
    # end function


@app.route('/api/xmr')
def BTC_XMR():
    # Pull JSON market data from Poloniex
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    # Pull JSON market data from Bittrex
    b = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    # Print value to user and assign to variable
    data = r.json()
    # Print value to user and assign to variable
    bittrex = b.json()
    # In this section highBid and lowAsk are unicode
    poloHighBid = data['BTC_XMR']['highestBid']
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
    providedJson = {"Market Name": marketName, "poloLast": poloLast, "bittrexLast": bittrexLast, "priceObject": pricesList, "poloLow": poloLowAsk, "poloHighBid": poloHighBid}

    return json.dumps(providedJson)
    # end function

# Bind to PORT if defined, otherwise default to 5000.
# I have this here for Heroku as Heroku needs the ability to specify a port
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0')
