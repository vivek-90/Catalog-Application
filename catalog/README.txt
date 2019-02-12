CATALOG APPLICATION:

Introduction: 
The catalog application provides a list of items within a variety of categories in the field of sports. The application also provides a user registration and authentication system.Registered users will have the ability to post, edit and delete their own items.

Required Libraries and dependencies (Version of Flask, Python, and SQLAlchemy)
Flask:1.0.2
Python:2.7.12
SQLAlchemy: 1.2.11

Project Contents ( * .py, static, template folder)
The Project contains:
Python Files
Database_setup.py file to setup the database.
lotsofitems.py file contains the items to populate the database
application.py file the main content to run the app.

Templates folder contains:
categories.html
deleteconfirmation.html
description.html
editItem.html
Items.html
login.html
newitem.html
publiccatalog.html
publlicdescription.html

Static folder contains:
styles.css


Operating Instructions, This includes:
How to run the database setup:
Once the vagrant is up and the virtual machine is running, the following commands can be used to run the database setup.
Python Database_setup.py 

How to populate the database:
Once the database is setup, we can populate it by the following command,
Python lotsofitems.py

How to run your application:
Once the data is populated with the items, the following command is used to run the application.
Python application.py

On exceution of this command, the following appears on the command propt:
Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)

On your browser, visit the localhost:8000/ to interact with the app.  
