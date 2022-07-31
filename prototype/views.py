import sqlite3
from flask import Flask, request
from flask import render_template
from . import app

import os

#Basic functions to load each page, need modifications
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/search")
def search():
    return render_template('search.html')

#Delete
@app.route("/layout")
def layout():
    return render_template('layout.html')










#TEMPLATE FOR BACKEND
@app.route("/search_students")
def search_students():
    options = load_bursary_options()
    rows = list_bursary()
    return render_template('bursary-search.html',aoss=options[0],institutions=options[1], nationalities=options[2], degree_types=options[3], rows=rows)


#-------------------- SEARCHING SEARCH PAGES --------------------------
@app.route('/search_scholarship_results', methods = ['POST', 'GET'])
def search_scholarship_results():
    def search_scholarship(category, search):
        try:
            #con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
            con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
        except:
            print("Can't connect to database")

        cur = con.cursor()

        #Build query!!!!!
        query = "SELECT * FROM scholarship WHERE "+category+" LIKE '%"+search+"%';"
        cur.execute(query)

        rows = list(cur.fetchall())

        return rows

    options = load_scholarship_options()
    if request.method == 'POST':
        category = request.form.get('search_by') 
        search = request.form['search_scholarship_value']

        if category=="Category" or search == "":
            rows = list_scholarship() #return all
        else:
            rows = search_scholarship(category, search) #search

    return render_template('scholarship-search.html',aoss=options[0],institutions=options[1], genders=options[2], nationalities=options[3], degree_types=options[4], rows=rows)

@app.route('/search_bursary_results', methods = ['POST', 'GET'])
def search_bursary_results():
    def search_bursary(category, search):
        print("Connecting database")
        try:
            #con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
            con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
        except:
            print("Can't connect to database")

        cur = con.cursor()

        #Build query!!!!!
        query = "SELECT * FROM bursary WHERE "+category+" LIKE '%"+search+"%';"
        cur.execute(query)

        rows = list(cur.fetchall())

        return rows

    print("search bursary results")
    options = load_bursary_options()
    if request.method == 'POST':
        category = request.form.get('search_by') 
        search = request.form['search_bursary_value']

        if category=="Category" or search == "":
            rows = list_bursary() #return all
        else:
            rows = search_bursary(category, search) #search

    return render_template('bursary-search.html',aoss=options[0],institutions=options[1], nationalities=options[2], degree_types=options[3], rows=rows)


#-------------------- FILTERING SEARCH PAGES --------------------------
@app.route('/filter_scholarship_results', methods = ['POST', 'GET'])
def filter_scholarship_results():
    options = load_scholarship_options()
    if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        aos = request.form.get('area-of-study-filter') 
        institution = request.form.get('institution-filter') 
        gender = request.form.get('gender-filter')          
        nationality = request.form.get('nationality-filter') 
        degree_type = request.form.get('degree-type-filter') 

    rows = filter_scholarship(aos, institution, gender, nationality, degree_type)

    return render_template('scholarship-search.html',aoss=options[0],institutions=options[1], genders=options[2], nationalities=options[3], degree_types=options[4], rows=rows)

@app.route('/filter_bursary_results', methods = ['POST', 'GET'])
def filter_bursary_results():
    options = load_bursary_options()

    if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        aos = request.form.get('area-of-study-filter') 
        institution = request.form.get('institution-filter')          
        nationality = request.form.get('nationality-filter') 
        degree_type = request.form.get('degree-type-filter') 
    
    rows = filter_bursary(aos, institution, nationality, degree_type)

    return render_template('bursary-search.html',aoss=options[0],institutions=options[1], nationalities=options[2], degree_types=options[3], rows=rows)
        
#-------------------- FILTER OPTIONS --------------------
def filter_scholarship(aos, institution, gender, nationality, degree_type):
    try:
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
    except:
        print("Can't connect to database")

    cur = con.cursor()

    #Build query
    query = "SELECT * FROM scholarship WHERE "
    parameters = []

    if not aos == "":
        print("AOS not null")
        query += "area_of_study = ? AND "
        parameters.append(aos)
    if not institution == "":
        print("Institution is not null")
        query += "institution = ? AND "
        parameters.append(institution)
    if not gender == "":
        print("gender is not null")
        query += "gender = ? AND "
        parameters.append(gender)
    if not nationality == "":
        print("nationality is not null")
        query += "nationality = ? AND "
        parameters.append(nationality)
    if not degree_type == "":
        print("degree_type is not null")
        query += "degree_type = ? AND "
        parameters.append(degree_type)

    #Make sure does not end with AND
    filter_query = query[:-5] + ";"
    print(filter_query)
    
    #execute query and get rows
    try:
        cur.execute(filter_query, parameters)
    except: 
        print("Error occured when executing query")

    #print to terminal
    rows = list(cur.fetchall())

    con.close()

    return rows

def filter_bursary(aos, institution, nationality, degree_type):
    try:
        # con = sqlite3.connect("prototype/static/databases/bursary_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
    except:
        print("Connection Error")

    cur = con.cursor()

    #Build query
    query = "SELECT * FROM bursary WHERE "
    parameters = []

    if not aos == "":
        print("AOS not null")
        query += "area_of_study = ? AND "
        parameters.append(aos)
    if not institution == "":
        print("Institution is not null")
        query += "institution = ? AND "
        parameters.append(institution)
    if not nationality == "":
        print("nationality is not null")
        query += "nationality = ? AND "
        parameters.append(nationality)
    if not degree_type == "":
        print("degree_type is not null")
        query += "degree_type = ? AND "
        parameters.append(degree_type)

    #Make sure does not end with AND
    filter_query = query[:-5] + ";"
    print(filter_query)
    
    #execute query and get rows
    try:
        cur.execute(filter_query, parameters)
    except:
        print("Cannot execute command")

    rows = list(cur.fetchall())
    
    con.close()

    return rows

#-------------------- GET ID FUNCTIONS --------------------
def filter_scholarship_by_id(id):
    try:
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
    except:
        print("Can't connect to database")

    cur = con.cursor()

    # BUILD QUERY
    query = "SELECT name, institution, price, area_of_study, deadline, url FROM scholarship WHERE id='" + id + "'"
    try:
        cur.execute(query)
    except: 
        print("Error occured when executing query")

    row = cur.fetchall()
    con.close()

    return row

def filter_bursary_by_id(id):
    try:
    # con = sqlite3.connect("prototype/static/databases/bursary_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
    except:
        print("Can't connect to database")

    cur = con.cursor()

    # BUILD QUERY
    query = "SELECT name, institution, area_of_study, url, desc FROM bursary WHERE id='" + id + "'"
    try:
        cur.execute(query)
    except: 
        print("Error occured when executing query")

    row = cur.fetchall()
    con.close()

    return row                    

#-------------------- LOADING OPTIONS FUNCTIONS --------------------
def load_scholarship_options():
    #get cursor
    # if os.path.isfile("prototype/static/databases/scholarship_database.db"):
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, gender, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'gender', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM scholarship ORDER BY "+ param +" ASC;"
        cur.execute(query)
        values = cur.fetchall()
        
        for v in values:
            op.append(v[0]) #append the actual values instead of sql row object

        options.append(op)

    return options

def load_bursary_options():
    #get cursor
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM bursary ORDER BY "+ param +" ASC;"
        cur.execute(query)
        values = cur.fetchall()
        
        for v in values:
            op.append(v[0]) #append the actual values instead of sql row object

        options.append(op)

    return options


@app.route("/list_bursary")
def list_bursary():
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from bursary")
    
    rows = list(cur.fetchall())

    return rows

#Print all from database to terminal
def list_scholarship():
    # if os.path.isfile("prototype/static/databases/scholarship_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from scholarship")

    rows = list(cur.fetchall())
    
    return rows


