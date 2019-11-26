# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

This application provides the following:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit existing drinks.

### Getting Started

In order to get the application running on your machine you need to do the following:

#### Pre-requisites

You need to have Git, Python3, pip3, SQLite3, Node and the Ionic CLI installed on your machine. 

#### Code

To checkout the code, run: `git clone https://github.com/nicholaspretorius/udacity-coffee-shop.git`
Once the project is on your computer, change into the project directory: `cd udacity-coffee-shop`

#### Database

Change into the directory: `/backend/src/database`. From there, run: 

`sqlite3 database.db` to connect to the database
`.databases` will print the path to the db
`.tables` will list the table names (You should see a table called 'drink')
`.schema drink` will list the schema of the 'drink' table
`SELECT * FROM drink;` will list all data in your database.

Please note: You need to uncomment line 19 in the file `/backend/src/api.py` when first running the application. This will drop any existing db and create a new one.

#### Backend

Change into your backend folder: `cd backend`
To install the dependencies, run: `pip install requirements.txt`
To run the app, change into your 'src' folder (from the 'backend' folder): `cd src`

From the 'src' folder, run: 
```
export FLASK_APP=api.py; export FLASK_ENV=development; flask run --reload;
```

The API will no be running on: http://localhost:5000/. You should see a JSON response containing: 

```
{
    "ping": "pong",
    "success": true
}
```

#### Frontend

From the root folder, change into the /frontend folder. 

From there, run: `npm install`
Once all the dependencies are installed, run: `ionic serve`

This will open the frontend of the website at: `http://localhost:8100`

You can explore the application from there. 

Please note: Both the backend and frontend apps need to be running in order for the application to work. For the Postman Collection (see below), only the backend (and database) need to be running.


#### Postman Collection

You need to have the standalone Postman application installed on your computer. From Postman, import the Postman collection from `/backend/udacity-fsnd-udaspicelatte.postman_collection.json`. 

From there, you can see all the endpoints in the collection along with example data and JWTs. You can see the contents of the JWTs by pasting the JWT into the 'Encoded' textarea at [JWT.io](https://jwt.io/). 

You can run the tests from the "Runner" tab at top left. Select the appropriate collection and all the tests will be run. 

Please note: Depending on what data you have in your database at the time, the example of ID 1 may or may not pass depending on whether you have an item with Id of 1 in your database. Just check your Ids in relation to your database.