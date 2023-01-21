
import sqlite3 as sql


from flask import Flask, request,redirect,url_for
from flask import render_template

from prototype.static.databases.database import *
from . import app

import requests

import os
from prototype.api import get_news_by_interest


#Basic functions to load each page, need modifications
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', username='')

@app.route("/profile",methods=["POST","GET"])
def profile():
    global interests
    news=[]
    try:
        interests=list(get_specific_student(email,password)[0])#Gets the interests and stores them in the interests variable
        print(interests)
        inter=list(get_news_by_interest(email,password)[0])[1].split(",")#Gets the interests
        news=[]
        for interest in inter:#loops through the interests
            news.append(get_news_by_interest(interest,1))#gets the news for a specific interest
        print(news)
    except:
        interests=[]
   
    if(request.method=="POST"):
        return redirect(url_for("profile_change"))#When the user clicks the update change button it will redirect them to the profile change website
    return render_template('profile.html',info=interests,news=news)
@app.route("/profileChange",methods=["GET","POST"])
def profile_change():
    global email
    global password
    try:
        interests=list(get_specific_student(email,password)[0])# Gets the interests
    except:
        interests=[]
    if(request.method=="POST"):
        data=[request.form.get("username"),request.form.get("email"),request.form.get("password"),request.form.get("Age"),request.form.get("City Born In"),request.form.get("interests")]#Gets the inputed data
        for i in range(len(data)):
            print(email)
            print(password)
            print(get_specific_student(email,password))
            if(data[i]!=""):#checks if the data is not empty then update the data
                if(i==0):
                    update("students","name",data[0],int(get_specific_student(email,password)[0][6]))#updates the username
                    email=data[0]
                if(i==1):
                    update("students","email",data[1],get_specific_student(email,password)[0][6])#updates the email
                if(i==2):
                    update("students","password",data[2],get_specific_student(email,password)[0][6])#updates the password
                    password=data[2]
                if(i==3):
                    update("students","age",data[3],get_specific_student(email,password)[0][6])#updates the age of the person
                if(i==4):
                    update("students","State",data[4],get_specific_student(email,password)[0][6])#updates the state the person lives in
                if(i==5):
                    update("students","Interests",data[5],get_specific_student(email,password)[0][6])#updates the interests
                return redirect(url_for("profile"))
    return render_template("profile_change.html",info=interests)

#Search Page
@app.route("/search",methods=["POST","GET"])
def search():
    people=[]
    search_people=[]
  
    if(request.method=="POST"):
       
        to_search=request.form.get("term")
        print(to_search)
        try:
            people.append(get_similar_interests("students",to_search))
        except:
            print(get_similar_interests("students",to_search))
            print("did not work")
            people=[]
    print(people)
    for s in people:
        for i in s:
            search_people.append(get_specific_student_id(i[0]))
    print(search_people)

    

        
    
    


    return render_template('search.html',people=search_people)


# 1. Home Page

# - Login function 
@app.route("/login/", methods = ['POST', 'GET'])
def login(): 
    print("check")
    if request.method == 'POST':

        global email 
        global password
        email = request.form.get('email') #gets the email
        password = request.form.get('password')#gets the paassword

        success=check_if_user_exists(email,password)#checks if user exists
        print(success)
        
        if success[0]>0 or success[1]>0 :#check if they exist in the students or mentors (Nothing is any different now)
            
            print(success)
            print(success[0])
            print(success[1])
            return redirect(url_for('profile'))#if the user exists send them to the profile page
            
    return render_template('home.html')



#register function 
@app.route("/register",methods = ['POST', 'GET'])
def register():
    data=["ID","name","password","email","imageUrl","age","country","State","Interests","mentors"]#Gets the data
    if request.method == 'POST':
        print(request.form.get("password"))
        print(request.form.get("confirm_password"))
        print(request.form.get("password")==request.form.get("confirm_password"))
        if(request.form.get("password")==request.form.get("confirm_password")):#checks if the password == to the confirm password
            print(get_number_of_ids())
            data[0]=get_number_of_ids()[0][0]+1#create a id number for the person
            data[1] = request.form.get('name') #sets the name
            data[2] = request.form.get('password')#sets the password
            data[3] = request.form.get('email') #sets the email
        create_student(data)#creates a student as a beginning
        print(data)
    return render_template("register.html")

def _register():
    print(" register check")
  







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