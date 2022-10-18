#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, jsonify
from flask_mysqldb import MySQL
import os
import json

app = Flask(__name__)

# Set database configurations
app.config['MYSQL_HOST'] = os.environ['RABBIT_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DATABASE']

mysql = MySQL(app)

# to ensure that the table exist
isCreated = False


class Person():
    
    # constructor
    def __init__(self, name, emotion, date):
        self.name = name
        self.emotion = emotion
        self.date = date
    
    # to convert attributes to a dict (json)
    def to_json(self):
        return {
            "name": self.name,
            "emotion": self.email,
            "date": self.date
        }

@app.route('/', methods=['GET'])
def get_records():

    # Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    # query to execute
    query_string = "SELECT * FROM emotions_table"

    # Executing SQL Statements
    cursor.execute(query_string)

    # Fetches all rows from the last executed statement
    result = cursor.fetchall()
        
    # output list
    output = []
    
    # Iterate over the rows
    for row in result:
        person = Person(row[1],row[2],row[3])
        output.append(person.to_json())
        
    # we close both the cursor and connection
    cursor.close()
    
    return jsonify(output)
    
def create_record(data):
    
    global isCreated
    # Ensure that the table exists
    if not isCreated:
        createTable()
        isCreated = True
        
    # Parse string to JSON object
    data = json.loads(data)
    
    # Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    # query to execute
    query_string = "INSERT INTO emotions_analysis VALUES(%s,%s,%s)"
    
    # Iterate and add the information to the table
    print("Adding Data")
    for person in data:
        print(person['name'], person['emotion'],person['date'])
        #Executing SQL Statements
        cursor.execute(query_string,person['name'],person['emotion'],person['date'])
        
    #Saving the Actions performed on the DB
    mysql.connection.commit()
    
    # we close both the cursor and connection
    cursor.close()
    
def createTable():
    # Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    # Query for Creating the table
    query_string = "CREATE TABLE emotions_analysis (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), emotion VARCHAR(255), date VARCHAR(255))"
    
    #Executing SQL Statement
    cursor.execute(query_string)
    
    #Saving the Actions performed on the DB
    mysql.connection.commit()
    
def run():
    app.run(debug=True, host='0.0.0.0')
    