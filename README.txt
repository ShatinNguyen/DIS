***** DATABASE AND INFORMATION SYSTEMS PROJECT 2024 *****

Our E/R diagram can be found in report.pdf along with a short description of
how to compile our web-app and how to run and interact with the web-app.
The report will also describe how we used SQL to interact with the database with
INSERT/UPDATE/DELETE/SELECT statements.


***** SETUP YOUR DATABASE BEFORE RUNNING app.py *****

After your database is running then use script.sql to COPY data into your database by using:

    psql -d chessproject -U username -f ./script.sql   (The directory to script.sql depend on your setup)

NOTE    You might need to modify the directory location after FROM in script.sql 
        if your terminal/command cannot find dataset.csv

RUNNING THE WEBSITE
After successfully COPY the dataset into your DATABASE go to app.py 
and change USER and PASSWORD to your username and password.
The application can started by running app.py