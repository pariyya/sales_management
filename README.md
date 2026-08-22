# sales management system

## this project is a backend system for manage products,customers,orders,inventory,authentication and sales reports.



## technologies:

- python

- fastapi\:for creating API

- sqlalchemy\:a library for connects the application to the database and work with database tables,its for use queries,add,delete from database

- pydantic\:to validate  users input

- sqlite\:its our database

- jwt\:we use it for create and verify authentication tokens

- pytest\:library for write tests

## project structure:

- app\:main application

-app/main.py

- app/models\:database models

- app/schemas\:pydantic schema for input validation

- app/routers\:business logic

- app/database.py\:database connections

- app/security.py\:hashing password and jwt

- tests\:project tests

- tests/test\_main\:main project test

## modules project\:it has atributes for each tables in database

## router: we use APIROUTER  to create our router (when user send request this router uses the (path + HTTP method) to find the destination function.)

## product routers

- handles product creation, display, update and delete

- recieves product information from the user

- use sqlalchemy to access the product table in the database

- check the products not to be exists with same name before creating

- check the products  to be exists with same id before updating

## Customer Route

- handles creating, displaying, updating and deleting customers

- receive customer information through pydantic schemas to be format

- uses sqlalchemy to access the customer table from database

- find customers by their id

- return an HTTP error when the customer is not found

## Order Router

- handles creating orders and changing order status,if it has the condidents

- uses sqlalchemy to access products and orders in the database

- checks if the product exists and is active

- checks if there is enough stock

- calculates the total order price

- creates Order and OrderItem objects

- decreases product stock after creating the order

- uses OrderStatus Enum to manage order status

- prevents invalid order status changes

## Inventory Router

- handles product stock operations

- uses sqlalchemy to access the Product table

- increases or decreases product stock

- checks if the product exists

- displays the current product stock

## Authentication Router

- handles user registration and login

- uses pydantic schemas to validate user input

- uses sqlalchemy to find users in the database

- hashes the password before saving it

- verifies the password during login

- creates jwt tokens after successful authentication

- verifies jwt tokens to identify the current user

- checks the user role for admin access

## security

- it hash input password and hash password saved in database

- verify\_password function match the saved password in database and input password(by hash new input password each time)

- make\_token function for create token after user login,that has indevisual expire time 