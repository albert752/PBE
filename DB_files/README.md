{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 ArialMT;}
{\colortbl;\red255\green255\blue255;\red26\green26\blue26;\red255\green255\blue255;\red16\green60\blue192;
}
{\*\expandedcolortbl;;\cssrgb\c13333\c13333\c13333;\cssrgb\c100000\c100000\c100000;\cssrgb\c6667\c33333\c80000;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sl220\partightenfactor0

\f0\fs20 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 #MongoDB database\
##Prerequisites\
First of all, you must install mongodb in your computer. Here is a useful [link](\'a0{\field{\*\fldinst{HYPERLINK "https://docs.mongodb.com/manual/installation/"}}{\fldrslt \cf4 \ul \ulc4 \strokec4 https://docs.mongodb.com/manual/installation/}})\
\
##Creation of the database\
Once you've installed mongodb, you should run it. Typically:\
'sudo service mongod start'\
Then enter the shell:\
'mongo'\
Now you're ready to create a db. So then, you must create a db named suparurdinado (which will be the database of this project) by typing:\
'use suparurdinado'\
You have now created an empty database that you will fill with the collections we provide here.\
\
##Import collections\
Exit the mongo shell if you're running it. Now enter DB_files/COLLECTIONS directory and type the following commands:\
'''\
mongoimport -d suparurdinado -c Timetables --file Timetables.json\
mongoimport -d suparurdinado -c Users --file Users.json\
mongoimport -d suparurdinado -c Marks --file Marks.json\
'''\
The database is ready to work with the server.}