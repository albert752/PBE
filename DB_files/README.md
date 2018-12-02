#MongoDB database
##Prerequisites
First of all, you must install mongodb in your computer. Here is a useful [link]( https://docs.mongodb.com/manual/installation/)

##Creation of the database
Once you've installed mongodb, you should run it. Typically:
'sudo service mongod start'
Then enter the shell:
'mongo'
Now you're ready to create a db. So then, you must create a db named suparurdinado (which will be the database of this project) by typing:
'use suparurdinado'
You have now created an empty database that you will fill with the collections we provide here.

##Import collections
Exit the mongo shell if you're running it. Now enter DB_files/COLLECTIONS directory and type the following commands:
'''
mongoimport -d suparurdinado -c Timetables --file Timetables.json
mongoimport -d suparurdinado -c Users --file Users.json
mongoimport -d suparurdinado -c Marks --file Marks.json
'''
The database is ready to work with the server.
