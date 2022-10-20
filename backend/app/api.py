#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, jsonify
import json
import os
import mysql.connector

app = Flask(__name__)

# environment to connect to the database
host = os.environ['HOST']
port = os.environ['PORT']
config = {
    'user': 'user',
    'password': 'password',
    'host': host,
    'port': port,
    'database': 'emotions_db'
}

# This function creates the desired table into the database when its initilized


def createTable():
    try:
        # Estabilishing  a connection cursor
        connection = mysql.connector.connect(**config)

        # Query for Creating the table
        query_string = """CREATE TABLE IF NOT EXISTS emotions_table (
                        id int NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                        name VARCHAR(255), 
                        emotion VARCHAR(255), 
                        date VARCHAR(255))"""

        # Creating a connection cursor
        cursor = connection.cursor()

        # Executing SQL Statement
        cursor.execute(query_string)

        # Saving the Actions performed on the DB
        connection.commit()

        print("\n✅ Table created successfully")

    except mysql.connector.Error as error:
        print("❎ Failed to create table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_records():
    try:
        # Estabilishing  a connection cursor
        connection = mysql.connector.connect(**config)

        # Query for Creating the table
        query_string = "DELETE FROM emotions_table"

        # Creating a connection cursor
        cursor = connection.cursor()

        # Executing SQL Statement
        cursor.execute(query_string)

        # Saving the Actions performed on the DB
        connection.commit()
        print("\n✅ "+str(cursor.rowcount),
              "record(s) deleted successfully from table\n\n")

    except mysql.connector.Error as error:
        print("❎ Failed to delete record from table: {}".format(error))
    finally:
        if connection.is_connected():
            
            # Close the cursor and connection
            cursor.close()
            connection.close()

# This function insert single and multiple rows into the database table.
def create_record(data):
    try:
        # Estabilishing  a connection cursor
        connection = mysql.connector.connect(**config)

        # Query for Creating the table
        query_string = "INSERT INTO emotions_table (name, emotion, date) VALUES(%s,%s,%s)"

        # Parse string to JSON object
        data = json.loads(data)

        # Iterate and add the information to the table
        records_to_insert = []
        print("\nAdding Data...")
        for person in data:
            print(" -", person['name'], person['emotion'], person['date'])
            records_to_insert.append(
                (person['name'], person['emotion'], person['date']))

        # Creating a connection cursor
        cursor = connection.cursor()

        # Executing SQL Statements
        cursor.executemany(query_string, records_to_insert)

        # Saving the Actions performed on the DB
        connection.commit()
        print("\n✅ "+str(cursor.rowcount),
              "record(s) inserted successfully into table")

    except mysql.connector.Error as error:
        print("❎ Failed to insert record: {}".format(error))
    finally:
        if connection.is_connected():

            # Close the cursor and connection
            cursor.close()
            connection.close()


# Class save people information before sending it.
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
            "emotion": self.emotion,
            "date": self.date
        }

# Get method that return all the people information saved in the database


@app.route('/', methods=['GET'])
def get_records():
    try:
        # Estabilishing  a connection cursor
        connection = mysql.connector.connect(**config)

        # Query for Creating the table
        query_string = "SELECT * FROM emotions_table"

        # Creating a connection cursor
        cursor = connection.cursor()

        # Executing SQL Statement
        cursor.execute(query_string)

        # Fetches all rows from the last executed statement
        records = cursor.fetchall()

        # output list
        output = []

        # Iterate over the rows
        for row in records:
            person = Person(row[1], row[2], row[3])
            output.append(person.to_json())

        # we close both the cursor and connection
        cursor.close()
        connection.close()

        print("\n✅ "+str(len(output)),
              "record(s) sent successfully")

        response = jsonify(output)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
        return jsonify({'error': 'Connection error. Data not found'})


def run():
    # Create table
    createTable()
    # delete_records()
    # Run api
    app.run(debug=False, host='0.0.0.0')
