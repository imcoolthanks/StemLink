import sqlite3 as sql

# 1. users.db
# email TEXT, password TEXT, name TEXT, age INT, role TEXT, pfp_url TEXT

def create_users():
    #Create database file/connect to it
    conn = sql.connect("users.db")

    #Create table
    conn.execute("""CREATE TABLE users (email TEXT PRIMARY KEY, password TEXT, name TEXT, age INT, role TEXT, pfp_url TEXT) 
                                            """)

    print("table created")

    conn.close()

def new_user(row): #Pass in an array of info (email, password, name, age, role) like this

    #Connect to database
    conn = sql.connect("users.db")
    cur = conn.cursor()

    #Load all rows
    insert_query = """INSERT INTO users (email, password, name, age, role, pfp_url) 
                                        VALUES (?,?,?,?,?,?)"""
    cur.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

# ---- DEBUGGING ---------
def list_user(): 
    conn = sql.connect("users.db")
    cur = conn.cursor()

    cur.execute("select * from users")
    
    rows = list(cur.fetchall())

    conn.close()

    return rows

def create_new_users():
    create_users()
    new_user(("123@gmail.com","123","Rick",123,"student","default_user_icon.jpg"))
    list_user()
# -------------------------




# 2. interests.db
# email TEXT, interest TEXT

def create_interests():
    #Create database file/connect to it
    conn = sql.connect("interests.db")

    #Create table
    conn.execute("""CREATE TABLE interests (email TEXT, interest TEXT, PRIMARY KEY (email, interest))""")

    print("table created")

    conn.close()

def new_interest(row): #Pass in an array of info (email, interest) like this

    #Connect to database
    conn = sql.connect("interests.db")
    cur = conn.cursor()

    #Load all rows
    insert_query = """INSERT INTO interests (email, interest) 
                                        VALUES (?,?)"""
    cur.execute(insert_query, (row[0], row[1]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

# ---- DEBUGGING ---------
def list_interests(): 
    conn = sql.connect("interests.db")
    cur = conn.cursor()

    cur.execute("select * from interests")
    
    rows = list(cur.fetchall())

    conn.close()

    return rows

def create_new_interests():
    create_interests()
    new_interest(("123@gmail.com","computer science"))
    print(list_interests())
# -------------------------



