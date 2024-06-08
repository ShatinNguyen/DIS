***** SETUP YOUR DATABASE BEFORE RUNNING app.py *****

After your database is running then use script.sql to COPY data into your database by using:

    psql -d chessproject -U username -f ./script.sql   (The directory to script.sql depend on your setup)

NOTE    You might need to modify the directory location after FROM in script.sql 
        if your terminal/command cannot find dataset.csv

RUNNING THE WEBSITE
First go to app.py and change USER and PASSWORD to your username and password.
After successfully COPY the dataset into your DATABASE the application 
started by running app.py