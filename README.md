# Coin-Counter-API
A python api for crypto currencies which aggregates pricing data from different markets and displays the average for the given coin. This is the api whose code is open source. Plan to integrate this into a mobile app also.

Using Flask, a number of cryptomarkets are pulled using the requests module. Each market select has provided a public API for us to use which does not need a API key or secret.

The pricing data for a number of currencies is pulled down, aggregated and then inserted in a data model. 
A webapp is provided with this api for the tracking of assets.

To access the api:
API routes are available for a number of currencies to get there you will need to navagate to /api/currencyName. e.g 
`/api/sdc`  
To access the web app:  
Please see [user guide](#User-Guide)

### Roadmap
+ <del> Flask server access from other device - Run on 0.0.0.0 and access the IP of the PC serving it</del>  
+ <del>Login/Signup functionality </del>  
+ <del> Landing page describing webapp</del>  
+ <del>Dashboard page for initial view </del>  
+ <del>About & Contact Page  </del>  
+ <del>Adding a currency to a user </del>
+ Styling login and signup forms
+ Perhaps some stock asset tracking if time perhaps  
+ Dashboard page   
+ Charting for assets  
+ Host api on a hosting provider

#### User Guide
Upon loading the website you will be required to either sign in to the default profile or to register your own account which will require an email and password.
Once registered the dashboard appears. On the sidemenu are a number of quick link to different sections of the app aswell as buttons on the dashboard.  
To add a Currency:  
Navagate to the currency page. Initially there will be none there however clicking 'New' in the top right corner of the table will present a modal for adding a currency.
Select your amount, relevant ticker and submit. The currencies price will be queried from the database and the asset added to your account. Adding more of the same currency will affect the previous entry and not create a new one.
Entering a negative value will devalue your asset possibly into negative values. This is left in for margin trading capability.


#### Data Representation and Querying Project 2016

This repository contains code and information for a third-year undergraduate project for the module Data Representation and Querying. The module is taught to undergraduate students at GMIT in the Department of Computer Science and Applied Physics. The lecturer is Ian McLoughlin.

The project was guided by the following excerpt from the project instructions:

> You are required to develop a single-page web application(SPA) written in the programming language Python using the Flask framework. You must devise an idea for a web application, write the software, write documentation explaining how the application works, and write a short user guide for it.

This will initially be the API for the project. I may expand it in itself to be a webapp or I may create a webapp using another framework and simply consume the api.




How to run the application

The application is written using the Flask library in Python 3. Both must be installed to run the project.

Once these prerequisites are installed, the application can be run locally:

> $ python altcoinapi.py

Once the application is running, it can be accessed by pointing your browser at http://127.0.0.1:5000/ .

#####Architecture

This web application runs in Python 3 using the Flask web micro-framework and uses Requests to make http requests. Python 3 and Flask were requirements for the project, but Requests was selected for its ease of use, its detailed documentation and it is a recommended extension on flask website.

##### Extenstions Used:
See requirements.txt for full list of extenstions
