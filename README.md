# Financial Portfolio Flask
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![GitHub version](https://badge.fury.io/gh/boennemann%2Fbadges.svg)](http://badge.fury.io/gh/boennemann%2Fbadges)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)  
A Flask Python webapp which utilises a Bootstrap front-end.
Allows for the tracking and visualisation of Cryptocurrency or Stock investments.    
Presently the webapp supports 3 physical currencies out of box (EUR, USD, CNY) however the API used to gather currency pricing data has support for up to 11 more which can be configured.
There is also a charting view available for your currencies which utilises Chart.js

The UI of the app is mobile friendly and the tables change to vertical for smaller screens less than 768px  
Please see [user guide](#User-Guide)

The app is now hosted and working on heroku. To visit the app please head to https://financial-portfolio-flask.herokuapp.com
From initial testing the pages load blazingly quick, I take some pride in that.

#### Features
+ Now working on heroku

+ Majority of programming language done in Python. Github says 98% python.
+ Responsive Design
+ Optimized page load speed
+ Mobile Friendly - Tested on iPad Mini, Samsung J3
+ Abstracted models - can add other assets 
+ Currently supports over 100 Cryptocurrencies.
+ Configurable support for all stocks on Google Finace API (5+ Out of box)
+ Charting views to see your assets with neutral colours

#### User Guide
###### Installation:
The easiest way to install the webapp is to clone the repo in its entirety and either install requirements.txt, use the venv provided with extensions installed, if you have used python you more than likely have most extensions installed.
To run the webapp, nagate to the directory and enter:

> $ python webapp.py 
 
or

> $ flask webapp.py  

Upon loading the website you will be required to either sign in to the default profile or to register your own account which will require an email and password.
Once registered the dashboard appears. On the sidemenu are a number of quick link to different sections of the app aswell as buttons on the dashboard.  
###### To add a Currency:  
Navagate to the currency page. Initially there will be none there however clicking 'New' in the top right corner of the table will present a modal for adding a currency.
Select your amount, relevant ticker and submit. The currencies price will be queried from the database and the asset added to your account. Adding more of the same currency will affect the previous entry and not create a new one.
Entering a negative value will devalue your asset possibly into negative values. This is left in for margin trading capability.
Once added, you will see the amount held and values in BTC, EUR, USD and CNY
###### To add a Stock:  
Navagate to the stock page. Initially there will be none there however clicking 'New' in the top right corner of the table will present a modal for adding a stock.
Select your amount, relevant ticker and submit. The stocks value will be queried from the database and the asset added to your account. Adding more of the same stock will affect the previous entry and not create a new one.
Entering a negative value will devalue your asset possibly into negative values. This is left in for margin trading capability.
Once added, you will see the amount held, values in EUR, USD and the market of the stock (NYSE, NASDAQ)
###### Charts:
Once currencies are added to your account you can utilises charts of your investments for a visual representation. Charts availble for amount of each held and the value of your assets in EUR, USD and CNY

###### API:
To access the api:
API routes are available for a number of currencies to get there you will need to navagate to /api/currencyName. e.g 
`/api/sdc`  
 

### Roadmap
+ <del>Login/Signup functionality </del>  
+ <del> Landing page describing webapp</del>  
+ <del>Dashboard page for initial view </del>  
+ <del> EXTRA: Stock trading </del> 
+ <del>Dashboard page </del > 
+ <del>Charting for assets  </del>
+ <del>Host webapp on a hosting provider after grading.</del>
+ Some form of real time price updating via Redis. API calls and results stored in redis for real-time pricing and update SQL db every so often.




#### Data Representation and Querying Project 2016

This repository contains code and information for a third-year undergraduate project for the module Data Representation and Querying. The module is taught to undergraduate students at GMIT in the Department of Computer Science and Applied Physics. The lecturer is Ian McLoughlin.

The project was guided by the following excerpt from the project instructions:

> You are required to develop a single-page web application(SPA) written in the programming language Python using the Flask framework. You must devise an idea for a web application, write the software, write documentation explaining how the application works, and write a short user guide for it.


How to run the application

The application is written using the Flask library in Python 3. Both must be installed to run the project.

Once these prerequisites are installed, the application can be run locally:

> $ python webapp.py

Once the application is running, it can be accessed by pointing your browser at http://127.0.0.1:5000/ or http://0.0.0.0:5000/.

#####Architecture

This web application runs in Python 3 using the Flask web micro-framework and uses Requests to make http requests. Python 3 and Flask were requirements for the project, but Requests was selected for its ease of use, its detailed documentation and it is a recommended extension on flask website.

##### References:
A number of extensions were used in this app. Please see requirements.txt or the 'About' page in the app for info.
Front end in Bootstrap
Backend and logic in python
Chart.js for charting

Some bootstrap components have been used which have been expanded on and changed to make my own. There are referenced in the source code.
##### Extenstions Used:
See requirements.txt for full list of extenstions
