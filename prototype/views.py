from re import L
import sqlite3 as sql


from flask import Flask, request
from flask import render_template

from prototype.static.databases.database import *
from . import app

import requests

import os

#Basic functions to load each page, need modifications
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', username='')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/search")
def search():
    return render_template('search.html')


# 1. Home Page

# - Login function 
@app.route("/login/", methods = ['POST', 'GET'])
def login(): 
    print("check")
    if request.method == 'POST':
        global user_email
        global user_username

        email = request.form.get('email') 
        password = request.form.get('password')

        success, error_msg = _login(email, password)
        
        if success:
            info = get_info(email)
            interests = get_interests(email)[:3] #get top 3
            interest_str = ', '.join(interests)

            #for now!!
            people = [{'username': 'Queen', 'interest':'Computer Science', 'pfp':'default_user_icon.jpg'},
                        {'username': 'Rick', 'interest':'You', 'pfp':'default_user_icon.jpg'},
                        {'username': 'Adam', 'interest':'Anime', 'pfp':'default_user_icon.jpg'}]

            news = get_news_by_interest(interests[0], 3)

            return render_template("dashboard.html", user_username = info[2], pfp_url=info[5],
                                    interests=interest_str, people = people, all_news=news)
             
        else:
            return render_template('home.html') #, error=error_msg

    return render_template('login.html')

def _login(email, password):
    print("check")
    conn = sql.connect("users.db")
    cur = conn.cursor()

    try:
        query = 'SELECT password FROM users WHERE email = ?'
        cur.execute(query, (email,))
        true_password = cur.fetchall()[0][0]
    except:
        return False, "Invalid Email Address."

    conn.close()

    if password == true_password:
        return True, ""
    else:
        return False, print("Wrong Password.")


#register function 
@app.route("/register/",methods = ['POST', 'GET'])
def register():
    data=["ID","name","password","email","imageUrl","age","country","State","Interests","mentors"]
    if request.method == 'POST':
        print(request.form.get("password"))
        print(request.form.get("confirm_password"))
        print(request.form.get("password")==request.form.get("confirm_password"))
        if(request.form.get("password")==request.form.get("confirm_password")):
            print(get_number_of_ids())
            data[0]=get_number_of_ids()[0][0]+1
            data[1] = request.form.get('name') 
            data[2] = request.form.get('password')
            data[3] = request.form.get('email') 
        create_student(data)
        print(data)
    return render_template("register.html")

def _register():
    print(" register check")
  


# 2. Dashboard

# - Display all user info
def get_info(email):
    conn = sql.connect("users.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT * FROM users WHERE email = ?'
    cur.execute(query, (email,))
    info = cur.fetchall()[0]

    print(info)

    conn.close()

    return info

# - Display user's interest
def get_interests(email):
    conn = sql.connect("interests.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT interest FROM interests WHERE email = ?'
    cur.execute(query, (email,))
    rows = list(cur.fetchall())

    conn.close()

    interests = []

    for r in rows:
        interests.append(r[0])

    #return an array of interests
    return interests

# - Display news based on interest
def get_news_by_interest(interest, num):
    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    query_params = {
      "sortBy": "top",
      "apiKey": "803faabb3328410ebf50846c453353e2",
      "q": interest,
      "language":"en"
    }
    main_url = " https://newsapi.org/v2/everything"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    data = res.json()
 
    # getting all articles in a string article
    article = data["articles"]
 
    # empty list which will
    # contain all trending news
    all_results = []
      
    for i in range(num):
        curr = dict()

        ar = article[i]

        curr['title'] = ar["title"]
        curr['description'] = ar["description"]
        curr['url'] = ar["url"]
        curr['urlToImage'] = ar["urlToImage"]

        all_results.append(curr)

    return all_results


# - Enter interest, takes in interest as string and return people (name and pfp) (Adam)



# - Display results




# 3. Search Page (let's wait for grant)

# - Display results




# 4. Profile


# - When users changed their info and submits, update database (Adam)





# 5. Log Out (Queena)

# - Log out function






















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
            #con = sql.connect("prototype/static/databases/scholarship_database.db")
            con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
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
            #con = sql.connect("prototype/static/databases/scholarship_database.db")
            con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
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
        # con = sql.connect("prototype/static/databases/scholarship_database.db")
        con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
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
        # con = sql.connect("prototype/static/databases/bursary_database.db")
        con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
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
        # con = sql.connect("prototype/static/databases/scholarship_database.db")
        con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
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
    # con = sql.connect("prototype/static/databases/bursary_database.db")
        con = sql.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
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
        # con = sql.connect("prototype/static/databases/scholarship_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db"
    if os.path.isfile(path):
        con = sql.connect(path)

    con.row_factory = sql.Row
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
    #     con = sql.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sql.connect(path)

    con.row_factory = sql.Row
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


@app.route("/list_user")
def list_user():
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sql.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sql.connect(path)

    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("select * from bursary")
    
    rows = list(cur.fetchall())

    return rows