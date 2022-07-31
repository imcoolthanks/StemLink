
import sqlite3 as sql
import csv

def create_scholarship():
    #Create database file/connect to it
    conn = sql.connect("scholarship_database.db")

    #Create table
    conn.execute("""CREATE TABLE scholarship (name TEXT, price TEXT, area_of_study TEXT, institution TEXT, gender TEXT, 
                                            nationality TEXT, country TEXT, residency TEXT, url TEXT, degree_type TEXT,
                                            deadline TEXT,id TEXT PRIMARY KEY)""")

    print("table created")

    conn.close()

def populate_scholarship():
    #Get all rows from csv file
    with open('D:/Programming/VisualCode/Hackathon/Starhacks real/building-tuition/prototype/static/databases/scholarship.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader) #skip headers line
        data = list(reader)

    #Connect to database
    conn = sql.connect("scholarship_database.db")
    cur = conn.cursor()

    #Load all rows
    for row in data:
        print(row) #Debug
        insert_query = """INSERT INTO scholarship (name, price, area_of_study, institution, gender, 
                                        nationality, country, residency, url, degree_type, deadline, id)
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

def create_bursary():
    #Create database file/connect to it
    conn = sql.connect("bursary_database.db")

    #Create table
    conn.execute("""CREATE TABLE bursary (name TEXT, age TEXT, area_of_study TEXT, institution TEXT, degree_type TEXT, 
                                            nationality TEXT, country TEXT, residency TEXT, url TEXT, id TEXT PRIMARY KEY, desc TEXT)""")

    print("table created")

    conn.close()

def populate_bursary():
    #Get all rows from csv file
    with open('D:/Programming/VisualCode/Hackathon/Starhacks real/building-tuition/prototype/static/databases/bursary.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader) #skip headers line
        data = list(reader)

    #Connect to database
    conn = sql.connect("bursary_database.db")
    cur = conn.cursor()

    #Load all rows
    for row in data:
        print(row) #Debug
        insert_query = """INSERT INTO bursary (name, age, area_of_study, institution, degree_type, 
                                        nationality, country, residency, url, id, desc)
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

