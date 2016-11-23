# Coin-Counter-API
A python api for crypto currencies which aggregates pricing data from different markets and displays the average for the given coin. This is the api whose code is open source. Plan to integrate this into a mobile app also.

Using Flask, a number of cryptomarkets are pulled are the requests module. Each market select has provided a public API for us to use which does not need a API key or secret.

The pricing data for a number of currencies is pulled down, aggregated and then inserted in a data model. 

### Roadmap

+Perhaps some stock asset tracking if time perhaps  
+ Dashboard page   
+ Charting for assets  
+ Create an API using the webapp's logic so other devs can use it
+ Host api on a hosting provider

Further plans are to consume this api itself to create a web app and perhaps a mobile app 

#### Data Representation and Querying Project 2016

This repository contains code and information for a third-year undergraduate project for the module Data Representation and Querying. The module is taught to undergraduate students at GMIT in the Department of Computer Science and Applied Physics. The lecturer is Ian McLoughlin.

The project was guided by the following excerpt from the project instructions:

> You are required to develop a single-page web application(SPA) written in the programming language Python using the Flask framework. You must devise an idea for a web application, write the software, write documentation explaining how the application works, and write a short user guide for it.

This will initially be the API for the project. I may expand it in itself to be a webapp or I may create a webapp using another framework and simply consume the api.




How to run the application

The application is written using the Flask library in Python 3. Both must be installed to run the project.

Once these prerequisites are installed, the application can be run locally:

> $ python nameOfFile.py

Once the application is running, it can be accessed by pointing your browser at http://127.0.0.1:4000/ .

#####Architecture

This web application runs in Python 3 using the Flask web micro-framework and uses Requests to make http requests. Python 3 and Flask were requirements for the project, but Requests was selected for its ease of use, its detailed documentation and it is a recommended extension on flask website.
